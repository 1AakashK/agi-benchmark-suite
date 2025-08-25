import requests
import json
import time

class OllamaInterface:
    """Interface for interacting with Ollama models."""
    
    def __init__(self, model_name="gemma3:latest", base_url="http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        self.api_url = f"{base_url}/api/generate"
        self.conversation_history = []
    
    def solve(self, task_description):
        """Solve a task using the Ollama model.
        
        Args:
            task_description: A string describing the task to solve
            
        Returns:
            str: The model's solution to the task
        """
        # Add the task to conversation history
        self.conversation_history.append({"role": "user", "content": task_description})
        
        # Prepare the request
        request_data = {
            "model": self.model_name,
            "prompt": task_description,
            "stream": False
        }
        
        # Send the request to Ollama
        try:
            response = requests.post(self.api_url, json=request_data)
            response.raise_for_status()
            result = response.json()
            
            # Extract the generated response
            solution = result.get("response", "")
            
            # Add the response to conversation history
            self.conversation_history.append({"role": "assistant", "content": solution})
            
            return solution
            
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Ollama: {e}")
            return ""
    
    def reset(self):
        """Reset the conversation history."""
        self.conversation_history = []