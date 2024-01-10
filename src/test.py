
import pandas as pd

# Sample DataFrame
df = pd.DataFrame({
    'A': [1, 0, 3, 0],
    'B': [4, 0, 6, 0],
    'C': [7, 0, 9, 0]
})

# Specify the columns to check for sum
columns_to_check = ['A', 'B']

# Filter out rows where the sum of specified columns is zero
df_filtered = df[df[columns_to_check].sum(axis=1) != 0]

print(df_filtered)