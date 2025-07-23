# etl/update_feature_layer.py
from arcgis.gis import GIS
from arcgis.features import FeatureLayer
from datetime import datetime, timedelta, timezone
from dateutil.parser import parse
from dotenv import load_dotenv
import os
import requests

# --- CONFIGURATION ---
load_dotenv()
AGOL_USERNAME = os.environ.get("AGOL_USERNAME")
AGOL_PASSWORD = os.environ.get("AGOL_PASSWORD")
FEATURE_LAYER_URL = "https://services1.arcgis.com/KUeKSLlMUcWvuPRM/arcgis/rest/services/crime_layer_fl/FeatureServer/0"

# Socrata API
API_URL = "https://data.boston.gov/api/3/action/datastore_search"
RESOURCE_ID = "b973d8cb-eeb2-4e7e-99da-c92938efc9c0"
PAGE_LIMIT = 1000

def fetch_all_records(api_url, resource_id, days_back, field_map=None):
    latest_occurred_date = None
    offset = 0
    all_features = []
    cutoff_time = datetime.now(timezone.utc) - timedelta(days=days_back)

    agol_field_names = set(field_map["attributes"].keys()) if field_map else set()

    while True:
        params = {
            "resource_id": resource_id,
            "limit": PAGE_LIMIT,
            "offset": offset
        }
        response = requests.get(API_URL, params=params)

        if response.status_code != 200:
            break

        data = response.json()
        if "result" not in data or "records" not in data["result"]:
            break

        records = data["result"]["records"]

        if not records:
            break

        for rec in records:
            try:
                lat_raw = rec.get(field_map.get("latitude", "Lat")) if field_map else rec.get("Lat")
                lon_raw = rec.get(field_map.get("longitude", "Long")) if field_map else rec.get("Long")
                if lat_raw is None or lon_raw is None:
                    continue
                lat = float(lat_raw)
                lon = float(lon_raw)
                occurred_date_str = rec.get(field_map.get("occurred_on_date", "OCCURRED_ON_DATE")) if field_map else rec.get("OCCURRED_ON_DATE")
                if not occurred_date_str:
                    continue
                occurred_date = parse(occurred_date_str)
                if occurred_date.tzinfo is None:
                    occurred_date = occurred_date.replace(tzinfo=timezone.utc)
                if latest_occurred_date is None or occurred_date > latest_occurred_date:
                    latest_occurred_date = occurred_date
                if occurred_date < cutoff_time:
                    continue
            except (KeyError, ValueError, TypeError):
                continue

            if field_map:
                base_attrs = {k: rec.get(v) for k, v in field_map.get("attributes", {}).items()}
            else:
                base_attrs = {
                    "incident_number": rec.get("INCIDENT_NUMBER"),
                    "offense_description": rec.get("OFFENSE_DESCRIPTION"),
                    "occurred_on_date": rec.get("OCCURRED_ON_DATE")
                }
            base_attrs["updated_on"] = datetime.now(timezone.utc).isoformat()

            valid_attrs = {k: v for k, v in base_attrs.items() if k in agol_field_names or k == "updated_on"}

            all_features.append({
                "geometry": {
                    "x": lon,
                    "y": lat,
                    "spatialReference": {"wkid": 4326}
                },
                "attributes": base_attrs
            })

        offset += PAGE_LIMIT

        if len(records) < PAGE_LIMIT:
            break

    return all_features

def update_feature_layer(username, password, org_url, feature_layer_url, api_url, resource_id, field_map, days_back=7):
    try:
        features = fetch_all_records(api_url, resource_id, days_back, field_map=field_map)

        if not features:
            return
        
        gis = GIS(org_url, username, password, verify_cert=False)

        target_layer = FeatureLayer(feature_layer_url)
        del_result = target_layer.delete_features(where="1=1")

        if features:
            def chunk_features(features, size):
                for i in range(0, len(features), size):
                    yield features[i:i + size]

            for i, chunk in enumerate(chunk_features(features, 500)):
                result = target_layer.edit_features(adds=chunk)
        else:
            pass

    except Exception:
        pass

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Update an ArcGIS Online feature layer from an external API.")
    parser.add_argument("--username", required=True, help="ArcGIS Online username")
    parser.add_argument("--password", required=True, help="ArcGIS Online password")
    parser.add_argument("--org-url", required=True, help="Your ArcGIS organization URL (e.g., https://yourorg.maps.arcgis.com)")
    parser.add_argument("--layer-url", required=True, help="Feature layer URL ending in /FeatureServer/0")
    parser.add_argument("--api-url", required=True, help="External API base URL")
    parser.add_argument("--resource-id", required=False, help="Resource ID from the external API (optional)")
    parser.add_argument("--days", type=int, default=7, help="How many days back to include in the update (default: 7)")
    parser.add_argument("--field-map", type=str, required=True, help="Path to field mapping JSON file")

    args = parser.parse_args()

    import json
    field_map = None
    if args.field_map:
        with open(args.field_map, "r") as f:
            field_map = json.load(f)

    update_feature_layer(
        username=args.username,
        password=args.password,
        org_url=args.org_url,
        feature_layer_url=args.layer_url,
        api_url=args.api_url,
        resource_id=args.resource_id,
        field_map=field_map,
        days_back=args.days
    )