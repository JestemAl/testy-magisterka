import pandas as pd
import os

def combine_metrics_by_model_count(aggregated_files):
    metrics = ["FPS", "GPU Frame Time", "CPU Frame Time", "Draw Calls", "Total Frame Time"]
    combined_tables = {metric: pd.DataFrame() for metric in metrics}

    for file in aggregated_files:
        seed_id = os.path.basename(file).split('_')[2]  # Wydobywa ID seeda z nazwy pliku np. 10
        df = pd.read_csv(file)
        
        for metric in metrics:
            if "Model Interval" in df.columns:
                # Przypisanie wartości metryki do odpowiedniego przedziału Model Count
                combined_tables[metric][seed_id] = df[metric]
                combined_tables[metric]['Model Interval'] = df['Model Interval']
    
    # Zapisanie tabel dla każdej metryki
    for metric, table in combined_tables.items():
        # Upewnienie się, że kolumna Model Interval jest pierwsza
        cols = table.columns.tolist()
        cols.insert(0, cols.pop(cols.index('Model Interval')))
        table = table[cols]
        
        # Zapisz do pliku CSV
        file_name = f'combined_{metric}_by_model_count.csv'
        table.to_csv(file_name, index=False)
        print(f"Zapisano tabelę dla metryki {metric} do pliku: {file_name}")

# Przykładowe pliki zagregowane na podstawie liczby modeli
aggregated_files = [
    'aggregated_seed_10_performance_summary.csv',
    'aggregated_seed_169_performance_summary.csv',
    'aggregated_seed_4444_performance_summary.csv',
    'aggregated_seed_77777_performance_summary.csv',
    'aggregated_seed_123456_performance_summary.csv'
]

combine_metrics_by_model_count(aggregated_files)
