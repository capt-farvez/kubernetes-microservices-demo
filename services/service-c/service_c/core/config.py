import os

from dotenv import load_dotenv

load_dotenv()

SERVICE_A_URL = os.getenv("SERVICE_A_URL", "http://localhost:8005")
SERVICE_B_URL = os.getenv("SERVICE_B_URL", "http://localhost:8006")
