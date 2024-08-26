import pandas as pd
import os

def parse_results(file_path):
    data = {
        "FPS": [],
        "GPU Frame Time": [],
        "CPU Frame Time": [],
        "Draw Calls": [],
        "Total Frame Time": [],
        "Model Count": [],
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
                elif "Model Count" in line:
                    data["Model Count"].append(int(line.split(": ")[1].strip()))
            except Exception as e:
                print(f"Błąd przetwarzania linii: {line}")
                print(f"Szczegóły błędu: {e}")
    
    return pd.DataFrame(data)

def process_files(files):
    for file in files:
        seed_id = os.path.basename(file).split('-')[2]  # Wydobywa ID seeda z nazwy pliku np. 10
        df = parse_results(file)
        
        # Sortowanie danych według liczby modeli
        df = df.sort_values(by="Model Count", ascending=True)
        
        # Zapisz dane do pliku CSV dla tego seeda
        new_file_name = f'seed_{seed_id}_performance_summary.csv'
        df.to_csv(new_file_name, index=False)
        print(f"Dane dla seeda {seed_id} zapisane do pliku: {new_file_name}")

# Przykładowe pliki
files = [
    'pomiary/rendering-seed-10-performance-results.txt',
    'pomiary/rendering-seed-169-performance-results.txt',
    'pomiary/rendering-seed-4444-performance-results.txt',
    'pomiary/rendering-seed-77777-performance-results.txt',
    'pomiary/rendering-seed-123456-performance-results.txt'
]

process_files(files)
