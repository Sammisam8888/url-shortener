import random
import string
import re  # Import regex for URL validation
from flask import Flask, request, redirect, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_url = db.Column(db.String(6), unique=True, nullable=False)

def generate_short_url():
    """Generate a random 6-character alphanumeric short URL"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=6))

def is_valid_url(url):
    """Validate the URL format using a regular expression."""
    regex = re.compile(
        r'^(http|https)://'  # URL must start with http:// or https://
        r'([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'  # Domain name
        r'(:[0-9]{1,5})?'  # Optional port
        r'(/.*)?$'  # Optional path
    )
    return re.match(regex, url) is not None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        original_url = request.form["original_url"]

        # Validate the URL
        if not is_valid_url(original_url):
            return jsonify({"error": "Invalid URL format. Please provide a valid URL."}), 400

        short_url = generate_short_url()

        # Ensure uniqueness
        while URL.query.filter_by(short_url=short_url).first():
            short_url = generate_short_url()

        new_entry = URL(original_url=original_url, short_url=short_url)
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({"short_url": request.host_url + short_url})

    return render_template("index.html")

@app.route("/<short_url>")
def redirect_to_original(short_url):
    entry = URL.query.filter_by(short_url=short_url).first()
    if entry:
        return redirect(entry.original_url)
    return render_template("error.html"), 404

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
