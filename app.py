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

def generate_short_url(original_url):
    """Generate a short URL based on phrases from the original URL."""
    # Extract the domain name without 'www.' or protocol
    domain = re.sub(r'^(http://|https://|www\.)', '', original_url).split('/')[0]
    # Take the first two characters of each domain segment to form the short URL
    short_url = ''.join([word[:2] for word in domain.split('.') if word])[:4]
    # Ensure the short URL is at least 4 characters and no more than 6 characters
    if len(short_url) < 4:
        short_url += ''.join(random.choices(string.ascii_letters + string.digits, k=4 - len(short_url)))
    return short_url

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
    short_url = None
    error = None

    if request.method == "POST":
        original_url = request.form["original_url"]

        # Automatically prepend https:// if not present
        if not original_url.startswith(("http://", "https://")):
            original_url = "https://" + original_url

        # Validate the URL
        if not is_valid_url(original_url):
            error = "Invalid URL format. Please provide a valid URL."
        else:
            # Check if the URL already exists in the database
            existing_entry = URL.query.filter_by(original_url=original_url).first() #if no data is present in database for the corresponding original url then it returns None - False
            if existing_entry:
                short_url = request.host_url + existing_entry.short_url
            else:
                short_url = generate_short_url(original_url)

                # Ensure uniqueness
                while URL.query.filter_by(short_url=short_url).first():
                    short_url += random.choice(string.ascii_letters + string.digits)

                new_entry = URL(original_url=original_url, short_url=short_url)
                db.session.add(new_entry)
                db.session.commit()
                short_url = request.host_url + short_url

    return render_template("index.html", title="SnapURL", short_url=short_url, error=error)

@app.route("/<short_url>",methods=["GET"])
def redirect_to_original(short_url):
    entry = URL.query.filter_by(short_url=short_url).first()
    if entry:
        return redirect(entry.original_url)
    return render_template("error.html"), 404

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    # app.run(debug=True) # use while production
    # app.run(host="0.0.0.0", port=10000) #use while deployment
