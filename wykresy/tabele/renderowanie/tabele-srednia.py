import pandas as pd
import os

def add_mean_and_std_dev(aggregated_files):
    for file in aggregated_files:
        # Wczytaj dane z pliku CSV
        df = pd.read_csv(file)
        
        # Oblicz średnią (Mean) i odchylenie standardowe (Std Dev) dla każdej liczby modeli
        df['Mean'] = df.iloc[:, 1:].mean(axis=1)  # Oblicza średnią dla wszystkich kolumn oprócz "Model Interval"
        df['Std Dev'] = df.iloc[:, 1:].std(axis=1)  # Oblicza odchylenie standardowe dla wszystkich kolumn oprócz "Model Interval"
        
        # Zapisz zaktualizowany plik CSV
        new_file_name = f'{os.path.splitext(file)[0]}_with_mean_std.csv'
        df.to_csv(new_file_name, index=False)
        print(f"Dodano kolumny Mean i Std Dev do pliku: {new_file_name}")

# Przykładowe pliki zagregowane na podstawie liczby modeli
aggregated_files = [
    'renderowanie/scaleone/combined_FPS_by_model_count.csv',
    'renderowanie/scaleone/combined_GPU Frame Time_by_model_count.csv',
    'renderowanie/scaleone/combined_CPU Frame Time_by_model_count.csv',
    'renderowanie/scaleone/combined_Draw Calls_by_model_count.csv',
    'renderowanie/scaleone/combined_Total Frame Time_by_model_count.csv'
]

add_mean_and_std_dev(aggregated_files)
