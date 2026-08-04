from unittest.mock import MagicMock, patch

import pytest

from src import generator


USER_PREFS = {
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.8,
    "likes_acoustic": False,
}

RECOMMENDATIONS = [
    (
        {
            "id": 1,
            "title": "Test Pop Track",
            "artist": "Test Artist",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.8,
        },
        4.5,
        "Genre matches favorite genre (pop); Mood matches favorite mood (happy)",
    ),
    (
        {
            "id": 2,
            "title": "Chill Lofi Loop",
            "artist": "Test Artist",
            "genre": "lofi",
            "mood": "calm",
            "energy": 0.3,
        },
        1.2,
        "Energy similarity contributed 1.20 points",
    ),
]


@pytest.fixture(autouse=True)
def reset_client_cache():
    """generator caches its Gemini client in a module-level global; make
    sure each test starts with a clean slate so mocks/env changes don't leak
    between tests."""
    generator._client = None
    yield
    generator._client = None


def test_generate_recommendation_summary_returns_empty_message_for_no_songs():
    summary = generator.generate_recommendation_summary(USER_PREFS, [])
    assert "No songs matched" in summary


def test_generate_recommendation_summary_raises_without_api_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    with pytest.raises(RuntimeError, match="GEMINI_API_KEY"):
        generator.generate_recommendation_summary(USER_PREFS, RECOMMENDATIONS)


def test_generate_recommendation_summary_calls_llm_with_grounded_prompt(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")

    mock_response = MagicMock()
    mock_response.text = "These songs suit your pop, happy taste."

    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = mock_response

    with patch.object(generator.genai, "Client", return_value=mock_client):
        summary = generator.generate_recommendation_summary(USER_PREFS, RECOMMENDATIONS)

    assert summary == "These songs suit your pop, happy taste."

    # The LLM should only ever see the songs that were actually retrieved.
    _, kwargs = mock_client.models.generate_content.call_args
    prompt_text = kwargs["contents"]
    assert "Test Pop Track" in prompt_text
    assert "Chill Lofi Loop" in prompt_text
    assert kwargs["model"] == generator.MODEL
    assert "strictly on the candidate songs" in kwargs["config"].system_instruction


def test_client_is_created_once_and_reused(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")

    with patch.object(generator.genai, "Client") as mock_client_cls:
        generator._get_client()
        generator._get_client()

    mock_client_cls.assert_called_once()
