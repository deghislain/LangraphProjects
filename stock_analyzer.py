import streamlit as st
from typing import TypedDict
from WebStockReportWriter.stock_web_search import generate_web_report
from StockDataReportWriter.stock_data_fetcher import generate_data_report
from stock_prompt import get_analyse_prompt
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
from utils import generate_pdf

llm = ChatOpenAI(model="granite3.1-dense:2b", temperature=0, base_url="http://localhost:11434/v1", api_key="ollama")


class State(TypedDict):
    text: str
    web_report: str
    data_report: str
    fin_report: str
    outcome: str


def generate_web_report_node(state: State):
    web_report = generate_web_report(state["text"])
    return {"web_report": web_report}


def generate_data_report_node(state: State):
    data_report = generate_data_report(state["text"])
    return {"data_report": data_report}


def perform_financial_analyse_node(state: State):
    comb_report = state["data_report"] + state["web_report"]
    logging.info(f"******************************* perform_financial_analyse_node comb_report: {comb_report}")
    stock_symbol = state["text"]
    query = f"Given the following content: {comb_report}, write an outstanding report about this stock: {stock_symbol}"
    messages = [
        SystemMessage(content=get_analyse_prompt()),
        HumanMessage(content=query)
    ]

    fin_report = llm.invoke(messages).content.strip()
    logging.info(f"******************************* perform_financial_analyse_node END with Output: {fin_report}")
    return {"fin_report": fin_report}


def generate_pdf_report_node(state: State):
    outcome = generate_pdf(state["fin_report"], state["text"])
    return {"outcome": outcome}


def main(stock_symbol: str) -> str:
    logging.info(f"Stock Analyzer START with input: {stock_symbol}")
    workflow = StateGraph(State)
    workflow.add_node("generate_web_report_node", generate_web_report_node)
    workflow.add_node("generate_data_report_node", generate_data_report_node)
    workflow.add_node("financial_analyse_node", perform_financial_analyse_node)
    workflow.add_node("generate_pdf_report_node", generate_pdf_report_node)

    workflow.set_entry_point("generate_web_report_node")
    workflow.add_edge("generate_web_report_node", "generate_data_report_node")
    workflow.add_edge("generate_data_report_node", "financial_analyse_node")
    workflow.add_edge("financial_analyse_node", "generate_pdf_report_node")
    workflow.add_edge("generate_pdf_report_node", END)
    app = workflow.compile()
    state_input = {"text": stock_symbol}
    result = app.invoke(state_input)
    final_answer = result["fin_report"]
    if not final_answer:
        final_answer = result["outcome"]
    logging.info(f"******************************* Stock Analyzer ENDED with output: {final_answer}")
    return final_answer


if __name__ == "__main__":
    stock_symbol = st.text_input(":blue[Enter a stock symbol here:]", placeholder="eg IBM")
    submit_btn = st.button("Submit")
    if stock_symbol and submit_btn:
        report = main(stock_symbol)
        st.write(report)
