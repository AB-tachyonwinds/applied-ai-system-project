import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """Represents a song and its attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """Recommends songs to a user based on their profile."""
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top k songs recommended for the given user."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a human-readable explanation for why a song was recommended."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from a CSV file into a list of dicts with parsed numeric fields."""
    print(f"Loading songs from {csv_path}...")
    float_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in float_fields:
                row[field] = float(row[field])
            row["id"] = int(row["id"])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a single song against user preferences, returning the score and matching reasons."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs["favorite_genre"]:
        score += 2.0
        reasons.append(f"Genre matches favorite genre ({song['genre']})")

    if song["mood"] == user_prefs["favorite_mood"]:
        score += 1.0
        reasons.append(f"Mood matches favorite mood ({song['mood']})")

    energy_similarity = 2.0 * (1 - abs(song["energy"] - user_prefs["target_energy"]))
    score += energy_similarity
    reasons.append(f"Energy similarity contributed {energy_similarity:.2f} points")

    if user_prefs["likes_acoustic"] and song["acousticness"] > 0.6:
        score += 0.5
        reasons.append("Acoustic bonus applied (user likes acoustic and song is acoustic)")

    return (score, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores and sorts songs by preference match, returning the top k with reasons."""
    scored = [
        (song, score, "; ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]
    scored.sort(key=lambda entry: entry[1], reverse=True)
    return scored[:k]
