import pandas as pd
import re

# Function to check if topics include "mining" and either "land dispute" or "pollution" (accounting for typos)
def contains_mining_and_other_topics(topic):
    if isinstance(topic, str):
        # Regex patterns to account for common spelling mistakes
        mining_pattern = re.compile(r'\b(m[i1]{1,2}n[i1]{1,2}ng)\b', re.IGNORECASE)
        land_dispute_pattern = re.compile(r'\b(land[\s_-]?dispute)\b', re.IGNORECASE)
        pollution_pattern = re.compile(r'\b(pollut[i1]{1,2}on)\b', re.IGNORECASE)

        has_mining = bool(mining_pattern.search(topic))
        has_land_dispute = bool(land_dispute_pattern.search(topic))
        has_pollution = bool(pollution_pattern.search(topic))

        return has_mining, has_land_dispute, has_pollution
    return False, False, False  # Return False if topic is not a string (e.g., NaN or float)

# Load the CSV file
df = pd.read_csv('manupatra_anno.csv')

# Apply the contains_mining_and_other_topics function to 'case topics' column
df[['has_mining', 'has_land_dispute', 'has_pollution']] = df['Case Topics'].apply(
    lambda x: pd.Series(contains_mining_and_other_topics(x))
)

# Filter for cases that contain "mining"
mining_cases_df = df[df['has_mining']]

print (len(mining_cases_df))
# Calculate the distribution
land_dispute_only = mining_cases_df[(mining_cases_df['has_land_dispute']) & (~mining_cases_df['has_pollution'])].shape[0]
pollution_only = mining_cases_df[(mining_cases_df['has_pollution']) & (~mining_cases_df['has_land_dispute'])].shape[0]
both_topics = mining_cases_df[(mining_cases_df['has_land_dispute']) & (mining_cases_df['has_pollution'])].shape[0]

# Output the results
print(f"Cases with 'mining' and 'land dispute' only: {land_dispute_only}")
print(f"Cases with 'mining' and 'pollution' only: {pollution_only}")
print(f"Cases with 'mining', 'land dispute', and 'pollution': {both_topics}")
