from chatbot.agents.hospital_rag_agent import hospital_rag_agent_executor

# Experience tool
query_1 = "What have patlients said about their quality of rest during their stay?"
print("Q: ", query_1)
example_1 = hospital_rag_agent_executor.invoke({"input": query_1})
print("A: ", example_1.get("output"))
print()

# Graph tool
query_2 = "Query the graph database to show me the reviews written by patient 7674"
print("Q: ", query_2)
example_2 = hospital_rag_agent_executor.invoke(
    {"input": query_2}
    # {"input": "Show me reviews written by patient 7674."}
)
print("A: ", example_2.get("output"))
print()

# Waits tool
query_3 = "What is the wait time at Wallace-Hamilton?"
print("Q: ", query_3)
example_3 = hospital_rag_agent_executor.invoke({"input": query_3})
print("A: ", example_3.get("output"))
