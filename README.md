# Hospitality-digitalization-TECHFEST
# Hostel Room Allocation Application

## Overview
This web application allocates rooms in hostels based on group information and hostel capacities.

## Logic
- The Flask application (`app.py`) handles file uploads, processes CSV data using pandas, and allocates rooms based on group gender and hostel capacities.
- The HTML template (`index.html`) provides a form to upload `group.csv` and `hostel.csv` files.
- The allocation algorithm ensures groups stay together, genders are segregated in hostels, and room capacities are respected.

## Usage
1. **Installation**:
   - Ensure Python and Flask are installed.
   - Install required dependencies using `pip install -r requirements.txt`.

2. **Running the Application**:
   - Run the Flask application using `python app.py`.
   - Open your browser and go to `http://127.0.0.1:5000/`.
   - Upload `group.csv` and `hostel.csv` files and click "Upload and Allocate".
   - Download the allocated room details from the generated `room_allocation.csv` file.

