from typing import List
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate
from langchain.tools import Tool
from src.config.settings import OPENAI_API_KEY, LLM_MODEL
from src.tools.command_tools import CommandTools
# from src.tools.email_tools import EmailTools
from src.tools.email_tools import send_email
# from src.tools.storage_tools import StorageTools
from src.tools.storage_tools import upload_to_minio
from src.core.ssh_manager import SSHManager

class ServerWhispererAgent:
    """
    Agent that handles server management and log retrieval
    """
    def __init__(self):
        """Initialize the agent with tools and LLM"""
        self.llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model=LLM_MODEL)
        # self.email_tools = EmailTools()
        # self.storage_tools = StorageTools()
        
        # Initialize tools as Tool objects, not direct function references
        self.tools = [
            CommandTools.extract_command,
            SSHManager.execute_command,
            # self.email_tools.send_email,
            # self.storage_tools.upload_to_minio
            send_email,
            upload_to_minio
        ]
        
        # Create agent prompt
        self.prompt = ChatPromptTemplate.from_template("""
        You are an AI assistant, if the user request extracts SSH-related requests, executes them, and uploads the results. Use tools as needed. Stop the agent when the task is complete.

        ### Tasks:
        1. You are chatbot when user ask the question that dont related to SSH and docker, answer them, don't call function if not needed
                                                        
        2. Identify 'server_name' and 'command' from the user request.
           - If the command is not allowed, return "I am not granted the right to use this command, try again with another command like "docker logs --tail 100" and stop.
        3. Execute the command via SSH.
           - Only proceed if the command is valid. Return SHH error, please tell user check container or user.
        4. Upload the execution result as a report to MinIO.
           - Ensure the upload is successful before proceeding.
        5. Stop when the upload is confirmed as successful.

        ### Important Rules:
        - Only allow 'docker logs' commands. Deny all other commands.
        - If an error occurs at any step, report it and stop.
        - Keep the process efficient and avoid unnecessary loops.

        User request: {input}

        {agent_scratchpad}
        """)
        
        # Create agent and executor
        self.agent = create_openai_tools_agent(self.llm, self.tools, prompt=self.prompt)
        self.executor = AgentExecutor(
            agent=self.agent, 
            tools=self.tools, 
            verbose=True, 
            max_iterations=10
        )
    
    def _ssh_execute(self, server_name: str, command: str) -> str:
        """
        Connect to a server via SSH and execute the given command.
        This is a wrapper around the SSHManager for use as a tool.
        """
        return SSHManager.execute_command(server_name, command)
    
    def process_request(self, user_input: str) -> str:
        """
        Process a user request through the agent
        
        Args:
            user_input: User's input message
            
        Returns:
            Agent's response
        """
        try:
            result = self.executor.invoke({"input": user_input})
            return result['output']
        except Exception as e:
            return f"An error occurred: {str(e)}"