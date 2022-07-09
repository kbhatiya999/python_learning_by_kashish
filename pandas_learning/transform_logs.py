import csv
from datetime import datetime

import pandas as pd

# content of abc.csv
"""
ABC,TEST,TEST2
ABC,TEST,TEST2
ABC,TEST,TEST2
"""

# Read csv and provide headers yourself
# Reference : https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
df = pd.read_csv('abc.csv', names=['A', 'B', 'C'])

# Create datetime object using utc time
# Reference: https://docs.python.org/3/library/datetime.html#datetime.datetime.now
utc_time_now = datetime.utcnow()

# Create string from datetime object
# Reference: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
str_date_time = utc_time_now.strftime('%d/%m/%Y %H:%M:%S %f')

# Insert column at a specific index
# Reference: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.insert.html#pandas-dataframe-insert
df.insert(0, 'TIMESTAMP', str_date_time)

# Print sample dataframe
print(df.head().to_string())

# Create CSV without index without quoting the value,
# for example, we do not want quotes around string.
# But we don't want to use comma inside "10/05/2022 03:24:33,687742" as start of new column
# So we provide quoting=csv.QUOTE_NONE, escapechar='|', and we will have a | for all commas that should not be treated
# as column separator
# "10/05/2022 03:24:33,687742" -> 10/05/2022 03:24:33|,687742

# TIMESTAMP,A,B,C
# "10/05/2022 03:24:33,687742",ABC,TEST,TEST2
# "10/05/2022 03:24:33,687742",ABC,TEST,TEST2
# "10/05/2022 03:24:33,687742",ABC,TEST,TEST2
df.to_csv('xyz.csv', index=False, quoting=csv.QUOTE_NONE, escapechar='|')
"""
TIMESTAMP,A,B,C
10/05/2022 03:39:09 489070,ABC,TEST,TEST2
10/05/2022 03:39:09 489070,ABC,TEST,TEST2
10/05/2022 03:39:09 489070,ABC,TEST,TEST2
"""
