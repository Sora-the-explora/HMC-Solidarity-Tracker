import datetime
from datetime import timedelta
from writespreadsheet import write_spreadsheet
from parse_payments import parse_payments

today=datetime.datetime.now()
x =  datetime.date(today.year,today.month, today.day) + timedelta(weeks=-20)
new_payments = parse_payments(x)
write_spreadsheet(new_payments)
