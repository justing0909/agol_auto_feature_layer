#!/bin/bash

# Activate your environment
source /opt/anaconda3/etc/profile.d/conda.sh

# Activate your environment
conda activate arcgis_env

# Change to your project directory
cd /Users/justi/Projects/etl

# Run your script with full CLI args
python etl/update_feature_layer.py \
  --username guthrie.j_nu \
  --password Rndm#30729264235 \
  --org-url https://nu.maps.arcgis.com \
  --layer-url https://services1.arcgis.com/KUeKSLlMUcWvuPRM/arcgis/rest/services/crime_layer_fl/FeatureServer/0 \
  --api-url https://data.boston.gov/api/3/action/datastore_search \
  --resource-id b973d8cb-eeb2-4e7e-99da-c92938efc9c0 \
  --days 7 \
  --field-map field_map.json