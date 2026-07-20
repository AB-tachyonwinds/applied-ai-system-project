# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

My version is a simple recommender that evaluates a user's taste and scores it based on similarity. My recommender puts heavy emphasis on the genre and mood of the songs, as well as the energy and acousticness.

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
Loading songs from data/songs.csv...

============================================================
                    TOP RECOMMENDATIONS                     
============================================================

1. Sunrise City - Neon Echo
   Score: 4.96
   Reasons:
     - Genre matches favorite genre (pop)
     - Mood matches favorite mood (happy)
     - Energy similarity contributed 1.96 points

2. Gym Hero - Max Pulse
   Score: 3.74
   Reasons:
     - Genre matches favorite genre (pop)
     - Energy similarity contributed 1.74 points

3. Rooftop Lights - Indigo Parade
   Score: 2.92
   Reasons:
     - Mood matches favorite mood (happy)
     - Energy similarity contributed 1.92 points

4. Carnival Nights - Rio Solano
   Score: 1.90
   Reasons:
     - Energy similarity contributed 1.90 points

5. Night Drive Loop - Neon Echo
   Score: 1.90
   Reasons:
     - Energy similarity contributed 1.90 points

============================================================

---

## Experiments You Tried

We ran the profile with various different types of users in order to stress test the recommender. We had a user that tested when they had negative energy values, when their test just outright doesn't exist in the song list, when the profile is blank in specific areas, or when there is a uppercase mismatch. The below is the output of the first iteration of the model with these user edge cases.

```
============================================================
               NONEXISTENT TASTE (EDGE CASE)                
============================================================

1. Velvet Hours - Simone Delacroix
   Score: 1.90
   Reasons:
     - Energy similarity contributed 1.90 points

2. Uptown Static - Simone Delacroix
   Score: 1.84
   Reasons:
     - Energy similarity contributed 1.84 points

3. Midnight Coding - LoRoom
   Score: 1.84
   Reasons:
     - Energy similarity contributed 1.84 points

4. Focus Flow - LoRoom
   Score: 1.80
   Reasons:
     - Energy similarity contributed 1.80 points

5. Coffee Shop Stories - Slow Stereo
   Score: 1.74
   Reasons:
     - Energy similarity contributed 1.74 points

============================================================


============================================================
                NEGATIVE ENERGY (EDGE CASE)                 
============================================================

1. Storm Runner - Voltline
   Score: 2.18
   Reasons:
     - Genre matches favorite genre (rock)
     - Mood matches favorite mood (intense)
     - Energy similarity contributed -0.82 points

2. Moonlit Sonata Redux - Elias Vance
   Score: 0.50
   Reasons:
     - Energy similarity contributed 0.50 points

3. Spacewalk Thoughts - Orbit Bloom
   Score: 0.44
   Reasons:
     - Energy similarity contributed 0.44 points

4. Autumn Letters - Wren & Oak
   Score: 0.40
   Reasons:
     - Energy similarity contributed 0.40 points

5. Front Porch Sundown - Wren & Oak
   Score: 0.34
   Reasons:
     - Energy similarity contributed 0.34 points

============================================================


============================================================
            ACOUSTIC BOUNDARY == 0.6 (EDGE CASE)            
============================================================

1. Front Porch Sundown - Wren & Oak
   Score: 3.96
   Reasons:
     - Genre matches favorite genre (folk)
     - Energy similarity contributed 1.46 points
     - Acoustic bonus applied (user likes acoustic and song is acoustic)

2. Autumn Letters - Wren & Oak
   Score: 3.90
   Reasons:
     - Genre matches favorite genre (folk)
     - Energy similarity contributed 1.40 points
     - Acoustic bonus applied (user likes acoustic and song is acoustic)

3. Velvet Hours - Simone Delacroix
   Score: 2.20
   Reasons:
     - Energy similarity contributed 1.70 points
     - Acoustic bonus applied (user likes acoustic and song is acoustic)

4. Midnight Coding - LoRoom
   Score: 2.14
   Reasons:
     - Energy similarity contributed 1.64 points
     - Acoustic bonus applied (user likes acoustic and song is acoustic)

5. Focus Flow - LoRoom
   Score: 2.10
   Reasons:
     - Energy similarity contributed 1.60 points
     - Acoustic bonus applied (user likes acoustic and song is acoustic)

============================================================


============================================================
                BLANK GENRE/MOOD (EDGE CASE)                
============================================================

1. Velvet Hours - Simone Delacroix
   Score: 1.90
   Reasons:
     - Energy similarity contributed 1.90 points

2. Uptown Static - Simone Delacroix
   Score: 1.84
   Reasons:
     - Energy similarity contributed 1.84 points

3. Midnight Coding - LoRoom
   Score: 1.84
   Reasons:
     - Energy similarity contributed 1.84 points

4. Focus Flow - LoRoom
   Score: 1.80
   Reasons:
     - Energy similarity contributed 1.80 points

5. Coffee Shop Stories - Slow Stereo
   Score: 1.74
   Reasons:
     - Energy similarity contributed 1.74 points

============================================================


============================================================
            CASE MISMATCH POP/HAPPY (EDGE CASE)             
============================================================

1. Sunrise City - Neon Echo
   Score: 1.96
   Reasons:
     - Energy similarity contributed 1.96 points

2. Rooftop Lights - Indigo Parade
   Score: 1.92
   Reasons:
     - Energy similarity contributed 1.92 points

3. Carnival Nights - Rio Solano
   Score: 1.90
   Reasons:
     - Energy similarity contributed 1.90 points

4. Night Drive Loop - Neon Echo
   Score: 1.90
   Reasons:
     - Energy similarity contributed 1.90 points

5. Ashes We Carry - Grim Ferrous
   Score: 1.84
   Reasons:
     - Energy similarity contributed 1.84 points

============================================================
```

---

## Limitations and Risks

It heavily favors genre and mood, and the flexibility of the profiles is quite limited with the amount of attributes currently.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

It's no wonder that for some engineers, their only job is to work with the algorithm. By using data and assigning it a value, songs can be matched up to users' preferences and internal values. Every action or preference made by the user can be used in the predictions. There are biases that can occur, such as feedback loops where a popular song keeps getting recommended so it's the only song being recommended. Songs with less information (like if the genre of a song is undetermined or simply not as popular) can also be unfairly reduced by the algorithm, even if it suits the user's preference much better than popular songs. I thought it was interesting putting it into practice for this project.

I put my reflection on the engineering process in model_card.md.


