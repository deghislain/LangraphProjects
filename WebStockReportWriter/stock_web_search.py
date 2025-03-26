from typing import TypedDict
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchResults
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from langgraph.graph import StateGraph, END
import logging
import streamlit as st
import sys

sys.path.insert(0, '../')
from utils import save_markdown_to_file

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
llm = ChatOpenAI(model="granite3-dense:latest", temperature=0, base_url="http://localhost:11434/v1", api_key="ollama")
stock_symbol = ""


class State(TypedDict):
    """
       Represents the state of a workflow for processing a given query.

       Attributes:
           text: The original query text.
           search_result: The result retrieved from internet search.
           parsing_result: The parsed content derived from the search result.
           report: The generated report based on the parsing result.
           outcome: The final outcome or status of the process.
       """
    text: str
    search_result: str
    parsing_result: str
    report: str
    outcome: str


def search_node(state: State):
    search_query = state["text"]

    search = DuckDuckGoSearchResults()
    search_result = search.run(search_query)
    return {"search_result": search_result}


def parsing_node(state: State):
    parsing_result = ""
    search_results = state["search_result"]
    contents = search_results.split(', snippet: ')
    for content in contents[1:]:
        parts = content.split(', title: ')
        if len(parts) == 2:
            parsing_result += parts[0]
    return {"parsing_result": parsing_result}


def reporting_node(state: State):
    prompt = PromptTemplate(
        input_variables=["text"],
        template="""You are experienced writer. Use the following text to write a comprehensive
          and accurate report. Use the markdown format.\n\nText:{text}\n\nReport""")
    message = HumanMessage(content=prompt.format(text=state["parsing_result"]))
    report = llm.invoke([message]).content.strip()
    return {"report": report}


def write_to_storage_node(state: State):
    prompt = state["text"]
    words = prompt.split()
    stored = save_markdown_to_file(state["report"],  words[-1], 'web')
    return {"stored": stored}


def generate_web_report(prompt: str) -> str:
    logging.info(f"******************************* generate_web_report START with input: {prompt}")
    workflow = StateGraph(State)
    workflow.add_node("search_node", search_node)
    workflow.add_node("parsing", parsing_node)
    workflow.add_node("reporting", reporting_node)
    workflow.add_node("storing", write_to_storage_node)

    workflow.set_entry_point("search_node")
    workflow.add_edge("search_node", "parsing")
    workflow.add_edge("parsing", "reporting")
    workflow.add_edge("reporting", "storing")
    workflow.add_edge("storing", END)

    app = workflow.compile()

    state_input = {"text": prompt}
    result = app.invoke(state_input)
    final_answer = result["report"]
    if not final_answer:
        final_answer = result["outcome"]
    logging.info(f"******************************* generate_web_report END with output: {final_answer}")

    return final_answer


if __name__ == "__main__":
    prompt = "What are the latest about this stock: "
    stock_symbol += st.text_input(":blue[Enter a stock symbol here:]", placeholder="eg IBM")
    submit_btn = st.button("Submit")
    if stock_symbol and submit_btn:
        prompt += stock_symbol
        report = generate_web_report(prompt)
        st.write(report)
