import pandas as pd
import spacy
from collections import Counter
from tqdm import tqdm
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# Load the CSV file
file_path = 'output.csv'  # Replace with your actual file path
data = pd.read_csv(file_path)

#Consider only the first 10 rows for demonstration purposes
# data = data.head(10)

# Load a pre-trained NLP model for English
nlp = spacy.load('en_core_web_sm')

# Initialize geolocator
geolocator = Nominatim(user_agent="geoapiExercises", timeout=10)  # Increased timeout
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1, max_retries=5)  # Increased retries

# Function to extract geographical locations from the "Judgement" column
def extract_locations(text):
    if isinstance(text, str):  # Check if the input is a valid string
        doc = nlp(text)
        locations = [ent.text for ent in doc.ents if ent.label_ == 'GPE']
        return locations
    return []  # Return an empty list for non-string entries

# Function to map locations to states using geopy
def map_to_state(locations):
    states = []
    # Write for loop to geocode each location and extract the state with tqdm progress bar
    for loc in tqdm(locations, desc='Geocoding', unit='location'):
        try:
            location = geocode(loc)
            print(location)
            if location:
                address = location.raw.get('address', {})
                state = address.get('state')
                if state:
                    states.append(state)
        except Exception as e:
            print(f"Error geocoding {loc}: {e}")
    return states


# Apply the functions to the "Judgement" column with tqdm progress bar
tqdm.pandas()  # Enable tqdm for pandas
data['Locations'] = data['Judgement'].progress_apply(extract_locations)
print(data['Locations'])

# Create a frequency table of the extracted locations
all_locations = [loc for sublist in data['Locations'] for loc in sublist]
location_counts = Counter(all_locations)
location_freq_df = pd.DataFrame(location_counts.items(), columns=['Location', 'Frequency'])
location_freq_df = location_freq_df.sort_values(by='Frequency', ascending=False)
print(location_freq_df.head(10))

# Write the extracted locations to a CSV file in descending order of frequency
output_file = 'extracted_locations.csv'
location_freq_df.to_csv(output_file, index=False)
print(f"Extracted locations saved to {output_file}")
