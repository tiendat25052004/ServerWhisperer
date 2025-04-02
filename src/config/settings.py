import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# MinIO Configuration
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_HOST = "172.27.102.178:9000"
MINIO_SECURE = False

# Email Configuration
EMAIL_SENDER = "tiendatruong@gmail.com"
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# File paths
CONFIG_FILE = "data/servers_config.json"
LOGS_DIR = "data/logs"

# LLM Configuration
LLM_MODEL = "gpt-4o-mini"

# Define allowed commands
ALLOWED_COMMANDS = ["docker logs"]