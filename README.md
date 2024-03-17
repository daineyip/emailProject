# Project Structure

This project is organized into several directories, each with a specific role in the application's architecture: \

emailProject/
│
├── app/                      # Application source files
│   ├── __init__.py           # Initializes Python package
│   ├── emailListener.py      # Module to scrape emails for 2FA codes
│   ├── emailHandler.py       # Module to forward 2FA codes to the iPhone messaging service
│   ├── messageForwarder.py   # Module to forward 2FA codes to the iPhone messaging service
│   └── utils.py              # Utility functions used across the project
│
├── tests/                    
│   ├── __init__.py
│   ├── test_emailListener.py
|   ├── test_emailHandler.py
│   └── test_messageForwarder.py
│
├── venv/                     # Virtual environment (exclude from version control)
│
├── .gitignore                # Specifies intentionally untracked files to ignore
├── requirements.txt          # Fixed versions of all the dependencies
├── setup.py                  # Setup script for installing the project
├── README.md                 # Overview of the project, installation instructions, etc.
├── LICENSE                   # License for the project
└── config.ini                # Configuration file (optional, could be .yaml or .json as well)

# Api Request Flow
**Initialization**: The application starts, initializing the emailListener component. This module begins monitoring the inbox for new emails, acting as the primary point of entry for the email processing workflow.
**Email Detection**: The emailListener continuously checks for new emails. Once it detects an email containing a 2FA code, it retrieves the email content and forwards it to the emailHandler.
**Email Processing**: The emailHandler takes over, parsing the received email content to extract the 2FA code. It's responsible for interpreting the email's data, ensuring the 2FA code is correctly identified amidst the email content.
**Forwarding 2FA Code**: After extracting the 2FA code, the emailHandler passes it to the messageForwarder. This component is tasked with the crucial role of securely transmitting the 2FA code to the user's phone, likely through an SMS or messaging service API.
**Completion**: The messageForwarder ensures that the 2FA code is delivered to the intended recipient's phone. Upon successful forwarding, the process concludes, and the system awaits the next email or can shut down if it's a one-time operation.
