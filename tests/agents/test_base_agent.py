import pytest
from unittest.mock import MagicMock, patch, ANY
from pydantic import BaseModel, Field
from agents.base_agent import BaseAgent

class ResponseModel(BaseModel):  # Changed from TestResponseModel to ResponseModel
    """Model for structured responses"""
    name: str = Field(description="A name")
    value: int = Field(description="A value")
    
class MockAgent(BaseAgent):  # Changed from TestAgent to MockAgent
    """Mock implementation of BaseAgent for testing"""
    def process(self, input_data):
        return input_data

@pytest.fixture
def agent_with_mocks():
    """Create an agent with mocked clients for testing"""
    # Patch both clients during initialization to avoid instructor type checking
    with patch('agents.base_agent.instructor.from_openai'), \
         patch('agents.base_agent.OpenAI'):
        agent = MockAgent("test role", "Test Agent")  # Updated class name
        
        # Now create the actual mocks we'll use for testing
        agent.standard_client = MagicMock()
        agent.instructor_client = MagicMock()
        
        yield agent

def test_base_agent_init():
    """Test BaseAgent initialization creates both clients"""
    with patch('agents.base_agent.OpenAI') as mock_openai, \
         patch('agents.base_agent.instructor.from_openai') as mock_instructor:
        # Set up return values
        mock_openai.return_value = MagicMock()
        mock_instructor.return_value = MagicMock()
        
        # Execute
        agent = MockAgent("test role", "Test Agent")  # Updated class name
    
        # Assert
        assert hasattr(agent, "standard_client")
        assert hasattr(agent, "instructor_client")
        assert mock_openai.called
        assert mock_instructor.called

def test_call_llm(agent_with_mocks):
    """Test _call_llm uses standard client"""
    # Setup
    agent = agent_with_mocks
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Test response"
    agent.standard_client.chat.completions.create.return_value = mock_response
    
    # Execute
    result = agent._call_llm("Test prompt")
    
    # Assert
    assert result == "Test response"
    agent.standard_client.chat.completions.create.assert_called_once()

def test_call_structured_llm(agent_with_mocks):
    """Test _call_structured_llm uses instructor client"""
    # Setup
    agent = agent_with_mocks
    expected_response = ResponseModel(name="Test", value=42)  # Updated class name
    agent.instructor_client.chat.completions.create.return_value = expected_response
    
    # Execute
    result = agent._call_structured_llm("Test prompt", ResponseModel)
    
    # Assert
    assert result == expected_response
    agent.instructor_client.chat.completions.create.assert_called_once_with(
        model=agent.model_name,
        messages=ANY,  # Use unittest.mock.ANY instead of pytest.ANY
        response_model=ResponseModel,  # Updated class name
        temperature=agent.temperature,
        max_tokens=agent.max_tokens
    )

def test_call_structured_llm_error_handling(agent_with_mocks):
    """Test error handling in _call_structured_llm"""
    # Setup
    agent = agent_with_mocks
    agent.instructor_client.chat.completions.create.side_effect = Exception("Test error")
    
    # Execute & Assert
    with pytest.raises(Exception):
        agent._call_structured_llm("Test prompt", ResponseModel)  # Updated class name
