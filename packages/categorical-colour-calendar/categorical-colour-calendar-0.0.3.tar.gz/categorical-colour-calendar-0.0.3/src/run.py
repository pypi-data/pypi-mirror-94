import pandas as pd
from cccalendar import draw_colour_calendar
dates = pd.date_range(start='2021-01-01', end='2021-02-01')
df = pd.Series(range(len(dates)), index=dates)
draw_colour_calendar(df, {})