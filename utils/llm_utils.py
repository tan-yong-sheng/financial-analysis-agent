import json
import re
import logging
from typing import Dict, Any, Union, Optional, Type, TypeVar, List, Generic
from pydantic import BaseModel, ValidationError, create_model

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=BaseModel)

def parse_llm_json_response(
    response: str, 
    default_structure: Optional[Dict[str, Any]] = None,
    logger_name: str = "llm_json_parser"
) -> Dict[str, Any]:
    """
    Parse JSON from LLM responses with multiple fallback strategies.
    
    Args:
        response (str): The raw LLM response text
        default_structure (dict, optional): Default structure to return if parsing fails
        logger_name (str): Name to use in logging messages for context
        
    Returns:
        dict: The parsed JSON object or a fallback structure
    """
    if not response or not response.strip():
        logger.error(f"{logger_name}: Empty response received")
        return default_structure or {"error": "Empty response received"}
    
    # Strategy 1: Direct JSON parsing
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        logger.debug(f"{logger_name}: Direct JSON parsing failed, trying code block extraction")
    
    # Strategy 2: Extract JSON from code blocks
    json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', response, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            logger.debug(f"{logger_name}: Code block JSON parsing failed, trying curly braces extraction")
    
    # Strategy 3: Extract content between curly braces
    json_match = re.search(r'(\{.*\})', response, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            logger.debug(f"{logger_name}: Curly braces JSON parsing failed")
    
    # If we reach here, all parsing attempts failed
    logger.warning(f"{logger_name}: All JSON parsing strategies failed, using fallback")
    
    # Return either the provided default or a simple structure with the raw text
    if default_structure is not None:
        return default_structure
    
    return {
        "text": response,
        "parsing_note": "Generated from raw text due to JSON parsing failure"
    }

def parse_and_validate_llm_response(
    response: str,
    model_class: Type[T],
    logger_name: str = "llm_json_validator"
) -> Union[T, Dict[str, Any]]:
    """
    Parse and validate LLM response against a Pydantic model.
    
    Args:
        response (str): The raw LLM response text
        model_class (Type[BaseModel]): Pydantic model class for validation
        logger_name (str): Name to use in logging messages for context
        
    Returns:
        Union[T, Dict[str, Any]]: Validated model instance or error dictionary
    """
    try:
        # First parse the JSON using our robust parser
        parsed_data = parse_llm_json_response(
            response,
            default_structure=None,
            logger_name=logger_name
        )
        
        # Then validate against the model
        validated_data = model_class.model_validate(parsed_data)
        return validated_data
    
    except ValidationError as e:
        logger.error(f"{logger_name}: Validation error: {e}")
        return {
            "error": f"JSON validation failed: {str(e)}",
            "raw_data": parsed_data if 'parsed_data' in locals() else None
        }
    except Exception as e:
        logger.error(f"{logger_name}: Unexpected error during validation: {str(e)}")
        return {"error": f"Failed to validate response: {str(e)}"}

def create_openai_function_schema(model_class: Type[BaseModel], name: str, description: str) -> Dict[str, Any]:
    """
    Create a function schema for OpenAI structured outputs based on a Pydantic model.
    
    Args:
        model_class (Type[BaseModel]): The Pydantic model to convert
        name (str): The name of the function
        description (str): Description of the function
        
    Returns:
        Dict[str, Any]: Function schema for OpenAI functions API
    """
    schema = model_class.model_json_schema()
    function_schema = {
        "name": name,
        "description": description,
        "parameters": schema
    }
    return function_schema

def parse_list_response(
    response: str,
    item_model: Type[T] = None,
    default_items: List[Dict[str, Any]] = None,
    logger_name: str = "llm_list_parser"
) -> List[Union[T, Dict[str, Any]]]:
    """
    Parse a list response from LLM with optional validation.
    
    Args:
        response (str): The raw LLM response text
        item_model (Type[BaseModel], optional): Pydantic model for list items
        default_items (list, optional): Default list to return on parsing failure
        logger_name (str): Name to use in logging messages
        
    Returns:
        list: The parsed and optionally validated list
    """
    try:
        # First try to parse as JSON list
        parsed_data = parse_llm_json_response(response, default_structure=None, logger_name=logger_name)
        
        if not isinstance(parsed_data, list):
            logger.warning(f"{logger_name}: Response did not parse as a list")
            if isinstance(parsed_data, dict) and any(k.startswith('item') for k in parsed_data.keys()):
                # Try to extract a list from dictionary with item keys
                items = [v for k, v in parsed_data.items() if k.startswith('item') or k.isdigit()]
                if items:
                    parsed_data = items
            else:
                # Return default or empty list
                return default_items or []
        
        # If no model is provided, just return the parsed list
        if item_model is None:
            return parsed_data
        
        # Validate each item against the model
        validated_items = []
        for i, item in enumerate(parsed_data):
            try:
                validated_item = item_model.model_validate(item)
                validated_items.append(validated_item)
            except ValidationError as e:
                logger.warning(f"{logger_name}: Item {i} validation failed: {e}")
                validated_items.append({"error": f"Validation error: {str(e)}", "raw_item": item})
        
        return validated_items
    
    except Exception as e:
        logger.error(f"{logger_name}: Failed to parse list response: {str(e)}")
        return default_items or []