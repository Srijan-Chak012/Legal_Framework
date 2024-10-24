import pandas as pd
from collections import Counter

# Load the CSV file
file_path = 'manupatra_anno.csv'  # Replace with your actual file path
data = pd.read_csv(file_path)

# Normalize topics to lowercase and split the comma-separated values
topics_list = data['Case Topics'].dropna().apply(lambda x: x.lower().split(', '))

# Flatten the list of lists into a single list of topics
all_topics = [topic for sublist in topics_list for topic in sublist]

# Use Counter to count the frequency of each topic
topic_counts = Counter(all_topics)

# Convert the Counter object to a DataFrame
frequency_table = pd.DataFrame(topic_counts.items(), columns=['Topic', 'Frequency'])

# Sort the DataFrame by 'Frequency' in descending order
frequency_table_sorted = frequency_table.sort_values(by='Frequency', ascending=False)

# Display the sorted frequency table
print(frequency_table_sorted)

# Save the sorted frequency table to a CSV file
frequency_table_sorted.to_csv('topic_frequency_table.csv', index=False)