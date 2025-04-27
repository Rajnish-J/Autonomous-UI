# 🤖 Browser Automation Agent

This project automates browser tasks using Anchor Browser sessions and integrates with Google's Generative AI (`gemini-2.0-flash-exp`) for advanced task execution. The application is modularized for better maintainability and scalability.

## 📋 Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Project Structure](#project-structure)
7. [Contributing](#contributing)
8. [License](#license)


## 🌟 Overview

The Browser Automation Agent creates an Anchor Browser session, performs predefined tasks (e.g., navigating to Google and searching for AI tools), updates an HTML file with the session ID, logs all activities, and closes the session upon completion. This modular design ensures clean separation of concerns and easy extensibility.

## ✨ Features

- **Anchor Browser Integration**: Create and manage browser sessions via the Anchor API.
- **Browser Automation**: Automate tasks using Chrome DevTools Protocol (CDP).
- **AI-Powered Tasks**: Leverage Google's Generative AI for advanced automation logic.
- **Dynamic HTML Updates**: Update the `index.html` file with the latest session ID.
- **Logging**: Maintain detailed logs of all operations for debugging and auditing.
- **Modular Design**: Organized into reusable modules for better maintainability.

## ⚙️ Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.8 or higher
- Pip (Python package manager)
- Git (optional, for version control)

Additionally, you need the following API keys:
- **Google API Key** (for Generative AI integration)
- **Anchor API Key** (for browser session management)

## 🛠 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/browser-automation-agent.git
cd browser-automation-agent
```

### Step 2: Set Up a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

Install the required packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the root directory and add your API keys:

```plaintext
GOOGLE_API_KEY=your_google_api_key_here
ANCHOR_API_KEY=your_anchor_api_key_here
```

## 🚀 Usage

Run the application using the following command:

```bash
python main.py
```

### What Happens Next?

1. **Session Creation**: A new Anchor Browser session is created.
2. **HTML Update**: The `index.html` file is updated with the session ID.
3. **Automation Task**: The browser navigates to Google and performs a search for "AI tools."
4. **Session Closure**: The Anchor Browser session is closed after the task is complete.
5. **Logs**: All activities are logged in `execution_logs.txt`.

## 📂 Project Structure

```
browser-automation-agent/
│
├── .env                  # Environment variables (API keys)
├── index.html            # HTML file updated with session ID
├── main.py               # Entry point for the application
├── requirements.txt      # List of dependencies
├── README.md             # Project documentation
├── execution_logs.txt    # Logs generated during execution
└── Agent/                # Modularized codebase
    ├── anchor.py         # Handles Anchor session creation and closure
    ├── automation.py     # Contains browser automation logic
    ├── html_updater.py   # Updates the HTML file with the latest session ID
    ├── logging.py        # Manages logging functionality
    └── __init__.py       # Makes the Agent directory a Python package
```
