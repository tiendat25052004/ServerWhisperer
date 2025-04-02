import json
import paramiko
from src.config.settings import CONFIG_FILE
from langchain.tools import tool

class SSHManager:
    """
    Manages SSH connections and command execution on remote servers
    """
    def load_server_config():
        """Load server configuration from file"""
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    @tool
    def execute_command(server_name: str, command: str) -> str:
        """
        Connect to a server via SSH and execute the given command
        
        Args:
            server_name: Name of the server as defined in config
            command: Command to execute
            
        Returns:
            Output of the command or error message
        """
        config = SSHManager.load_server_config()
        server_info = config.get(server_name)
        
        if not server_info:
            return f"Server '{server_name}' not found in configuration."
        
        ip = server_info.get("ip")
        username = server_info.get("username")
        ssh_key = server_info.get("ssh_key")
        password = server_info.get("password")
        
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            if ssh_key:
                client.connect(ip, username=username, key_filename=ssh_key)
            else:
                client.connect(ip, username=username, password=password)
            
            stdin, stdout, stderr = client.exec_command(command)
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()
            client.close()
            
            return output if output else error
        except Exception as e:
            return f"SSH Error: {e}"