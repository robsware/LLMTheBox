# langchain_ask.py

import os
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain_community.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from createchroma import initialize_chroma_db
from scraper import scrape_links_and_save
from download_page_content import extract_htb_data
import warnings  # Import the warnings module

# Suppress all warnings
warnings.filterwarnings("ignore")



def initialize_chat_model(model_name: str = "gpt-4-turbo", temperature: float = 0.8):
    """
    Initialize the OpenAI chat model.

    Args:
        model_name (str): Name of the model.
        temperature (float): Temperature setting for the model.

    Returns:
        ChatOpenAI: Instance of ChatOpenAI.
    """
    return ChatOpenAI(model_name=model_name, temperature=temperature)


def initialize_embeddings():
    """
    Initialize the OpenAI embeddings.

    Returns:
        OpenAIEmbeddings: Instance of OpenAIEmbeddings.
    """
    return OpenAIEmbeddings()


def load_chroma_db(persist_directory: str = "data", collection_name: str = "htb_small_db"):
    """
    Load the Chroma database from disk.

    Args:
        persist_directory (str): Directory where the Chroma database is persisted.
        collection_name (str): Name of the collection in the Chroma database.

    Returns:
        Chroma: Instance of the Chroma database.
    """
    embeddings = initialize_embeddings()
    return Chroma(persist_directory=persist_directory,
                  embedding_function=embeddings,
                  collection_name=collection_name)


def get_user_query():
    """
    Get the query from the user.

    Returns:
        str: User's query.
    """
    return input("Please enter your query: ")


def execute_query(chroma_db, llm, query: str):
    """
    Execute the query using the Chroma database and the language model.

    Args:
        chroma_db (Chroma): Instance of the Chroma database.
        llm (ChatOpenAI): Instance of ChatOpenAI.
        query (str): User's query.

    Returns:
        str: Response from the model.
    """
    tagged_docs = chroma_db.get(where={"tag": "htb_small"})

    if tagged_docs:
        chain = RetrievalQA.from_chain_type(llm=llm,
                                            chain_type="stuff",
                                            retriever=chroma_db.as_retriever())
        response = chain(query)
        return response['result']
    else:
        return "No documents found in the collection."


def check_data_folder(folder_path: str = "data") -> bool:
    """
    Check if the data folder exists and contains files.

    Args:
        folder_path (str): Path to the data folder.

    Returns:
        bool: True if the folder exists and contains files, False otherwise.
    """
    if os.path.exists(folder_path) and os.listdir(folder_path):
        return True
    return False


def main():
    """
    Main function to execute the user query.
    """
    if not check_data_folder():
        print("Data folder is empty")
        print("Generating links to scrape...")
        scrape_links_and_save()
        print("Downloading page contents...")
        extract_htb_data()
        print("Creating DB...")
        chroma_db = initialize_chroma_db("data/htbtext_short.txt", "data", "htb_small_db")
        print("Chroma DB created successfully.")
    

    llm = initialize_chat_model()
    chroma_db = load_chroma_db()
    user_query = get_user_query()
    query = "Answer questions based on the document you have received. " + user_query

    # print('Similarity search:')
    # print(chroma_db.similarity_search(query))

    # print('Similarity search with score:')
    # print(chroma_db.similarity_search_with_score(query))

    response = execute_query(chroma_db, llm, query)
    print(response)


if __name__ == "__main__":
    main()
