# 🎵 Music Recommender and Summarizer Simulation

## Project Summary

My original project was Module 3: Show Music Recommender Simulation. Its main purpose is to represent songs and a user "taste profile" as data. It will score the songs according to the user's taste profile, and return recommended songs.

To extend the original, this project will have an AI summary that explains the song choices. This AI summary can detect gaps in the taste profile, like when the genre is not set or not found in any of songs. The application will only use the songs listed in the data folder.

---

## Architecture Overview

Streaming platformers often use multiple different techniques to find songs that a user will like. It can analyze the song's metadata and compare how similar it is to other songs. In our system, we will prioritize the numerical distance (decided internally) of the song's attributes, like energy or mood. We will also implement a summary that explains why the songs were chosen.

![System Diagram](diagrams/system_diagram.mmd)

The diagram breaks the pipeline into four stages. **Input** is the song CSVs (`data/songs*.csv`) and the user's taste profile (favorite genre, mood, target energy, acoustic preference). **Processing** is a RAG-style flow: `load_songs()` parses the CSVs, the retriever (`score_song()` / `recommend_songs()` in `src/recommender.py`) scores and ranks songs against the profile, and the generator (`generate_recommendation_summary()` in `src/generator.py`) is the LLM agent that writes a natural-language summary grounded only in the retrieved songs. **Output** is the ranked list of songs with scores/reasons, plus that AI-written summary. **Human & Automated Checks** wraps the whole thing: pytest tests (`tests/test_recommender.py`, `tests/test_generator.py`, including mocked LLM calls) verify the loader/retriever/generator, grounding guardrails handle profile-gap detection and 429 retry/backoff, and a human reviews the printed reasons and AI summary via `src/main.py`'s console output.

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

Negative Energy Taste:
```
============================================================
                NEGATIVE ENERGY (EDGE CASE)                 
============================================================

1. Night Siege - Voltline
   Score: 2.24
   Reasons:
     - Genre matches favorite genre (rock)
     - Mood matches favorite mood (intense)
     - Energy similarity contributed -0.76 points

2. Thunder Road - Iron Harbor
   Score: 2.22
   Reasons:
     - Genre matches favorite genre (rock)
     - Mood matches favorite mood (intense)
     - Energy similarity contributed -0.78 points

3. Storm Runner - Voltline
   Score: 2.18
   Reasons:
     - Genre matches favorite genre (rock)
     - Mood matches favorite mood (intense)
     - Energy similarity contributed -0.82 points

4. Rust and Roses - Shadow Pulse
   Score: 1.68
   Reasons:
     - Genre matches favorite genre (rock)
     - Energy similarity contributed -0.32 points

5. Stone Garden - Ever Ash
   Score: 1.64
   Reasons:
     - Genre matches favorite genre (rock)
     - Energy similarity contributed -0.36 points

--- AI Summary (grounded in the songs retrieved above) ---
If you're looking for intense rock tracks, "Night Siege" by Voltline and "Thunder Road" by Iron Harbor are great matches for your favorite genre and mood, though it is worth noting that their energy levels are significantly higher than your target profile. "Night Siege" takes the top spot just ahead of runner-up "Thunder Road" because its energy is slightly closer to your preference, giving it a marginally better overall fit. You can also check out "Storm Runner" for the same intense rock feel, or lower-ranked options like "Rust and Roses" by Shadow Pulse, which hit your preferred rock genre but miss out on the intense mood.

============================================================
```

Missing Genre and Mood in User Profile:
```
============================================================
                BLANK GENRE/MOOD (EDGE CASE)                
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
Since none of the candidate songs matched a specific favorite genre or mood, these picks rely entirely on hitting your target energy level. "Broken Compass" by Simone Delacroix takes the top spot because its energy level is an almost exact match to your preference, giving it a slightly better fit than the runner-up, "Velvet Hours." Whilethese selections and others like "Velvet Static" capture your desired intensity well, keep in mind that they rely strictly on energy alignment rather than specific genreor mood matches.

============================================================
```
---

## Design Decisions

I went with a simple numerical scoring function instead of embeddings or a vector database, mostly because the song data was already structured (genre, mood, energy, acousticness). This choice made `score_song()` easy to debug and implement, but it also means genre and mood matches are all-or-nothing. This means that even if the genre is close to another, it won't be considered in the scoring at all. This trade-off was made for simplicity sake, but also to limit the amount of tokens needed for implementation.

For a similar reason, I decided to keep the LLM out of the actual song picking. `recommend_songs()` does all the ranking, and `generate_recommendation_summary()` only ever gets handed the songs that were already chosen — its job is to explain the results, not decide them. This felt important for trust and testability: I didn't want the summary to ever contradict or override the scoring logic, and it meant I could mock the LLM call in `tests/test_generator.py` and test the retrieval and generation pieces independently.

Like the previous project iteration, I also limit the user profile to a single favorite genre, mood, and energy value, so a user is not able to pick multiple options. It simplified the scoring and the profile-gap detection, but it's too limiting and doesn't accurately portray a user's varied tastes.

---

## Testing Summary

Testing for the AI summary is done through human evaluation, as many of the summaries are geared towards preference and "what feels right". The following inputs were tested for edge cases. The sample interactions and their specific profiles are located in assets/sample_interactions.txt. 

| Test Input | Evaluation Criteria | Result |
| --- | --- | --- |
| Rock User Profile | AI summary accurate, Song choices accurate | Passed |
| Parsing too many user profiles at once | When tokens run out, exit gracefully | Failed, not the most user friendly |
| Profile with genres/moods that don't exist | AI summary and song choices accurate | Passed |
| Profile with negative energy | AI summary accurate, song reasons accurate | Passed |
| Profile with missing genre and mood | AI summary and song choices accurate | Passed |

I feel that even with missing information, the current AI summary does a decent job at summarizing the recommendations. It will note gaps in its judgement and relay that properly to the user.
On the other hand, my attempts to add logging and catching errors was difficult and I ran into errors when I hit my rate limit. In general, my logging practices are a bit rusty, so doing this project helped me identify that skill gap.
Overall, these tests helped pinpoint situations that I should look out for while using RAG for explanations and summaries.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

I put my reflection on the engineering process in model_card.md.


