import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_aggregated_metrics(files):
    for file in files:
        # Wczytaj dane z pliku CSV
        df = pd.read_csv(file)
        
        # Wydobywamy nazwę metryki z nazwy pliku
        metric = os.path.basename(file).split('_')[1]  # Przykład: wyodrębnia 'FPS' z 'aggregated_FPS_summary.csv'
        
        # Przekształcenie nazw metryk na język polski
        metric_translation = {
            'FPS': 'Liczba klatek na sekundę',
            'GPU Frame Time': 'Czas ramki GPU',
            'CPU Frame Time': 'Czas ramki CPU',
            'Draw Calls': 'Liczba wywołań rysowania',
            'Total Frame Time': 'Całkowity czas ramki'
        }
        
        # Rysowanie wykresu
        plt.figure(figsize=(12, 6))  # Duży rozmiar wykresu
        
        for column in df.columns[1:]:  # Pomijamy pierwszą kolumnę "Time Interval"
            plt.plot(df['Time Interval'], df[column], marker='o', label=column)
                
        plt.title(f'{metric_translation.get(metric, metric)} w zależności od przedziału czasowego', fontsize=14, pad=20)

        # Ustal etykietę osi Y bez [ms] dla metryki 'Draw Calls'
        if metric == 'Draw Calls':
            plt.ylabel(f'{metric_translation.get(metric, metric)}', fontsize=12, labelpad=20)
        else:
            plt.ylabel(f'{metric_translation.get(metric, metric)} [ms]', fontsize=12, labelpad=20)  # Użycie nawiasów kwadratowych dla milisekund dla pozostałych metryk

        plt.xlabel('Przedział czasowy [s]', fontsize=12, labelpad=20)  # Użycie nawiasów kwadratowych dla jednostki sekund
        plt.grid(True)

        # Obrót etykiet osi X dla lepszej czytelności
        plt.xticks(rotation=45, ha='right')

        # Dostosowanie marginesów, aby zwiększyć odstęp na dole wykresu
        plt.tight_layout(rect=[0, 0, 0.85, 1]) 
        
        # Umieszczenie legendy po prawej stronie wykresu, z mniejszymi odstępami i mniejszym rozmiarem
        plt.legend(
            title='Liczba instancji trawy', 
            loc='center left', 
            bbox_to_anchor=(1, 0.9),  # Po prawej stronie, wycentrowane na osi Y
            fontsize='x-small',           # Bardzo mała czcionka w legendzie
            title_fontsize='small',       # Mała czcionka dla tytułu legendy
            markerscale=0.6,              # Mniejsze markery w legendzie
            handletextpad=0.4,            # Mniejsze odstępy między markerami a tekstem
            borderpad=0.5,                # Zmniejszenie marginesów wewnątrz legendy
            labelspacing=0.4              # Zmniejszenie odstępów między wierszami w legendzie
        )
        
        # Obrót etykiet osi X dla lepszej czytelności
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout(rect=[0, 0, 0.85, 1])  # Zmniejszenie miejsca na wykresie, aby uniknąć zbyt dużej przestrzeni po prawej
        
        # Zapisz wykres do pliku PNG
        plot_file_name = f'{metric}_by_time_interval_plot.png'
        plt.savefig(plot_file_name, bbox_inches='tight')  # Upewnienie się, że cała legenda jest widoczna
        plt.close()
        print(f"Wykres dla metryki {metric_translation.get(metric, metric)} zapisany do pliku: {plot_file_name}")

# Przykładowe pliki zagregowane na podstawie interwałów czasowych (sekund)
files = [
    'trawa/agregowane/aggregated_FPS_summary.csv',
    'trawa/agregowane/aggregated_GPU Frame Time_summary.csv',
    'trawa/agregowane/aggregated_CPU Frame Time_summary.csv',
    'trawa/agregowane/aggregated_Draw Calls_summary.csv',
    'trawa/agregowane/aggregated_Total Frame Time_summary.csv'
]

plot_aggregated_metrics(files)
