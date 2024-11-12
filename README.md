# Data Type Inferencer using Django and React

This project is a simple web application that allows users to upload a CSV file and view the inferred data types for each column. The backend is built using Django and the frontend is built using React.

## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

- Python 3.6 or higher
- Node.js 12.18.3 or higher
- npm 6.14.6 or higher
- pip 20.1.1 or higher
- virtualenv 20.0.21 or higher
- Django 3.0.8 or higher
- Django REST framework 3.11.0 or higher
- React 16.13.1 or higher

### Backend Installation

1. Clone the repo
   ```sh
   git clone git@github.com:ramil811/rhombus-tech-interview.git
    ```

2. Install the required packages
    ```sh
    cd rhombus-tech-interview
    pip install -r requirements.txt
    ```

3. Create a python virtual environment

    ```sh
    python -m venv env
    ```

4. Activate the virtual environment
    <br/>
    On Windows:
    <br/>
    ```sh
    .\env\Scripts\activate
    ```
    On MacOS/Linux:
    <br/>
    ```sh
    source env/bin/activate
    ```

5. Start the Django server
    ```sh
    cd rhombus-tech-interview
    cd backend
    python manage.py runserver
    ```

### Frontend Installation

1. Install npm packages
    ```sh
    cd rhombus-tech-interview
    cd frontend
    npm install
    ```

2. Start the React server
    ```sh
    npm start
    ```

## Usage

1. Open your browser and go to `http://localhost:3000/`
2. Upload a CSV or an Excel file
3. Click on the `Upload` button
4. View the inferred data types for each column

