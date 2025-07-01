import os
import glob
import hashlib
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.memory import ConversationBufferMemory

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("La variable d'environnement OPENAI_API_KEY est requise.")

# Fonction pour calculer le hash des fichiers PDF
def calculate_pdf_hash():
    pdf_files = glob.glob("docs/*.pdf")
    if not pdf_files:
        raise ValueError("Aucun fichier PDF trouvé dans le dossier docs/")
    
    # Créer un hash basé sur les noms et tailles des fichiers
    hash_input = ""
    for pdf_file in sorted(pdf_files):
        stat = os.stat(pdf_file)
        hash_input += f"{pdf_file}:{stat.st_size}:{stat.st_mtime}:"
    
    return hashlib.md5(hash_input.encode()).hexdigest()

# Chargement ou création des embeddings
EMBEDDINGS_DIR = "embeddings_cache"
current_hash = calculate_pdf_hash()
embeddings_path = os.path.join(EMBEDDINGS_DIR, f"faiss_index_{current_hash}")

if os.path.exists(embeddings_path):
    print("🔄 Chargement des embeddings existants...")
    embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectordb = FAISS.load_local(embeddings_path, embedding, allow_dangerous_deserialization=True)
    print("✅ Embeddings chargés depuis le cache")
else:
    print("🔄 Création des embeddings (première fois ou fichiers modifiés)...")
    
    # Chargement de tous les PDFs du dossier docs
    pdf_files = glob.glob("docs/*.pdf")
    all_docs = []
    for pdf_file in pdf_files:
        print(f"Chargement du fichier : {pdf_file}")
        loader = PyPDFLoader(pdf_file)
        docs = loader.load()
        all_docs.extend(docs)

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(all_docs)

    # Vectorisation
    embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectordb = FAISS.from_documents(chunks, embedding)
    
    # Sauvegarde des embeddings
    os.makedirs(EMBEDDINGS_DIR, exist_ok=True)
    vectordb.save_local(embeddings_path)
    print("✅ Embeddings créés et sauvegardés")

retriever = vectordb.as_retriever()

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

qa = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0),
    retriever=retriever,
    memory=memory,
)

# Création de l'app FastAPI
app = FastAPI()

@app.post("/ask")
async def ask_question(req: Request):
    data = await req.json()
    query = data.get("question", "")
    if not query:
        return JSONResponse(status_code=400, content={"error": "Question manquante"})
    result = qa({"question": query})
    return {"answer": result["answer"]}

# Frontend static - monté après les endpoints API
app.mount("/", StaticFiles(directory="static", html=True), name="static")
