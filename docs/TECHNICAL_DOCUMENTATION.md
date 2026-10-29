# Universal SpecGPT — Technical Documentation



## 1. Project Overview



### 1.1 Purpose



Universal SpecGPT is a Generative AI prototype designed to help users understand functional specification documents by asking questions in natural language.



Instead of manually searching through lengthy documents, users can ask a question and receive an answer generated using relevant passages retrieved from the specification.



The project uses semantic search and a Large Language Model (LLM) to produce context-grounded answers and return supporting source chunks for traceability.



### 1.2 Problem Statement



Functional specification documents describe system behavior, business rules, workflows, actors, and validation requirements. Finding a specific requirement can require manually navigating multiple sections and interpreting technical terminology.



Universal SpecGPT aims to simplify this process by providing a question-answering workflow over specification documents.



### 1.3 Project Scope



The current prototype implements the following capabilities:



\- Load Microsoft Word `.docx` specification documents.

\- Extract paragraphs and tables in document order.

\- Extract document-level metadata where supported by the document structure.

\- Organize content into chunks based on document headings.

\- Generate semantic embeddings for document chunks.

\- Retrieve relevant chunks using cosine similarity.

\- Construct an LLM prompt using retrieved content.

\- Generate an answer using the OpenAI API.

\- Return the answer and supporting source chunks with their metadata.



### 1.4 Intended Use



The project is intended to help developers, business analysts, testers, and other project stakeholders explore functional requirements more efficiently.



The current implementation is a prototype. Generated answers should be verified against the original specification, especially when interpreting important business rules.



### 1.5 Technology Stack



| Component | Technology |

|---|---|

| Programming language | Python 3.12 |

| Document processing | python-docx |

| Embedding model | Sentence Transformers — `all-MiniLM-L6-v2` |

| Similarity calculation | scikit-learn cosine similarity |

| LLM integration | OpenAI Python SDK |

| Configuration | python-dotenv |

| Automated testing | pytest |

| Development environment | Conda and Jupyter Notebook |

| Source control | Git and GitHub |



### 1.6 Current Limitations



The current prototype has the following limitations:



\- Microsoft Word `.docx` is the supported input format.

\- Document chunks and embeddings are held in memory.

\- A persistent vector database has not been implemented.

\- No web user interface or deployed API is included.

\- Retrieval and answer quality have not yet undergone systematic evaluation.

\- The prototype has a limited automated test suite.



These limitations define the current implementation and provide direction for future development.



## 2. System Architecture



### 2.1 Architectural Overview



Universal SpecGPT follows a Retrieval-Augmented Generation (RAG) architecture. It retrieves relevant content from a functional specification and supplies that content to an LLM to generate an answer.



The implementation separates document processing, embedding generation, retrieval, context construction, and answer generation into reusable Python modules.



### 2.2 Main Components



| Component | Module | Responsibility |

|---|---|---|

| Document loader | `document\_loader.py` | Loads DOCX documents and extracts paragraphs and tables. |

| Chunking and metadata | `chunker.py` | Extracts document metadata, associates content with headings, and creates chunks. |

| Embedding generation | `embeddings.py` | Loads the embedding model and generates vectors for document chunks. |

| Semantic retrieval | `retriever.py` | Embeds a question and ranks document chunks using cosine similarity. |

| Context construction | `context\_builder.py` | Formats retrieved chunks and source metadata for the LLM prompt. |

| Answer generation | `generator.py` | Calls the OpenAI API to generate a context-grounded answer. |

| Pipeline orchestration | `pipeline.py` | Connects document preparation and question answering into reusable functions. |



### 2.3 End-to-End Workflow



The application has two main operations: document preparation and question answering.



\*\*Document preparation\*\*



1\. Load the specification document.

2\. Extract paragraphs and tables in their original order.

3\. Extract document-level metadata.

4\. Associate document content with section and subsection headings.

5\. Create heading-based document chunks.

6\. Load the sentence embedding model.

7\. Generate an embedding vector for each chunk.

8\. Retain the chunks, metadata



## 3. Python Module Design



### 3.1 Package Structure



The application code is located in `src/specgpt/`. Each module has a focused responsibility, allowing the document-processing and question-answering stages to be maintained and tested independently.



The package contains the following files:



\- `\_\_init\_\_.py`

\- `document\_loader.py`

\- `chunker.py`

\- `embeddings.py`

\- `retriever.py`

\- `context\_builder.py`

\- `generator.py`

\- `pipeline.py`



### 3.2 `document\_loader.py`



\*\*Purpose:\*\* Load a DOCX file and extract its content in document order.



The module uses `python-docx` to access paragraphs and tables. Its main functions are:



\- `iter\_block\_items(parent)` — iterates through paragraph and table elements in their original order.

\- `extract\_blocks(document)` — converts paragraphs and tables into structured dictionaries.

\- `load\_document(file\_path)` — validates the supplied path and file extension, opens the DOCX document, and returns the extracted blocks.



Paragraph blocks contain their text and paragraph style. Table blocks contain their rows and basic structural metadata, including row and column counts.



The loader raises a `FileNotFoundError` if the document does not exist and a `ValueError` if the file extension is not `.docx`.



### 3.3 `chunker.py`



\*\*Purpose:\*\* Extract document metadata and divide specification content into meaningful chunks.



The module defines the `DocumentChunk` dataclass, which stores chunk text and a metadata dictionary.



Its main functions are:



\- `add\_section\_context(blocks)` — associates paragraph blocks with the current section and subsection headings.

\- `extract\_document\_metadata(blocks)` — extracts metadata from a table whose headers are `Document Item` and `Value`.

\- `create\_chunks(blocks, document\_metadata)` — creates chunks based on heading boundaries and attaches document and section metadata.



Each chunk can contain the document ID, document version, source filename, section, and subsection.



Heading-based chunking preserves the specification's structural organization and makes retrieved passages easier to trace back to their source sections.



### 3.4 `embeddings.py`



\*\*Purpose:\*\* Convert document text into numerical vector representations for semantic retrieval.



The module uses Sentence Transformers with the default model `all-MiniLM-L6-v2`.



Its functions are:



\- `load\_embedding\_model(model\_name)` — loads the requested sentence embedding model.

\- `embed\_texts(model, texts)` — generates embeddings for a list of text strings.

\- `embed\_chunks(model, chunks)` — generates one embedding vector for each document chunk.



In the prototype, the embedding model produces vectors with 384 dimensions. Embeddings are retained in memory for retrieval.



### 3.5 `retriever.py`



\*\*Purpose:\*\* Find the document chunks most relevant to a user's question.



The `retrieve\_chunks()` function:



1\. Validates that the query is not empty.

2\. Checks that the number of chunks matches the number of chunk embeddings.

3\. Generates an embedding for the query.

4\. Calculates cosine similarity between the query vector and chunk vectors.

5\. Sorts the similarity scores in descending order.

6\. Returns the highest-ranked chunks with their scores.



The `top\_k` parameter controls how many results are returned. Its default value is five.



The similarity score measures vector similarity; it is not a guarantee that a passage fully answers the question.



### 3.6 `context\_builder.py`



\*\*Purpose:\*\* Format retrieved chunks into context that can be supplied to the LLM.



The `build\_context(results)` function combines the retrieved content with source information, including:



\- Source rank

\- Document ID and version

\- Source filename

\- Section and subsection

\- Similarity score

\- Chunk content



This formatted context helps the LLM use relevant specification passages and makes the supporting source information available for inspection.



### 3.7 `generator.py`



\*\*Purpose:\*\* Generate an answer using the OpenAI API and the retrieved specification context.



The `generate\_answer()` function accepts a client, a question, and a context string.



It constructs system and user prompts, then sends a chat completion request to the configured model. The default model is `gpt-4o-mini`, and the request uses a temperature of zero.



The system prompt instructs the assistant to:



\- Answer using only the supplied specification context.

\- Avoid inventing requirements or business rules.

\- State when the context is insufficient to answer.

\- Mention the relevant section or subsection when possible.



The function returns the generated answer text. The prompt instructions encourage grounded answers but do not guarantee that every generated claim is correct.



### 3.8 `pipeline.py`



\*\*Purpose:\*\* Coordinate document preparation and question answering through reusable functions.



The module exposes two main functions.



\*\*`prepare\_document(file\_path, embedding\_model=None)`\*\*



This function loads the document, extracts document metadata, adds section context, records the source filename, creates chunks, loads an embedding model when one is not supplied, and generates chunk embeddings.



It returns a dictionary containing:



\- `document\_metadata`

\- `chunks`

\- `embedding\_model`

\- `chunk\_embeddings`



\*\*`ask\_question(query, prepared\_document, client, top\_k=5)`\*\*



This function retrieves relevant chunks, builds the LLM context, generates an answer, and returns a dictionary containing:



\- `question`

\- `answer`

\- `sources`



Each source result contains a similarity score and its corresponding chunk.



Separating preparation from question answering allows the same prepared document and embeddings to be reused for multiple questions during the same running process.



### 3.9 `\_\_init\_\_.py`



This file marks `specgpt` as a Python package. The project is configured in `pyproject.toml` to discover packages under the `src` directory.



### 3.10 Module Dependencies



The main processing dependencies are:



`document\_loader.py` → `chunker.py` → `embeddings.py` → `retriever.py` → `context\_builder.py` → `generator.py`



`pipeline.py` orchestrates these modules rather than implementing a separate version of each processing step.



## 4. Pipeline Usage and Example



### 4.1 Overview



SpecGPT provides a reusable pipeline for preparing a functional specification document and answering questions using retrieved document content.



The main workflow is implemented in `src/specgpt/pipeline.py` through two functions:



\- `prepare\_document()` — loads the document, extracts metadata, creates structured chunks, loads the embedding model, and generates chunk embeddings.

\- `ask\_question()` — retrieves relevant chunks for a user query, builds the context, generates an answer using the OpenAI API, and returns the answer with its source chunks.



### 4.2 Prerequisites



Before running the pipeline, ensure that:



\- The SpecGPT project dependencies are installed.

\- An OpenAI API key is configured in the project’s `.env` file.

\- A supported `.docx` functional specification is available locally.

\- The Python environment is activated and the project is installed or its `src` directory is available for imports.



The API key must remain private and must never be committed to source control.



### 4.3 Example Usage



The following example demonstrates how to prepare a document and ask a question.



Run this example from the project root directory, using the configured Python environment.



```python

from dotenv import load\_dotenv

from openai import OpenAI



from specgpt.pipeline import prepare\_document, ask\_question



# Load environment variables from the project root.

load\_dotenv()



# Initialize the OpenAI client using OPENAI\_API\_KEY.

client = OpenAI()



# Replace this path with the location of your own DOCX file.

file\_path = "data/raw/your\_specification.docx"



# Prepare the specification for semantic retrieval.

prepared\_document = prepare\_document(file\_path)



# Ask a question about the specification.

result = ask\_question(

&#x20;   query="What are the rules for registering an animal?",

&#x20;   prepared\_document=prepared\_document,

&#x20;   client=client,

)



# Display the answer.

print("Question:", result\["question"])

print("Answer:", result\["answer"])



# Display the retrieved source sections.

print("\\nRetrieved sources:")

for source in result\["sources"]:

&#x20;   chunk = source\["chunk"]

&#x20;   print(

&#x20;       f"Section: {chunk.metadata.get('section')} | "

&#x20;       f"Subsection: {chunk.metadata.get('subsection')} | "

&#x20;       f"Similarity: {source\['score']:.4f}"

&#x20;   )

```



The example uses a placeholder file path. Replace it with the path to an actual DOCX specification. The `.env` file must contain a valid `OPENAI\_API\_KEY`.



### 4.4 Pipeline Output



The `ask\_question()` function returns a dictionary containing:



| Field | Description |

|---|---|

| `question` | The original user question. |

| `answer` | The answer generated by the language model using the retrieved context. |

| `sources` | The ranked document chunks retrieved for the question, including similarity scores and metadata. |



Each source entry contains a `score` and a `chunk`. The chunk includes its text and metadata, such as document ID, version, source filename, section, and subsection.



### 4.5 Answer Grounding



The generator is instructed to answer using only the retrieved specification context and not to invent requirements or business rules. If the available context is insufficient, it is instructed to state that the specification does not provide enough information.



The returned source chunks help developers inspect which document content was supplied to the language model. However, the current implementation does not guarantee that every generated statement is correct or fully supported. Retrieval quality and answer grounding require further evaluation as the project evolves.



### 4.6 Current Implementation Considerations



\- The document loader currently supports DOCX files.

\- The embedding model defaults to `all-MiniLM-L6-v2`.

\- Semantic retrieval uses cosine similarity and returns up to five chunks by default.

\- Answer generation defaults to `gpt-4o-mini`.

\- Document embeddings are prepared in memory for the current workflow.

\- Persistent vector storage, a web interface, and production deployment are outside the current prototype scope.



## 5. Notebook Walkthrough



The project includes Jupyter notebooks for validating the development environment and exploring the document-processing workflow.



### 5.1 Environment Check



\*\*Notebook:\*\* `notebooks/01\_environment\_check.ipynb`



This notebook is used to verify the Python environment and check whether the required libraries are available.



It provides an initial validation step before running the SpecGPT document-processing pipeline.



### 5.2 Document Extraction and Processing



\*\*Notebook:\*\* `notebooks/02\_document\_extraction.ipynb`



This notebook demonstrates the document-processing workflow using a functional specification in DOCX format.



The workflow includes:



1\. Loading a specification document.

2\. Extracting paragraphs and tables while preserving their document order.

3\. Inspecting extracted content and document metadata.

4\. Adding section and subsection context.

5\. Creating structured document chunks.

6\. Generating embeddings for the chunks.

7\. Exploring semantic retrieval for user queries.



The notebook supports interactive experimentation and helps developers understand how the individual stages work.



### 5.3 Notebooks and Source Code



The notebooks are intended for exploration and validation. The reusable implementation is maintained in `src/specgpt/`.



The main application workflow is implemented through `prepare\_document()` and `ask\_question()` in `src/specgpt/pipeline.py`. These functions allow the processing logic to be reused outside Jupyter notebooks.



### 5.4 Handling Notebook Outputs and Test Data



Before publishing the repository, ensure notebook outputs do not contain API keys, confidential information, or proprietary specification content.



Sample specification documents are local test data. They should only be published if their distribution is explicitly authorized.



## 6. Installation and Setup



This section describes how to configure the local development environment and run the SpecGPT prototype.



### 6.1 Prerequisites



Ensure the following are available:



\- Windows or another compatible Python development environment.

\- Anaconda or Miniconda.

\- Python 3.12.

\- Git.

\- An OpenAI API key with API access and available billing.

\- Internet access for installing dependencies, downloading the embedding model, and calling the OpenAI API.



### 6.2 Clone the Repository



Clone the repository and navigate to the project directory.



```bash

git clone https://github.com/swapnilpatil96/SpecGPT.git

cd SpecGPT

```



If the repository is private, GitHub authentication and repository access are required.



### 6.3 Create and Activate the Python Environment



Create a dedicated Conda environment:



```bash

conda create -n specgpt python=3.12

conda activate specgpt

```



### 6.4 Install Dependencies



Install the project dependencies:



```bash

python -m pip install -r requirements.txt

python -m pip install -e .

```



The requirements file includes the libraries used for document extraction, embeddings, semantic retrieval, and OpenAI API integration.



### 6.5 Configure Environment Variables



Create a `.env` file in the project root directory.



Add the following entry, replacing the placeholder with your own API key:



```text

OPENAI\_API\_KEY=your\_openai\_api\_key

```



Do not commit the `.env` file to Git. The repository's `.gitignore` should exclude it from version control.



### 6.6 Prepare a Specification Document



Place an authorized DOCX specification in the local `data/raw/` directory, or use another valid local file path.



The document loader currently supports `.docx` files. The prototype extracts paragraphs and tables and prepares structured chunks for semantic retrieval.



Do not use confidential or proprietary documents unless you are authorized to process them with the selected services.



### 6.7 Run the Prototype



From the project root, activate the Conda environment and run the Python example described in Section 4.



The first execution may download the sentence-transformer embedding model. The pipeline then prepares the document, generates embeddings, retrieves relevant chunks for the question, and calls the OpenAI API to generate an answer.



### 6.8 Run Automated Tests



Run the project tests from the root directory:



```bash

python -m pytest

```



The tests validate the implemented functionality covered by the current test suite. Passing tests do not guarantee the correctness of every generated answer or the suitability of the prototype for production use.



### 6.9 Troubleshooting Notes



\- \*\*Import errors:\*\* Confirm the `specgpt` Conda environment is active and the project has been installed in editable mode.

\- \*\*Missing API key:\*\* Verify that `.env` exists in the project root and that `OPENAI\_API\_KEY` is configured correctly.

\- \*\*OpenAI API errors:\*\* Check API credentials, API access, billing, and model availability.

\- \*\*Embedding model download errors:\*\* Check network connectivity and access to the model repository.

\- \*\*Missing document:\*\* Verify that the DOCX file path exists and points to a supported file.



## 7. Limitations and Future Enhancements



### 7.1 Current Limitations



The current implementation is a proof of concept intended to demonstrate document-based question answering using Retrieval-Augmented Generation (RAG).



Current limitations include:



\- \*\*Document format:\*\* Only DOCX files are supported by the document loader.

\- \*\*Retrieval quality:\*\* Semantic similarity retrieval may not always identify every relevant requirement or business rule.

\- \*\*Chunking strategy:\*\* Chunks are created using document headings and subsections. More advanced chunking strategies may be needed for complex specifications.

\- \*\*In-memory processing:\*\* Document chunks and embeddings are held in memory during the current workflow.

\- \*\*Source traceability:\*\* Retrieved chunks include section metadata, but the prototype does not yet provide precise page-level citations.

\- \*\*Answer verification:\*\* Answers are generated using retrieved context, but there is no independent verification mechanism to guarantee correctness.

\- \*\*Application interface:\*\* The current workflow is exposed through Python modules and Jupyter notebooks rather than a dedicated user interface.

\- \*\*Testing coverage:\*\* The current automated tests cover selected functionality; broader evaluation is needed for retrieval relevance and answer quality.

\- \*\*Production readiness:\*\* Authentication, authorization, multi-user support, monitoring, deployment, and production-grade data controls are outside the current implementation scope.



### 7.2 Planned Enhancements



Potential future enhancements include:



1\. \*\*Additional document formats:\*\* Support PDF and other commonly used specification formats.

2\. \*\*Improved retrieval:\*\* Evaluate hybrid search, metadata filtering, reranking, and more advanced chunking strategies.

3\. \*\*Persistent vector storage:\*\* Store document embeddings in a vector database to support larger document collections.

4\. \*\*Precise source citations:\*\* Provide section-level and, where feasible, page-level references for generated answers.

5\. \*\*Document management:\*\* Support uploading, replacing, versioning, and managing multiple specification documents.

6\. \*\*Evaluation framework:\*\* Create a representative question-and-answer dataset to measure retrieval relevance and answer grounding.

7\. \*\*User interface:\*\* Develop a web interface for uploading documents and asking questions.

8\. \*\*Security and access control:\*\* Introduce appropriate authentication, authorization, and data-isolation controls for multi-user usage.

9\. \*\*Observability:\*\* Add structured logging, error handling, usage tracking, and performance monitoring.

10\. \*\*Deployment:\*\* Package and deploy the application in a suitable cloud environment after security and reliability requirements are addressed.



These enhancements are potential directions rather than implemented capabilities. They should be prioritized based on evaluation results and intended use cases.



### 7.3 Conclusion



SpecGPT demonstrates a reusable approach to answering questions from functional specification documents. It combines document extraction, structured chunking, embedding generation, semantic retrieval, context construction, and LLM-based answer generation.



The current prototype establishes a foundation for further experimentation and development toward a more general-purpose specification assistant.
