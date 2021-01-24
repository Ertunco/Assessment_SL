import unittest
from data_handler import HandleData
import pandas as pd
import numpy as np

class TestHandleData(unittest.TestCase):
    def test_check_file_format(self):
        hd = HandleData()
        self.assertTrue(hd.check_file_format("some_file_name.csv"))
        self.assertTrue(hd.check_file_format("some_file_name.CsV"))
        self.assertFalse(hd.check_file_format("some_file_name.html"))
        self.assertFalse(hd.check_file_format("some_file_name.HTTml"))

    def test_check_file_name(self):
        hd = HandleData()
        self.assertTrue(hd.check_file_name("orders"))
        self.assertTrue(hd.check_file_name("OrdERS"))
        self.assertFalse(hd.check_file_name("wrong_file_name"))
        self.assertFalse(hd.check_file_name("WroNNg_File_name"))

    def test_write_csv_to_df(self):
        hd = HandleData()
        self.assertIsInstance(hd.write_csv_to_df("orders"), pd.DataFrame)
        self.assertIsInstance(hd.write_csv_to_df("OrdERS"), pd.DataFrame)
        self.assertIsNone(hd.write_csv_to_df("wrong_file_name"))
        self.assertIsNone(hd.write_csv_to_df("WroNNg_File_name"))

    def test_has_df_nan(self):
        hd = HandleData()
        df_orders = hd.write_csv_to_df("orders")
        df_order_lines = hd.write_csv_to_df("order_lines")
        self.assertTrue(hd.has_df_nan(df_orders))
        self.assertTrue(hd.has_df_nan(df_order_lines))

    def test_has_df_cols(self):
        hd = HandleData()
        df_orders = hd.write_csv_to_df("orders")
        df_test = pd.DataFrame(columns=['A','B','C','D','E','F','G'])
        self.assertTrue(hd.has_df_cols(df_orders, "id", "created_at", "vendor_id", "customer_id"))
        self.assertFalse(hd.has_df_cols(df_test, 'A','B','C','D','E','F'))

    def test_validate_df(self):
        hd = HandleData()
        df_order_lines = hd.write_csv_to_df("order_lines")
        df_test = pd.DataFrame(columns=['A','B','C','D','E','F','G'])
        self.assertTrue(hd.has_df_cols(df_order_lines, "order_id", "product_id", "product_description", "product_price", "product_vat_rate",\
                "discount_rate", "quantity","full_price_amount", "discounted_amount", "vat_amount", "total_amount"))
        self.assertFalse(hd.has_df_cols(df_test, 'A','B','C','D','E','F'))

    def test_round_up(self):
        hd = HandleData()
        n1 = 155000171.52235325
        d1 = 2
        num1 = hd.round_up(n1, d1)
        self.assertEqual(num1, 155000171.53)
        n2 = 168091848.74244543
        d2 = 3
        num2 = hd.round_up(n2, d2)
        self.assertEqual(num2, 168091848.743)
        n3 = 185569868.96233523
        d3 = 2
        num3 = hd.round_up(n3, d3)
        self.assertNotEqual(num3, 185569868.972)
        

if __name__ == "__main__":
    unittest.main()