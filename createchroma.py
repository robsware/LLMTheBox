# langchain_util.py

# Import required modules from the LangChain package
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings


def load_and_split_document(file_path: str, encoding: str = 'cp437'):
    """
    Load a text document and split it into sections.

    Args:
        file_path (str): Path to the text document.
        encoding (str): Encoding of the text document.

    Returns:
        List[Document]: List of documents after splitting.
    """
    loader = TextLoader(file_path, encoding=encoding)
    return loader.load_and_split()


def initialize_embeddings():
    """
    Initialize the OpenAI embeddings.

    Returns:
        OpenAIEmbeddings: Instance of OpenAIEmbeddings.
    """
    return OpenAIEmbeddings()


def load_or_create_chroma_db(docs, embeddings, persist_directory: str = "data", collection_name: str = "htb_small_db"):
    """
    Load the Chroma database from disk or create a new one if it doesn't exist.

    Args:
        docs (List[Document]): List of documents to add to the Chroma database.
        embeddings (OpenAIEmbeddings): Instance of OpenAIEmbeddings.
        persist_directory (str): Directory to persist the Chroma database.
        collection_name (str): Name of the collection in the Chroma database.

    Returns:
        Chroma: Instance of the Chroma database.
    """
    chroma_db = Chroma(persist_directory=persist_directory,
                       embedding_function=embeddings,
                       collection_name=collection_name)

    collection = chroma_db.get()

    if len(collection['ids']) == 0:
        chroma_db = Chroma.from_documents(
            documents=docs,
            embedding=embeddings,
            persist_directory=persist_directory,
            collection_name=collection_name
        )
        chroma_db.persist()

    return chroma_db


def main(file_path: str):
    """
    Main function to load, split document, initialize embeddings, and load or create Chroma database.

    Args:
        file_path (str): Path to the text document.
    """
    docs = load_and_split_document(file_path)
    embeddings = initialize_embeddings()
    chroma_db = load_or_create_chroma_db(docs, embeddings)

    return chroma_db


if __name__ == "__main__":
    # Example usage
    file_path = "data/htbtext_short.txt"
    main(file_path)
