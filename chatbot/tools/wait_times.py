import os
from typing import Any, Dict, Tuple, Union

import dotenv
import numpy as np
from langchain.tools import BaseTool
from langchain_community.graphs import Neo4jGraph

dotenv.load_dotenv()


def _get_current_hospitals() -> list[str]:
    """Fetch a list of current hospital names from a Neo4j database."""
    graph = Neo4jGraph(
        url=os.getenv("NEO4J_URI"), username=os.getenv("NEO4J_USERNAME"), password=os.getenv("NEO4J_PASSWORD")
    )

    current_hospitals = graph.query(
        """
        MATCH (h:Hospital)
        RETURN h.name AS hospital_name
        """
    )

    return [d["hospital_name"].lower() for d in current_hospitals]


def _get_current_wait_time_minutes(hospital: str) -> int:
    """Get the current wait time at a hospital in minutes."""
    current_hospitals = _get_current_hospitals()

    if hospital.lower() not in current_hospitals:
        return -1

    return np.random.randint(low=0, high=600)


def get_current_wait_times(hospital: str) -> str:
    """Get the current wait time at a hospital formatted as a string."""
    wait_time_in_minutes = _get_current_wait_time_minutes(hospital)

    if wait_time_in_minutes == -1:
        return f"Hospital '{hospital}' does not exist."

    hours, minutes = divmod(wait_time_in_minutes, 60)

    if hours > 0:
        return f"{hours} hours {minutes} minutes"
    else:
        return f"{minutes} minutes"


def get_most_available_hospital() -> dict[str, float]:
    """Find the hospital with the shortest wait time."""
    current_hospitals = _get_current_hospitals()

    current_wait_times = [_get_current_wait_time_minutes(h) for h in current_hospitals]

    best_time_idx = np.argmin(current_wait_times)
    best_hospital = current_hospitals[best_time_idx]
    best_wait_time = current_wait_times[best_time_idx]

    return {best_hospital: best_wait_time}


class MostAvailableHospital(BaseTool):
    name = "Availability"
    description = """
    Use when you need to find out which hospital has the shortest
    wait time. This tool does not have any information about aggregate
    or historical wait times. This tool returns a dictionary with the
    hospital name as the key and the wait time in minutes as the value.
    """

    def _to_args_and_kwargs(self, tool_input: Union[str, Dict]) -> Tuple[Tuple, Dict]:
        return (), {}

    def _run(self):
        """Use the tool."""
        response = get_most_available_hospital()
        return response

    def _arun(self):
        """Use the tool asynchronously."""
        raise NotImplementedError("get_most_available_hospital does not support async")
