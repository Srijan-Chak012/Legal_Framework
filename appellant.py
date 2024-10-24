import pandas as pd
from collections import Counter

# Load the CSV file (assuming there's a column named 'appellant category')
file_path = 'manupatra_anno.csv'  # Replace with your actual file path
data = pd.read_csv(file_path)

# Normalize the categories by converting to lowercase and stripping extra spaces
categories_list = data['Appelant Category'].dropna().apply(lambda x: x.lower().strip())

# Use Counter to count the frequency of each category
category_counts = Counter(categories_list)

# Convert the Counter object to a DataFrame
frequency_table = pd.DataFrame(category_counts.items(), columns=['Category', 'Frequency'])

# Sort the DataFrame by 'Frequency' in descending order
frequency_table_sorted = frequency_table.sort_values(by='Frequency', ascending=False)

# Display the sorted frequency table
print(frequency_table_sorted)

# Save the sorted frequency table to a CSV file
frequency_table_sorted.to_csv('appellant_category_frequency_table.csv', index=False)