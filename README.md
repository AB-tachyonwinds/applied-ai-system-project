# 🎵 Music Recommender and Summarizer Simulation

## Project Summary

My original project was Module 3: Show Music Recommender Simulation. Its main purpose is to represent songs and a user "taste profile" as data and gives the user a recommendation score.



---

## Architecture Overview

Streaming platformers often use multiple different techniques to find songs that a user will like. It can analyze the song's metadata and compare how similar it is to other songs. It can also compare what other similar users listen to. In our system, we will prioritize the numerical distance (decided internally) of the song's attributes, like energy or mood. We will also implement a summary of the songs and why they were chosen.

Each Song uses genre, mood, energy, tempo, valence, dancability, and acousticness. The UserProfile stores favorite genre, mood, targeted energy, and whether or not they like acoustic. We will use a taste profile as a base of comparison, which may be a bit narrow. The recommender will compare the values with the user's profile. 

Every specific match in our algorithm recipe will yield different points. Genre match will yield +2.0 points if it's an exact match. Mood match will yield +1.0 points if it's an exact match. Energy similarity can yield up to +2.0 points. There can also be an acoustic bonus of +0.5 if the song matches the user's preference. There may be an overreliance on genre as a deciding factor and it might be possible to add more variables to the user profile, but this process is simplified for now.

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

3. Create an environmental variable file that contains the following:
   ```
   GEMINI_API_KEY=[your-api-key]
   RAG_SUMMARY=0
   ```
   Set up your Gemini api-key (I used the free tier). IIf RAG_SUMMARY is 0, then it will run without RAG. If RAG_SUMMARY is any other number, then the RAG summary will be used.

4. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

I primarily ran it with:
```
python -m pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Interactions

Happy case (Normal profile that enjoys rock):
```
Loading songs from data/songs.csv...
Loading songs from data/songs_roc.csv...
Loading songs from data/songs_var.csv...

============================================================
                     DEEP INTENSE ROCK                      
============================================================

1. Night Siege - Voltline
   Score: 4.94
   Reasons:
     - Genre matches favorite genre (rock)
     - Mood matches favorite mood (intense)
     - Energy similarity contributed 1.94 points

2. Thunder Road - Iron Harbor
   Score: 4.92
   Reasons:
     - Genre matches favorite genre (rock)
     - Mood matches favorite mood (intense)
     - Energy similarity contributed 1.92 points

3. Storm Runner - Voltline
   Score: 4.88
   Reasons:
     - Genre matches favorite genre (rock)
     - Mood matches favorite mood (intense)
     - Energy similarity contributed 1.88 points

4. Alien Anthem - Wildfire
   Score: 4.00
   Reasons:
     - Genre matches favorite genre (rock)
     - Energy similarity contributed 2.00 points

5. Highway Echo - Neon Cross
   Score: 3.98
   Reasons:
     - Genre matches favorite genre (rock)
     - Energy similarity contributed 1.98 points

--- AI Summary (grounded in the songs retrieved above) ---
"Night Siege" by Voltline leads the list as your best overall match, delivering your favorite rock genre and an intense mood with an almost exact match to your desired energy level. It edges out "Thunder Road" by Iron Harbor for the top spot because its energy is just a bit closer to your target, though both—along with "Storm Runner"—fit your taste profile exceptionally well. On the other hand, tracks like "Alien Anthem" and "Highway Echo" hit your target energy flawlessly, but they fall short by lacking the intense mood match found in the top-ranked selections.

============================================================
```

Non-existent Taste:
```

============================================================
               NONEXISTENT TASTE (EDGE CASE)                
============================================================

1. Broken Compass - Simone Delacroix
   Score: 1.94
   Reasons:
     - Energy similarity contributed 1.94 points

2. Velvet Hours - Simone Delacroix
   Score: 1.90
   Reasons:
     - Energy similarity contributed 1.90 points

3. Velvet Static - Simone Delacroix
   Score: 1.90
   Reasons:
     - Energy similarity contributed 1.90 points

4. Uptown Static - Simone Delacroix
   Score: 1.84
   Reasons:
     - Energy similarity contributed 1.84 points

5. Midnight Coding - LoRoom
   Score: 1.84
   Reasons:
     - Energy similarity contributed 1.84 points

--- AI Summary (grounded in the songs retrieved above) ---
While none of the available songs matched your preferred polka genre or melancholic-but-danceable mood, these recommendations lean entirely on hitting your ideal energy level instead. "Broken Compass" by Simone Delacroix takes the top spot because its energy level is a noticeably closer fit to your preference than the runner-up, "Velvet Hours." Additional choices like "Velvet Static" and "Uptown Static" similarly offer balanced energy matches, though you should keep in mind that none of these selections capture your target genre or emotional vibe.

============================================================

```
---

## Design Decisions


---

## Testing Summary

Testing for the AI summary is done through human evaluation, as many of the summaries are geared towards preference and "what feels right". The following w

| Test Input | Evaluation Criteria | Result |
| --- | --- | --- |
| Rock User Profile | AI summary accurate, Song choices accurate | Passed |
| Parsing too many user profiles at once | When tokens run out, exit gracefully | Failed, not the most user friendly |
| Profile with missing information | AI summary and song choices accurate | Passed |

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

I put my reflection on the engineering process in model_card.md.


