# Bank AI Assistant

This project is a smart banking assistant for  (Commercial International Bank) built with Python, LangChain, Streamlit, and a local vector database for retrieval-augmented generation (RAG).

## Overview

The system can:

- answer banking questions using the knowledge base
- explain products and services
- calculate estimated loan installments
- estimate certificate returns
- help trigger card freeze emergency actions
- provide an Arabic/English conversational banking experience

## Project Structure

- `app.py` — Streamlit web app for the chatbot interface
- `src/agent.py` — banking agent and LLM orchestration
- `src/rag.py` — vector store setup and retriever logic
- `src/tools.py` — custom banking tools
- `data/knowledge.txt` — source knowledge data
- `vector_db/` — local Chroma database
- `requirements.txt` — Python dependencies

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your API key:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

4. Build the vector database:
   ```bash
   python -m src.rag
   ```

## Run the app

Start the Streamlit interface:

```bash
streamlit run app.py
```

## Example usage

The assistant can help with questions like:

- What is the premium certificate?
- How much is the monthly installment for a personal loan?
- How do I freeze my card?
- What are banking services and terms?

## Notes

- This is a demo assistant for informational and basic banking support purposes.
- It does not replace official bank procedures or customer support.
- Sensitive data such as PIN or CVV should never be shared with the AI agent.

## Technology Stack

- Python
- Streamlit
- LangChain
- LangGraph
- Google Generative AI
- Chroma vector database

## License

This project is for educational and prototype use.
