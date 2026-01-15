from unittest.mock import patch

import prompts


def test_initial_prompt():
    result = prompts.initial_prompt("Give me inspiration")

    assert "Give me inspiration" in result
    assert "fetch_quote()" in result
    assert "fetch_headlines()" in result


def test_generate_judgement_prompt():
    result = prompts.generate_judgement_prompt("test prompt", "test response")

    assert "test prompt" in result
    assert "test response" in result
    assert "pass" in result
    assert "fail" in result


def test_generate_prompt_from_tools_with_quote():
    with patch("prompts.fetch_quote") as mock_fetch_quote:
        mock_fetch_quote.return_value = ("Author Name", "Quote content")

        result = prompts.generate_prompt_from_tools(["[TOOL: fetch_quote()]"])

        assert "Author Name" in result
        assert "Quote content" in result


def test_generate_prompt_from_tools_with_headlines():
    with patch("prompts.fetch_news_headlines") as mock_fetch_headlines:
        mock_fetch_headlines.return_value = [
            {"content": "First headline content"},
            {"content": "Second headline content"},
        ]

        result = prompts.generate_prompt_from_tools(["[TOOL: fetch_headlines()]"])

        assert "First headline content" in result


def test_generate_prompt_from_tools_strips_suffix():
    with patch("prompts.fetch_news_headlines") as mock_fetch_headlines:
        mock_fetch_headlines.return_value = [
            {"content": "Headline content [+1234 chars]"}
        ]

        result = prompts.generate_prompt_from_tools(["[TOOL: fetch_headlines()]"])

        assert "Headline content" in result
        assert "[+1234 chars]" not in result


def test_generate_prompt_from_tools_skips_duplicate_headlines():
    with patch("prompts.fetch_news_headlines") as mock_fetch_headlines:
        mock_fetch_headlines.return_value = [
            {"content": "Same headline"},
            {"content": "Same headline"},
            {"content": "Different headline"},
        ]

        result = prompts.generate_prompt_from_tools(
            ["[TOOL: fetch_headlines()]", "[TOOL: fetch_headlines()]"]
        )

        assert "Same headline" in result
        assert "Different headline" in result


def test_generate_prompt_from_tools_skips_none_content():
    with patch("prompts.fetch_news_headlines") as mock_fetch_headlines:
        mock_fetch_headlines.return_value = [
            {"content": None},
            {"content": "Valid headline"},
        ]

        result = prompts.generate_prompt_from_tools(["[TOOL: fetch_headlines()]"])

        assert "Valid headline" in result


def test_generate_prompt_from_tools_ignores_non_tool_entries():
    with patch("prompts.fetch_quote") as mock_fetch_quote:
        mock_fetch_quote.return_value = ("Author", "Quote")

        result = prompts.generate_prompt_from_tools(
            ["not a tool call", "[TOOL: fetch_quote()]"]
        )

        assert "Quote" in result
