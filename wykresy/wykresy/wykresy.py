import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data from the text file 
results_file = 'webgl-chrome-v2-performance-results.txt'

data = {
    "timestamp": [],
    "cpuUsage": [],
    "usedJSHeapSize": [],
    "totalJSHeapSize": [],
    "modelCount": [],
    "fps": [],
}

# Read the file and extract the data
with open(results_file, 'r') as file:
    lines = file.readlines()
    for line in lines:
        if "Timestamp" in line:
            data["timestamp"].append(line.split(": ")[1].strip())
        elif "CPU Usage" in line:
            data["cpuUsage"].append(float(line.split(": ")[1].strip()))
        elif "Memory Usage" in line:
            data["usedJSHeapSize"].append(int(line.split(": ")[1].strip()))
        elif "Total JS Heap Size" in line:
            data["totalJSHeapSize"].append(int(line.split(": ")[1].strip()))
        elif "Number of Models" in line:
            data["modelCount"].append(int(line.split(": ")[1].strip()))
        elif "FPS" in line:
            data["fps"].append(int(line.split(": ")[1].strip()))

# Create a DataFrame for easier analysis
df = pd.DataFrame(data)

# Convert timestamps to datetime and calculate elapsed time in seconds
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['elapsed_time'] = (df['timestamp'] - df['timestamp'].iloc[0]).dt.total_seconds()

# Group by model count and calculate statistics
grouped = df.groupby('modelCount').agg({
    'cpuUsage': ['mean', 'std', 'count'],
    'usedJSHeapSize': ['mean', 'std', 'count'],
    'totalJSHeapSize': ['mean', 'std', 'count'],
    'fps': ['mean', 'std', 'count']
})

# Calculate confidence intervals
grouped['cpuUsage', 'ci'] = 1.96 * grouped['cpuUsage', 'std'] / np.sqrt(grouped['cpuUsage', 'count'])
grouped['usedJSHeapSize', 'ci'] = 1.96 * grouped['usedJSHeapSize', 'std'] / np.sqrt(grouped['usedJSHeapSize', 'count'])
grouped['totalJSHeapSize', 'ci'] = 1.96 * grouped['totalJSHeapSize', 'std'] / np.sqrt(grouped['totalJSHeapSize', 'count'])
grouped['fps', 'ci'] = 1.96 * grouped['fps', 'std'] / np.sqrt(grouped['fps', 'count'])

# Plot CPU Usage vs. Number of Models
plt.figure(figsize=(10, 6))
plt.errorbar(grouped.index, grouped['cpuUsage', 'mean'], yerr=grouped['cpuUsage', 'ci'], fmt='o', color='r', ecolor='lightcoral', capsize=5)
plt.title('CPU Usage vs. Number of Models (with 95% Confidence Intervals)')
plt.xlabel('Number of Models')
plt.ylabel('CPU Usage (ms)')
plt.grid(True)
plt.savefig('cpu_usage_vs_models.png')
plt.show()

# Plot Memory Usage vs. Number of Models
plt.figure(figsize=(10, 6))
plt.errorbar(grouped.index, grouped['usedJSHeapSize', 'mean'], yerr=grouped['usedJSHeapSize', 'ci'], fmt='o', color='g', ecolor='lightgreen', capsize=5)
plt.title('Memory Usage vs. Number of Models (with 95% Confidence Intervals)')
plt.xlabel('Number of Models')
plt.ylabel('Used JS Heap Size (bytes)')
plt.grid(True)
plt.savefig('memory_usage_vs_models.png')
plt.show()

# Plot Total JS Heap Size vs. Number of Models
plt.figure(figsize=(10, 6))
plt.errorbar(grouped.index, grouped['totalJSHeapSize', 'mean'], yerr=grouped['totalJSHeapSize', 'ci'], fmt='o', color='b', ecolor='lightblue', capsize=5)
plt.title('Total JS Heap Size vs. Number of Models (with 95% Confidence Intervals)')
plt.xlabel('Number of Models')
plt.ylabel('Total JS Heap Size (bytes)')
plt.grid(True)
plt.savefig('total_heap_vs_models.png')
plt.show()

# Plot FPS vs. Number of Models
plt.figure(figsize=(10, 6))
plt.errorbar(grouped.index, grouped['fps', 'mean'], yerr=grouped['fps', 'ci'], fmt='o', color='purple', ecolor='lavender', capsize=5)
plt.title('FPS vs. Number of Models (with 95% Confidence Intervals)')
plt.xlabel('Number of Models')
plt.ylabel('FPS')
plt.grid(True)
plt.savefig('fps_vs_models.png')
plt.show()

# Plot Memory Usage Ratio (Percentage of Heap Used)
df['memoryUsageRatio'] = (df['usedJSHeapSize'] / df['totalJSHeapSize']) * 100
plt.figure(figsize=(12, 6))
plt.plot(df['elapsed_time'], df['memoryUsageRatio'], color='green', label='Memory Usage Ratio (%)')
plt.title('Memory Usage Ratio Over Time')
plt.xlabel('Elapsed Time (seconds)')
plt.ylabel('Memory Usage Ratio (%)')
plt.ylim(0, 100)  # Since it's a percentage, limit the y-axis to 0-100%
plt.grid(True)
plt.savefig('memory_usage_ratio.png')
plt.show()

# Plot Area Chart for Memory Utilization
plt.figure(figsize=(12, 6))
plt.fill_between(df['elapsed_time'], df['usedJSHeapSize'], color='lightblue', label='Used JS Heap Size (bytes)')
plt.plot(df['elapsed_time'], df['totalJSHeapSize'], color='red', linestyle='--', label='Total JS Heap Size (bytes)')
plt.title('JavaScript Heap Memory Utilization Over Time')
plt.xlabel('Elapsed Time (seconds)')
plt.ylabel('Memory Usage (bytes)')
plt.legend()
plt.grid(True)
plt.savefig('area_chart_heap_size.png')
plt.show()
