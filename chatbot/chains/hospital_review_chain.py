import os

import dotenv
import toml
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_cohere import ChatCohere, CohereEmbeddings
from langchain_community.graphs import Neo4jGraph
from langchain_community.vectorstores import Neo4jVector

dotenv.load_dotenv()
config = toml.load("config.toml")

llm = ChatCohere(model=config["model"]["qa_model"])

graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"), username=os.getenv("NEO4J_USERNAME"), password=os.getenv("NEO4J_PASSWORD")
)

reviews_embeddings = graph.query(
    """
        MATCH (r:Review)
        WHERE r.embedding IS NOT null
        RETURN r.embedding AS embeddings
        LIMIT 1
        """
)
is_embeddings_in_store = len(reviews_embeddings) > 0

if is_embeddings_in_store:
    # return the instance of the store without inserting any new embeddings.
    neo4j_vector_index = Neo4jVector.from_existing_index(
        embedding=CohereEmbeddings(),
        url=os.getenv("NEO4J_URI"),
        username=os.getenv("NEO4J_USERNAME"),
        password=os.getenv("NEO4J_PASSWORD"),
        index_name="reviews",
    )
else:
    # first time to insert any new embeddings to the store
    neo4j_vector_index = Neo4jVector.from_existing_graph(
        embedding=CohereEmbeddings(),
        url=os.getenv("NEO4J_URI"),
        username=os.getenv("NEO4J_USERNAME"),
        password=os.getenv("NEO4J_PASSWORD"),
        index_name="reviews",
        node_label="Review",
        text_node_properties=["physician_name", "patient_name", "text", "hospital_name"],
        embedding_node_property="embedding",
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

reviews_vector_chain = RetrievalQA.from_chain_type(
    llm=llm, chain_type="stuff", retriever=retriever, chain_type_kwargs={"prompt": prompt_template}
)
