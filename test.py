from datetime import datetime
from dateutil.relativedelta import relativedelta

# Get the current date
current_date = datetime.now().date()

# Add 3 months to the current date
new_date = current_date + relativedelta(days=1)

print("Current date:", current_date)
print("New date after adding 3 months:", type(str(new_date)))
