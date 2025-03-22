# Boston Crime ETL

A flexible, reusable Python tool for updating an ArcGIS Online feature layer from an external API (e.g., Boston's crime data). Built for automation, custom data structures, and team collaboration.

---

## 🚀 Features
- Scheduled or manual updates from any JSON API
- Custom field mapping support
- ArcGIS Online feature layer integration
- Date filtering
- Cron-ready and log-friendly

---

## 🔧 Requirements
- Python 3.8+
- `arcgis`, `requests`, `python-dateutil`, `python-dotenv`

Install them with:
```bash
pip install -r requirements.txt
```

---

## 🗂 Project Structure
```bash
etl/
├── update_crime_layer.py
├── field_map.json         # Optional config for mapping fields
├── update_log.txt         # Log file written by script
├── run_update.sh          # Bash script for scheduled runs
├── requirements.txt
└── README.md
```

---

## ⚙️ Usage

### 🧾 Sample API to Feature Layer
```bash
python folder/update_feature_layer.py \
  --username your_user \
  --password your_pass \
  --org-url https://yourorg.maps.arcgis.com \
  --layer-url https://yourlayer-url/FeatureServer/0 \
  --api-url https://data.boston.gov/api/3/action/datastore_search \
  --resource-id b973d8cb-eeb2-4e7e-99da-c92938efc9c0 \
  --days 7 \
  --field-map field_map.json
```

### ✅ Arguments
| Argument       | Description |
|----------------|-------------|
| `--username`   | AGOL username |
| `--password`   | AGOL password |
| `--org-url`    | ArcGIS Online organization URL |
| `--layer-url`  | Target hosted feature layer URL (must end in `/FeatureServer/0`) |
| `--api-url`    | Source API URL |
| `--resource-id`| Resource ID (e.g., from Socrata) |
| `--days`       | Number of days back to include |
| `--field-map`  | Path to JSON file defining field mappings (optional) |

---

## 📄 Sample `field_map.json`
```json
{
  "latitude": "Lat",
  "longitude": "Long",
  "occurred_on_date": "OCCURRED_ON_DATE",
  "attributes": {
    "incident_number": "INCIDENT_NUMBER",
    "offense_description": "OFFENSE_DESCRIPTION"
  }
}
```

---

## 🕒 Automating with Cron
Create a `run_update.sh` like:
```bash
#!/bin/bash
source /opt/anaconda3/etc/profile.d/conda.sh
conda activate conda_env
cd /Users/you/Projects/feature-layer-etl
python feature-layer-etl/update_feature_layer.py --args...
```

Schedule with:
```bash
crontab -e
```
And add:
```cron
*/10 * * * * /Users/you/Projects/feature-layer-etl/run_update.sh >> /Users/you/Projects/feature-layer-etl/cron_output.log 2>&1
```

---

## 🔐 Security Tips
- Store credentials securely using `.env`, `.netrc`, or OS keychain
- Avoid logging passwords

---

## ✅ Built-In Safety
- Script fetches all data *before* deleting features
- If update fails, the existing layer is left unchanged
- All errors and results logged in `update_log.txt`

---

## 👥 For Your Team: How to Set It Up

### 🧑‍💻 What Your Coworker Needs to Do

1. **Clone the repo**
```bash
git clone https://github.com/yourusername/feature-layer-updater.git
cd feature-layer-updater
```

2. **(Optional but recommended) Create and activate a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **(Optional) Install as CLI tool**
```bash
pip install -e .
crime-etl --help
```

5. **Create their own `field_map.json`**
Adjust the keys and values based on their API and feature layer fields.

6. **Create their own `run_update.sh`**
Customize with their own credentials and layer/API URLs.

7. **Add their own cron job**
```bash
crontab -e
```
```cron
*/10 * * * * /Users/them/Path/run_update.sh >> /Users/them/Path/cron_output.log 2>&1
```

---

## 🙌 Contributions
Pull requests welcome for:
- Polygon/line support
- GeoJSON ingestion
- More robust auth

---

## 📬 Questions?
Ping [justin.m.guthrie@gmail.com] or drop an issue in the GitHub repo.

---

### Made with support from GIS Pro & OpenAI


