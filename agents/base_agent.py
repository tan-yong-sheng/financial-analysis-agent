import sys
import os
import json
from typing import List, Dict, Any, Optional, Type
from openai import OpenAI
import logging
from pydantic import BaseModel
from utils.llm_utils import create_openai_function_schema

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE, OPENAI_MAX_TOKENS, AGENT_MEMORY_LIMIT

logger = logging.getLogger(__name__)

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
        self.client = OpenAI(api_key=OPENAI_API_KEY, base_url=base_url) if base_url else OpenAI(api_key=OPENAI_API_KEY)
        self.role = role
        self.name = name
        self.model_name = model_name or OPENAI_MODEL  # Fix: Changed from self.model to self.model_name
        self.temperature = OPENAI_TEMPERATURE
        self.max_tokens = OPENAI_MAX_TOKENS
        self.memory = []
        self.memory_limit = AGENT_MEMORY_LIMIT
        self.conversation_memory: List[Dict[str, str]] = [
            {"role": "system", "content": f"You are {name}, {role}. Always respond with JSON when appropriate."}
        ]
        
    def _call_llm(self, prompt: str, response_model: Optional[Type[BaseModel]] = None, use_structured_output: bool = False):
        """
        Call LLM with prompt and return the response.
        
        Args:
            prompt: The prompt to send to the LLM
            response_model: Optional Pydantic model to format response as structured JSON
            use_structured_output: Whether to use OpenAI's function calling for structured output
            
        Returns:
            str: The LLM response
        """
        messages = [
            {"role": "system", "content": f"You are {self.role}."},
            {"role": "user", "content": prompt}
        ]
        
        if use_structured_output and response_model:
            # Create function schema for structured output
            function_schema = create_openai_function_schema(
                model_class=response_model,
                name="generate_structured_response", 
                description="Generate a structured response according to the specified format"
            )
            
            # Call OpenAI with function calling
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                functions=[function_schema],
                function_call={"name": "generate_structured_response"}
            )
            
            # Extract the JSON response from function call
            function_call = response.choices[0].message.function_call
            if function_call and function_call.arguments:
                return function_call.arguments
        else:
            # Regular LLM call without structured output
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages
            )
            
            return response.choices[0].message.content
    
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
