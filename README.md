# SababaJobs.co.il - Demo Application & Tests

Demo project of a resume submission system with automated tests for SababaJobs.co.il.

## Local Setup
1. Create virtual environment:
   python -m venv venv
   source venv/bin/activate  # bash / mac
   venv\Scripts\activate     # windows
2. Install dependencies:
   pip install -r requirements.txt
3. Run the app:
   export FLASK_APP=app.py
   flask run
   (or) python app.py

App runs at http://127.0.0.1:5000

## Running Tests
- API tests: pytest tests/test_api.py
- UI tests (Selenium): start Flask app, then pytest tests/test_ui.py
- CI: see .github/workflows/ci.yml

## Tips
- webdriver-manager avoids manual driver setup.
- CI uses selenium/standalone-chrome service.
