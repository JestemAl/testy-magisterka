import pandas as pd
import os

def aggregate_every_10_seconds(df):
    # Dodajemy kolumnę, która identyfikuje 10-sekundowe przedziały w formie tekstowej
    df['Time Interval'] = pd.cut(df.index + 1, 
                                 bins=range(0, df.index.max() + 11, 10), 
                                 labels=[f"{i}-{i+9}" for i in range(1, df.index.max() + 1, 10)],
                                 right=True)
    
    # Agregujemy dane w ramach tych przedziałów czasowych
    aggregated_df = df.groupby('Time Interval').mean().reset_index()
    
    return aggregated_df

def process_aggregated_files(files):
    for file in files:
        df = pd.read_csv(file)
        aggregated_df = aggregate_every_10_seconds(df)
        
        # Zapisujemy zredagowany plik CSV
        base_name = os.path.basename(file)
        new_file_name = f'aggregated_{base_name}'
        aggregated_df.to_csv(new_file_name, index=False)
        print(f"Zredagowane dane zapisane do pliku: {new_file_name}")

# Pliki wygenerowane przez poprzedni program
files = [
    'trawa/wyniki/FPS_summary.csv',
    'trawa/wyniki/GPU Frame Time_summary.csv',
    'trawa/wyniki/CPU Frame Time_summary.csv',
    'trawa/wyniki/Draw Calls_summary.csv',
    'trawa/wyniki/Total Frame Time_summary.csv'
]

process_aggregated_files(files)
