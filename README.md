# Product Management System

A simple Product Management application built with **Flask (Python)** for the backend and **Vanilla JS** for the frontend. This project implements full CRUD (Create, Read, Update, Delete) functionality and is tested using **Behave (BDD)** and **Selenium**.

## features

- **Create**: Add new products to the inventory.
- **Read**: View product details and list all products.
- **Update**: Edit existing product information.
- **Delete**: Remove products from the system.
- **Search**: Find products by name.

## Tech Stack

- **Backend**: Flask, Flask-API
- **Frontend**: HTML5, CSS3, JavaScript (Fetch API)
- **Testing**: Behave, Selenium (Gherkin syntax)
- **Database**: In-memory (Mocked using Product Model)

## Installation

1. Clone this repository:
   ```bash
   git clone (https://github.com/muhsamudra12/product-management.git)

   cd product-management
   ```

2. Install dependencies:
```Bash
    pip install -r requirements.txt
```

3. Run the application:
```Bash
    python run.py

    Open: http://127.0.0.1:5000 in your browser.
```


## Testing with Behave
To run the BDD tests, ensure the server is running or configured for testing, then execute:

```Bash
python -m behave
```

## Project Structure
- service/: Contains Flask routes and models.
- features/: Contains Gherkin .feature files and step definitions.
- static/ or templates/: Contains index.html.

