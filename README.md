# AI-Powered Selenium Test Generator

This tool leverages a local Large Language Model (LLM) to automatically generate Selenium browser tests from user stories written in a JSON format.

## Features

-   **JSON Parsing**: Reads user stories, epics, and acceptance criteria from a `data.json` file.
-   **AI-Powered Test Generation**: Uses a local LLM (via Ollama) to interpret user stories and generate concrete test steps.
-   **Selenium Code Generation**: Creates Python-based Selenium test scripts using `pytest` for structure and execution.
-   **Modular Architecture**: The code is organized into distinct modules for clarity and maintainability.

## Architecture

The tool is built with a simple, modular architecture:

1.  **`json_reader.py`**: Parses the input `data.json` file to extract user stories.
2.  **`ai_processor.py`**: Connects to the Ollama LLM to convert stories into a structured list of test steps.
3.  **`code_generator.py`**: Transforms the structured test steps into executable Python/Selenium code.
4.  **`output_writer.py`**: Saves the generated test code into `.py` files in the `tests/` directory.
5.  **`main.py`**: The main script that orchestrates the entire process.

## Stack

-   **Python**: Core programming language.
-   **Ollama**: For running the local LLM (`llama3.2` is the default).
-   **LangChain**: To manage prompts and interactions with the LLM.
-   **Selenium**: For the generated browser automation test code.
-   **pytest**: As the framework for the generated test cases.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install Ollama:**
    Follow the instructions at [https://ollama.ai/](https://ollama.ai/) to install and start the Ollama server.

3.  **Pull the LLM model:**
    This project is configured to use `llama3.2`. Pull it from Ollama:
    ```bash
    ollama pull llama3.2
    ```

4.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Define User Stories:**
    Add your user stories to the `data.json` file, following the existing structure.

2.  **Run the Test Generation Script:**
    Execute the main script from the root directory:
    ```bash
    python -m src.main
    ```

3.  **Find Generated Tests:**
    The generated test files will be saved in the `tests/` directory.

4.  **Execute the Tests:**
    Run the generated tests using `pytest`:
    ```bash
    pytest tests/
    ```
    *Note: You will need a WebDriver (like `chromedriver`) installed and in your system's PATH for Selenium to run the tests.*

## Generated Tests

The output is a series of Python files in the `tests` directory, each corresponding to a user story. For example, a story with the title "User Login/Logout" will generate a file named `tests/test_user_login_logout.py`. 