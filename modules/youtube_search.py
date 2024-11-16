import requests
import os
API_KEY = os.getenv("yt")

def search_youtube(country, tax_form):
    query = f"How to fill {tax_form} for {country}"
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&maxResults=2&key={API_KEY}"
    
    response = requests.get(url)
    if response.status_code != 200:
        return []

    data = response.json()
    video_ids = [item["id"]["videoId"] for item in data.get("items", [])]
    return [f"https://www.youtube.com/watch?v={video_id}" for video_id in video_ids]
