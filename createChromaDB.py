# Import required modules from the LangChain package
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings

# Load a text document and split it into sections
loader = TextLoader("data/htbtext_short.txt", encoding='cp437')
docs = loader.load_and_split()

# Initialize the OpenAI embeddings
embeddings = OpenAIEmbeddings()

# Load the Chroma database from disk or create a new one if it doesn't exist
chroma_db = Chroma(persist_directory="data", 
                   embedding_function=embeddings,
                   collection_name="htb_small_db")

# Get the collection from the Chroma database
collection = chroma_db.get()

# If the collection is empty, create a new one
if len(collection['ids']) == 0:
    # Create a new Chroma database from the documents
    chroma_db = Chroma.from_documents(
        documents=docs, 
        embedding=embeddings, 
        persist_directory="data",
        collection_name="htb_small_db"
    )

    # Save the Chroma database to disk
    chroma_db.persist()
