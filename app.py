import streamlit as st
import json
from modules.youtube_search import search_youtube
from modules.audio_to_text import transcribe_video
from modules.watsonx_api import generate_instructions

# Load countries and forms
with open("data/countries_and_forms.json", "r") as f:
    country_data = json.load(f)

st.title("AI Tax Form Helper")

# Select country and tax form
selected_country = st.selectbox("Select your country", list(country_data.keys()))
selected_form = st.selectbox("Select a tax form", country_data[selected_country])

if st.button("Find Help"):
    with st.spinner("Searching for videos..."):
        # Step 1: Search YouTube
        videos = search_youtube(selected_country, selected_form)
        
    if not videos:
        st.error("No relevant videos found!")
    else:
        with st.spinner("Transcribing videos..."):
            # Step 2: Transcribe audio to text
            transcripts = [transcribe_video(video) for video in videos]
        
        st.write("Transcriptions:")
        for idx, transcript in enumerate(transcripts):
            st.write(f"**Video {idx + 1}:**")
            st.write(transcript)

        with st.spinner("Generating detailed instructions..."):
            # Step 3: Generate instructions
            detailed_guide = generate_instructions(selected_country, selected_form, transcripts)
        
        st.write("**Detailed Instructions:**")
        st.write(detailed_guide)

        st.download_button("Download Instructions", detailed_guide, file_name="tax_guide.txt")
