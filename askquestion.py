# Import required modules from the LangChain package
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings

# Initialize the OpenAI chat model
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.8)

# Initialize the OpenAI embeddings
embeddings = OpenAIEmbeddings()

# Load the Chroma database from disk
chroma_db = Chroma(persist_directory="data", 
                   embedding_function=embeddings,
                   collection_name="htb_small_db")

# Prepare query
#query = "Answer questions based on the document you have received. Give me an example of each vulnerability. Based on this document, what vulnerabilities can I look for?"
def get_user_query():
    return input("Please enter your query: ")

query = "Answer questions based on the document you have received." + get_user_query()

print('Similarity search:')
#print(chroma_db.similarity_search(query))

print('Similarity search with score:')
#print(chroma_db.similarity_search_with_score(query))

# Fetch all documents in the collection


    # Find the document with the custom metadata tag
tagged_docs = chroma_db.get(where={"tag": "htb_small"})

if tagged_docs:
    # Prompt the model
    chain = RetrievalQA.from_chain_type(llm=llm,
                                        chain_type="stuff",
                                        retriever=chroma_db.as_retriever())

    # Execute the chain
    response = chain(query)

    # Print the response
    print(response['result'])

else:
    print("No documents found in the collection.")
