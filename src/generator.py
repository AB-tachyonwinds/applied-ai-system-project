"""
Generation layer for the Music Recommender's RAG loop.

recommend_songs() in recommender.py is the RETRIEVAL step: it scores every
song against a user profile and returns the top-k matches with reasons.

This module is the GENERATION step: it takes exactly those retrieved songs
and asks an LLM to write a natural-language recommendation grounded ONLY in
that retrieved data (not general music knowledge).
"""

import os
from typing import Dict, List, Tuple

from google import genai
from google.genai import types

MODEL = "gemini-2.5-flash"

_client = None


def _get_client() -> genai.Client:
    """Lazily creates a single shared Gemini client."""
    global _client
    if _client is None:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not set. Set it as an environment "
                "variable (see README) before generating summaries."
            )
        _client = genai.Client(api_key=api_key)
    return _client


def _build_prompt(user_prefs: Dict, recommendations: List[Tuple[Dict, float, str]]) -> str:
    """Formats the user's profile and retrieved songs into a grounded prompt."""
    lines = [
        "User taste profile:",
        f"- Favorite genre: {user_prefs['favorite_genre']}",
        f"- Favorite mood: {user_prefs['favorite_mood']}",
        f"- Target energy: {user_prefs['target_energy']}",
        f"- Likes acoustic: {user_prefs['likes_acoustic']}",
        "",
        "Retrieved candidate songs (already ranked, highest score first):",
    ]
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        lines.append(
            f"{rank}. \"{song['title']}\" by {song['artist']} "
            f"(score: {score:.2f}) — {explanation}"
        )
    return "\n".join(lines)


def generate_recommendation_summary(
    user_prefs: Dict, recommendations: List[Tuple[Dict, float, str]]
) -> str:
    """
    Generates a short natural-language recommendation write-up using only the
    songs already retrieved by recommend_songs(). Grounds the model in that
    data so it can't invent songs or facts outside the retrieved list.
    """
    if not recommendations:
        return "No songs matched this profile, so no recommendation could be generated."

    prompt = _build_prompt(user_prefs, recommendations)

    system_prompt = (
        "You are a music recommendation assistant. You must base your answer "
        "strictly on the candidate songs provided below, in the order given. "
        "Do not mention, invent, or suggest any song that is not in the list. "
        "Write 2-4 friendly sentences explaining why these songs suit the "
        "user's taste profile, referencing specific songs and their match "
        "reasons. If none of the candidate songs can be honestly recommended "
        "for this profile, reply exactly: "
        "\"I do not have a good recommendation based on these songs.\""
    )

    try:
        client = _get_client()
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                max_output_tokens=300,
            ),
        )
        return (response.text or "").strip()
    except Exception as e:
        return f"Unable to generate a recommendation summary. ({type(e).__name__}: {e})"
