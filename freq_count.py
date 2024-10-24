import pandas as pd

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('output.csv')

# Initialize an empty dictionary to store counts
act_counts = {}

# Assuming the column name is 'Acts'
column_name = 'Acts/Rules/Orders'

# Loop through each row in the DataFrame
count = 0
for index, row in df.iterrows():
    if count == 6:
        break
    count += 1
    
    entries = row[column_name].split('; ') if pd.notna(row[column_name]) else []  # Split the entries by semicolon and space
    
    # Iterate through the entries and update the dictionary counts
    for entry in entries:
        # Trim any leading or trailing whitespaces to ensure key matching
        entry = entry.strip()
        act_counts[entry] += 1

# Print the dictionary with counts in the specified format
for act, count in act_counts.items():
    print(f'{act}: {count}')




