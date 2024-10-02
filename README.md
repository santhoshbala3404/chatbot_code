ChatBot-:
This is a chatbot which interacts with ERP system for managing documents, expenses, invoices, budgets, and reminders. 

It utilizes various libraries such as Tesseract for OCR, spaCy for natural language processing, and SQLite for data storage.


Requirements-:

1)Python 3.x

2)pip (Python package manager)

Required Libraries-:

You will need the following libraries:

1)Flask

2)pytesseract

3)Pillow

4)spacy

5)sqlite3 (part of the Python standard library)

6)PyJWT

7)scikit-learn

8)Werkzeug

Installation-:

1)Clone the repository:

bash-

Copy code

git clone <repository_url>

cd <repository_directory>

2)Install the required libraries:

If you have pip set up, run the following command:

bash-

Copy code

pip install Flask pytesseract Pillow spacy scikit-learn pyjwt Werkzeug

3)Download the spaCy model:

Run the following command to download the English language model:


bash-

Copy code

python -m spacy download en_core_web_sm

Install Tesseract OCR:

4)Follow the installation instructions for Tesseract OCR.

a)Ensure that the Tesseract executable is in your system's PATH.

Running the Application

Set the secret key:

b)Update the SECRET_KEY in the code to a secure value.

5)Run the application:

In your terminal, execute the following command:

bash-

Copy code

python app.py

6)Access the application:

Open a web browser and go to HTTP link given on executing


API Endpoints

The following API endpoints are available:

1)Document Upload-

POST /uploads-

Uploads a document and extracts text using Tesseract OCR.

2)Named Entity Recognition (NER)-

POST /ner-

Performs NER on provided text.

3)Train Classifier-

POST /train_classifier-

Trains the document classifier with provided documents and labels.

4)Classify Document-

POST /classify-

Classifies a given document based on the trained model.

5)Search Documents-

GET /search-

Searches documents in the database.

6)User Verification-

POST /verify-

Verifies user credentials and returns a JWT token.

7)Dashboard-

GET /dashboard-

Returns a welcome message if the token is valid.

8)Account Balance Inquiry-

GET /account_balance-

Returns dummy account balances.

9)Transaction History-

GET /transaction_history-

Returns a list of transactions, optionally filtered by date, type, and amount.

10)Invoice Management-

POST /invoices-

Creates a new invoice.-

GET /invoices-

Lists all invoices.

GET /invoice_status/<invoice_id>-

Returns the status of a specific invoice.

11)Expense Tracking-

POST /track_expense-

Tracks a new expense.

GET /monthly_expenses-

Returns monthly expense summary.

12)Budget Management-

POST /set_budget-

Sets a new budget.

GET /budget_summary-

Returns the budget summary for a specific category.

13)Payment Reminders-

POST /payment_remainder-

Sets a payment reminder.

GET /payment_reminders-

Lists all payment reminders.

14)Role Management-

POST /role_management-

Updates the role of a user.

Team Members and Contributions:

1)Santhosh B-: Worked on the code and took demo video 

2)Vignesh Balamurugan-: Worked on the code and created the presentation regarding our project

3)Darshan R-: Worked on the code and created the README file

4)Jeevan M-:Debugged the code and uploaded the code in GitHub

This solution stands out from other document management and processing applications due to several unique features and capabilities:

1. Integrated OCR Functionality
Tesseract Integration: The use of Tesseract for Optical Character Recognition (OCR) allows the application to convert images of text (like scanned invoices) into machine-readable text, making it more versatile for document management.
2. Natural Language Processing (NLP)
spaCy for Named Entity Recognition: By leveraging spaCy, the application can perform NLP tasks such as identifying and classifying entities within the text. This is particularly useful for extracting relevant information from documents.
3. Custom Document Classification
Machine Learning Classifier: The inclusion of a custom DocumentClassifier class utilizing Naive Bayes for classification allows users to train the model based on their specific documents and labels, which is tailored to their needs.
4. User Management with JWT
JWT Authentication: The implementation of JWT (JSON Web Tokens) for user verification adds a layer of security and scalability, allowing for secure session management and role-based access control.
5. Comprehensive API Design
RESTful API Endpoints: The application provides a rich set of RESTful API endpoints, covering document uploads, classification, NER, transaction management, budget tracking, and more, making it a full-fledged backend solution.
6. Dynamic Expense and Budget Tracking
Financial Management Features: It includes functionality for tracking expenses, setting budgets, and generating summaries, catering specifically to financial management needs, which is not commonly found in standard document management systems.
7. Data Persistence with SQLite
SQLite Integration: By using SQLite, the application provides a lightweight, serverless database solution for storing documents and user data, making it easy to deploy and manage without complex database setups.
8. Flexibility and Extensibility
Modular Design: The architecture is modular, allowing for easy extension and integration of additional features or third-party services in the future.
9. User-Friendly Error Handling
Clear Responses: The application includes thoughtful error handling and clear JSON responses, making it easier for developers to understand issues and debug the application.
10. Demo-Friendly
Built-in Dummy Data: It includes dummy data for transactions and account balances, which is helpful for demonstrating the application’s features without requiring user input or real data.

