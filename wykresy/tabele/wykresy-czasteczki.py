import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_combined_metrics(files):
    for file in files:
        # Wczytaj dane z pliku CSV
        df = pd.read_csv(file)
        
        # Wydobywamy nazwę metryki z nazwy pliku
        metric = os.path.basename(file).split('_')[0]
        
        # Rysowanie wykresu
        plt.figure(figsize=(12, 6))
        
        for column in df.columns[1:]:  # Pomijamy pierwszą kolumnę "Time Interval"
            plt.plot(df['Time Interval'], df[column], marker='o', label=column)
        
        plt.title(f'{metric} by Time Interval')
        plt.xlabel('Time Interval (Seconds)')
        plt.ylabel(metric)
        plt.legend(title='File')
        plt.grid(True)
        
        # Obrót etykiet osi X dla lepszej czytelności
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()  # Automatyczne dopasowanie układu, aby wszystkie elementy były widoczne
        
        # Zapisz wykres do pliku PNG
        plot_file_name = f'{metric}_by_time_interval_plot.png'
        plt.savefig(plot_file_name)
        plt.close()
        print(f"Wykres dla metryki {metric} zapisany do pliku: {plot_file_name}")

# Przykładowe pliki CSV zagregowane na podstawie interwałów czasowych
files = [
    'FPS_combined_by_time_interval.csv',
    'GPU Frame Time_combined_by_time_interval.csv',
    'CPU Frame Time_combined_by_time_interval.csv',
    'Draw Calls_combined_by_time_interval.csv',
    'Total Frame Time_combined_by_time_interval.csv'
]

plot_combined_metrics(files)
