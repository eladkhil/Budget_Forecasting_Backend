from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.embeddings import OllamaEmbeddings
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Load the Ollama LLM (using a model suitable for forecasting and question-answering)
llm = OllamaLLM(model="llama3.2")

# Define the prompt template for budget forecasting
template = """
You are a helpful financial assistant.

Here are some relevant past budget forecasting data:
{forecast_data}

Now, answer the following question about budget forecasting:
{question}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | llm

# Initialize vector store (for past budget forecasts)
db_location = "./chroma_budget_db"
collection_name = "budget_forecasts"

# Load budget forecasting data (if available)
df = pd.read_excel("prevision_budgets_detaillee.xlsx")

# Prepare documents from the forecast data for the vector store
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
    doc = Document(page_content=text, metadata={"source": "budget_forecast"})
    documents.append(doc)

# Create or load the vector store
vector_store = Chroma(
    collection_name=collection_name,
    persist_directory=db_location,
    embedding_function=OllamaEmbeddings(model="mxbai-embed-large")
)

# Add documents to the vector store if needed
if not os.path.exists(db_location):
    vector_store.add_documents(documents=documents)

# Expose retriever
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

@app.route('/forecast-chat', methods=['POST'])
def forecast_chat():
    try:
        # Get the question from the user
        data = request.json
        question = data.get("question", "")
        if not question:
            return jsonify({"error": "No question provided"}), 400
        
        # Retrieve relevant documents for the question
        docs = retriever.invoke(question)
        forecast_data = "\n\n".join([doc.page_content for doc in docs])

        # Generate the answer using the LLM
        result = chain.invoke({"forecast_data": forecast_data, "question": question})

        return jsonify({"answer": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
