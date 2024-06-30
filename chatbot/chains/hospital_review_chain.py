from dotenv import dotenv_values
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_cohere import ChatCohere, CohereEmbeddings
from langchain_community.vectorstores import Neo4jVector

llm = ChatCohere(model="command-r")
config = dotenv_values(".env")

# first time to insert any new embeddings to the store
# neo4j_vector_index = Neo4jVector.from_existing_graph(
#     embedding=CohereEmbeddings(),
#     url=config["NEO4J_URI"],
#     username=config["NEO4J_USERNAME"],
#     password=config["NEO4J_PASSWORD"],
#     index_name="reviews",
#     node_label="Review",
#     text_node_properties=["physician_name", "patient_name", "text", "hospital_name"],
#     embedding_node_property="embedding",
# )

# return the instance of the store without inserting any new embeddings.
neo4j_vector_index = Neo4jVector.from_existing_index(
    embedding=CohereEmbeddings(),
    url=config["NEO4J_URI"],
    username=config["NEO4J_USERNAME"],
    password=config["NEO4J_PASSWORD"],
    index_name="reviews",
)
retriever = neo4j_vector_index.as_retriever(k=10)

template = """Your job is to use patient
reviews to answer questions about their experience at a hospital. Use
the following context to answer questions. Be as detailed as possible, but
don't make up any information that's not from the context. If you don't know
an answer, say you don't know.

{context}
"""

system_prompt = SystemMessagePromptTemplate(prompt=PromptTemplate(input_variables=["context"], template=template))
human_prompt = HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=["question"], template="{question}"))

messages = [system_prompt, human_prompt]
prompt_template = ChatPromptTemplate(input_variables=["context", "question"], messages=messages)

qa_chain = create_stuff_documents_chain(llm, prompt_template)
reviews_vector_chain = create_retrieval_chain(retriever, qa_chain)
