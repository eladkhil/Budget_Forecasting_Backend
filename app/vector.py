from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import pandas as pd
import os

# Load budget forecast data (use the pre-processed forecast data)
df = pd.read_excel("prevision_budgets_detaillee.xlsx")

# Create embeddings with Ollama for budget forecasting data
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

# Define Chroma DB location and collection name
db_location = "./chroma_budget_db"
collection_name = "budget_forecasts"

# Check if DB already exists
add_documents = not os.path.exists(db_location)

# Only prepare documents on first run
if add_documents:
    documents = []
    for _, row in df.iterrows():
        text = f"""
        Year: {row['Année']}
        Direction: {row['Direction']}
        Rubrique: {row['Rubrique']}
        Groupement: {row['Groupement']}
        Investissement: {row['Investissement']}
        Fonctionnement: {row['Fonctionnement']}
        Services: {row['Services']}
        Formation: {row['Formation']}
        Consommation: {row['Consommation']}
        Écart: {row['Écart']}
        """
        doc = Document(page_content=text, metadata={"source": "forecast_data"})
        documents.append(doc)

# Create or load the vector store
vector_store = Chroma(
    collection_name=collection_name,
    persist_directory=db_location,
    embedding_function=embeddings
)

# Add documents to the DB if needed
if add_documents:
    vector_store.add_documents(documents=documents)
