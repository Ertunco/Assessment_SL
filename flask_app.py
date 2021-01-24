from flask import Flask, render_template, request, jsonify
from data_handler import HandleData
from datetime import datetime
import pandas as pd
import json
import math

app = Flask(__name__)

# Keep the order of the dictionary and prevent jsonify to sort the order of the keys
app.config['JSON_SORT_KEYS'] = False

# Set dataframe max row display
pd.set_option('display.max_row', 500)

# Set dataframe max column width to 20
pd.set_option('display.max_columns', 20)

# Allow chained assignments and ignore SettingWithCopyWarning
pd.options.mode.chained_assignment = None  # default='warn'

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/form', methods = ["POST", "GET"])
def form():
    if request.method == "POST":
        hd = HandleData()
        response_dict = hd.generate_dict()

        date_info_str = request.form["datepicker"]      # Datepicker Returned Date String Object
        if date_info_str == "":
            warning = "Please Enter a Value Before Clicking on Submit Button!!"
            return render_template("dateform.html", warning=warning)

        date_info_dt = datetime.strptime(date_info_str, "%Y-%m-%d").date()      # Datepicker Returned Date String Object formatted to Date Object    

        date_info_dt_min = datetime.combine(date_info_dt, datetime.min.time())        # Datepicker Returned Date String Object formatted to Datetime Object Min Value
        date_info_dt_max = datetime.combine(date_info_dt, datetime.max.time())        # Datepicker Returned Date String Object formatted to Datetime Object Max Value

        # CSV files to pandas dataframes and validate dataframes

        if hd.check_file_name("orders") and hd.check_file_format("orders.csv"):
            df_orders = hd.write_csv_to_df("orders")
            hd.validate_df(df_orders,"id", "created_at", "vendor_id", "customer_id")
        
        if hd.check_file_name("order_lines") and hd.check_file_format("order_lines.csv"):
            df_order_lines = hd.write_csv_to_df("order_lines")
            hd.validate_df(df_order_lines, "order_id", "product_id", "product_description", "product_price", "product_vat_rate",\
                "discount_rate", "quantity","full_price_amount", "discounted_amount", "vat_amount", "total_amount")

        if hd.check_file_name("product_promotions") and hd.check_file_format("product_promotions.csv"):
            df_product_promotions = hd.write_csv_to_df("product_promotions")
            hd.validate_df(df_product_promotions, "date", "product_id", "promotion_id")

        if hd.check_file_name("commissions") and hd.check_file_format("commissions.csv"):
            df_commissions = hd.write_csv_to_df("commissions")
            hd.validate_df(df_commissions, "date", "vendor_id", "rate")
        
        # Find the count of customers
        df_orders['created_at'] = pd.to_datetime(df_orders['created_at'])
        df_orders_betw_dt = df_orders[(df_orders['created_at'] >= date_info_dt_min) & (df_orders['created_at'] <= date_info_dt_max)]
        
        count_of_customers = df_orders_betw_dt.shape[0]

        # Find the total discounted amount, the total number of items, the average order total
        df_merged_order_lines_order = pd.merge(df_orders_betw_dt, df_order_lines, left_on="id", right_on="order_id", how="left")       # Joined order_lines.csv with orders.csv
        
        print(df_merged_order_lines_order.columns)

        # print(df_merged_order_lines_order.head(30))

        total_discount_amount = df_merged_order_lines_order["discounted_amount"].sum()
        total_number_of_items = df_merged_order_lines_order["quantity"].sum()

        total_order_amount = df_merged_order_lines_order["full_price_amount"].sum()     # The total order amount
        count_of_orders = df_merged_order_lines_order.shape[0]      # The number of orders
        avg_order_total = total_order_amount/count_of_orders        # Calculate the average order total by dividing total order amount to number of items ordered

        
        # The discount rate is multiplied with quantity to find total discount rate applied
        df_merged_order_lines_order["discount_rates"] = df_merged_order_lines_order["discount_rate"] * df_merged_order_lines_order["quantity"]

        # The total discount rate is divided by the total number of items to find the average discount rate
        total_discount_rate = df_merged_order_lines_order["discount_rates"].sum()
        discount_rate_avg = total_discount_rate/total_number_of_items

        # The orders dataframe and the commissions dataframe date values are transformed to be able to join successfuly

        # df_orders["created_at"] = pd.to_datetime(df_orders['created_at'])
        # df_orders["created_at"] = df_orders["created_at"].dt.date
        df_orders_betw_dt["created_at"] = df_orders_betw_dt["created_at"].dt.date

        df_commissions["date"] = pd.to_datetime(df_commissions["date"])
        df_commissions["date"] = df_commissions["date"].dt.date

        df_commisions_on_dt = df_commissions[df_commissions['date'] == date_info_dt]

        # Join the orders dataframe and the commissions dataframe
        df_orders_commisions_dt = pd.merge(df_orders_betw_dt, df_commisions_on_dt, left_on=['created_at','vendor_id'], right_on=['date','vendor_id'], how="left")

        # Join the orders commissions joined dataframe with the order lines dataframe
        df_orders_commisions_dt_order_lines = pd.merge(df_orders_commisions_dt, df_order_lines, left_on="id", right_on="order_id", how="left")

        # Total amount of commissions found by multiplying full price amount column with commision rate applied
        df_orders_commisions_dt_order_lines["total_amount_commisions"] = df_orders_commisions_dt_order_lines["rate"] * df_orders_commisions_dt_order_lines["full_price_amount"]
        total_amount_commisions = df_orders_commisions_dt_order_lines["total_amount_commisions"].sum()


        # Average amount of commissions found by dividing the total amount of commissions with the number of orders
        aver_amount_of_comms_per_order = total_amount_commisions/count_of_orders

        # Join the orders commissions order lines joined dataframe with the product promotions dataframe
        df_orders_commisions_dt_order_lines_product_promotions = pd.merge(df_orders_commisions_dt_order_lines,df_product_promotions,on="product_id",how="left")

        promotions_dict = {}        # Empty dictionary initialized to store promotion types as key values and total amount per promotion type

        # Found unique values of the promotion_id column of joined data frame to obtain which promotions were applied and cleaned nan values
        promotion_list = df_orders_commisions_dt_order_lines_product_promotions["promotion_id"].unique().tolist()
        promotion_list = [int(prom) for prom in promotion_list if str(prom) != "nan"]

        # Find the total amount per promotion type
        for prom in promotion_list:
            df_promotion_total_amount_calc = df_orders_commisions_dt_order_lines_product_promotions[df_orders_commisions_dt_order_lines_product_promotions["promotion_id"] == float(prom)]
            df_promotion_total_amount_calc["promotion_total_amount"] = df_promotion_total_amount_calc["rate"] * df_promotion_total_amount_calc["full_price_amount"]
            promotions_dict[str(prom)] = round(df_promotion_total_amount_calc["promotion_total_amount"].sum(), 2)

        # Found values are assigned to structured dictionary object
        response_dict["customers"] = count_of_customers
        response_dict["total_discount_amount"] = round(total_discount_amount, 2)
        response_dict["items"] = total_number_of_items.item()   # numpy.int64 to int
        response_dict["order_total_avg"] = round(avg_order_total, 2)
        response_dict["discount_rate_avg"] = hd.round_up(discount_rate_avg,2)        
        response_dict["commisions"]["total"] = round(total_amount_commisions, 2)
        response_dict["commisions"]["order_average"] = round(aver_amount_of_comms_per_order, 2)
        response_dict["commisions"]["promotions"] = promotions_dict

        # Dictionary object to required JSON format
        json_object = json.dumps(response_dict, indent = 4)
        print(json_object)

        # Date object that will go to the title of the page
        # date_info_formatted = hd.date_str_to_date_format_day_month_year(date_info_str)
        
        return jsonify(response_dict)
        # return render_template("display.html", date_info=date_info_formatted, json_object=json_object)
        # return render_template("display.html", date_info=date_info_formatted)
    else:    
        return render_template("dateform.html")

# @app.route('/display', methods = ["POST", "GET"])
# def display(date_info):
#     return render_template("display.html", date_info=date_info)

if __name__ == '__main__':
    app.run(debug=True)