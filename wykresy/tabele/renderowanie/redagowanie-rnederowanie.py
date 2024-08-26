import pandas as pd
import os

def aggregate_by_model_count(df):
    # Dodajemy kolumnę, która identyfikuje przedziały modelCount co 10 modeli
    df['Model Interval'] = pd.cut(df['Model Count'], bins=range(0, df['Model Count'].max() + 10, 10), right=True)
    
    # Agregujemy dane w ramach tych przedziałów
    aggregated_df = df.groupby('Model Interval').mean().reset_index()
    
    return aggregated_df

def process_and_aggregate_files(files):
    for file in files:
        df = pd.read_csv(file)
        
        # Agregujemy dane co 10 modeli
        aggregated_df = aggregate_by_model_count(df)
        
        # Zapisz zredagowany plik CSV
        seed_id = os.path.basename(file).split('_')[1]  # Wydobywa ID seeda z nazwy pliku np. 10
        new_file_name = f'aggregated_seed_{seed_id}_performance_summary.csv'
        aggregated_df.to_csv(new_file_name, index=False)
        print(f"Zredagowane dane zapisane do pliku: {new_file_name}")

# Przykładowe pliki wygenerowane w poprzednim kroku
files = [
    'seed_10_performance_summary.csv',
    'seed_169_performance_summary.csv',
    'seed_4444_performance_summary.csv',
    'seed_77777_performance_summary.csv',
    'seed_123456_performance_summary.csv'
]

process_and_aggregate_files(files)
