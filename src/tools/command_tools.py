# from src.config.settings import ALLOWED_COMMANDS

# class CommandTools:
#     """
#     Tools for validating and extracting commands
#     """
#     @staticmethod
#     def extract_command(server_name: str, command: str, email: str = None) -> dict:
#         """
#         Extract and validate command information from user request.
        
#         Args:
#             server_name: Name of the server to connect to
#             command: Command to execute
#             email: Optional email address to send results to
            
#         Returns:
#             Dictionary with extracted information or error message
#         """
#         # Check if command is allowed
#         if not any(command.startswith(allowed_cmd) for allowed_cmd in ALLOWED_COMMANDS):
#             return {
#                 "error": "Permission denied. You are only allowed to retrieve docker logs."
#             }
        
#         result = {"server_name": server_name, "command": command}
        
#         if email:
#             result["email"] = email
            
#         return result

from langchain.tools import tool
from src.config.settings import ALLOWED_COMMANDS

class CommandTools:
    """
    Tools for validating and extracting commands
    """
    @tool
    def extract_command(server_name: str, command: str, email: str = None) -> dict:
        """
        Extract and validate command information from user request.
        
        Args:
            server_name: Name of the server to connect to
            command: Command to execute
            email: Optional email address to send results to
            
        Returns:
            Dictionary with extracted information or error message
        """
        # Check if command is allowed
        if not any(command.startswith(allowed_cmd) for allowed_cmd in ALLOWED_COMMANDS):
            return {
                "error": "Permission denied. You are only allowed to retrieve docker logs."
            }
        
        result = {"server_name": server_name, "command": command}
        
        if email:
            result["email"] = email
            
        return result