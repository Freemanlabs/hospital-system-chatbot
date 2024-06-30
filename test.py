from chatbot.agents.hospital_rag_agent import hospital_rag_agent_executor
from chatbot.chains.hospital_review_chain import neo4j_vector_index, retriever, reviews_vector_chain

# from chatbot import hospital_agent_executor, review_chain

# question = """Has anyone complained about communication with the hospital staff?"""
# # print(review_chain.invoke(question))

# print(hospital_agent_executor.invoke({"input": "What is the current wait time at hospital C?"}))
# print("================")
# print(hospital_agent_executor.invoke({"input": "What have patients said about their comfort at the hospital?"}))

# query = """What have patients said about hospital efficiency? Mention details from specific reviews."""

# response = reviews_vector_chain.invoke({"question": query})
# print("Response: ", response)

response = hospital_rag_agent_executor.invoke({"input": "What is the wait time at Wallace-Hamilton?"})
