import csv
import json
import math
import pandas as pd
from datetime import datetime

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class DataframeValidationError(Error):
    """Exception raised when validation fails"""
    pass

class HandleData:
    def __init__(self):
        self.file_names_list = ["commissions", "order_lines", "orders", "product_promotions", "products", "promotions"]

    def check_file_format(self, file_name):
        """Checks if the format of the file matches the desired format"""
        chars = file_name.lower().split(".")
        if chars[1] == "csv":
            return True

    def check_file_name(self, file_name):
        """Checks if the name of the file is in the list of file names we work with"""
        if file_name.lower() in self.file_names_list:
            return True

    def write_csv_to_df(self, file_name):
        """Converts a CSV file to pandas dataframe returns None if csv file not found"""
        file_name = file_name.lower()
        try:
            df = pd.read_csv('csv_files/{}.csv'.format(file_name), index_col=False)
            if not df.empty:
                return df
            else:
                return None
        except FileNotFoundError:
                return None

    def has_df_nan(self, df):
        """Checks if pandas dataframe has none value and drops if it finds"""
        if not df.isnull().values.any():
            df.dropna()
            return True

    def has_df_cols(self, df, *col_names):
        """Checks if pandas dataframe column names are as expected"""
        if list(col_names) == df.columns.values.tolist():
            return True
        else:
            return False

    def validate_df(self, df, *col_names):
        """Validates pandas dataframe on column name check and on none value check prints and raises error if unsuccessful"""
        nan_check = self.has_df_nan(df)
        col_names_check = self.has_df_cols(df,*col_names)
        try:
            if nan_check and col_names_check:
                print("Validation Successful")
                return True
            else:
                raise DataframeValidationError
        except DataframeValidationError:
                print("Error! Dataframe has either nan values or column names don't match")
                return False

    def generate_dict(self):
        """Generates the desired response format as a dictionary object"""
        dict_obj = {
            "customers":"",
            "total_discount_amount":"",
            "items":"",
            "order_total_avg":"",
            "discount_rate_avg":"",
            "commisions":{
                "promotions":{

                },
                "total":"",
                "order_average":""
            }
        }
        return dict_obj

    def round_up(self, n, decimals=0):
        """Rounds given value to desired decimal value"""
        multiplier = 10 ** decimals
        return math.ceil(n * multiplier) / multiplier

if __name__ == '__main__':
    hd = HandleData()
    
