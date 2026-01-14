from unittest.mock import patch, MagicMock
import sys

def test_inspiratron_judge_passes():
    # Remove cached module if present
    if 'inspiratron' in sys.modules:
        del sys.modules['inspiratron']
    
    with patch("prompts.initial_prompt") as mock_initial_prompt, \
         patch("prompts.generate_prompt_from_tools") as mock_generate_prompt, \
         patch("task.generate_tool_calls") as mock_generate_tool_calls, \
         patch("task.generate_response") as mock_generate_response, \
         patch("task.judge_response") as mock_judge_response, \
         patch("builtins.print") as mock_print:
        
        mock_initial_prompt.return_value = "tool_prompt"
        mock_generate_tool_calls.return_value = ["tool_call"]
        mock_generate_prompt.return_value = "combined_prompt"
        mock_generate_response.return_value = "generated_text"
        mock_judge_response.return_value = True
        
        import inspiratron
        
        mock_initial_prompt.assert_called_once()
        mock_generate_tool_calls.assert_called_once_with("tool_prompt")
        mock_generate_prompt.assert_called_once_with(["tool_call"])
        assert mock_generate_response.call_count == 1
        mock_judge_response.assert_called_once()
        mock_print.assert_called_once_with("generated_text")

def test_inspiratron_judge_fails():
    # Remove cached module if present
    if 'inspiratron' in sys.modules:
        del sys.modules['inspiratron']
    
    with patch("prompts.initial_prompt") as mock_initial_prompt, \
         patch("prompts.generate_prompt_from_tools") as mock_generate_prompt, \
         patch("task.generate_tool_calls") as mock_generate_tool_calls, \
         patch("task.generate_response") as mock_generate_response, \
         patch("task.judge_response") as mock_judge_response, \
         patch("builtins.print") as mock_print:
        
        mock_initial_prompt.return_value = "tool_prompt"
        mock_generate_tool_calls.return_value = ["tool_call"]
        mock_generate_prompt.return_value = "combined_prompt"
        mock_generate_response.side_effect = ["first_response", "second_response"]
        mock_judge_response.return_value = False  # Judge fails, triggers retry
        
        import inspiratron
        
        # generate_response called twice (initial + retry)
        assert mock_generate_response.call_count == 2
        mock_print.assert_called_once_with("second_response")
