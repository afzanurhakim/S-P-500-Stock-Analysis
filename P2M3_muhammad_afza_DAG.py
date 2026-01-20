from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import psycopg2
from elasticsearch import Elasticsearch, helpers
import csv
import re


# 
# Default Arguments 
# 
default_args = {
    'owner': 'Afza',
    'start_date': datetime(2024, 11, 1),
    'retries': 1
}

# =================================================
# EXTRACT
# =================================================
def extract():
    conn = psycopg2.connect(
        host="postgres",
        port="5432",
        database="milestone", 
        user="airflow",
        password="airflow"
    )

    df_raw = pd.read_sql("SELECT * FROM stocks", conn)
    df_raw.to_csv(
        '/opt/airflow/dags/P2M3_muhammad_afza_data_raw.csv',
        index=False
    )

    conn.close()
    print(f"Berhasil extract {len(df_raw)} rows dari PostgreSQL")


# 
# TRANSFORM
# 
def transform():
    df = pd.read_csv('/opt/airflow/dags/P2M3_muhammad_afza_data_raw.csv')

    # 1. REMOVE DUPLICATES
    initial_count = len(df)
    df = df.drop_duplicates()
    print(f"Duplicates removed: {initial_count - len(df)}")

    # 2. COLUMN NAME NORMALIZATION 
    # def normalize_column_name(col):
        
    #     col = col.lower()   
    #     col = re.sub(r'[^\w]', '_', col)
    #     col = re.sub(r'+', '', col).strip('_')
        
    #     return col
    def normalize_column_name(col):
        col = col.lower()   
        # 1. Ganti karakter non-alfanumerik dengan underscore
        col = re.sub(r'[^\w]', '_', col)
        
        # 2. PERBAIKAN DI SINI: Ganti underscore berlebih (_+) menjadi satu underscore saja (_)
        col = re.sub(r'_+', '_', col).strip('_')
        
        return col
    # Terapkan ke semua kolom
    df.columns = [normalize_column_name(c) for c in df.columns]

    print("Normalized columns:", df.columns.tolist())

    # 3. HANDLE MISSING VALUES
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].fillna('Unknown')
        else:
            df[col] = df[col].fillna(0)

    df.to_csv(
        '/opt/airflow/dags/P2M3_muhammad_afza_data_clean.csv',
        index=False,
        quoting=csv.QUOTE_ALL
    )

    print("Data clean berhasil disimpan")

# 
# LOAD
# 
def load():
    df = pd.read_csv('/opt/airflow/dags/P2M3_muhammad_afza_data_clean.csv')
    es = Elasticsearch("http://elasticsearch:9200")
    actions = [
        {
            "_index": "dagafza2",
            "_source": row.to_dict()
        }
        for _, row in df.iterrows()
    ]

    helpers.bulk(es, actions)
    print("Data berhasil dikirim ke Elasticsearch")

# 
# DAG
# 
with DAG(
    dag_id='dagafza2',
    default_args=default_args,
    description='ETL Pipeline PostgreSQL to Elasticsearch',
    schedule_interval='@daily',
    catchup=False
) as dag:

    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract
    )

    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform
    )

    load_task = PythonOperator(
        task_id='load',
        python_callable=load
    )

    extract_task >> transform_task >> load_task