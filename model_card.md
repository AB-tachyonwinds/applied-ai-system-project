# 🎧 Model Card: Music Recommender and Summarizer Simulation

## 1. Model Name  
VibeSeeker 2.0

---

## 2. Intended Use  

The user is assumed to have one favorite genre and one favorite mood. They also must have an opinion on the energy level of the song they're looking for and a general opinion on if they want the song to have acoustics. This model is moreso a proof of concept and currently not ready for production.

---

## 3. How the Model Works  

The model primarily uses genre, energy, mood, and acousticnesss to score the songs. This matches with what the user can set their preferences as. The model will compare the user's preferences with the song's attributes, checking how close they are. Once it is determined how close it is, the model will produce a score and then give the user the songs with the best scores. It will summarize the songs given and why it matches with the user's tastes.

---

## 4. Data  

There are 3 env files in the song list with a variety of different values: genre, mood, energy, tempo_bpm, valence,danceability, and acousticness. Genre, mood, energy, and acousticness are the values used in the current model, as the other values are not implemented.

---

## 5. Strengths  

Any exact matches for genre and mood is generally accurate, as it has the strongest correlation. Energy also has a decent sway on the variability of songs given. I think users who have a genre and mood that match the energy are often given the most consistent results.

---

## 6. Limitations and Bias 

Similar to my first iteration of the project, the genre match is all or nothing with its scoring, so similar genres are not scored positively at all. The User Profile is also very limited in its current state, where it can only have one favorite genre, mood, or energy. This is not accurate to many real users, who have varied tastes. As a result, the recommender can only profile a single taste of a user.


---

## 7. Evaluation  

We checked for a user that had negative energy values, when their genre/mood just outright doesn't exist in the song list, when their profile is blank in specific areas, or when there is a case mismatch in their profile (uppercase). I wanted to see what songs would be returned and we were looking for recommendations that would correspond properly to the user (negative energy values means returning a low energy song). 

Most of the options returned reasonable recommendations. For profiles missing information or with genres/moods that don't exist, it makes sense that the songs returned would be following values that do exist (like energy and if the user likes acoustics). While this heavily simplifies the songs returned, it makes sense why these would be recommended. For case mismatch, this one is just trying to catch a  issue with the profile's format like if it's all uppercase letters, so what is returned is what is expected of the genre/mood listed in the profile. The negative energy value did have a strange song for the first option as the song was so fast that it actually removed similarity points despite ranking very high in genre and mood.

---

## 8. Future Work  

In the future, I would want more flexible for the users. This means they can have multiple genres that they like or multiple moods that they're searching for. I would also want to add more categories to the songs so that the scoring system is more robust.

---

## 9. Personal Reflection  


