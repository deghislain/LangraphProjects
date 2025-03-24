from typing import TypedDict
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchResults
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from langgraph.graph import StateGraph, END
from IPython.display import display, Image
from dotenv import load_dotenv
from langchain_core.runnables.graph import MermaidDrawMethod

import os

load_dotenv()

os.environ["OPENAI_API_KEY"] = "ollama"

llm = ChatOpenAI(model="granite3-dense:latest", temperature=0)


class State(TypedDict):
    text: str
    search_result: str
    parsing_result: str
    report: str


def search_node(state: State):
    search = DuckDuckGoSearchResults()
    search_result = search.run(state["text"])
    return {"search_result": search_result}


def parsing_node(state: State):
    parsing_result = ""
    search_results = state["text"]
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
         report and accurate report.\n\nText:{text}\n\nReport""")
    message = HumanMessage(content=prompt.format(text=state["text"]))
    report = llm.invoke([message]).content.strip()
    return {"report": report}


def main():
    workflow = StateGraph(State)
    workflow.add_node("search_node", search_node)
    workflow.add_node("parsing", parsing_node)
    workflow.add_node("reporting", reporting_node)

    workflow.set_entry_point("search_node")
    workflow.add_edge("search_node", "parsing")
    workflow.add_edge("parsing", "reporting")
    workflow.add_edge("reporting", END)

    app = workflow.compile()
    display(
        Image(
            app.get_graph().draw_mermaid_png(
                draw_method=MermaidDrawMethod.API,
            )
        )
    )
    query = "What are the latest about IBM stocks"
    state_input = {"text": query}
    result = app.invoke(state_input)

    print(result)


if __name__ == "__main__":
    main()
