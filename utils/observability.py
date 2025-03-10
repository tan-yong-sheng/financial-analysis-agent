import logging
import json
import time
from functools import wraps
from typing import Any, Dict, Optional, Callable

class StructuredLogger:
    """Enhanced structured logger for improved observability."""
    
    def __init__(self, name: str, log_level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        self.context = {}
    
    def set_context(self, **kwargs):
        """Add persistent context to all log messages."""
        self.context.update(kwargs)
    
    def _log(self, level, message, **kwargs):
        """Internal logging with structured data."""
        log_data = {**self.context, **kwargs, "message": message}
        
        # Add timestamp if not present
        if "timestamp" not in log_data:
            log_data["timestamp"] = time.time()
            
        self.logger.log(level, json.dumps(log_data))
    
    def info(self, message, **kwargs):
        self._log(logging.INFO, message, **kwargs)
    
    def warning(self, message, **kwargs):
        self._log(logging.WARNING, message, **kwargs)
    
    def error(self, message, **kwargs):
        self._log(logging.ERROR, message, **kwargs)
    
    def debug(self, message, **kwargs):
        self._log(logging.DEBUG, message, **kwargs)
    
    def critical(self, message, **kwargs):
        self._log(logging.CRITICAL, message, **kwargs)

def log_execution_time(logger: StructuredLogger, operation_name: Optional[str] = None):
    """Decorator to log function execution time."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            op_name = operation_name or func.__name__
            
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                logger.info(f"{op_name} completed", 
                           execution_time=execution_time, 
                           status="success")
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(f"{op_name} failed",
                            execution_time=execution_time,
                            error_type=type(e).__name__,
                            error_message=str(e),
                            status="error")
                raise
        return wrapper
    return decorator

def monitor_agent_method(logger_name: str = None):
    """Decorator to monitor agent method calls with structured logging."""
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            method_name = func.__name__
            agent_name = getattr(self, 'name', self.__class__.__name__)
            logger_instance = logging.getLogger(logger_name or f"{agent_name}.{method_name}")
            
            # Create a clean dict of args for logging (avoid large objects)
            safe_args = {}
            for i, arg in enumerate(args):
                if isinstance(arg, (str, int, float, bool, type(None))):
                    safe_args[f"arg_{i}"] = arg
                else:
                    safe_args[f"arg_{i}_type"] = type(arg).__name__
            
            safe_kwargs = {}
            for k, v in kwargs.items():
                if isinstance(v, (str, int, float, bool, type(None))):
                    safe_kwargs[k] = v
                else:
                    safe_kwargs[f"{k}_type"] = type(v).__name__
            
            start_time = time.time()
            logger_instance.info(f"Starting {agent_name}.{method_name}", 
                               agent=agent_name,
                               method=method_name,
                               args=safe_args,
                               kwargs=safe_kwargs)
            
            try:
                result = func(self, *args, **kwargs)
                execution_time = time.time() - start_time
                
                # Log result summary if it's a dict
                result_summary = {}
                if isinstance(result, dict):
                    for k, v in result.items():
                        if k in ["error", "ticker", "status"]:
                            result_summary[k] = v
                        elif isinstance(v, (str, int, float, bool, type(None))):
                            result_summary[k] = v
                        elif isinstance(v, (list, tuple)) and len(v) > 0:
                            result_summary[f"{k}_count"] = len(v)
                        else:
                            result_summary[f"{k}_type"] = type(v).__name__
                
                logger_instance.info(f"Completed {agent_name}.{method_name}",
                                   agent=agent_name,
                                   method=method_name,
                                   execution_time=execution_time,
                                   status="success",
                                   result=result_summary)
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                logger_instance.error(f"Failed {agent_name}.{method_name}",
                                    agent=agent_name,
                                    method=method_name,
                                    execution_time=execution_time,
                                    error_type=type(e).__name__,
                                    error_message=str(e),
                                    status="error")
                raise
        return wrapper
    return decorator

class AgentTracer:
    """Trace agent activities for observability."""
    
    def __init__(self, agent_name: str, logger: StructuredLogger):
        self.agent_name = agent_name
        self.logger = logger
        self.current_task = None
        self.task_start_time = None
        
    def start_task(self, task_name: str, **context):
        """Record the start of an agent task."""
        self.current_task = task_name
        self.task_start_time = time.time()
        self.logger.info(f"Agent {self.agent_name} started task: {task_name}",
                        agent=self.agent_name,
                        task=task_name,
                        event="task_start",
                        **context)
        
    def end_task(self, status: str = "success", result_summary: Optional[Dict[str, Any]] = None, **context):
        """Record the end of an agent task."""
        if not self.current_task or not self.task_start_time:
            self.logger.warning(f"Attempting to end task for {self.agent_name} but no task was started")
            return
            
        execution_time = time.time() - self.task_start_time
        log_data = {
            "agent": self.agent_name,
            "task": self.current_task,
            "event": "task_end",
            "status": status,
            "execution_time": execution_time,
            **context
        }
        
        if result_summary:
            log_data["result"] = result_summary
            
        self.logger.info(f"Agent {self.agent_name} completed task: {self.current_task}", **log_data)
        self.current_task = None
        self.task_start_time = None
