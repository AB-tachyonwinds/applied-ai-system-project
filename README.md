# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

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

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



