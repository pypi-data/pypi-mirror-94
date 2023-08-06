import pandas as pd
from cccalendar import draw_colour_calendar
from datetime import datetime, date
my_data = pd.Series({
    datetime(2020,1,1): 'event_one',
})
colour_map = {
    'event_one': 'r',
    'event_two': 'b',
    'event_three': 'g',
    'event_four': 'y',
}
draw_colour_calendar(my_data, {})