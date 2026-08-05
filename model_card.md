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

There are 3 csv files in the song list with a variety of different values: genre, mood, energy, tempo_bpm, valence, danceability, and acousticness. Genre, mood, energy, and acousticness are the values used in the current model, as the other values are not implemented. The summaries primarily bases its information off of the scores.

---

## 5. Strengths  

Any exact matches for genre and mood is generally accurate, as it has the strongest correlation. Energy also has a decent sway on the variability of songs given. I think users who have a genre and mood that match the energy are often given the most consistent results.

The summary provides a reasonable explanation for why one song is used over another and also identifies any gaps in the taste profile. It is easy and friendly for users to read.

---

## 6. Limitations and Bias 

Similar to my first iteration of the project, the genre match is all or nothing with its scoring, so similar genres are not scored positively at all. The User Profile is also very limited in its current state, where it can only have one favorite genre, mood, or energy. This is not accurate to many real users, who have varied tastes. As a result, the recommender can only profile a single taste of a user.

Although definitely possible to implement, the project's AI does not use generation to make huge scoring decisions. I think this is a limitation because the current scoring system is not flexible and it could be possible for the AI to figure out a more specialized song list. I think this could be avoided with a more robust scoring system, since numerical score is more concrete than what the AI may potentially hallucinate.

---

## 7. Evaluation  

We checked for a user that had negative energy values, when their genre/mood just outright doesn't exist in the song list, when their profile is blank in specific areas, or when there is a case mismatch in their profile (uppercase). I wanted to see what songs would be returned and we were looking for recommendations that would correspond properly to the user (negative energy values means returning a low energy song). I paid close attention to if the AI summary pointed out gaps in the user's taste profile. That acknowledgement and the compare/contrast provided by the summary provides the most value to the system.

Most of the options returned reasonable recommendations. For profiles missing information or with genres/moods that don't exist, it makes sense that the songs returned would be following values that do exist (like energy and if the user likes acoustics). While this heavily simplifies the songs returned, it makes sense why these would be recommended. The negative energy value did have a strange song for the first option as the song was so fast that it actually removed similarity points despite ranking very high in genre and mood. For all of these cases, the missing genres/moods and the low energy score were noted in the AI summary. This is a good sign and more complex acknowledgement than I was expecting.

Still, since the retrieval is largely focused on the score, rather than the raw songs, the analysis is limited to only the top-k songs chosen from the score. AI is often confident, so it's important to consider than when evaluating the results.

---

## 8. Future Work  

In the future, I want to incorporate real songs and link specific ones to the user. I'd also want to have the AI retrieve from the catalog and create a ranking based on its judgement, rather than only reviewing top scoring songs. Adding a UI would also make this system much more friendly.

---

## 9. Personal Reflection  
Using RAG for a previous project put into perspective how powerful AI is, but it's still important to provide and understand the framework of the system. I felt fairly uninvolved when refactoring my code, but could stay engaged by asking for explanation from Claude. I'd always review what Claude was adding, but Claude was doing most of the implementation. ALthough I understood most of the code, it definitely felt weird being mostly hands-off with code and mostly focused on prompts and planning.

AI was generally very helpful with debugging. When I was having issues with implementing my Gemini key, AI allowed me to attempt several different solutions. It's convenient and quick, especially when people have encountered the issue before.

It was less helpful for when I would try implementing a new tool, like an external logger. While it does reference how logging is implemented, I ultimately removed the AI's implementation and suggestion because it complicated the code and would tell the user about main issues. Since I didn't understand how the external logger worked, I felt trying to implement it was not needed. A better prompt might fix my problem, but the complexity was not what my project needed currently.

Overall, I enjoyed using AI because it performed many tedious tasks and often made what I assume is "Pythonic" code. I will still always review it, but my code knowledge gap still feels very palpable while reviewing certain concepts. I think AI overall aided my learning. It's up to us to use it responsibly and learn, even if it's performing a lot of the work. I think learning by doing is the best way to learn and AI sometimes bypasses that, but it comes with the trade-off of faster speed and more specialized learning.


