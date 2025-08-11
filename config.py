# config.py
import os
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_KEY = os.getenv("OPENWEATHER_API_KEY")
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "devsecret")

if not OPENWEATHER_KEY:
    raise RuntimeError("OPENWEATHER_API_KEY not set in .env")