import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os

def calculate_confidence_intervals(df):
    ci_df = df.copy()
    
    # Obliczanie przedziałów ufności dla WebGL
    ci_df['CI_low_webgl'] = ci_df['Mean Across Seeds_webgl'] - stats.t.ppf(0.975, df=df.shape[0]-1) * (ci_df['Std Dev Across Seeds_webgl'] / np.sqrt(df.shape[0]))
    ci_df['CI_high_webgl'] = ci_df['Mean Across Seeds_webgl'] + stats.t.ppf(0.975, df=df.shape[0]-1) * (ci_df['Std Dev Across Seeds_webgl'] / np.sqrt(df.shape[0]))
    
    # Obliczanie przedziałów ufności dla WebGPU
    ci_df['CI_low_webgpu'] = ci_df['Mean Across Seeds_webgpu'] - stats.t.ppf(0.975, df=df.shape[0]-1) * (ci_df['Std Dev Across Seeds_webgpu'] / np.sqrt(df.shape[0]))
    ci_df['CI_high_webgpu'] = ci_df['Mean Across Seeds_webgpu'] + stats.t.ppf(0.975, df=df.shape[0]-1) * (ci_df['Std Dev Across Seeds_webgpu'] / np.sqrt(df.shape[0]))
    
    return ci_df

def plot_with_confidence_intervals(ci_df, metric):
    # Tworzenie folderu 'wykresy', jeśli nie istnieje
    os.makedirs('wykresy', exist_ok=True)
    
    plt.figure(figsize=(10, 6))
    
    # Wykres dla WebGL
    plt.errorbar(ci_df['Model Range'], ci_df['Mean Across Seeds_webgl'], 
                 yerr=[ci_df['Mean Across Seeds_webgl'] - ci_df['CI_low_webgl'], ci_df['CI_high_webgl'] - ci_df['Mean Across Seeds_webgl']], 
                 fmt='o', capsize=5, label='WebGL', color='blue')
    
    # Wykres dla WebGPU
    plt.errorbar(ci_df['Model Range'], ci_df['Mean Across Seeds_webgpu'], 
                 yerr=[ci_df['Mean Across Seeds_webgpu'] - ci_df['CI_low_webgpu'], ci_df['CI_high_webgpu'] - ci_df['Mean Across Seeds_webgpu']], 
                 fmt='o', capsize=5, label='WebGPU', color='red')
    
    plt.title(f'{metric} with Confidence Intervals')
    plt.xlabel('Model Range')
    plt.ylabel(metric)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    
    # Zapisanie wykresu do pliku PNG w folderze 'wykresy'
    plt.savefig(f'wykresy/{metric}_with_confidence_intervals.png')
    plt.close()

# Przykład użycia:
# Załóżmy, że masz dane w plikach CSV, które wcześniej scalono.
cpu_merged = pd.read_csv('wyniki/combined_CPU Usage.csv')
fps_merged = pd.read_csv('wyniki/combined_FPS.csv')
memory_merged = pd.read_csv('wyniki/combined_Memory Usage (usedJSHeapSize).csv')
total_js_heap_merged = pd.read_csv('wyniki/combined_Total JS Heap Size.csv')
draw_calls_merged = pd.read_csv('wyniki/combined_Draw Calls.csv')
vram_usage_merged = pd.read_csv('wyniki/combined_VRAM Usage.csv')
frame_time_merged = pd.read_csv('wyniki/combined_Frame Time.csv')
load_time_merged = pd.read_csv('wyniki/combined_Load Time.csv')

# Obliczenie przedziałów ufności
cpu_ci = calculate_confidence_intervals(cpu_merged)
fps_ci = calculate_confidence_intervals(fps_merged)
memory_ci = calculate_confidence_intervals(memory_merged)
total_js_heap_ci = calculate_confidence_intervals(total_js_heap_merged)
draw_calls_ci = calculate_confidence_intervals(draw_calls_merged)
vram_usage_ci = calculate_confidence_intervals(vram_usage_merged)
frame_time_ci = calculate_confidence_intervals(frame_time_merged)
load_time_ci = calculate_confidence_intervals(load_time_merged)

# Generowanie i zapisywanie wykresów
plot_with_confidence_intervals(cpu_ci, 'CPU Usage')
plot_with_confidence_intervals(fps_ci, 'FPS')
plot_with_confidence_intervals(memory_ci, 'Memory Usage')
plot_with_confidence_intervals(total_js_heap_ci, 'Total JS Heap Size')
plot_with_confidence_intervals(draw_calls_ci, 'Draw Calls')
plot_with_confidence_intervals(vram_usage_ci, 'VRAM Usage')
plot_with_confidence_intervals(frame_time_ci, 'Frame Time')
plot_with_confidence_intervals(load_time_ci, 'Load Time')
