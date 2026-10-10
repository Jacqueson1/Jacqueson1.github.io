from pathlib import Path
import yaml
from flask import Flask, render_template

BASE_DIR = Path(__file__).parent
app = Flask(__name__)

def load_content():
    with open(BASE_DIR / "content.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)

@app.route("/")
def index():
    resume_exists = (BASE_DIR / "static" / "resume.pdf"). exists()
    return render_template("index.html", content=load_content(), resume_exists=resume_exists,)

if __name__ == "__main__":
    app.run(debug=True)