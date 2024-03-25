# Project Structure

This project is organized into several directories, each with a specific role in the application's architecture: 

emailProject/ \
|-- app/ (Application Source Files) \
|   &#x3000;-- __init__.py \
|   &#x3000;-- emailListener.py     
|   &#x3000;-- emailHandler.py    
|   &#x3000;-- messageForwarder.py \
|   &#x3000;-- utils.py   
|-- tests/ \
|   &#x3000;-- __init__.py \
|   &#x3000;-- test_emailListener.py \
|   &#x3000;-- test_emailHandler.py \
|   &#x3000;-- test_messageForwarder.py \
|-- venv/ \
-- .gitignore \
-- requirements.txt \
-- setup.py \
-- README.md \
-- LICENSE \
.

# API Request Flow
**Initialization**: The application starts, initializing the emailListener component. This module begins monitoring the inbox for new emails, acting as the primary point of entry for the email processing workflow. \
**Email Detection**: The emailListener continuously checks for new emails. Once it detects an email containing a 2FA code, it retrieves the email content and forwards it to the emailHandler. \
**Email Processing**: The emailHandler takes over, parsing the received email content to extract the 2FA code. It's responsible for interpreting the email's data, ensuring the 2FA code is correctly identified amidst the email content. \
**Forwarding 2FA Code**: After extracting the 2FA code, the emailHandler passes it to the messageForwarder. This component is tasked with the crucial role of securely transmitting the 2FA code to the user's phone, likely through an SMS or messaging service API. \
**Completion**: The messageForwarder ensures that the 2FA code is delivered to the intended recipient's phone. Upon successful forwarding, the process concludes, and the system awaits the next email or can shut down if it's a one-time operation.

# Running Application
1. If you haven't already setup the Python Virtual Environment. Run ```python3 -m venv venv```
2. Run ```source venv/bin/activate``` to activate the virtual environment
3. Run the main program with ```python3 app/emailListener.py```
