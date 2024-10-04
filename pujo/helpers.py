from haversine import haversine

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
        lat = float(row["lat"])
        lon = float(row["lon"])
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
    
