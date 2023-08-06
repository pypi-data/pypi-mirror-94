# Parchment

A grid based financial tool for generating easy to use dictionary objects

## Usage

```python
import parchments
from datetime import datetime

row_index = (
    ('Debt', 'dollar', 2),
    ('Revenue', 'dollar', 2),
    ('Ratio', 'percentage', 4),
    ('Days', 'int', 0),
)

period_data = [
    200000.00,
    30000.00,
    0.7500,
    22,
]

other_period_data = [
    120000.00,
    60000.00,
    0.5000,
    14,
]

my_grid = parchments.Grid(row_index)

my_grid.add_period(datetime(2020, 4, 1), period_data)
my_grid.add_period(datetime(2020, 5, 1), other_period_data)
my_grid.add_period(datetime(2020, 6, 1), period_data)
my_grid.add_period(datetime(2020, 7, 1), other_period_data)

print(my_grid.to_dict())

```
