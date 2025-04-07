import unittest

from StockDataReportWriter.stock_tools import retrieve_stock_last_3years_info
from test.test_utils import read_json_file


class StockDataJson:
    def __init__(self, json_file, expected_output_file_name):
        self.json_file = json_file
        self.expected_output_file_name = expected_output_file_name

    def json(self):
        return read_json_file("test_resources/" + self.json_file)

    def get_expected_output(self):
        return read_json_file("test_resources/" + self.expected_output_file_name)


class TestStockTool(unittest.TestCase):
    def test_retrieve_income_statement(self):
        self.stock_data_json = StockDataJson("income.json", "income_expected_output.json")
        result = retrieve_stock_last_3years_info(self.stock_data_json, 'income_statement',
                                                 'annualReports')

        self.assertEqual(result, self.stock_data_json.get_expected_output())

    def test_retrieve_income_statement_missing_key_type(self):
        self.stock_data_json = StockDataJson("income.json", "income_expected_output.json")

        with self.assertRaises(ValueError) as ex:
            retrieve_stock_last_3years_info(self.stock_data_json, '',
                                            'annualReports')
            self.assertEqual(str(ex.exception), "Error: Invalid input make sure stock_data, key_type, "
                                                "and info_type have correct values.")

    def test_retrieve_income_statement_missing_info_type(self):
        self.stock_data_json = StockDataJson("income.json", "income_expected_output.json")

        with self.assertRaises(ValueError) as ex:
            retrieve_stock_last_3years_info(self.stock_data_json, 'income_statement',
                                            '')
            self.assertEqual(str(ex.exception), "Error: Invalid input make sure stock_data, key_type, "
                                                "and info_type have correct values.")

    def test_retrieve_income_statement_missing_stock_data(self):
        with self.assertRaises(ValueError) as ex:
            retrieve_stock_last_3years_info(None, 'income_statement',
                                            '')
            self.assertEqual(str(ex.exception), "Error: Invalid input make sure stock_data, key_type, "
                                                "and info_type have correct values.")


if __name__ == '__main__':
    unittest.main()
