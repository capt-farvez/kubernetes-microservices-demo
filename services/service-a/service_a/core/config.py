import os

from dotenv import load_dotenv

load_dotenv()

SERVICE_B_URL = os.getenv("SERVICE_B_URL", "http://localhost:8006")
SERVICE_C_URL = os.getenv("SERVICE_C_URL", "http://localhost:8007")
