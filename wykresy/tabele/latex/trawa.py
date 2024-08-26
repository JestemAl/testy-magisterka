import os
import pandas as pd

# Function to generate LaTeX table code from a dataframe
def generate_latex_table(df, caption, label):
    # Round all numerical data to 2 decimal places
    df = df.round(2)
    
    # Remove the 'Średnia' and 'Odchylenie standardowe' columns if they exist
    if 'Średnia' in df.columns:
        df = df.drop(columns=['Średnia'])
    if 'Odchylenie standardowe' in df.columns:
        df = df.drop(columns=['Odchylenie standardowe'])
    
    num_columns = len(df.columns) - 1  # The first column is the "Przedział liczby modeli"
    
    # Begin the LaTeX table environment with adjustbox
    latex_code = "\\begin{adjustbox}{max width=\\textwidth}\n\\begin{tabular}{|>{\\centering\\arraybackslash}m{3cm}|" + "m{1.5cm}<{\centering}|" * num_columns + "}\n"
    latex_code += "\\hline\n"
    
    # Add the multi-row and multi-column header
    latex_code += "\\multirow{2}{*}{{\\centering \\shortstack{Przedział\\\\liczby modeli}}} & \\multicolumn{" + str(num_columns) + "}{c|}{\\centering Średnie zużycie CPU dla różnych ilości trawy} \\\\\n\\cline{2-" + str(num_columns + 1) + "}\n"
    
    # Extract column names for the Grass Amount values
    columns = df.columns[1:]  # All columns except the first one
    latex_code += " & " + " & ".join(columns) + " \\\\\n\\hline\n"
    
    # Add the data rows
    for index, row in df.iterrows():
        row_data = " & ".join(row.astype(str))
        latex_code += row_data + " \\\\\n\\hline\n"
    
    # End the table environment
    latex_code += "\\end{tabular}\n\\end{adjustbox}\n"
    latex_code += f"\\caption{{{caption}}}\n"
    latex_code += f"\\label{{{label}}}\n"
    latex_code += "\\end{table}\n"
    
    return latex_code

# List of all CSV files and their respective labels and captions
files_info = [
    ('aggregated_Draw Calls_summary.csv', 'Draw Calls by Grass Amount', 'tab:draw_calls_grass'),
    ('aggregated_FPS_summary.csv', 'FPS by Grass Amount', 'tab:fps_grass'),
    ('aggregated_GPU Frame Time_summary.csv', 'GPU Frame Time by Grass Amount', 'tab:gpu_frame_time_grass'),
    ('aggregated_Total Frame Time_summary.csv', 'Total Frame Time by Grass Amount', 'tab:total_frame_time_grass'),
    ('aggregated_CPU Frame Time_summary.csv', 'CPU Frame Time by Grass Amount', 'tab:cpu_frame_time_grass'),
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
with open("generated_grass_tables.tex", "w") as f:
    f.write(latex_document)

print("LaTeX tables generated and saved to 'generated_grass_tables.tex'")
