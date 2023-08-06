import calendar
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd

from dateutils import count_months, get_week_of_month

__scale = 20


def num_to_day(num):
    # Midpoint of a polygon is at n - scale/4
    # Divide this by scale to find out how many days along we are
    return (num - (__scale / 4)) / __scale


def day_to_num(day):
    # Inverse of num_to_day
    return (day * __scale) + (__scale / 4)


def get_date_square_coordinates(day_of_week, week_of_month):
    x_start = __scale * day_of_week
    x_end = (__scale * day_of_week) + (__scale / 2)
    y_start = __scale * week_of_month
    y_end = (__scale * week_of_month) + (__scale / 2)

    bottom_left = (x_start, y_start)
    top_left = (x_start, y_end)
    top_right = (x_end, y_end)
    bottom_right = (x_end, y_start)

    centre = (((x_start + x_end) / 2), ((y_start + y_end) / 2))

    return [bottom_left, top_left, top_right, bottom_right], centre


def draw_date_square(date, data, colour_map, ax):
    day_of_week = date.weekday()
    week_of_month = get_week_of_month(date)

    corners, centre = get_date_square_coordinates(day_of_week, week_of_month)

    colour = 'm'
    if date in data.index and data[date] in colour_map:
        colour = colour_map[data[date]]

    shape = plt.Polygon(corners, color=colour)
    ax.add_patch(shape)
    ax.annotate(str(date.day), centre, color='w', weight='bold', fontsize=__scale * 0.75, ha='center', va='center')


def setup_weekday_axis(ax):
    secax = ax.secondary_xaxis('top', functions=(num_to_day, day_to_num))
    secax.set_xticks(range(7))
    secax.set_xticklabels(['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su'], fontsize=__scale)


def draw_month_calendar(data, colour_map, year, month, ax):
    month_start_day, month_num_days = calendar.monthrange(year, month)
    for day in range(1, month_num_days+1):
        current_date = datetime(year, month, day)
        draw_date_square(current_date, data, colour_map, ax)

    setup_weekday_axis(ax)
    ax.axis('scaled')
    ax.set_title(calendar.month_name[month] + ' ' + str(year), pad=20, fontsize=__scale)
    ax.axis('off')
    ax.plot()


def draw_colour_calendar(data, colour_map, months_per_row=3):
    data.index = pd.to_datetime(data.index)
    first_date = data.index.min()
    last_date = data.index.max()

    num_months = count_months(first_date, last_date)

    fig, axs = plt.subplots(int(num_months/months_per_row)+1, months_per_row, sharex=True, sharey=True, squeeze=False)

    total_axs = len(axs) * len(axs[0])  # could use months_per_row
    unused_axs = total_axs - num_months
    for u in range(unused_axs):
        axs[len(axs)-1][(months_per_row-1)-u].remove()

    month_counter = 0
    for year in range(first_date.year, last_date.year + 1):
        start_month = 1
        end_month = 12
        if year == first_date.year:
            start_month = first_date.month
        if year == last_date.year:
            end_month = last_date.month

        for month in range(start_month, end_month+1):
            axs_x = int(month_counter / months_per_row)
            axs_y = month_counter % months_per_row
            draw_month_calendar(data, colour_map, year, month, axs[axs_x][axs_y])
            month_counter = month_counter + 1

    axs[0][0].invert_yaxis()

    fig.set_size_inches(10*min(num_months, months_per_row), 10*len(axs))
    fig.set_dpi(200)
    fig.tight_layout()
    plt.show()
