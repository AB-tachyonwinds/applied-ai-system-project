# 🎵 Music Recommender and Summarizer Simulation

## Project Summary

My original project was Module 3: Show Music Recommender Simulation. Its main purpose is to represent songs and a user "taste profile" as data and gives the user a recommendation score.

I wanted to add more RAG capabilities that allows it

---

## Architecture Overview

Streaming platformers often use multiple different techniques to find songs that a user will like. It can analyze the song's metadata and compare how similar it is to other songs. It can also compare what other similar users listen to. In our system, we will prioritize the numerical distance (decided internally) of the song's attributes, like energy or mood. 

Each Song uses genre, mood, energy, tempo, valence, dancability, and acousticness. The UserProfile stores favorite genre, mood, targeted energy, and whether or not they like acoustic. We will use a taste profile as a base of comparison, which may be a bit narrow. The recommender will compare the values with the user's profile. 

Every specific match in our algorithm recipe will yield different points. Genre match will yield +2.0 points if it's an exact match. Mood match will yield +1.0 points if it's an exact match. Energy similarity can yield up to +2.0 points. There can also be an acoustic bonus of +0.5 if the song matches the user's preference. There may be an overreliance on genre as a deciding factor and it might be possible to add more variables to the user profile, but we can keep it simple for now.

We will choose which songs to recommend with recommend_songs() which will score and sort the songs, then returning the most similar ones.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Interactions

```

```
---

## Design Decisions


---

## Testing Summary



---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

I put my reflection on the engineering process in model_card.md.


