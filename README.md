# Flask URL Shortener

A simple URL shortener built with Flask and SQLite using SQLAlchemy. It generates 6-character alphanumeric short links and redirects users to the original URLs.

## Project Structure
```
url_shortener/
│── app.py                # Main Flask app
│── templates/
│   ├── index.html        # Homepage with input form and copy button
│── static/
│   ├── script.js         # JavaScript for copy button
│── database.db           # SQLite database (auto-generated)
│── requirements.txt      # Required dependencies
```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Sammisam8888/url-shortener.git
   cd url_shortener
   ```

2. Create and activate a new Python virtual environment:
   - On Windows:
     ```bash
     python3 -m venv venv && venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     python3 -m venv venv && source venv/bin/activate
     ```

3. Install the required dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

## Running the App Locally
1. Run the Flask application:
   ```bash
   python3 app.py
   ```

2. Visit `http://127.0.0.1:5000/` in your browser.

## Usage
1. Enter the URL you want to shorten in the input form on the homepage.
2. Click the "Generate URL" button.
3. Copy the generated short URL using the "Copy" button.

## License
This project is licensed under the MIT License.
