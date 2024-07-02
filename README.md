# Hospital System Chatbot

A simple RAG chatbot designed to assist stakeholders to access and query their hospital data without needing technical expertise. This tool greatly improved data visibility and decision-making efficiency.

## Description
This chatbot is built using Python and utilizes machine learning techniques to understand and respond to user inputs.

## Built With

- [Python](https://www.python.org/)
- [LangChain](https://www.langchain.com/)
- [Cohere API](https://cohere.ai) - Natural language processing
- [Neo4j](https://neo4j.com) - Graph database

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Freemanlabs/hospital-system-chatbot.git
    cd hospital-system-chatbot
    ```

2. **Set up a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
    For windows users, replace the `source venv/bin/activate` with `venv\Scripts\activate` to activate the environment.

3. **Install the necessary dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**
    Create a `.env` file in the project root and add the necessary configuration details (e.g., API keys, database URLs). An example of what is requires is shown in the `dotenv` file

    1. **Get a Cohere API Key:**
        - Sign up at [Cohere](https://cohere.ai).
        - Navigate to the API Keys section of your account.
        - Copy your API key.

    2. **Set up a Neo4j account:**
        - Sign up at [Neo4j](https://neo4j.com/cloud/aura-free/).
        - Click the Start Free button and create an account. 
        - Click New Instance and create a free instance.
        - Open the text file you downloaded with your Neo4j credentials and copy the NEO4J_URI, NEO4J_USERNAME, and NEO4J_PASSWORD

    3. **Add the following to your `.env` file:**

    ```plaintext
    COHERE_API_KEY=your-cohere-api-key
    NEO4J_URI=your-neo4j-uri
    NEO4J_USERNAME=your-neo4j-username
    NEO4J_PASSWORD=your-neo4j-password
    ```
5. **Populate the Neo4j database:**

    Run the following script to populate the Neo4j database with the required data:

    ```bash
    python neo4j_etl/hospital_bulk_csv_write.py
    ``
    `
## Usage

Here are some examples of how to use the chatbot:

1. **Running the chatbot locally:**

    The below script contains 3 examples to verify the output from 3 different agane tools. Feel free to use any query example you want

    ```bash
    python run.py
    ```

## Configuration

To customize the chatbot, modify the `config.toml` configuration file. You can adjust settings such as data paths, LLM model type, and more.