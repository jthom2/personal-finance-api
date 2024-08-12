
# FastAPI Financial Application

This project is a Python-based web application built using FastAPI. It provides functionality for user authentication, transaction management, and various validation services. The application uses JWT for secure authentication and SQLAlchemy for database interactions.

## Features

- **User Authentication**: Secure user login and registration with JWT-based authentication.
- **Transaction Management**: Add, retrieve, and manage financial transactions.
- **Validation Services**: Email and IP address validation to ensure data integrity.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/yourproject.git
   cd yourproject
   ```

2. **Install Dependencies**:
   This project uses Poetry for dependency management. Install the dependencies by running:
   ```bash
   poetry install
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the root directory and configure your environment variables (e.g., `DATABASE_URL`, `SECRET_KEY`, `MAILBOXVALIDATOR_API_KEY`, `IPQUALITYSCORE_API_KEY`).

4. **Run the Application**:
   Start the FastAPI server using Uvicorn:
   ```bash
   uvicorn main:app --reload
   ```

## Project Structure

- `main.py`: The entry point of the application.
- `app/`: Contains all the core application modules and utilities.
  - `utils/`: Utility functions and modules, including JWT handling and validators.
  - `finance_class.py`: Defines the financial data structure and logic.
  - `database.py`: Database connection and session management.
  - `models.py`: SQLAlchemy models representing the database schema.
  
## Usage

- **Register**: Create a new user account.
- **Login**: Authenticate with your credentials to receive a JWT token.
- **Add Transaction**: Submit financial transactions.
- **Get Transactions**: Retrieve transaction history.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
