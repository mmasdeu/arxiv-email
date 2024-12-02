from emailgen import *
import os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(".env")

USER = os.environ.get("GMAIL_USER")
PASSWORD = os.environ.get("GMAIL_PASSWORD")
RECIPIENT = os.environ.get("RECIPIENT")
subscriptions = ["math.NT"]
html_file = Path("out/index.html")

html = send_email(RECIPIENT,subscriptions,USER,PASSWORD)


html_file.parent.mkdir(exist_ok=True, parents=True)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html)
