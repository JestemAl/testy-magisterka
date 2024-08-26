import pandas as pd
import os

def merge_results(webgl_file, webgpu_file, metric):
    # Check if files exist
    if not os.path.exists(webgl_file):
        print(f"File not found: {webgl_file}")
        return
    if not os.path.exists(webgpu_file):
        print(f"File not found: {webgpu_file}")
        return

    # Load the data
    webgl_data = pd.read_csv(webgl_file)
    webgpu_data = pd.read_csv(webgpu_file)

    # Merge the data on Model Range
    merged_data = pd.merge(webgl_data, webgpu_data, on='Model Range', suffixes=('_webgl', '_webgpu'))

    # Rearrange columns to group WebGL and WebGPU results
    final_columns = [
        'Model Range',
        'Mean Across Seeds_webgl', 'Std Dev Across Seeds_webgl',
        'Mean Across Seeds_webgpu', 'Std Dev Across Seeds_webgpu'
    ]
    
    merged_data = merged_data[final_columns]
    
    # Save the combined results
    output_filename = f'combined_{metric}.csv'
    merged_data.to_csv(output_filename, index=False)
    print(f'Combined {metric} results saved to {output_filename}')

# Files for WebGL and WebGPU results
webgl_files = {
    'CPU Usage': r'wyniki\webgl\CPU Usage_summary.csv',
    'FPS': r'wyniki\webgl\FPS_summary.csv',
    'Memory Usage (usedJSHeapSize)': r'wyniki\webgl\Memory Usage_summary.csv',
    'Total JS Heap Size': r'wyniki\webgl\Total JS Heap Size_summary.csv',
    'Draw Calls': r'wyniki\webgl\Draw Calls_summary.csv',
    'VRAM Usage': r'wyniki\webgl\VRAM Usage_summary.csv',
    'Frame Time': r'wyniki\webgl\Frame Time_summary.csv',
    'Load Time': r'wyniki\webgl\Load Time_summary.csv'
}

webgpu_files = {
    'CPU Usage': r'wyniki\webgpu\CPU Usage_summary.csv',
    'FPS': r'wyniki\webgpu\FPS_summary.csv',
    'Memory Usage (usedJSHeapSize)': r'wyniki\webgpu\Memory Usage_summary.csv',
    'Total JS Heap Size': r'wyniki\webgpu\Total JS Heap Size_summary.csv',
    'Draw Calls': r'wyniki\webgpu\Draw Calls_summary.csv',
    'VRAM Usage': r'wyniki\webgpu\VRAM Usage_summary.csv',
    'Frame Time': r'wyniki\webgpu\Frame Time_summary.csv',
    'Load Time': r'wyniki\webgpu\Load Time_summary.csv'
}

# Combine results for each metric
for metric in webgl_files.keys():
    merge_results(webgl_files[metric], webgpu_files[metric], metric)
