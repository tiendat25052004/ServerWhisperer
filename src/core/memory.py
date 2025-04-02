import time
from typing import List, Dict, Any

class ChatMemory:
    """
    Maintains a history of chat messages with timestamps
    """
    def __init__(self):
        self.history: List[Dict[str, Any]] = []
    
    def add_message(self, role: str, content: str):
        """Add a message to the chat history"""
        self.history.append({
            "role": role,
            "content": content,
            "timestamp": time.strftime("%H:%M:%S", time.localtime())
        })
    
    def get_context(self, window_size: int = 4) -> str:
        """
        Get the most recent conversation context
        
        Args:
            window_size: Number of recent messages to include
            
        Returns:
            String representation of recent conversation
        """
        recent_messages = self.history[-window_size:] if len(self.history) > 0 else []
        return "\n".join(
            f"{msg['role']} ({msg['timestamp']}): {msg['content']}" 
            for msg in recent_messages
        )
    
    def clear(self):
        """Clear the chat history"""
        self.history = []