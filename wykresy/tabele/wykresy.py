import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_aggregated_metrics(files):
    for file in files:
        # Wczytaj dane z pliku CSV
        df = pd.read_csv(file)
        
        # Wydobywamy nazwę metryki z nazwy pliku
        metric = os.path.basename(file).split('_')[1]  # Przykład: wyodrębnia 'FPS' z 'aggregated_FPS_summary.csv'
        
        # Rysowanie wykresu
        plt.figure(figsize=(12, 6))  # Zwiększenie rozmiaru wykresu dla lepszej widoczności
        
        for column in df.columns[1:]:  # Pomijamy pierwszą kolumnę "Time Interval"
            plt.plot(df['Time Interval'], df[column], marker='o', label=f'Seed {column}')
        
        plt.title(f'{metric} by Time Interval')
        plt.xlabel('Time Interval (Seconds)')
        plt.xticks(rotation=45)  # Obrót etykiet osi X dla lepszej czytelności
        plt.tight_layout()  # Automatyczne dopasowanie układu, aby wszystko się zmieściło
        plt.ylabel(metric)
        plt.legend(title='Seed')
        plt.grid(True)
        
        # Obrót etykiet osi X dla lepszej czytelności
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()  # Automatyczne dopasowanie układu, aby wszystkie elementy były widoczne
        
        # Zapisz wykres do pliku PNG
        plot_file_name = f'{metric}_by_time_interval_plot.png'
        plt.savefig(plot_file_name)
        plt.close()
        print(f"Wykres dla metryki {metric} zapisany do pliku: {plot_file_name}")

# Przykładowe pliki zagregowane na podstawie interwałów czasowych (sekund)
files = [
    'trawa/agregowane/aggregated_FPS_summary.csv',
    'trawa/agregowane/aggregated_GPU Frame Time_summary.csv',
    'trawa/agregowane/aggregated_CPU Frame Time_summary.csv',
    'trawa/agregowane/aggregated_Draw Calls_summary.csv',
    'trawa/agregowane/aggregated_Total Frame Time_summary.csv'
]

plot_aggregated_metrics(files)
