import pandas as pd
from fuzzywuzzy import process

# Load the data from output.csv file
data = pd.read_csv('output.csv')

# Known Indian states (you can add more if necessary)
states = [
    'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
    'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka',
    'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
    'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu',
    'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal',
    'Delhi'
]

# Function to match location to state using fuzzy matching and return top result
def match_state(location):
    best_match = process.extractOne(location, states)
    return best_match  # Returns both the state and the confidence score

# Create a list to store results
results = []

# Apply the function to all rows and store the top match
for index, row in data.iterrows():
    judgement_text = row['Judgement']
    
    # Ensure the judgement_text is a valid string
    if isinstance(judgement_text, str):
        top_match = match_state(judgement_text)  # Get the top fuzzy match based on the Judgement text
        results.append({
            'Judgement': judgement_text,
            'Top State': top_match[0],  # State
            'Confidence': top_match[1]  # Confidence score
        })
    else:
        # If judgement_text is not a string, append a None or handle accordingly
        results.append({
            'Judgement': judgement_text,
            'Top State': None,  # No state could be matched
            'Confidence': None  # No confidence score
        })

# Convert the results into a DataFrame
results_df = pd.DataFrame(results)

# Write the results to a CSV file
results_df.to_csv('extracted_state_judgements.csv', index=False)

# Display the results (optional)
# print(results_df)
