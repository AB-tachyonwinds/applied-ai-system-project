"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


# ---------------------------------------------------------------------------
# Sample user preference profiles
# ---------------------------------------------------------------------------

HIGH_ENERGY_POP = {
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.9,
    "likes_acoustic": False,
}

CHILL_LOFI = {
    "favorite_genre": "lofi",
    "favorite_mood": "calm",
    "target_energy": 0.2,
    "likes_acoustic": True,
}

DEEP_INTENSE_ROCK = {
    "favorite_genre": "rock",
    "favorite_mood": "intense",
    "target_energy": 0.85,
    "likes_acoustic": False,
}

# ---------------------------------------------------------------------------
# Edge-case profiles designed to probe/"trick" the scoring logic
# ---------------------------------------------------------------------------

# No genre or mood in the dataset should ever match this, so every song's
# score should come purely from the energy_similarity term (and possibly the
# acoustic bonus) -- a good check that unmatched genre/mood don't silently
# add points.
NONEXISTENT_TASTE = {
    "favorite_genre": "polka",
    "favorite_mood": "melancholic-but-danceable",
    "target_energy": 0.5,
    "likes_acoustic": False,
}

NEGATIVE_ENERGY = {
    "favorite_genre": "rock",
    "favorite_mood": "intense",
    "target_energy": -0.5,
    "likes_acoustic": False,
}

# Acousticness threshold boundary: the bonus only applies when
# acousticness > 0.6 (strictly greater). A song with acousticness == 0.6
# exactly should NOT receive the bonus -- a classic off-by-one/boundary trap.
ACOUSTIC_BOUNDARY_TESTER = {
    "favorite_genre": "folk",
    "favorite_mood": "calm",
    "target_energy": 0.6,
    "likes_acoustic": True,
}

# Empty/blank strings for genre and mood. If any song in the CSV has a blank
# genre or mood field (or load_songs doesn't strip whitespace), this could
# produce a false "match" and inflate a score for the wrong reason.
BLANK_PREFERENCES = {
    "favorite_genre": "",
    "favorite_mood": "",
    "target_energy": 0.5,
    "likes_acoustic": False,
}

# Case-sensitivity trap: CSV genres/moods are typically lowercase, so
# "Pop"/"Happy" should NOT match "pop"/"happy" if score_song does a naive
# `==` comparison. Checks whether matching is (or should be) case-insensitive.
CASE_MISMATCH_TASTE = {
    "favorite_genre": "Pop",
    "favorite_mood": "Happy",
    "target_energy": 0.8,
    "likes_acoustic": False,
}

PROFILES = {
    "High-Energy Pop": HIGH_ENERGY_POP,
    "Chill Lofi": CHILL_LOFI,
    "Deep Intense Rock": DEEP_INTENSE_ROCK,
    "Nonexistent Taste (edge case)": NONEXISTENT_TASTE,
    "Negative Energy (edge case)": NEGATIVE_ENERGY,
    "Acoustic Boundary == 0.6 (edge case)": ACOUSTIC_BOUNDARY_TESTER,
    "Blank Genre/Mood (edge case)": BLANK_PREFERENCES,
    "Case Mismatch Pop/Happy (edge case)": CASE_MISMATCH_TASTE,
}


def print_recommendations(label: str, user_prefs: dict, songs, k: int = 5) -> None:
    recommendations = recommend_songs(user_prefs, songs, k=k)

    print("\n" + "=" * 60)
    print(label.upper().center(60))
    print("=" * 60)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']} - {song['artist']}")
        print(f"   Score: {score:.2f}")
        reasons = explanation.split("; ") if explanation else []
        if reasons:
            print("   Reasons:")
            for reason in reasons:
                print(f"     - {reason}")

    print("\n" + "=" * 60 + "\n")


def main() -> None:
    songs = load_songs("data/songs.csv")

    for label, user_prefs in PROFILES.items():
        print_recommendations(label, user_prefs, songs, k=5)


if __name__ == "__main__":
    main()
