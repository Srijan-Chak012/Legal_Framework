import pandas as pd

# Load the top state matches from CSV
results_df = pd.read_csv('extracted_state_judgements.csv')

# Filter out rows where 'Top State' is None
valid_results_df = results_df.dropna(subset=['Top State'])

# Create a frequency table by counting occurrences of each state
state_frequency = valid_results_df['Top State'].value_counts().reset_index()

# Rename columns for clarity
state_frequency.columns = ['State', 'Frequency']

# Sort the frequency table in descending order
state_frequency = state_frequency.sort_values(by='Frequency', ascending=False)

# Save the frequency table to a CSV file
state_frequency.to_csv('state_frequency_table.csv', index=False)

# Display the frequency table (optional)
print(state_frequency)
