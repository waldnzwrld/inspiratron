from unittest.mock import patch, MagicMock, ANY
import torch
import task

def test_task_calls_login():
    # login() is called at module import time (task.py line 8)
    # verify the module loaded successfully and token was read
    assert hasattr(task, 'token')
    assert task.token is not None

def test_task_generate_response_call():
    with patch("task.tokenizer") as mock_tokenizer, patch("task.model") as mock_model:
        mock_input_ids = torch.tensor([[1, 2, 3]])
        mock_tokenizer.encode.return_value = mock_input_ids
        mock_output = torch.tensor([[1, 2, 3, 4, 5, 6]])
        mock_model.generate.return_value = mock_output
        mock_tokenizer.decode.return_value = "response"
        
        result = task.generate_response("prompt", 10, 0.5, 0.9, 1.2, stop_strings=["]", "\n"])

        mock_tokenizer.encode.assert_called_once_with("prompt", return_tensors="pt")
        mock_model.generate.assert_called_once_with(
            mock_input_ids,
            max_new_tokens=10,
            do_sample=True,
            temperature=0.5,
            top_p=0.9,
            repetition_penalty=1.2,
            stopping_criteria=ANY
        )
        mock_tokenizer.decode.assert_called_once()
        assert result == "response"

def test_task_generate_tool_calls():
    with patch("task.generate_response") as mock_generate_response, \
         patch("task.judge_response") as mock_judge_response:
        # Return different values to avoid infinite loop in "while len(set(tool_calls)) == 1"
        mock_generate_response.side_effect = ["tool_call_1", "tool_call_2", "tool_call_3"]
        # Return True to avoid infinite loop in "while not judge_response"
        mock_judge_response.return_value = True
        
        result = task.generate_tool_calls("prompt")
        
        assert result == ["tool_call_1", "tool_call_2", "tool_call_3"]
        assert mock_generate_response.call_count == 3
        assert mock_judge_response.call_count == 3

def test_task_judge_response():
    with patch("task.generate_response") as mock_generate_response:
        mock_generate_response.return_value = "pass"
        
        result = task.judge_response("prompt", "response")
        
        assert result
