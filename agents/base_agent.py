import sys
import os
import json
from typing import List, Dict, Any, Optional, Type, TypeVar, Generic
from openai import OpenAI
import logging
from pydantic import BaseModel
import instructor
from utils.schema_utils import clean_schema_for_llm

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE, OPENAI_MAX_TOKENS, AGENT_MEMORY_LIMIT

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=BaseModel)

class BaseAgent:
    """Base class for all agents in the system."""
    
    def __init__(self, role: str, name: str, base_url: str = None, model_name: str = None):
        """
        Initialize the base agent.
        
        Args:
            role (str): The role description for the agent.
            name (str): The name of the agent.
            base_url (str, optional): OpenAI API base URL
            model_name (str, optional): OpenAI model name to use
        """
        # Create standard client for regular completions
        self.standard_client = OpenAI(api_key=OPENAI_API_KEY, base_url=base_url) if base_url else OpenAI(api_key=OPENAI_API_KEY)
        
        # Create instructor-patched client for structured outputs
        self.instructor_client = instructor.from_openai(OpenAI(api_key=OPENAI_API_KEY, base_url=base_url) if base_url else OpenAI(api_key=OPENAI_API_KEY))
        
        self.role = role
        self.name = name
        self.model_name = model_name or OPENAI_MODEL
        self.temperature = OPENAI_TEMPERATURE
        self.max_tokens = OPENAI_MAX_TOKENS
        self.memory = []
        self.memory_limit = AGENT_MEMORY_LIMIT
        self.conversation_memory: List[Dict[str, str]] = [
            {"role": "system", "content": f"You are {name}, {role}. Always respond with JSON when appropriate."}
        ]
        
    def _call_llm(self, prompt: str):
        """
        Call LLM with prompt and return the raw text response.
        
        Args:
            prompt: The prompt to send to the LLM
            
        Returns:
            str: The LLM response
        """
        messages = [
            {"role": "system", "content": f"You are {self.role}."},
            {"role": "user", "content": prompt}
        ]
        
        # Use the standard client (not patched with instructor) for regular text responses
        response = self.standard_client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        
        return response.choices[0].message.content
    
    def _call_structured_llm(self, prompt: str, response_model: Type[T]) -> T:
        """
        Call LLM with prompt and return a structured response based on the model.
        
        Args:
            prompt: The prompt to send to the LLM
            response_model: Pydantic model for the expected response structure
            
        Returns:
            T: Structured response data as a Pydantic model instance
        """
        messages = [
            {"role": "system", "content": f"You are {self.role}. Respond with structured data."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            # Use a patched instructor client that cleans schema defaults
            client = self.instructor_client
            
            # For models that use function calling (e.g., VertexAI)
            if hasattr(client, '_client') and hasattr(client._client, '_prepare_function_call'):
                # Monkey patch the instructor client's schema preparation
                original_prepare = client._client._prepare_function_call
                
                def patched_prepare(model, messages, response_model, **kwargs):
                    result = original_prepare(model, messages, response_model, **kwargs)
                    
                    # Clean schemas if tools exist
                    if 'tools' in result and isinstance(result['tools'], list):
                        for tool in result['tools']:
                            if 'function' in tool:
                                if 'parameters' in tool['function']:
                                    tool['function']['parameters'] = clean_schema_for_llm(tool['function']['parameters'])
                    
                    return result
                
                # Apply the patch
                client._client._prepare_function_call = patched_prepare
            
            # Use the instructor-patched client for structured responses
            response = client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                response_model=response_model,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            # Restore original prepare function if we patched it
            if hasattr(client, '_client') and hasattr(client._client, '_prepare_function_call'):
                client._client._prepare_function_call = original_prepare
                
            return response
        except Exception as e:
            logger.error(f"Error in structured LLM call: {str(e)}")
            # Create an instance with default values if possible
            try:
                return response_model()
            except:
                raise e
    
    def process(self, input_data: Any) -> Any:
        """
        Process input data according to the agent's role.
        Must be implemented by subclasses.
        
        Args:
            input_data: The input data for the agent to process.
            
        Returns:
            Any: The processed output.
        """
        raise NotImplementedError("Subclasses must implement process method")
    
    def reset_memory(self):
        """Reset the agent's conversation memory, keeping only the system message."""
        system_message = self.conversation_memory[0]
        self.conversation_memory = [system_message]
