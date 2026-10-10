from pathlib import Path
from flask_frozen import Freezer
from app import app

BASE_DIR = Path(__file__).parent

app.config["FREEZER_DESTINATION"] = str(BASE_DIR / "docs")
app.config["FREEZER_RELATIVES_URLS"] = True

freezer = Freezer(app)

if __name__ == "__main__":
    freezer.freeze()
    (BASE_DIR / "docs" / ".nojekyll").touch()
    print("Built to docs/")