from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from app.config import settings

# 1. Load the existing vector base
embeddings = OllamaEmbeddings(model="nomic-embed-text")
db = Chroma(persist_directory=settings.CHROMA_DB_PATH, embedding_function=embeddings) # reads the existing vector db in the file path
retriever = db.as_retriever(search_kwargs={"k":3}) # k indicates the amount of chunks it will retrieve per query

# 2. Define a prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer using only the context below. If the answer isn't there, say so.\nAfter your answer, cite the sources you used in the format: (Source: filename).\nContext: {context}"),
    ("human", "{question}")
])

def format_docs_with_sources(docs):
    return "\n\n".join(
        f"[Source: {doc.metadata.get('source', 'unknown')}]\n{doc.page_content}"
        for doc in docs
    )

# 3. Build the chain
## This is built at module level, outside of a function. This way it is only loaded once when the api initializes and not once per request
llm = ChatOllama(model="llama3")

chain = (
    {"context": retriever | format_docs_with_sources, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)