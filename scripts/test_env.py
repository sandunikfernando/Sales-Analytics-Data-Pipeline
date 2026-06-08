from dotenv import load_dotenv
import os

load_dotenv()

print(os.getenv("SNOWFLAKE_USER"))