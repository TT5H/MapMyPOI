import tkinter as tk
from tkinter import messagebox, filedialog
import requests
import openpyxl
from geopy.geocoders import Nominatim
import folium

# Function to get latitude and longitude using Google Maps API
def get_lat_long_from_address(address, google_api_key):
    """Fetch latitude and longitude for a given address using Google Maps API."""
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={google_api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            messagebox.showerror("Error", f"No results found for the address: {address}")
    else:
        messagebox.showerror("Error", f"Error fetching data from Google API: {response.status_code}")
    return None, None

# Function to get points of interest within a radius
def get_pois_within_radius(lat, lng, radius_km, google_api_key, poi_type):
    """Retrieve POIs of a specified type within a defined radius using Google Places API."""
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius_km * 1000}&type={poi_type}&key={google_api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['results']
    else:
        messagebox.showerror("Error", f"Error fetching POIs from Google API: {response.status_code}")
        return []

# Function to create an interactive map displaying POIs within a radius
def create_map_with_pois(lat, lng, pois, radius_km, address):
    """Generate an HTML map with POI markers and a radius circle."""
    map_center = [lat, lng]
    m = folium.Map(location=map_center, zoom_start=14)

    # Add radius circle to the map
    folium.Circle(
        location=map_center,
        radius=radius_km * 1000,  # Convert km to meters
        color='blue',
        fill=True,
        fill_opacity=0.3,
        popup=f'{radius_km} km radius around {address}'
    ).add_to(m)

    # Add markers for each POI
    for poi in pois:
        poi_name = poi['name']
        poi_lat = poi['geometry']['location']['lat']
        poi_lng = poi['geometry']['location']['lng']
        folium.Marker(
            location=[poi_lat, poi_lng],
            tooltip=poi_name,
            popup=f"{poi_name}\n{poi.get('vicinity', '')}"
        ).add_to(m)

    # Save the map as an HTML file
    map_file = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
    if map_file:
        m.save(map_file)
        messagebox.showinfo("Success", f"Map with POIs saved as {map_file}")

# Function to save POI data to a file
def save_results(addresses_results):
    """Save address and POI details in .txt or .xlsx format based on user choice."""
    file_format = format_var.get()
    filename = filedialog.asksaveasfilename(defaultextension=f".{file_format}", filetypes=[(f"{file_format.upper()} files", f"*.{file_format}")])
    if file_format == "txt":
        with open(filename, 'w') as file:
            for address, pois in addresses_results.items():
                file.write(f"{address}:\n")
                for poi in pois:
                    file.write(f"{poi['name']} - {poi.get('vicinity', '')}\n")
                file.write("\n")
        messagebox.showinfo("Success", f"Results saved to {filename}")
    elif file_format == "xlsx":
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(["Address", "POI Name", "Location"])
        for address, pois in addresses_results.items():
            for poi in pois:
                sheet.append([address, poi['name'], poi.get('vicinity', '')])
        workbook.save(filename)
        messagebox.showinfo("Success", f"Results saved to {filename}")

# Function to process the address input and find POIs
def process_address():
    """Main function to process input data, retrieve POIs, and display/save results."""
    address = address_entry.get()
    radius_km = int(radius_entry.get())
    google_api_key = api_key_entry.get()
    poi_type = poi_type_entry.get()

    lat, lng = get_lat_long_from_address(address, google_api_key)
    if lat and lng:
        pois = get_pois_within_radius(lat, lng, radius_km, google_api_key, poi_type)
        addresses_results = {address: pois}

        create_map_with_pois(lat, lng, pois, radius_km, address)

        save_option = messagebox.askyesno("Save Results", "Do you want to save the results?")
        if save_option:
            save_results(addresses_results)

# GUI setup
app = tk.Tk()
app.title("MapMyPOI")

tk.Label(app, text="Google API Key:").grid(row=0, column=0)
api_key_entry = tk.Entry(app, width=50)
api_key_entry.grid(row=0, column=1)

tk.Label(app, text="Address:").grid(row=1, column=0)
address_entry = tk.Entry(app, width=50)
address_entry.grid(row=1, column=1)

tk.Label(app, text="Radius (km):").grid(row=2, column=0)
radius_entry = tk.Entry(app, width=50)
radius_entry.grid(row=2, column=1)

tk.Label(app, text="POI Type (e.g., restaurant, park, hotel):").grid(row=3, column=0)
poi_type_entry = tk.Entry(app, width=50)
poi_type_entry.grid(row=3, column=1)

tk.Button(app, text="Find POIs", command=process_address).grid(row=4, column=1)

# Dropdown for save file format
format_var = tk.StringVar(app)
format_var.set("txt")  # Default format
tk.Label(app, text="Save Format:").grid(row=5, column=0)
tk.OptionMenu(app, format_var, "txt", "xlsx").grid(row=5, column=1)

app.mainloop()
