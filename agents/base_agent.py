import sys
import os
import json
from typing import List, Dict, Any, Optional
from openai import OpenAI

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE, OPENAI_MAX_TOKENS, AGENT_MEMORY_LIMIT

class BaseAgent:
    """Base class for all specialized agents."""
    
    def __init__(self, role: str, agent_name: str, base_url: str = None, model_name: str = None):
        """
        Initialize the base agent.
        
        Args:
            role (str): The role description for the agent.
            agent_name (str): The name of the agent.
            base_url (str, optional): OpenAI API base URL
            model_name (str, optional): OpenAI model name to use
        """
        self.client = OpenAI(api_key=OPENAI_API_KEY, base_url=base_url) if base_url else OpenAI(api_key=OPENAI_API_KEY)
        self.role = role
        self.agent_name = agent_name
        self.model = model_name or OPENAI_MODEL
        self.temperature = OPENAI_TEMPERATURE
        self.max_tokens = OPENAI_MAX_TOKENS
        self.conversation_memory: List[Dict[str, str]] = [
            {"role": "system", "content": f"You are {agent_name}, {role}. Always respond with JSON when appropriate."}
        ]
        
    def _call_llm(self, prompt: str, temperature: Optional[float] = None) -> str:
        """
        Call the OpenAI API with a prompt.
        
        Args:
            prompt (str): The prompt to send to the LLM.
            temperature (float, optional): Override default temperature if specified.
        
        Returns:
            str: The response from the LLM.
        """
        self.conversation_memory.append({"role": "user", "content": prompt})
        
        # Limit memory size
        if len(self.conversation_memory) > AGENT_MEMORY_LIMIT + 1:  # +1 for system message
            # Keep system message and recent messages
            self.conversation_memory = [
                self.conversation_memory[0], 
                *self.conversation_memory[-(AGENT_MEMORY_LIMIT):]
            ]
            
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_memory,
                temperature=temperature if temperature is not None else self.temperature,
                max_tokens=self.max_tokens
            )
            
            message_content = response.choices[0].message.content
            self.conversation_memory.append({"role": "assistant", "content": message_content})
            return message_content
        except Exception as e:
            error_msg = f"Error calling LLM: {str(e)}"
            print(error_msg)
            return json.dumps({"error": error_msg})
    
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
