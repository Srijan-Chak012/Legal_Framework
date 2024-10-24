import pandas as pd
import json

# Read the JSON data from a file
with open('dictionary.json', 'r') as file:
    json_data = json.load(file)

# Create a DataFrame from the JSON data
df = pd.DataFrame(json_data)

# Write the DataFrame to an Excel file
df.to_excel('dictionary.xlsx', index=False)

print("Data written to dictionary.xlsx file.")
