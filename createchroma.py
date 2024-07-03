from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings

def initialize_chroma_db(file_path, persist_directory, collection_name):
    # Load a text document and split it into sections
    loader = TextLoader(file_path, encoding='cp437')
    docs = loader.load_and_split()

    # Initialize the OpenAI embeddings
    embeddings = OpenAIEmbeddings()

    # Load the Chroma database from disk or create a new one if it doesn't exist
    chroma_db = Chroma(persist_directory=persist_directory, 
                       embedding_function=embeddings,
                       collection_name=collection_name)

    # Get the collection from the Chroma database
    collection = chroma_db.get()

    # If the collection is empty, create a new one
    if len(collection['ids']) == 0:
        # Create a new Chroma database from the documents
        chroma_db = Chroma.from_documents(
            documents=docs, 
            embedding=embeddings, 
            persist_directory=persist_directory,
            collection_name=collection_name
        )

        # Save the Chroma database to disk
        chroma_db.persist()

    return chroma_db

# Example of how to call the function
# chroma_db = initialize_chroma_db("data/htbtext_short.txt", "data", "htb_small_db")
