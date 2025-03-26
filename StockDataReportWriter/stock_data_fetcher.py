from typing import TypedDict, List, Dict
from stock_tools import StockTools
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from langchain_openai import ChatOpenAI
from utils import save_markdown_to_file
from langgraph.graph import StateGraph, END
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

llm = ChatOpenAI(model="granite3-dense:latest", temperature=0, base_url="http://localhost:11434/v1", api_key="ollama")


class State(TypedDict):
    """
          Represents the state of a workflow for processing a given query.

          Attributes:
              text: The original query text.
              fetched_data: The result retrieved from specialized stock data.
              md_report: The generated report based on the fetched data.
              outcome: The final outcome or status of the process.
          """
    text: str
    fetched_data: List[Dict]
    md_report: str
    outcome: str


def fetch_data_node(state: State):
    stock_tools = StockTools(state["text"])
    logging.info(f"****************************fetch_data_node with Input: {stock_tools} START")
    fetched_data = stock_tools.fetch()
    logging.info(f"****************************fetch_data_node with Output: {fetched_data} END")
    return {"fetched_data": fetched_data}


def reporting_node(state: State):
    prompt = PromptTemplate(
        input_variables=["text"],
        template="""You are experienced writer. Use the following text to write a comprehensive
          and accurate report. Use the markdown format.\n\nText:{text}\n\nReport""")
    message = HumanMessage(content=prompt.format(text=state["fetched_data"]))
    report = llm.invoke([message]).content.strip()
    logging.info(f"******************************* reporting_node END with Output: {report}")
    return {"md_report": report}


def write_to_storage_node(state: State):
    prompt = state["text"]
    outcome = save_markdown_to_file(state["md_report"], prompt, 'data')
    return {"outcome": outcome}


def generate_data_report(stock_symbol: str) -> str:
    logging.info(f"******************************* generate_data_report START with input: {stock_symbol}")
    workflow = StateGraph(State)
    workflow.add_node("fetch_data_node", fetch_data_node)
    workflow.add_node("reporting", reporting_node)
    workflow.add_node("storing", write_to_storage_node)

    workflow.set_entry_point("fetch_data_node")
    workflow.add_edge("fetch_data_node", "reporting")
    workflow.add_edge("reporting", "storing")
    workflow.add_edge("storing", END)

    app = workflow.compile()
    state_input = {"text": stock_symbol}
    result = app.invoke(state_input)
    final_answer = result["md_report"]

    if not final_answer:
        final_answer = result["outcome"]
    logging.info(f"******************************* generate_web_report END with output: {final_answer}")

    return final_answer

if __name__ == "__main__":
    generate_data_report("IBM")
