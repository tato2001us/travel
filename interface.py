import streamlit as st

# Define the Streamlit app
def app():
    # Set up the app layout
    st.set_page_config(page_title="My Streamlit App")
    st.title("Welcome to my Streamlit app!")
    
    # Add some text and an image
    st.write("This is a basic Streamlit app interface.")
    st.write("You can add text, images, charts, and more!")
    st.image("https://picsum.photos/200")
    
    # Add a slider and a button
    age = st.slider("What is your age?", 0, 100, 25)
    if st.button("Submit"):
        st.write(f"You entered {age} as your age.")
