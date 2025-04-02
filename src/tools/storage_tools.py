import os
from langchain.tools import tool
from minio import Minio
from src.config.settings import (
    MINIO_ACCESS_KEY, 
    MINIO_SECRET_KEY, 
    MINIO_HOST, 
    MINIO_SECURE,
    MINIO_ENDPOINT,
    LOGS_DIR
)


@tool
def upload_to_minio(server_name: str, logs: str) -> dict:
    """Upload logs as a report to MinIO and return the file URL."""
    minio_client = Minio(
        "172.27.102.178:9000",
        access_key=os.getenv("MINIO_ACCESS_KEY"),
        secret_key=os.getenv("MINIO_SECRET_KEY"),
        secure=False
    )

    logs_dir = "/logs"
    file_path = os.path.join(logs_dir, f"{server_name}_docker_logs.txt")
    os.makedirs(logs_dir, exist_ok=True)
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("")

    bucket_name = "ataiongke"
    file_name = f"{server_name}_docker_logs.txt"    
    file_path = f"/logs/{file_name}"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(logs)

    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)

    minio_client.fput_object(bucket_name, f"logs/{file_name}", file_path)

    file_url = f"{os.getenv('MINIO_ENDPOINT')}/browser/{bucket_name}/logs/{file_name}"
    return {"status": "success", "file_url": file_url}
