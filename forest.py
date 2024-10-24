import pandas as pd
from datetime import datetime
import re

# Function to check for forest-related topics (accounting for typos)
def contains_forest(topic):
    # Check if the input is a string
    if isinstance(topic, str):
        # Define a regex pattern to account for common spelling mistakes or variations
        forest_pattern = re.compile(r'\b(f[o0r]{1,2}e?[s5]{1,2}t)\b', re.IGNORECASE)
        return bool(forest_pattern.search(topic))
    return False  # Return False if topic is not a string (e.g., NaN or float)

# Load the CSV file
df = pd.read_csv('manupatra_anno.csv')

# Convert the 'date' column to datetime
df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y', errors='coerce')

# Total forest cases count
df_total_forest_cases = df['Case Topics'].apply(contains_forest).sum()

# Print the total number of forest-related cases
print(df_total_forest_cases)

# Filter cases after 2006
df_after_2006 = df[df['Date'].dt.year > 2006].copy()  # Use .copy() to avoid the slice issue

df_after_2006.loc[:, 'contains_forest'] = df_after_2006['Case Topics'].apply(contains_forest)

# Get the count of cases containing 'forest'
forest_cases_count = df_after_2006['contains_forest'].sum()

# Get the count of cases containing 'forest'
forest_cases_count = df_after_2006['contains_forest'].sum()

# Print the count of cases containing 'forest'
print(forest_cases_count)