import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_mean_with_confidence_intervals(aggregated_files):
    for file in aggregated_files:
        # Wczytaj dane z pliku CSV
        df = pd.read_csv(file)
        
        # Wydobycie nazwy metryki z nazwy pliku
        metric = os.path.basename(file).split('_')[1]
        
        # Obliczanie przedziałów ufności
        df['Lower Bound'] = df['Mean'] - 1.96 * df['Std Dev']
        df['Upper Bound'] = df['Mean'] + 1.96 * df['Std Dev']
        
        # Rysowanie wykresu
        plt.figure(figsize=(12, 6))
        
        # Rysowanie linii dla średnich wartości z liniami błędów dla przedziałów ufności
        plt.errorbar(df['Model Interval'], df['Mean'], 
                     yerr=1.96 * df['Std Dev'], fmt='-o', 
                     ecolor='blue', capsize=5, label='Mean with 95% CI')
        
        # Ustawienia wykresu
        plt.title(f'{metric} Mean with 95% Confidence Intervals')
        plt.xlabel('Model Count Interval')
        plt.ylabel(metric)
        plt.xticks(rotation=45)  # Obrót etykiet osi X dla lepszej czytelności
        plt.tight_layout()  # Automatyczne dopasowanie układu, aby wszystko się zmieściło
        plt.grid(True)
        plt.legend()

        # Zapisanie wykresu do pliku PNG
        plot_file_name = f'{metric}_mean_with_confidence_intervals_plot.png'
        plt.savefig(plot_file_name)
        plt.close()
        print(f"Wykres dla metryki {metric} z przedziałami ufności zapisany do pliku: {plot_file_name}")

# Przykładowe pliki CSV z dodanymi kolumnami Mean i Std Dev
aggregated_files = [
    'renderowanie/scaleone/combined_FPS_by_model_count_with_mean_std.csv',
    'renderowanie/scaleone/combined_GPU Frame Time_by_model_count_with_mean_std.csv',
    'renderowanie/scaleone/combined_CPU Frame Time_by_model_count_with_mean_std.csv',
    'renderowanie/scaleone/combined_Draw Calls_by_model_count_with_mean_std.csv',
    'renderowanie/scaleone/combined_Total Frame Time_by_model_count_with_mean_std.csv'
]

plot_mean_with_confidence_intervals(aggregated_files)
