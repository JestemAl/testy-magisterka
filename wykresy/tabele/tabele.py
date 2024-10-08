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

def process_files(files):
    tables = {
        "FPS": pd.DataFrame(),
        "GPU Frame Time": pd.DataFrame(),
        "CPU Frame Time": pd.DataFrame(),
        "Draw Calls": pd.DataFrame(),
        "Total Frame Time": pd.DataFrame(),
    }

    for file in files:
        file_id = os.path.basename(file).split('-')[2]  # Wydobywa liczbę z nazwy pliku np. 4096
        df = parse_results(file)
        
        # Dodanie kolumn do odpowiednich tabel
        for metric in tables.keys():
            tables[metric][file_id] = df[metric]
    
    return tables

# Przykładowe pliki
files = [
    'pomiary/trawa-liczba-4096-performance-results.txt',
    'pomiary/trawa-liczba-8192-performance-results.txt',
    'pomiary/trawa-liczba-16384-performance-results.txt',
    'pomiary/trawa-liczba-32768-performance-results.txt',
    'pomiary/trawa-liczba-65536-performance-results.txt'
]

tables = process_files(files)

# Zapisz każdą tabelę do osobnego pliku CSV
for metric, table in tables.items():
    table.to_csv(f'{metric}_summary.csv', index=False)

print("Tabele dla każdej metryki zostały wygenerowane i zapisane do plików CSV.")
