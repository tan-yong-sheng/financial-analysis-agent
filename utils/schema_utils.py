"""Utilities for handling JSON schemas for LLM function calls."""

from typing import Dict, Any, List, Optional, Type
from pydantic import BaseModel
import json
import copy

def clean_schema_for_llm(schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean a JSON schema to make it compatible with LLM function calls.
    Removes problematic fields like 'default' that cause issues with some LLMs.
    
    Args:
        schema: The JSON schema to clean
        
    Returns:
        Dict[str, Any]: A cleaned schema suitable for LLM function calls
    """
    cleaned = copy.deepcopy(schema)
    
    def _clean_object(obj: Dict[str, Any]) -> None:
        # Remove default field if present
        if 'default' in obj:
            del obj['default']
        
        # Clean properties if present
        if 'properties' in obj:
            for prop in obj['properties'].values():
                if isinstance(prop, dict):
                    _clean_object(prop)
        
        # Clean items if present (for arrays)
        if 'items' in obj and isinstance(obj['items'], dict):
            _clean_object(obj['items'])
    
    _clean_object(cleaned)
    return cleaned

def get_clean_model_schema(model_class: Type[BaseModel]) -> Dict[str, Any]:
    """
    Get a clean JSON schema from a Pydantic model class.
    
    Args:
        model_class: The Pydantic model class
        
    Returns:
        Dict[str, Any]: A schema suitable for LLM function calls
    """
    schema = model_class.model_json_schema()
    return clean_schema_for_llm(schema)

def create_clean_function_schema(model_class: Type[BaseModel], name: str, description: str) -> Dict[str, Any]:
    """
    Create a clean function schema for LLM function calls using a Pydantic model.
    
    Args:
        model_class: The Pydantic model class
        name: The function name
        description: The function description
        
    Returns:
        Dict[str, Any]: A clean function schema
    """
    schema = get_clean_model_schema(model_class)
    function_schema = {
        "name": name,
        "description": description,
        "parameters": schema
    }
    return function_schema
