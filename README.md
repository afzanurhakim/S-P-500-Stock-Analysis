# Judul Project
S&P 500 Stock Analysis for Investment Purpose

## Repository Outline
1. README.md - Penjelasan gambaran umum project
2. P2M3_muhammad_afza_conceptual.txt - Notepad berisi jawaban untuk pertanyaan conceptual
3. P2M3_muhammad_afza_DAG_graph.jpg - Flowchart ETL yang berjalan di airflow
4. P2M3_muhammad_afza_ddl.txt - Query pembuatan table dan memasukkan baris data ke PostgreSQL
5. P2M3_muhammad_afza_GX.ipynb - Notebook berisi great expectation untuk validasi data setelah proses ETL
6. P2M3_muhammad_afza_DAG.py - Script berisi syntax DAG untuk melakukan ekstaksi data dari data PostgresSQL kemudian transformasi dan load data ke warehouse data ElasticSearch
7. P2M3_muhammad_afza_data_raw.csv - File .csv dataset yang belum dilakukan cleaning
8. P2M3_muhammad_afza_data_clean.csv - File .csv dataset yang telah dicleaning dengan Airflow
9. Image - File gambar visualisasi dan insight dari project

## Problem Background
Indeks S&P 500 adalah barometer utama ekonomi global, namun konsentrasi pasar pada sektor tertentu (seperti Teknologi) sering kali menutupi performa fundamental di sektor lain. Di tengah fluktuasi suku bunga, investor membutuhkan transparansi lebih dari sekadar harga saham; mereka membutuhkan data terintegrasi mengenai valuasi, efisiensi operasional, dan pembagian dividen untuk membuat keputusan investasi yang objektif

## Project Output
Proyek ini bertujuan untuk membangun automated data pipeline yang memproses data keuangan 500 perusahaan terbesar di AS. Hasil akhirnya adalah dashboard interaktif yang mampu mengidentifikasi anomali valuasi (saham murah vs mahal) dan memetakan kekuatan operasional antar sektor industri

## Data
Dataset ini berisi dataset harga saham S&P 500 di bulan July 2020

- 4 character variables:
        - Symbol: Ticker symbol used to uniquely identify each company on a particular stock market
        - Name: Legal name of the company
        - Sector: An area of the economy where businesses share a related product or service
        - SEC Filings: Helpful documents relating to a company

    - 10 numeric variables:
        - Price: Price per share of the company
        - Price to Earnings (PE): The ratio of a company’s share price to its earnings per share
        - Dividend Yield: The ratio of the annual dividends per share divided by the price per share
        - Earnings Per Share (EPS): A company’s profit divided by the number of shares of its stock
        - 52 week high and low: The annual high and low of a company’s share price
        - Market Cap: The market value of a company’s shares (calculated as share price x number of shares)
        - EBITDA: A company’s earnings before interest, taxes, depreciation, and amortization; often used as a proxy for its profitability
        - Price to Sales (PS): A company’s market cap divided by its total sales or revenue over the past year
        - Price to Book (PB): A company’s price per share divided by its book value

## Method
Extraction data dari source PostgreSQL
Transformation pada Airflow untuk data cleaning
Load ke ElasticSearch sebagai data warehouse
Validation dengan Great Expectation
Visualization dengan Kibana

## Stacks
Language
- Python
- SQL
Library
- pandas
- psycopg2
- datetime
- airflow (DAG)
- airflow.operators.python (PythonOperator)
- elastchsearch (Elasticsearch, helpers)
- csv
- re
Container
- Docker
Database
- PostgreSQL
- ElasticSearch
Orchestrator
- Airflow
Visualization
- Kibana

## Reference

URL dataset =  https://www.kaggle.com/datasets/paytonfisher/sp-500-companies-with-financial-information
