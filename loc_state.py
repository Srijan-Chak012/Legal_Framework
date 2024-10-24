import pandas as pd
from fuzzywuzzy import process
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# Load the data from CSV file
data = pd.read_csv('extracted_locations.csv')

# Initialize geolocator with a rate limiter
geolocator = Nominatim(user_agent="geoapiExercises")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Known Indian states (you can add more if necessary)
states = [
    'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
    'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka',
    'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
    'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu',
    'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal',
    'Delhi'
]

# Function to match location to state using fuzzy matching
def match_state(location):
    best_match = process.extractOne(location, states)
    if best_match[1] > 80:  # Only consider matches with high confidence
        return best_match[0]
    else:
        return None

# Function to get state from location using geocoding and fuzzy matching
def get_state(location):
    if isinstance(location, str):
        if 'state of' in location.lower():
            # If location is already a state
            return match_state(location)
        else:
            location_details = geocode(location)
            if location_details:
                address = location_details.raw['address']
                if 'state' in address:
                    return address['state']
            return match_state(location)
    return None

# Apply the function to map each location to a state
data['State'] = data['Location'].apply(get_state)

# Filter out rows where the state could not be determined
data = data.dropna(subset=['State'])

# Group by state and sum the frequencies
state_frequency = data.groupby('State')['Frequency'].sum().reset_index()

# Sort the results
state_frequency = state_frequency.sort_values(by='Frequency', ascending=False)

# Save or display the results
print(state_frequency)
# Optionally, save to a CSV file
state_frequency.to_csv('state_frequency.csv', index=False)
