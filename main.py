import datetime
from datetime import timedelta
from writespreadsheet import write_spreadsheet
from parse_payments import parse_payments
import gmailauth

def update_sheet(data, context):
    today=datetime.datetime.now()
    today = datetime.date(today.year,today.month, today.day)
    x =  datetime.date(today.year,today.month, today.day) + timedelta(weeks=-5)
    new_payments = parse_payments(x, today)
    write_spreadsheet(new_payments)

if __name__ == "__main__":
    gmailauth.main()
    update_sheet(1,1)
