
###Stock Analyzer Application

This application showcases the integration of langgraph, AI-agent framework, and Granite, a large language model, to forecast stock performance based on provided stock symbols. The tool collects both specialized and general data to perform comprehensive stock analysis.
Overview

Given a stock symbol, the application utilizes the following components:

    StockDataReportWriter: Collects detailed data related to the stock from a specialized financial website.
    WebStockReportWriter: Gathers broader information pertaining to the specified stock from a general web source.
    Granite Model: Employed by langgraph, this powerful language model processes the collected data to generate stock analysis insights.

Getting Started

To launch the Stock Analyzer application, navigate to the project directory and execute the following command:

streamlit run StockAnalyzer/stock_analyzer.py
Copy

This command assumes that the project structure adheres to the default format within the LangraphProjects directory.

##Technologies Employed

    langgraph: An AI-agent framework leveraged to manage the application's workflow and simplify development processes.
    Streamlit: Provides the user interface, enabling interactive engagement through a web-based GUI.
    Granite Model: The core large language model responsible for analyzing and interpreting the collected stock data, generating meaningful insights.
    ollama: Utilized for local model deployment, ensuring efficient and controlled 