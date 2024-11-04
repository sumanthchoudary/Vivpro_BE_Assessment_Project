
# Songs Playlist API

## Overview

This project is the solution for the Assessment for a **Backend Engineer** role at Vivpro. This application includes modules to process and normalize JSON data into tabular format, and APIs to serve this normalized data. The project uses **Flask** and **SQLAlchemy** frameworks to create the APIs.

## Features

- **Data Normalization**: Converts a JSON structure of song attributes into a relational format, storing it in a SQLite database.
- **RESTful APIs**: Provides endpoints to:
  - Retrieve all songs (with pagination).
  - Search for songs by title.
  - Rate songs (and calculate average rating).
- **Unit Testing**: Includes tests for key API endpoints using `pytest`.

---

## How to Run the Application

1. **Set up a Virtual Environment** (optional):

   ```bash
   python3 -m venv venv
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare the JSON Data**:
   - Ensure that the `playlist.json` file is in the project root directory.

4. **Load JSON Data into SQLite**:

   ```bash
   python populate_db.py
   ```

   - This command normalizes and loads the data into the `songs.db` SQLite database.

5. **Start the Application**:

   ```bash
   flask run
   ```

   - The application will be available at [http://localhost:5000/](http://localhost:5000/).

---

## Testing the Application

To run all test cases from the project root, use:

```bash
python -m pytest test/test_routes.py
```

---

## Important Files

- **`app.py`**: Main Flask application file to initialize the app, configure the database, and register routes.
- **`models.py`**: Defines the `Song` model and schema, along with methods for converting song instances to dictionaries for JSON responses.
- **`populate_db.py`**: Script to load and normalize song data from `playlist.json` and populate it into `songs.db`.
- **`routes.py`**: Contains API endpoint definitions as specified in the assessment.
- **`test/test_routes.py`**: Unit tests to verify API functionality.

---
