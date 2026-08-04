"""
Generation layer for the Music Recommender's RAG loop.

recommend_songs() in recommender.py is the RETRIEVAL step: it scores every
song against a user profile and returns the top-k matches with reasons.

This module is the GENERATION step: it takes exactly those retrieved songs
and asks an LLM to write a natural-language recommendation grounded ONLY in
that retrieved data (not general music knowledge).
"""

import os
import time
from typing import Dict, List, Tuple

from google import genai
from google.genai import errors
from google.genai import types

MODEL = "gemini-flash-latest"
MAX_RETRIES = 3

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


def _detect_profile_gaps(user_prefs: Dict, recommendations: List[Tuple[Dict, float, str]]) -> List[str]:
    """Flags favorite genre/mood values that no retrieved candidate actually
    matched, so the LLM can be upfront about falling back to other attributes
    instead of silently implying a genre/mood match that didn't happen."""
    notes = []
    if not any(song["genre"] == user_prefs["favorite_genre"] for song, _, _ in recommendations):
        notes.append(
            f"No candidate song matched the favorite genre \"{user_prefs['favorite_genre']}\"; "
            "these picks are based on energy/mood/acousticness instead."
        )
    if not any(song["mood"] == user_prefs["favorite_mood"] for song, _, _ in recommendations):
        notes.append(
            f"No candidate song matched the favorite mood \"{user_prefs['favorite_mood']}\"; "
            "these picks are based on energy/genre/acousticness instead."
        )
    return notes


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
        genre_match = song["genre"] == user_prefs["favorite_genre"]
        mood_match = song["mood"] == user_prefs["favorite_mood"]
        energy_gap = abs(song["energy"] - user_prefs["target_energy"])
        lines.append(
            f"{rank}. \"{song['title']}\" by {song['artist']} "
            f"(score: {score:.2f}, genre_match: {genre_match}, mood_match: {mood_match}, "
            f"energy_gap: {energy_gap:.2f}) — {explanation}"
        )

    profile_gaps = _detect_profile_gaps(user_prefs, recommendations)
    if profile_gaps:
        lines.append("")
        lines.append("Profile gaps to acknowledge in the summary:")
        for gap in profile_gaps:
            lines.append(f"- {gap}")

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

    client = _get_client()

    prompt = _build_prompt(user_prefs, recommendations)

    system_prompt = (
        "You are a music recommendation assistant. You must base your answer "
        "strictly on the candidate songs provided below, in the order given. "
        "Do not mention, invent, or suggest any song that is not in the list. "
        "Write 2-4 friendly sentences explaining why these songs suit the "
        "user's taste profile, referencing specific songs and their match "
        "reasons. If none of the candidate songs can be honestly recommended "
        "for this profile, reply exactly: "
        "\"I do not have a good recommendation based on these songs.\"\n\n"
        "Each candidate is annotated with genre_match, mood_match, and "
        "energy_gap. If a song is strong on some of these but weak on "
        "others (e.g. genre_match and mood_match are true but energy_gap is "
        "large, or vice versa), say so plainly instead of presenting it as "
        "an equally confident match across the board.\n\n"
        "If a 'Profile gaps to acknowledge' section is present, incorporate "
        "it naturally into the summary — tell the user their favorite genre "
        "and/or mood wasn't found among the candidates and that the picks "
        "lean on the other attributes instead, rather than implying a match "
        "that didn't happen.\n\n"
        "Briefly contrast the top-ranked song against the next-best "
        "alternative (using the scores and match annotations) so the user "
        "understands why it was ranked first.\n\n"
        "Never write out raw numbers, scores, or percentages (e.g. do not "
        "say \"score: 0.82\" or \"energy_gap: 0.15\"). Translate them into "
        "plain qualitative language instead — e.g. \"a strong match,\" "
        "\"close energy levels,\" \"a noticeably better fit than the "
        "runner-up.\""
    )

    last_error = None

    for attempt in range(MAX_RETRIES):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    max_output_tokens=2048,
                ),
            )
            text = (response.text or "").strip()

            finish_reason = response.candidates[0].finish_reason if response.candidates else None
            if finish_reason == types.FinishReason.MAX_TOKENS:
                text += "\n\n[Note: summary may have been cut off before it finished.]"

            return text
        except errors.ClientError as e:
            last_error = e
            if e.code == 429:
                retry_delay = _extract_retry_delay(e) or (2 ** attempt)
                if attempt < MAX_RETRIES - 1:
                    time.sleep(retry_delay)
                    continue
                return (
                    "Unable to generate a recommendation summary: the Gemini free-tier "
                    "daily quota for this model has been used up. The recommendations "
                    "above are still valid (they don't depend on the LLM) — try again "
                    "later, use a different API key, or upgrade your plan at "
                    "https://ai.google.dev/gemini-api/docs/rate-limits."
                )
            return f"Unable to generate a recommendation summary. ({type(e).__name__}: {e})"
        except Exception as e:
            return f"Unable to generate a recommendation summary. ({type(e).__name__}: {e})"

    return f"Unable to generate a recommendation summary. ({type(last_error).__name__}: {last_error})"


def _extract_retry_delay(error: "errors.ClientError") -> float:
    """Pulls the server-suggested retry delay (seconds) out of a 429 error, if present."""
    try:
        details = error.details.get("error", {}).get("details", [])
        for detail in details:
            if detail.get("@type", "").endswith("RetryInfo"):
                delay_str = detail.get("retryDelay", "")
                if delay_str.endswith("s"):
                    return float(delay_str[:-1])
    except Exception:
        pass
    return None
