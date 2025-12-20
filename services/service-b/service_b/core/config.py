import os

from dotenv import load_dotenv

load_dotenv()

SERVICE_A_URL = os.getenv("SERVICE_A_URL", "http://localhost:8005")
SERVICE_C_URL = os.getenv("SERVICE_C_URL", "http://localhost:8007")
