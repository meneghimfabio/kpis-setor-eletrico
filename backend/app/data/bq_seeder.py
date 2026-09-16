import os
import logging
from google.cloud import bigquery
from google.auth.exceptions import DefaultCredentialsError
from app.core.config import settings
from app.data.bq_schemas import SCHEMAS
from app.data.seed_data import SEED_DATA

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bq_seeder")

def provision_bigquery_datasets():
    client = None
    try:
        client = bigquery.Client(project=settings.GCP_PROJECT_ID)
        # Test client with a quick query
        list(client.list_datasets(max_results=1))
        logger.info(f"Connected to GCP Project: {settings.GCP_PROJECT_ID}")
    except Exception as e:
        try:
            import subprocess
            from google.oauth2 import credentials
            token = subprocess.check_output(["gcloud", "auth", "print-access-token"]).decode().strip().split()[-1]
            creds = credentials.Credentials(token)
            client = bigquery.Client(project=settings.GCP_PROJECT_ID, credentials=creds)
            logger.info(f"Connected to GCP Project via gcloud token: {settings.GCP_PROJECT_ID}")
        except Exception as e2:
            logger.error(f"Cannot initialize BigQuery Client for GCP project '{settings.GCP_PROJECT_ID}': {e} / {e2}")
            logger.info("Skipping cloud provisioning. Local fallback is ready.")
            return

    location = os.getenv("BQ_LOCATION", "us-central1")
    logger.info(f"Target BigQuery location: {location}")

    created_datasets = 0
    created_tables = 0

    for dataset_name, tables in SCHEMAS.items():
        dataset_id = f"{settings.GCP_PROJECT_ID}.{dataset_name}"
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = location
        try:
            client.create_dataset(dataset, exists_ok=True)
            logger.info(f"Dataset verified/created: {dataset_id} in {location}")
            created_datasets += 1
        except Exception as e:
            logger.warning(f"Error creating dataset {dataset_id}: {e}")
            continue

        for table_name, schema_fields in tables.items():
            table_id = f"{dataset_id}.{table_name}"
            table = bigquery.Table(table_id, schema=schema_fields)
            try:
                table_obj = client.create_table(table, exists_ok=True)
                logger.info(f"Table verified/created: {table_id}")
                created_tables += 1
                
                # Check if seed data exists for this table and insert if table is empty
                seed_rows = SEED_DATA.get(dataset_name, {}).get(table_name, [])
                if seed_rows and isinstance(seed_rows, list):
                    count_query = f"SELECT count(1) as total FROM `{table_id}`"
                    try:
                        count_res = list(client.query(count_query).result())
                        if count_res and count_res[0].total == 0:
                            errors = client.insert_rows_json(table_obj, seed_rows)
                            if not errors:
                                logger.info(f"Seeded {len(seed_rows)} rows into {table_id}")
                            else:
                                logger.warning(f"Errors seeding {table_id}: {errors}")
                    except Exception as seed_err:
                        logger.warning(f"Could not seed {table_id}: {seed_err}")
            except Exception as e:
                logger.warning(f"Error creating table {table_id}: {e}")

    logger.info(f"Provisioning finished: {created_datasets} datasets, {created_tables} tables verified/created.")

if __name__ == "__main__":
    provision_bigquery_datasets()
