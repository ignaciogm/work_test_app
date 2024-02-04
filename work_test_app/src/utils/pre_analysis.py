import pandas as pd

# Reading the Parquet files
path22= r'C:\Users\GARCIAMARTII\OneDrive - FUJITSU\Documentos\Workspace\work_test_app\data\input\yellow_tripdata_2022-01.parquet'
path23 = r'C:\Users\GARCIAMARTII\OneDrive - FUJITSU\Documentos\Workspace\work_test_app\data\input\yellow_tripdata_2023-01.parquet'
df = pd.read_parquet(path22)
#df = pd.read_parquet(path23)

# Displaying the schema
df.info()

# columns to analyze
columns_to_analyze = ['trip_distance', 'tpep_pickup_datetime', 'tpep_dropoff_datetime', 'VendorID', 'total_amount','payment_type', 'RatecodeID']

for column in columns_to_analyze:
    print(f"\nCalidad de Datos para {column}:\n")
    
    # Verificar valores nulos
    null_count = df[column].isnull().sum()
    print(f" nulos en {column}: {null_count}")

    # Estadísticas básicas para columnas numéricas
    if df[column].dtype in ['int64', 'float64']:
        print(df[column].describe())

# Puedes agregar más análisis según sea necesario

# columnas categóricas
payment_type_mapping = {
    1: 'Credit card',
    2: 'Cash',
    3: 'No charge',
    4: 'Dispute',
    5: 'Unknown',
    6: 'Voided trip'
}

rate_code_mapping = {
    1: 'Standard rate',
    2: 'JFK',
    3: 'Newark',
    4: 'Nassau or Westchester',
    5: 'Negotiated fare',
    6: 'Group ride'
}
df['Payment_type_des'] = df['payment_type'].map(payment_type_mapping)
df['RateCodeID_des'] = df['RatecodeID'].map(rate_code_mapping)

# Conteo payment_type
payment_counts = df['Payment_type_des'].value_counts()
print("Frecuencia Payment_type:")
print(payment_counts)

# Conteo rateCodeID
rate_counts = df['RateCodeID_des'].value_counts()
print("\nFrecuencia de RateCodeID:")
print(rate_counts)
