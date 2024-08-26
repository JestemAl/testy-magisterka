import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_metrics(aggregated_files):
    for file in aggregated_files:
        # Wczytaj dane z pliku CSV
        df = pd.read_csv(file)
        
        # Wydobywamy nazwę metryki z nazwy pliku
        metric = os.path.basename(file).split('_')[1]
        
        # Rysowanie wykresu
        plt.figure(figsize=(10, 6))
        
        for column in df.columns[1:]:  # Pomijamy pierwszą kolumnę "Model Interval"
            plt.plot(df['Model Interval'], df[column], marker='o', label=f'Seed {column}')
        
        plt.title(f'{metric} by Model Count')
        plt.xlabel('Model Count Interval')
        plt.ylabel(metric)
        plt.xticks(rotation=45)  # Obrót etykiet osi X dla lepszej czytelności
        plt.tight_layout()  # Automatyczne dopasowanie układu, aby wszystko się zmieściło
        plt.grid(True)
        plt.legend(title='Seed')
        
        # Zapisz wykres do pliku PNG
        plot_file_name = f'{metric}_by_model_count_plot.png'
        plt.savefig(plot_file_name)
        plt.close()
        print(f"Wykres dla metryki {metric} zapisany do pliku: {plot_file_name}")

# Przykładowe pliki zagregowane na podstawie liczby modeli
aggregated_files = [
    'renderowanie/scaleone/combined_FPS_by_model_count.csv',
    'renderowanie/scaleone/combined_GPU Frame Time_by_model_count.csv',
    'renderowanie/scaleone/combined_CPU Frame Time_by_model_count.csv',
    'renderowanie/scaleone/combined_Draw Calls_by_model_count.csv',
    'renderowanie/scaleone/combined_Total Frame Time_by_model_count.csv'
]

plot_metrics(aggregated_files)
