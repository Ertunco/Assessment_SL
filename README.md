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

Run the app using below command.
```
python flask_app.py
```

On the browser, you can click on to enter date input
```
Press Go to Form
```

On the browser, simply pick a date or just type in a date you want the see the results for.
