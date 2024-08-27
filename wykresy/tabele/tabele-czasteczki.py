import pandas as pd
import os

def parse_results(file_path):
    data = {
        "FPS": [],
        "GPU Frame Time": [],
        "CPU Frame Time": [],
        "Draw Calls": [],
        "Total Frame Time": [],
    }
    
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            try:
                if "FPS" in line:
                    data["FPS"].append(float(line.split(": ")[1].strip()))
                elif "GPU Frame Time" in line:
                    data["GPU Frame Time"].append(float(line.split(": ")[1].strip().replace('ms', '').strip()))
                elif "CPU Frame Time" in line:
                    data["CPU Frame Time"].append(float(line.split(": ")[1].strip().replace('ms', '').strip()))
                elif "Draw Calls" in line:
                    data["Draw Calls"].append(int(line.split(": ")[1].strip()))
                elif "Total Frame Time" in line:
                    data["Total Frame Time"].append(float(line.split(": ")[1].strip().replace('ms', '').strip()))
            except Exception as e:
                print(f"Błąd przetwarzania linii: {line}")
                print(f"Szczegóły błędu: {e}")
    
    return pd.DataFrame(data)

def aggregate_every_10_seconds(df):
    # Dodajemy kolumnę, która identyfikuje 10-sekundowe przedziały w formie tekstowej
    df['Time Interval'] = pd.cut(df.index + 1, 
                                 bins=range(0, df.index.max() + 11, 10), 
                                 labels=[f"{i}-{i+9}" for i in range(1, df.index.max() + 1, 10)],
                                 right=True)
    
    # Agregujemy dane w ramach tych przedziałów czasowych
    aggregated_df = df.groupby('Time Interval').mean().reset_index()
    
    return aggregated_df

def process_and_combine_files(files):
    metrics = ["FPS", "GPU Frame Time", "CPU Frame Time", "Draw Calls", "Total Frame Time"]
    combined_tables = {metric: pd.DataFrame() for metric in metrics}

    for file in files:
        file_id = os.path.basename(file).split('-')[1].replace('performance-results.txt', '')  # Wydobywa np. "x48"
        df = parse_results(file)
        aggregated_df = aggregate_every_10_seconds(df)
        
        for metric in metrics:
            if "Time Interval" in aggregated_df.columns:
                combined_tables[metric][file_id] = aggregated_df[metric]
                combined_tables[metric]['Time Interval'] = aggregated_df['Time Interval']
    
    for metric, table in combined_tables.items():
        cols = table.columns.tolist()
        cols.insert(0, cols.pop(cols.index('Time Interval')))  # Upewnij się, że 'Time Interval' jest pierwszą kolumną
        table = table[cols]
        
        # Zapisz zredagowany plik CSV dla każdej metryki
        file_name = f'{metric}_combined_by_time_interval.csv'
        table.to_csv(file_name, index=False)
        print(f"Tabela dla metryki {metric} została zapisana do pliku: {file_name}")

# Lista plików do przetworzenia
files = [
    'czasteczki-x1-performance-results.txt',
    'czasteczki-x2-performance-results.txt',
    'czasteczki-x4-performance-results.txt',
    'czasteczki-x48-performance-results.txt',
    'czasteczki-x96-performance-results.txt',
]

process_and_combine_files(files)
