import pandas as pd
import numpy as np

def parse_results(file_path):
    data = {
        "webgl Number of Models": [],
        "webgl CPU Usage": [],
        "webgl Memory Usage (usedJSHeapSize)": [],
        "webgl Total JS Heap Size": [],
        "webgl FPS": [],
        "webgl Draw Calls": [],
        "webgl VRAM Usage": [],
        "webgl Frame Time": [],
        "webgl Load Time": []
    }
    
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()  # Usuń zbędne białe znaki
            try:
                if "Number of Models" in line:
                    data["Number of Models"].append(int(line.split(": ")[1].strip()))
                elif "CPU Usage (approx)" in line:
                    data["CPU Usage"].append(float(line.split(": ")[1].strip().replace('%', '')))
                elif "Memory Usage (usedJSHeapSize)" in line:
                    data["Memory Usage (usedJSHeapSize)"].append(int(line.split(": ")[1].strip().replace('bytes', '').strip()))
                elif "Total JS Heap Size" in line:
                    data["Total JS Heap Size"].append(int(line.split(": ")[1].strip().replace('bytes', '').strip()))
                elif "FPS" in line:
                    data["FPS"].append(int(line.split(": ")[1].strip()))
                elif "Draw Calls" in line:
                    data["Draw Calls"].append(int(line.split(": ")[1].strip()))
                elif "VRAM Usage" in line:
                    data["VRAM Usage"].append(int(line.split(": ")[1].strip().replace('bytes', '').strip()))
                elif "Frame Time" in line:
                    data["Frame Time"].append(float(line.split(": ")[1].strip().replace('ms', '').strip()))
                elif "Load Time" in line:
                    data["Load Time"].append(int(line.split(": ")[1].strip().replace('ms', '').strip()))
            except Exception as e:
                print(f"Error processing line: {line}")
                print(f"Error details: {e}")
    
    # Upewnij się, że wszystkie listy mają tę samą długość
    max_length = max(len(lst) for lst in data.values())
    for key, lst in data.items():
        while len(lst) < max_length:
            lst.append(None)  # Lub 0, w zależności od tego, co preferujesz
    
    return pd.DataFrame(data)

def generate_tables(combined_data):
    tables = {}

    metrics = {
        'CPU Usage': 'CPU Usage',
        'Memory Usage': 'Memory Usage (usedJSHeapSize)',
        'Total JS Heap Size': 'Total JS Heap Size',
        'FPS': 'FPS',
        'Draw Calls': 'Draw Calls',
        'VRAM Usage': 'VRAM Usage',
        'Frame Time': 'Frame Time',
        'Load Time': 'Load Time'
    }

    for metric_key, metric_name in metrics.items():
        table = combined_data.groupby(['Model Range', 'Seed']).agg(
            mean=(metric_name, 'mean')
        ).reset_index()

        table['Model Range'] = table['Model Range'].astype(str)
        pivot_table = table.pivot(index='Model Range', columns='Seed', values='mean')

        # Add mean and std deviation across all seeds
        pivot_table['Mean Across Seeds'] = pivot_table.mean(axis=1)
        pivot_table['Std Dev Across Seeds'] = pivot_table.std(axis=1)

        tables[metric_key] = pivot_table

    return tables


def process_files(files):
    combined_data = pd.DataFrame()

    for file in files:
        seed = file.split('-')[-3]  # Extract seed from filename (second last part)
        df = parse_results(file)
        df['Seed'] = seed
        combined_data = pd.concat([combined_data, df])
    
    combined_data['Model Range'] = pd.cut(combined_data['Number of Models'], bins=range(0, 260, 10))
    
    return combined_data

# Example files
files = [
    'pomiary/webgl-seed-7777777-performance-results.txt',
    'pomiary/webgl-seed-12345-performance-results.txt',
    'pomiary/webgl-seed-4444-performance-results.txt',
    'pomiary/webgl-seed-272-performance-results.txt',
    'pomiary/webgl-seed-9-performance-results.txt'
]

combined_data = process_files(files)
tables = generate_tables(combined_data)

# Save tables to CSV
for metric, table in tables.items():
    table.to_csv(f'{metric}_summary.csv')

print("Tables generated and saved to CSV.")
