from dotenv import load_dotenv
import os


def load_environment_variables():
    load_dotenv()
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    return DISCORD_TOKEN
