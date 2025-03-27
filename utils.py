from datetime import date
from pathlib import Path
from xhtml2pdf import pisa
from markdown_it import MarkdownIt  #pip install markdown-it-py
from io import BytesIO
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

REPORT_SUFFIX = "_stock_report.md"
PATH_TO_WEB_REPORT = "WebStockReportWriter/web_reports/"
PATH_TO_DATA_REPORT = "StockDataReportWriter/data_reports/"


def save_markdown_to_file(markdown_string, stock_symbol, report_type) -> str:
    logging.info(f"************************save_markdown_to_file for: {markdown_string}")
    """
    Save a given markdown string to a file on local disk.

    :param markdown_string: String containing markdown content.
    :param stock_symbol: The stock which info are being stored.
    """
    try:
        if report_type == "data":
            report_type = "StockDataReportWriter/" + report_type
        else:
            report_type = "WebStockReportWriter/" + report_type

        # Path configuration
        MD_OUTPUT_DIR = Path(f'{report_type}_reports/{stock_symbol}')
        MD_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        # Get today's date and format PDF name
        today = date.today().strftime("%Y%m%d")
        report_name = f"{today}_stock_report.md"

        report_path = MD_OUTPUT_DIR / report_name
        # Open the file in write mode ('w')
        with open(report_path, 'w', encoding='utf-8') as file:
            # Write the markdown content to the file
            file.write(markdown_string)
        logging.info(f"Markdown content saved to {report_path}")
        OUTCOME_MESSAGE = "Report successfully generated and stored"
    except IOError as e:
        logging.error(f"************************An error occurred while writing to file: {e}")
        OUTCOME_MESSAGE = "An Error has occurred: Unable to store the report"
    return OUTCOME_MESSAGE


def combine_markdown_files(file1_path, file2_path):
    """
    Reads and combines the contents of two Markdown files.

    :param file1_path: Path to the first Markdown file.
    :param file2_path: Path to the second Markdown file.
    :return: A string containing the combined contents of both input Markdown files.
    """
    try:
        # Open and read the contents of the first file
        with open(file1_path, 'r', encoding='utf-8') as file1:
            content1 = file1.read()
        # Open and read the contents of the second file
        with open(file2_path, 'r', encoding='utf-8') as file2:
            content2 = file2.read()

        # Combine the contents of both files
        combined_content = content1 + "\n\n" + content2
        logging.info(f"combine_markdown_files: combined content output: {combined_content}")
        return combined_content
    except FileNotFoundError as fe:
        logging.error(f"************************An error occurred while writing to file: {fe}")
        return f"Error: One or both of the files at paths '{file1_path}' and '{file2_path}' were not found."
    except Exception as e:
        logging.error(f"************************An error occurred while writing to file: {e}")
        return f"An unexpected error occurred: {str(e)}"


def generate_pdf(analyze_doc: str, stock_symbol: str) -> str:
    """
           Generate a PDF from the provided markdown content.
            Args:
                  stock_symbol: The stock symbol, e.g., "IBM".
                  analyze_doc: The markdown content to convert into a PDF
           """
    md = MarkdownIt()
    html_content = md.render(analyze_doc)
    pdf_output = BytesIO()
    pisa.CreatePDF(html_content, dest=pdf_output, encoding='utf-8')
    pdf_output.seek(0)  # Reset file pointer to beginning of PDF data

    # Path configuration
    PDF_OUTPUT_DIR = Path(f'reports/{stock_symbol}')
    PDF_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTCOME_MESSAGE = "Report successfully generated and stored"
    print("generate_pdf: Start")

    # Get today's date and format PDF name
    today = date.today().strftime("%Y%m%d")
    pdf_name = f"{today}_stock_report.pdf"

    pdf_path = PDF_OUTPUT_DIR / pdf_name
    print("***************************************", PDF_OUTPUT_DIR)

    try:
        # Convert markdown to PDF bytes
        pdf_content = pdf_output.getvalue()

        # Save PDF bytes to a file
        with open(pdf_path, "wb") as pdf_file:
            pdf_file.write(pdf_content)

        print("generate_pdf: Successfully generated PDF at", str(pdf_path))

    except FileExistsError as ex:
        logging.error(f"Error: PDF file already exists - {ex}")
    except Exception as ex:
        logging.error(f"Unexpected error while generating PDF: {ex}")

    return OUTCOME_MESSAGE
