from pathlib import Path
import yaml
from flask import Flask, render_template

BASE_DIR = Path(__file__).parent
app = Flask(__name__)

def load_content():
    with open(BASE_DIR / "content.yaml", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    certs_dir = BASE_DIR / "static" / "certificates"
    static_dir = BASE_DIR / "static"
    cert_list = data.get("certificate") or data.get("certificates") or []

    for item in cert_list:
        cert_val = (item.get("certificate") or "").strip()
        cert_file = None
        cert_url = None

        if cert_val:
            if cert_val.startswith("http://") or cert_val.startswith("https://"):
                cert_url = cert_val
            elif (certs_dir / cert_val).exists():
                cert_file = f"certificates/{cert_val}"
            elif (static_dir / cert_val).exists():
                cert_file = cert_val
            elif (certs_dir / f"{cert_val}.pdf").exists():
                cert_file = f"certificates/{cert_val}.pdf"
            elif (static_dir / f"{cert_val}.pdf").exists():
                cert_file = f"{cert_val}.pdf"
            else:
                # If specified directly, still prepare static path
                cert_file = f"certificates/{cert_val}"
        else:
            # Auto-detect file by item name if certificate field is empty
            name = item.get("name", "").strip()
            if name:
                for ext in [".pdf", ".png", ".jpg", ".jpeg"]:
                    candidates = [
                        name + ext,
                        name.lower() + ext,
                        name.replace(" ", "_") + ext,
                        name.replace(" ", "_").lower() + ext,
                        name.replace(" ", "-") + ext,
                        name.replace(" ", "-").lower() + ext,
                    ]
                    for cand in candidates:
                        if (certs_dir / cand).exists():
                            cert_file = f"certificates/{cand}"
                            break
                        elif (static_dir / cand).exists():
                            cert_file = cand
                            break
                    if cert_file:
                        break

        # Verify physical file existence before assigning certificate_file (prevents 404 in freeze)
        if cert_file and not (BASE_DIR / "static" / cert_file).exists():
            cert_file = None

        item["certificate_file"] = cert_file
        item["certificate_url"] = cert_url

    return data

@app.route("/")
def index():
    resume_exists = (BASE_DIR / "static" / "resume.pdf").exists()
    return render_template("index.html", content=load_content(), resume_exists=resume_exists)

if __name__ == "__main__":
    app.run(debug=True)