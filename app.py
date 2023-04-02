import streamlit as st
import requests

# Define the API endpoint for getting nearby places
PLACES_API_ENDPOINT = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

def get_nearby_places(location, type):
    params = {
        "location": location,
        "type": type,
        "radius": "5000",  # in meters
        "key": "YOUR_API_KEY_HERE"
    }
    response = requests.get(PLACES_API_ENDPOINT, params=params)
    data = response.json()
    return data["results"]

# Define the Streamlit app
def app():
    st.title("Travel Guide")
    st.write("Tell me your location and the type of places you want to visit, and I'll suggest some nearby options!")
    
    # User input
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
    
    # Get nearby places based on user input
    if location:
        nearby_places = get_nearby_places(location, place_type)
        if nearby_places:
            st.write("Here are some nearby places you might be interested in:")
            for place in nearby_places:
                st.write("- " + place["name"])
        else:
            st.write("Sorry, I couldn't find any nearby places of that type.")
    
    st.write("---")
    st.write("Do you want to visit places of a similar type near one of the nearby places I just suggested?")
    select_place = st.selectbox("Select a nearby place", [place["name"] for place in nearby_places])
    if select_place:
        selected_place = next(place for place in nearby_places if place["name"] == select_place)
        similar_places = get_nearby_places(
            f"{selected_place['geometry']['location']['lat']},{selected_place['geometry']['location']['lng']}",
            selected_place["types"][0]
        )
        if similar_places:
            st.write("Here are some similar places nearby:")
            for place in similar_places:
                st.write("- " + place["name"])
        else:
            st.write("Sorry, I couldn't find any similar places nearby.")
