import geopandas as gpd
import folium
from sklearn.cluster import KMeans

def generate_disaster_map(disasters):
    """
    Generates an interactive map using Folium.
    """
    # Create a base map
    disaster_map = folium.Map(location=[20.0, 0.0], zoom_start=2)

    # Add disaster markers
    for disaster in disasters:
        if disaster.latitude and disaster.longitude:
            folium.Marker(
                location=[disaster.latitude, disaster.longitude],
                popup=f"{disaster.title} ({disaster.category})",
                icon=folium.Icon(color="red" if disaster.severity == "High" else "blue")
            ).add_to(disaster_map)

    return disaster_map

def cluster_disaster_locations(disasters):
    """
    Uses KMeans clustering to identify disaster-prone zones.
    """
    # Extract coordinates
    coordinates = [
        [disaster.latitude, disaster.longitude]
        for disaster in disasters
        if disaster.latitude and disaster.longitude
    ]

    if not coordinates:
        return None

    # Apply KMeans clustering
    kmeans = KMeans(n_clusters=5, random_state=0)
    kmeans.fit(coordinates)

    return kmeans.cluster_centers_
