import pandas as pd
import json

# Load the JSON file into a Python object
with open('output.json', 'r') as f:
    data = json.load(f)

# Convert the object to a pandas DataFrame
df = pd.json_normalize(data)

# Save the DataFrame to a CSV file
df.to_csv('output.csv', index=True)
df.to_excel('output.xlsx', index=True)

df = pd.read_excel('output.xlsx')
df = df[['Manu_ID', 'Case_No', 'Court', 'Date', 'Subject', 'Case Category', 'Acts/Rules/Orders', 'Hon\'ble Judges/Coram', 'Appellant', 'Respondent', 'Counsel for Appellant', 'Counsel for Respondent', 'Disposition', 'relied on', 'Case Note', 'discussed', 'Cases Referred', 'Judgement']]

df.to_excel('output_arrange.xlsx', index=True)