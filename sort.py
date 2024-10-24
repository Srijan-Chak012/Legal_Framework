import pandas as pd

# Load the CSV file
file_path = 'topic_frequency_table.csv'  # Replace with your actual file path
data = pd.read_csv(file_path)

# Rename the columns for easier manipulation
data.columns = ['Topic', 'Frequency']

# Sort the data by 'Frequency' in descending order
sorted_data = data.sort_values(by='Frequency', ascending=False)

# Sum up the values in the 'Frequency' column
total_sum = sorted_data['Frequency'].sum()

# Display the sorted data and total sum
print(sorted_data)
print(f'Total sum of Frequency: {total_sum}')

# Write back the sorted data to the state_frequency_table.csv file
sorted_data.to_csv(file_path, index=False)
