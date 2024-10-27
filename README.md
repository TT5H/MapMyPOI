
# MapMyPOI

Discover points of interest within a radius of any location with MapMyPOI. This tool visually highlights places nearby on an interactive map and enables easy data export to text or Excel files.

## Features
- **Retrieve POIs**: Fetches points of interest (POIs) like restaurants, parks, hotels, and more within a user-defined radius from any address.
- **Interactive Map**: Displays POIs on a map with a circle radius indicator for visual clarity.
- **Save Results**: Allows users to save results in `.txt` or `.xlsx` format.
- **User-friendly Interface**: Built using Tkinter for easy navigation and interaction.

## Requirements
Ensure the following libraries are installed:
```bash
pip install requests geopy folium openpyxl
```

## Usage
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/TT5H/MapMyPOI.git
   cd MapMyPOI
   ```

2. **Run the Application**:
   ```bash
   python mapmypoi.py
   ```

3. **Enter the Required Information**:
   - **Google API Key**: Enter your Google Places API Key.
   - **Address**: The central address around which POIs are to be found.
   - **Radius (km)**: The search radius in kilometers.
   - **POI Type**: Type of places to search for (e.g., restaurant, park, hotel).

4. **View and Save Results**:
   - The app will display the POIs within the specified radius on an interactive map.
   - Users can save data in `.txt` or `.xlsx` format based on their preference.

## Code Structure
- `get_lat_long_from_address`: Fetches latitude and longitude for the provided address using the Google Maps API.
- `get_pois_within_radius`: Retrieves POIs of the specified type within the given radius using the Google Places API.
- `create_map_with_pois`: Generates an HTML map showing POIs and a radius circle.
- `save_results`: Saves address and POI details in `.txt` or `.xlsx` format.

## Example
1. **Set Up**: Enter your Google API Key.
2. **Search**: Input an address, such as "Central Park, New York".
3. **Specify Radius**: Choose a radius, such as 5 km, and enter a POI type, like "restaurant".
4. **Map Visualization**: MapMyPOI will display an interactive map of nearby restaurants around Central Park, with the option to save the data.


