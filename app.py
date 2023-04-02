import streamlit as st
import requests

# Define the API endpoint for getting nearby places
PLACES_API_ENDPOINT = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

def get_nearby_places(location, place_type):
    params = {
        "location": location,
        "type": place_type,
        "radius": "5000",  # in meters
        "key": "AIzaSyBVV-ASnn4IHJ-AtlUr71ftlQjg7-ovwG4"
    }
    response = requests.get(PLACES_API_ENDPOINT, params=params)
    data = response.json()
    return data["results"]

# Define the Streamlit app
def app():
    # Set up the app layout
    st.set_page_config(page_title="Travel Guide", page_icon=":airplane:", layout="wide")
    st.title("Travel Guide")
    
    # Get user input for location and place type
    location = st.text_input("Where are you now?")
    place_type = st.selectbox("What type of place do you want to visit?", [
        "All", "Museums", "Restaurants", "Hotels", "Parks"
    ])
    
    # Convert place type to Google Maps API type
    if place_type == "All":
        place_type = ""
    elif place_type == "Museums":
        place_type = "museum"
    elif place_type == "Restaurants":
        place_type = "restaurant"
    elif place_type == "Hotels":
        place_type = "lodging"
    elif place_type == "Parks":
        place_type = "park"
    
    # Display nearby places based on user input
    if location:
        st.subheader("Nearby Places")
        nearby_places = get_nearby_places(location, place_type)
        if nearby_places:
            for place in nearby_places:
                st.write(f"- {place['name']} ({place['vicinity']})")
        else:
            st.write("Sorry, I couldn't find any nearby places of that type.")
    
    # Allow user to select a nearby place and show similar places
    if nearby_places:
        st.subheader("Similar Places")
        select_place = st.selectbox("Select a nearby place to see similar places", [place["name"] for place in nearby_places])
        if select_place:
            selected_place = next(place for place in nearby_places if place["name"] == select_place)
            similar_places = get_nearby_places(
                f"{selected_place['geometry']['location']['lat']},{selected_place['geometry']['location']['lng']}",
                selected_place["types"][0]
            )
            if similar_places:
                for place in similar_places:
                    st.write(f"- {place['name']} ({place['vicinity']})")
            else:
                st.write("Sorry, I couldn't find any similar places nearby.")
