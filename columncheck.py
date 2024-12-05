import pandas as pd

file_path = 'data/src/Financial Sample.xlsx'
df = pd.read_excel(file_path, engine="openpyxl")

print(df.columns)