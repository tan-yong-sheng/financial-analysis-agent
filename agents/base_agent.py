import sys
import os
import json
from typing import List, Dict, Any, Optional, Type, TypeVar, Generic
from openai import OpenAI
from pydantic import BaseModel
import instructor
import time

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE, OPENAI_MAX_TOKENS, AGENT_MEMORY_LIMIT
from utils.observability import StructuredLogger, AgentTracer, monitor_agent_method


T = TypeVar('T', bound=BaseModel)

class BaseAgent:
    """Base class for all agents in the system."""
    
    def __init__(self, role: str, name: str, base_url: str = None, model_name: str = None):
        """
        Initialize the base agent with enhanced logging capabilities.
        """
        # Setup structured logging
        self.logger = StructuredLogger(f"agent.{name.lower()}")
        self.tracer = AgentTracer(name, self.logger)
        
        """
        Initialize the base agent.
        
        Args:
            role (str): The role description for the agent.
            name (str): The name of the agent.
            base_url (str, optional): OpenAI API base URL
            model_name (str, optional): OpenAI model name to use
        """
        # Create standard client for regular completions
        # Initialize OpenAI clients with logging
        self.logger.info(f"Initializing {name} with role: {role}", 
                        model=model_name or OPENAI_MODEL,
                        base_url=base_url)
        
        self.standard_client = OpenAI(api_key=OPENAI_API_KEY, base_url=base_url) if base_url else OpenAI(api_key=OPENAI_API_KEY)
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
        
    @monitor_agent_method()
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
        start_time = time.time()
        token_count = len(prompt.split())  # Rough estimation
        
        try:
            response = self.standard_client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            execution_time = time.time() - start_time
            response_tokens = len(response.choices[0].message.content.split())  # Rough estimation
            
            self.logger.info("LLM call completed",
                           model=self.model_name,
                           execution_time=execution_time,
                           input_tokens=token_count,
                           output_tokens=response_tokens,
                           total_tokens=token_count + response_tokens)
            
            return response.choices[0].message.content
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.logger.error("LLM call failed",
                            model=self.model_name,
                            execution_time=execution_time,
                            input_tokens=token_count,
                            error_type=type(e).__name__,
                            error_message=str(e))
            raise
    
    @monitor_agent_method()
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
        
        start_time = time.time()
        token_count = len(prompt.split())  # Rough estimation
        
        try:
            # Use the instructor-patched client for structured responses
            response = self.instructor_client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                response_model=response_model,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            execution_time = time.time() - start_time
            
            self.logger.info("Structured LLM call completed",
                           model=self.model_name,
                           execution_time=execution_time,
                           input_tokens=token_count,
                           response_type=response_model.__name__)
            
            return response
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.logger.error("Structured LLM call failed",
                            model=self.model_name,
                            execution_time=execution_time,
                            input_tokens=token_count,
                            response_type=response_model.__name__,
                            error_type=type(e).__name__,
                            error_message=str(e))
            
            # Create an instance with default values if possible
            try:
                return response_model()
            except:
                raise e
    
    @monitor_agent_method()
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
    
    @monitor_agent_method()
    def reset_memory(self):
        """Reset the agent's conversation memory, keeping only the system message."""
        self.logger.info(f"Resetting memory for {self.name}")
        system_message = self.conversation_memory[0]
        self.conversation_memory = [system_message]
