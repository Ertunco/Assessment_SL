# Assessment_SL

## The Challenge
Create an endpoint that, for a given date, will return a report that will contain the following metrics.

    - The total number of items sold on that day.
    - The total number of customers that made an order that day.
    - The total amount of discount given that day.
    - The average discount rate applied to the items sold that day.
    - The average order total for that day
    - The total amount of commissions generated that day.
    - The average amount of commissions per order for that day.
    - The total amount of commissions earned per promotion that day.

Data is in CSV format and shared as a zip file.

## Setup
Clone the repository to your local computer
```
git clone https://github.com/Ertunco/Assessment_SL.git
```

Setup a virtual environment using below command.
```
python -m venv venv
```

Activate the virtual environment using below command.
```
source venv/bin/activate
```

Install the packages using requirements.txt file on the virtual environment.
```
pip install -r requirements.txt
```

## Execution

Run the app using below command.
```
python flask_app.py
```

On the browser, you can click on to enter date input
```
Press Go to Form
```

On the browser, simply pick a date or just type in a date you want the see the results for.
You can see the report for the given date both on console and the browser


## Tests

### Selenium e2e
To be able to run the selenium e2e test on test_flask_app.py, chromedriver should be installed from [here](https://chromedriver.chromium.org/downloads).

"ChromeDriver 88.0.4324.96" was used for this task but please check your chrome version before installing one.

Simply place the chromedriver on the project directory and run the test with below command.
```
python test_flask_app.py
```

### unittest
Please run the command below to see the unit tests.
```
python test_data_handler.py
```