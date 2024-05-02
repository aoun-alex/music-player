import openai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import tkinter as tk
from tkinter import messagebox
import vlc
from ai_downloader_helper import DownloadTrackCommand
import json

# Strategy

current_player = None

def load_credentials():
    with open('secret.json', 'r') as f:
        credentials = json.load(f)
    return credentials

credentials = load_credentials()
openai_api_key = credentials['openai_key']
spotify_credentials = {
    'client_id': credentials['spotify_client_id'],
    'client_secret': credentials['spotify_client_secret']
}

# Base class for recommendation strategies.
class RecommendationStrategy:
    def get_recommendations(self, num_of_tracks, music_prompt, min_bpm, max_bpm):
        pass

# Implementation of genre-based music recommendation using OpenAI.
class GenreBasedRecommendation(RecommendationStrategy): #TODO: make ai features better
    def get_recommendations(self, num_of_tracks, music_prompt, min_bpm, max_bpm):
        openai.api_key = openai_api_key
        prompt = f'Recommend {music_prompt} music. You should provide {num_of_tracks} tracks. BPM should be between {min_bpm} and {max_bpm}.'
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k-0613",
            messages=[
                {"role": "system", "content": "You are an AI helpful DJ assistant with great knowledge of music."},
                {"role": "system", "content": "Always reply with a JSON array named 'tracks' with the only objects 'track' for the song name and 'artist' for the artist name."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=1,
            n=1,
            stop=None,
        )
        tracks = response.choices[0].message.content.strip()
        return tracks

# VLC player management functions.
def play_pause_preview(url, btn):
    global current_player
    if current_player is not None:
        if current_player.get_media().get_mrl() == url:
            if current_player.is_playing():
                current_player.pause()
                btn.config(text="Play")
            else:
                current_player.play()
                btn.config(text="Pause")
        else:
            current_player.stop()
            start_new_player(url, btn)
    else:
        start_new_player(url, btn)

def start_new_player(url, btn):
    global current_player
    if url == "No preview available":
        messagebox.showerror("Error", "No preview available for this track.")
        return
    current_player = vlc.MediaPlayer(url)
    current_player.play()
    update_button_states(btn)

def update_button_states(active_btn):
    for btn in play_buttons:
        if btn == active_btn:
            btn.config(text="Pause")
        else:
            btn.config(text="Play")

play_buttons = []

# Spotify recommendation based on track IDs.
def spotify_recommendations(tracks_json, sp, num_of_tracks):
    global play_buttons
    play_buttons.clear()

    track_ids = []
    for track in tracks_json:
        track_name = track['track']
        artist_name = track['artist']
        results = sp.search(q=f"track:{track_name} artist:{artist_name}", type='track', limit=1)
        if results['tracks']['items']:
            track_ids.append(results['tracks']['items'][0]['id'])

    if track_ids:
        recommendations = sp.recommendations(seed_tracks=track_ids[:5], limit=int(num_of_tracks))
        for track in recommendations['tracks']:
            track_info = f"Recommended Track: {track['name']} by {track['artists'][0]['name']}"
            results_text.insert(tk.END, track_info + '\n')
            spotify_url = track['external_urls']['spotify'] if track['external_urls']['spotify'] else "No Spotify URL available"
            preview_url = track['preview_url'] if track['preview_url'] else "No preview available"

            play_btn = tk.Button(results_text, text="Play")
            play_btn.config(command=lambda url=preview_url, b=play_btn: play_pause_preview(url, b))
            results_text.window_create(tk.END, window=play_btn)

            download_btn = tk.Button(results_text, text="Download")
            download_btn.config(command=lambda url=spotify_url: DownloadTrackCommand(url).execute())
            results_text.window_create(tk.END, window=download_btn)

            results_text.insert(tk.END, '\n\n')
            play_buttons.append(play_btn)

# Main recommendation function handling UI and logic.
def on_recommend():
    num_of_tracks = num_tracks_entry.get()
    music_prompt = music_prompt_entry.get()
    min_bpm = min_bpm_entry.get()
    max_bpm = max_bpm_entry.get()

    if not num_of_tracks or not music_prompt or not min_bpm or not max_bpm:
        messagebox.showerror("Error", "All fields are required!")
        return

    current_strategy = GenreBasedRecommendation()  # Using the genre-based strategy
    recommended_tracks = current_strategy.get_recommendations(num_of_tracks, music_prompt, min_bpm, max_bpm)

    try:
        tracks_json = json.loads(recommended_tracks)["tracks"]
    except json.JSONDecodeError as e:
        messagebox.showerror("Error", f"Failed to parse the JSON response: {e}")
        return

    if not tracks_json:
        messagebox.showinfo("Info", "No song recommendations found.")
        return

    client_credentials_manager = SpotifyClientCredentials(
        client_id=spotify_credentials['client_id'],
        client_secret=spotify_credentials['client_secret'])
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    results_text.delete(1.0, tk.END)
    spotify_recommendations(tracks_json, sp, num_of_tracks)

# UI handling for user input fields.
def on_entry_click(event, entry, default_text):
    if entry.get() == default_text:
        entry.delete(0, "end")
        entry.insert(0, '')
        entry.config(fg='black')

def on_focusout(event, entry, default_text):
    if entry.get() == '':
        entry.insert(0, default_text)
        entry.config(fg='grey')

# Main tkinter application setup.
root = tk.Tk()
root.title("Music Recommendation System")


num_tracks_entry = tk.Entry(root, fg='grey', width=30)
num_tracks_entry.insert(0, "Total number of tracks")
num_tracks_entry.bind("<FocusIn>", lambda event, entry=num_tracks_entry: on_entry_click(event, entry, "Total number of tracks"))
num_tracks_entry.bind("<FocusOut>", lambda event, entry=num_tracks_entry: on_focusout(event, entry, "Total number of tracks"))
num_tracks_entry.pack()

music_prompt_entry = tk.Entry(root, fg='grey', width=30)
music_prompt_entry.insert(0, "Music genre (e.g., chill, energetic, etc.)")
music_prompt_entry.bind("<FocusIn>", lambda event, entry=music_prompt_entry: on_entry_click(event, entry, "Music genre (e.g., chill, energetic, etc.)"))
music_prompt_entry.bind("<FocusOut>", lambda event, entry=music_prompt_entry: on_focusout(event, entry, "Music genre (e.g., chill, energetic, etc.)"))
music_prompt_entry.pack()

min_bpm_entry = tk.Entry(root, fg='grey', width=30)
min_bpm_entry.insert(0, "Minimum BPM")
min_bpm_entry.bind("<FocusIn>", lambda event, entry=min_bpm_entry: on_entry_click(event, entry, "Minimum BPM"))
min_bpm_entry.bind("<FocusOut>", lambda event, entry=min_bpm_entry: on_focusout(event, entry, "Minimum BPM"))
min_bpm_entry.pack()

max_bpm_entry = tk.Entry(root, fg='grey', width=30)
max_bpm_entry.insert(0, "Maximum BPM")
max_bpm_entry.bind("<FocusIn>", lambda event, entry=max_bpm_entry: on_entry_click(event, entry, "Maximum BPM"))
max_bpm_entry.bind("<FocusOut>", lambda event, entry=max_bpm_entry: on_focusout(event, entry, "Maximum BPM"))
max_bpm_entry.pack()

recommend_button = tk.Button(root, text="Recommend", command=on_recommend)
recommend_button.pack()

exit_button = tk.Button(root, text="Exit", command=root.destroy)
exit_button.pack(anchor='nw')

results_text = tk.Text(root, height=10, width=50)
results_text.pack()

root.mainloop()
