import dotenv
import toml
from langchain import hub
from langchain.agents import AgentExecutor, Tool
from langchain_cohere import ChatCohere, create_cohere_react_agent

from chatbot.chains.hospital_cypher_chain import hospital_cypher_chain
from chatbot.chains.hospital_review_chain import reviews_vector_chain
from chatbot.tools.wait_times import MostAvailableHospital, get_current_wait_times, get_most_available_hospital

dotenv.load_dotenv()
config = toml.load("config.toml")

agent_llm = ChatCohere(model=config["model"]["agent_model"])

tools = [
    Tool(
        name="Experiences",
        func=reviews_vector_chain.invoke,
        description="""Useful when you need to answer questions
        about patient experiences, feelings, or any other qualitative
        question that could be answered about a patient using semantic
        search. Not useful for answering objective questions that involve
        counting, percentages, aggregations, or listing facts. Use the
        entire prompt as input to the tool. For instance, if the prompt is
        "Are patients satisfied with their care?", the input should be
        "Are patients satisfied with their care?".
        """,
    ),
    Tool(
        name="Graph",
        func=hospital_cypher_chain.invoke,
        description="""Useful for answering questions about patients,
        physicians, hospitals, insurance payers, patient review
        statistics, and hospital visit details. Use the entire prompt as
        input to the tool. For instance, if the prompt is "How many visits
        have there been?", the input should be "How many visits have
        there been?".
        """,
    ),
    Tool(
        name="Waits",
        func=get_current_wait_times,
        description="""Use when asked about current wait times
        at a specific hospital. This tool can only get the current
        wait time at a hospital and does not have any information about
        aggregate or historical wait times. Do not pass the word "hospital"
        as input, only the hospital name itself. For example, if the prompt
        is "What is the current wait time at Jordan Inc Hospital?", the
        input should be "Jordan Inc".
        """,
    ),
    # MostAvailableHospital(), #takes a lot of time as it needs to query the database for all hospitals which are large in number
]

hospital_agent_prompt = hub.pull("hwchase17/openai-functions-agent")

hospital_rag_agent = create_cohere_react_agent(llm=agent_llm, tools=tools, prompt=hospital_agent_prompt)

hospital_rag_agent_executor = AgentExecutor(
    agent=hospital_rag_agent, tools=tools, return_intermediate_steps=False, verbose=False
)
