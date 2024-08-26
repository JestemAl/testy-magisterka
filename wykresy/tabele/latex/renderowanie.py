import os
import pandas as pd

# Function to generate LaTeX table code from a dataframe
def generate_latex_table(df, caption, label):
    latex_code = "\\begin{table}[H]\n\\centering\n\\begin{tabular}{|l" + " |c" * (len(df.columns) - 1) + "|}\n"
    latex_code += "\\hline\n"
    
    # Add the header row
    headers = " & ".join(df.columns)
    latex_code += headers + " \\\\\n\\hline\n"
    
    # Add the data rows
    for index, row in df.iterrows():
        row_data = " & ".join(row.astype(str))
        latex_code += row_data + " \\\\\n"
    
    # End the table environment
    latex_code += "\\hline\n\\end{tabular}\n"
    latex_code += f"\\caption{{{caption}}}\n"
    latex_code += f"\\label{{{label}}}\n"
    latex_code += "\\end{table}\n"
    
    return latex_code

# List of all CSV files and their respective labels and captions
files_info = [
    ('combined_FPS_by_model_count_with_mean_std.csv', 'FPS by Model Count', 'tab:fps_model_count'),
    ('combined_GPU Frame Time_by_model_count_with_mean_std.csv', 'GPU Frame Time by Model Count', 'tab:gpu_frame_time'),
    ('combined_Total Frame Time_by_model_count_with_mean_std.csv', 'Total Frame Time by Model Count', 'tab:total_frame_time'),
    ('combined_CPU Frame Time_by_model_count_with_mean_std.csv', 'CPU Frame Time by Model Count', 'tab:cpu_frame_time'),
    ('combined_Draw Calls_by_model_count_with_mean_std.csv', 'Draw Calls by Model Count', 'tab:draw_calls'),
]

# Path where the files are stored
base_path = '.'

# Generate LaTeX code for each file
latex_tables = []
for file_name, caption, label in files_info:
    file_path = os.path.join(base_path, file_name)
    df = pd.read_csv(file_path)
    latex_code = generate_latex_table(df, caption, label)
    latex_tables.append(latex_code)

# Join all LaTeX table codes into a single string
latex_document = "\n\n".join(latex_tables)

# Save the LaTeX document to a file
with open("generated_tables.tex", "w") as f:
    f.write(latex_document)

print("LaTeX tables generated and saved to 'generated_tables.tex'")
