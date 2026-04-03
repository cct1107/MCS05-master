Food Daily Project
==================

This project provides tools for food recognition, dataset processing, and search functionalities.  
It contains several modules grouped into the following directories:

- extract_data – data extraction utilities
- generate_answer – answer generation modules
- process_dataset – dataset preparation tools
- search_data – indexing and search functions
- scripts – main entry points to run the system

------------------------------------------------------------
Usage
------------------------------------------------------------

Running Queries:
    python scripts/query.py

Initialize Datasets (build index from scratch):
    python scripts/build_index.py

Add More Data to Index:
    python scripts/add_index.py

------------------------------------------------------------
Installation
------------------------------------------------------------

1. Create Virtual Environment:
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1

2. Install Required Packages:
    pip install sentence_transformers chromadb google-genai python-dotenv fastapi uvicorn pymupdf spacy nltk
    pip install torch torchvision pillow flask tqdm kaggle roboflow ultralytics
    pip install numpy==2.2.6 rank-bm25==0.2.2 opencv-python==4.12.0.88

3. Extra Setup:
    - Download NLTK stopwords:
        python -c "import nltk; nltk.download('stopwords')"

    - Download SpaCy model:
        python -m spacy download en_core_web_sm

------------------------------------------------------------
Running the Application
------------------------------------------------------------

Backend (FastAPI):
    uvicorn main:app --reload

Frontend:
    npm start

------------------------------------------------------------
Notes
------------------------------------------------------------

- Always activate the virtual environment before running:
    .\.venv\Scripts\Activate.ps1

- To deactivate:
    deactivate

------------------------------------------------------------
Common Commands Reference
------------------------------------------------------------

Reinstall packages if needed:
    .\.venv\Scripts\python.exe -m pip install --force-reinstall torch torchvision pillow flask tqdm kaggle roboflow spacy nltk

Install Ultralytics and Roboflow:
    .\.venv\Scripts\python.exe -m pip install -U ultralytics roboflow
