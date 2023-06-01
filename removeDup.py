#!/usr/bin/env python3
import pandas as pd

input_file = "2104.csv"
output_file = "output.csv"

# Read the input CSV file into a DataFrame
df = pd.read_csv(input_file)

# Drop duplicate rows based on the "Player" column
df = df.drop_duplicates(subset="Player", keep="first")

# Write the modified DataFrame to the output CSV file
df.to_csv(output_file, index=False)

print("Duplicates removed. Output saved to", output_file)
