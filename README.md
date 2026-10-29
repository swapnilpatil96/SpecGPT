# SpecGPT



**A GenAI-powered assistant for answering questions from functional specification documents.**



SpecGPT is a Python-based prototype that uses semantic search and a Large Language Model (LLM) to retrieve relevant passages from a specification document and generate context-grounded answers.



The goal is to make functional specifications easier to explore by allowing users to ask questions in natural language rather than manually searching through lengthy documents.



## Features



- **DOCX document extraction** — extracts paragraphs and tables while preserving their document order.

- **Document metadata extraction** — captures metadata such as document ID, version, status, and domain.

- **Heading-based chunking** — organizes specification content into meaningful chunks with section metadata.

- **Semantic retrieval** — uses sentence embeddings and cosine similarity to find relevant content.

- **Context-grounded answers** — uses the OpenAI API to generate answers based on retrieved specification passages.

- **Source traceability** — returns the retrieved passages and their section metadata alongside the answer.

- **Automated tests** — includes tests for chunk creation and retrieval behavior.



## How It Works



1. Load a DOCX functional specification.

2. Extract document content and metadata.

3. Divide the content into heading-based chunks.

4. Generate vector embeddings for the chunks.

5. Convert a user's question into an embedding and retrieve relevant chunks.

6. Build a context from the retrieved passages.

7. Send the question and context to an LLM to generate an answer.

8. Return the answer and supporting source chunks.



## Technology Stack



- Python 3.12+

- python-docx

- Sentence Transformers (`all-MiniLM-L6-v2`)

- scikit-learn

- OpenAI Python SDK

- python-dotenv

- pytest



## Project Structure



```text

SpecGPT/

├── notebooks/

│   ├── 01_environment_check.ipynb

│   └── 02_document_extraction.ipynb

├── src/

│   └── specgpt/

│       ├── __init__.py

│       ├── document_loader.py

│       ├── chunker.py

│       ├── embeddings.py

│       ├── retriever.py

│       ├── context_builder.py

│       ├── generator.py

│       └── pipeline.py

├── tests/

│   ├── test_chunker.py

│   └── test_retriever.py

├── data/

│   ├── raw/

│   └── processed/

├── .env.example

├── .gitignore

├── pyproject.toml

├── requirements.txt

└── README.md

```



## Setup



### 1. Clone the repository



```bash

git clone https://github.com/swapnilpatil96/SpecGPT.git

cd SpecGPT

```



### 2. Create and activate a Conda environment



```bash

conda create -n specgpt python=3.12 -y

conda activate specgpt

```



### 3. Install dependencies



```bash

python -m pip install -r requirements.txt

python -m pip install -e .

python -m pip install pytest

```



### 4. Configure the OpenAI API key



Create a `.env` file in the project root:



```text

OPENAI_API_KEY=your_api_key_here

```



Replace the placeholder with your own API key. Never commit `.env` or share your API key publicly.



### 5. Add a specification document



Place a DOCX functional specification that you are authorized to use in:



```text

data/raw/

```



The example document used during development is not included in the repository.



## Running the Prototype



Open Jupyter Notebook from the project environment:



```bash

jupyter notebook

```



Open `notebooks/02_document_extraction.ipynb` to explore document extraction, chunking, embeddings, semantic retrieval, context construction, and answer generation.



The reusable pipeline is available through:



- `prepare_document()` — loads and prepares a specification for retrieval.

- `ask_question()` — retrieves relevant passages and generates an answer with supporting sources.



Example usage:



```python

from pathlib import Path

from dotenv import load_dotenv

from openai import OpenAI

from specgpt.pipeline import prepare_document, ask_question



load_dotenv()



client = OpenAI()



document_path = Path("data/raw/your_specification.docx")

prepared_document = prepare_document(document_path)



result = ask_question(

&#x20;   query="What are the key business rules?",

&#x20;   prepared_document=prepared_document,

&#x20;   client=client,

)



print(result["answer"])



for source in result["sources"]:

&#x20;   chunk = source["chunk"]

&#x20;   print(chunk.metadata)

```



Run this example from the project root. The question is illustrative; answer quality depends on the document and retrieved context.



## Running Tests



Run the automated tests from the project root:



```bash

python -m pytest tests/ -v

```



The current tests cover chunk creation, metadata preservation, retrieval ranking, and validation of mismatched chunk and embedding counts.



## Current Limitations



This is an early-stage prototype.



- DOCX is the currently supported input format.

- Retrieval uses in-memory embeddings; a persistent vector database is not implemented.

- There is no web interface or deployed API yet.

- Retrieval quality depends on chunk boundaries and semantic similarity.

- Answers are grounded in retrieved context but should still be checked against the original specification.

- Automated evaluation of answer accuracy and retrieval quality is still needed.

- OpenAI API usage may incur charges.



## Roadmap



- Improve retrieval quality and evaluate answer grounding.

- Expand automated tests and add a repeatable evaluation dataset.

- Improve configuration and error handling.

- Add document-level and source-level validation.

- Explore an API or user interface for interactive specification analysis.



## Security



- Keep API keys in environment variables or `.env`.

- Do not commit secrets or confidential specifications.

- Use only documents you are authorized to process or share.



## Status



**Phase 1 — Prototype and reusable Python pipeline.**



This project is being developed as a learning and engineering project focused on GenAI, semantic retrieval, and grounded question answering over functional specifications.