from haversine import haversine
from datetime import datetime, timezone
import math

"""
    Find the nearest Transport record to the target coordinates.

    Parameters:
    df : DataFrame
        DataFrame containing 'lat' and 'lon' columns.
    target_coords : tuple
        Tuple containing the target latitude and longitude.

    Returns:
    nearest_transport_id : UUID or None
        The ID of the nearest Transport record or None if no transport is found.
"""
def find_nearest_transport(df, target_coords):
    distances = []

    # Extract target latitude and longitude
    target_lat, target_lon = target_coords

    # Calculate distances for each row in the DataFrame
    for index, row in df.iterrows():
        lat = float(row['lat'])  
        lon = float(row['lon'])  
        distance = haversine((target_lat, target_lon), (lat, lon))
        distances.append(distance)

    if not distances:
        return None

    # Find the index of the smallest distance
    min_index = distances.index(min(distances))
    nearest_transport_id = df.iloc[min_index]["id"]
    nearest_distance = distances[min_index]

    # Return the nearest transport
    return nearest_transport_id, nearest_distance

'''
updated_at needs to be in this format => 2024-10-06 11:06:44.456247+00
tau is in seconds
significance of tau: tau controls the rate at which the score decays over time
default to 1800 ==> 30 mins / this means that the score will decrease by approx 63% every 30 minutes
Purpose: To reduce the score of a venue over time
Why: To prioritize recent interactions over older ones
How: The score decreases exponentially as time passes
'''
def calculate_decay_factor(updated_time, tau=1800):
    if updated_time is None:
        return 1
    else:
        # Ensure updated_at is a datetime object and get the current time
        if isinstance(updated_time, str):
            updated_time = datetime.fromisoformat(updated_time)

        now = datetime.now(timezone.utc)  
        t = (now - updated_time).total_seconds() 
        return math.exp(-t / tau)

'''
Purpose: To Promote less popular venue
Why: To prevent dominant venues from always ranking first
How: Add a bonus to venue with lower ranks
Alpha => higher alpha will strongly promote less popular venues
'''
def calculate_novelty_bonus(index, alpha=0.5):
    return alpha * (10 - (index))

'''
We are using time decay algorithm to reduce venue scores exponentially over time to prioritize recent interactions
'''
def get_score(venue, index):
    # Decay factor and novelty bonus calculation
    current_score = venue.search_score
    decay_factor = calculate_decay_factor(venue.updated_at)
    novelty_bonus = calculate_novelty_bonus(index)
    return (current_score * decay_factor) + novelty_bonus
