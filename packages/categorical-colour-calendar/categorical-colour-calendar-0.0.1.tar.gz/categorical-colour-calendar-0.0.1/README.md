# Categorical Colour Calendar
Highlight dates on a monthly calendar from categorical events
## Setup
```
pip install categorical-colour-calendar
```
## Usage
```python
import pandas as pd
from cccalendar import draw_colour_calendar

dates = pd.date_range(start='2021-01-01', end='2021-05-01')
df = pd.Series(range(len(dates)), index=dates)
draw_colour_calendar(df, {})
```
## Development
```
pip install -e .[dev]
```

## To Do
- Check Date/Datetime compatibility
- Check DataFrame/Series compatibility
- Multiple events on one day
- Automatically assigned colours if not specified
- Tests
- Allow override of default sizing/scaling values
- Test different Python versions