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

## Output

```python
{
    "row_data": {
        "Debt": [
            {
                "actual_number": True,
                "period_key": "20200401",
                "value_amount": {
                    "raw": 200000.0,
                    "clean": 200000.0,
                    "verbose": "$200,000.00",
                    "type": "dollar",
                    "decimals": 2,
                },
                "growth_amount": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "$0.00",
                    "type": "dollar",
                    "decimals": 2,
                },
                "growth_percentage": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 4,
                },
                "over_growth_amount": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "$0.00",
                    "type": "dollar",
                    "decimals": 2,
                },
                "over_growth_percentage": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 4,
                },
            },
            {
                "actual_number": True,
                "period_key": "20200501",
                "value_amount": {
                    "raw": 120000.0,
                    "clean": 120000.0,
                    "verbose": "$120,000.00",
                    "type": "dollar",
                    "decimals": 2,
                },
                "growth_amount": {
                    "raw": -80000.0,
                    "clean": -80000.0,
                    "verbose": "$-80,000.00",
                    "type": "dollar",
                    "decimals": 2,
                },
                "growth_percentage": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 4,
                },
                "over_growth_amount": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "$0.00",
                    "type": "dollar",
                    "decimals": 2,
                },
                "over_growth_percentage": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 4,
                },
            },
            {
                "actual_number": True,
                "period_key": "20210401",
                "value_amount": {
                    "raw": 120000.0,
                    "clean": 120000.0,
                    "verbose": "$120,000.00",
                    "type": "dollar",
                    "decimals": 2,
                },
                "over_growth_amount": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "$0.00",
                    "type": "dollar",
                    "decimals": 2,
                },
                "over_growth_percentage": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 4,
                },
                "growth_amount": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "$0.00",
                    "type": "dollar",
                    "decimals": 2,
                },
                "growth_percentage": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 4,
                },
            },
            {
                "actual_number": True,
                "period_key": "20210501",
                "value_amount": {
                    "raw": 200000.0,
                    "clean": 200000.0,
                    "verbose": "$200,000.00",
                    "type": "dollar",
                    "decimals": 2,
                },
                "over_growth_amount": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "$0.00",
                    "type": "dollar",
                    "decimals": 2,
                },
                "over_growth_percentage": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 4,
                },
                "growth_amount": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "$0.00",
                    "type": "dollar",
                    "decimals": 2,
                },
                "growth_percentage": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 4,
                },
            },
        ],
        "Revenue": [
            {
                "actual_number": True,
                "period_key": "20200401",
                "value_amount": {
                    "raw": 30000.0,
                    "clean": 30000.0,
                    "verbose": "$30,000.00",
                    "type": "dollar",
                    "decimals": 2,
                },
                "growth_amount": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "$0.00",
                    "type": "dollar",
                    "decimals": 2,
                },
                "growth_percentage": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 4,
                },
                "over_growth_amount": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "$0.00",
                    "type": "dollar",
                    "decimals": 2,
                },
                "over_growth_percentage": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 4,
                },
            },
            {
                "actual_number": True,
                "period_key": "20200501",
                "value_amount": {
                    "raw": 60000.0,
                    "clean": 60000.0,
                    "verbose": "$60,000.00",
                    "type": "dollar",
                    "decimals": 2,
                },
                "growth_amount": {
                    "raw": 30000.0,
                    "clean": 30000.0,
                    "verbose": "$30,000.00",
                    "type": "dollar",
                    "decimals": 2,
                },
                "growth_percentage": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 4,
                },
                "over_growth_amount": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "$0.00",
                    "type": "dollar",
                    "decimals": 2,
                },
                "over_growth_percentage": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 4,
                },
            },
            {
                "actual_number": True,
                "period_key": "20210401",
                "value_amount": {
                    "raw": 60000.0,
                    "clean": 60000.0,
                    "verbose": "$60,000.00",
                    "type": "dollar",
                    "decimals": 2,
                },
                "over_growth_amount": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "$0.00",
                    "type": "dollar",
                    "decimals": 2,
                },
                "over_growth_percentage": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 4,
                },
                "growth_amount": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "$0.00",
                    "type": "dollar",
                    "decimals": 2,
                },
                "growth_percentage": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 4,
                },
            },
            {
                "actual_number": True,
                "period_key": "20210501",
                "value_amount": {
                    "raw": 30000.0,
                    "clean": 30000.0,
                    "verbose": "$30,000.00",
                    "type": "dollar",
                    "decimals": 2,
                },
                "over_growth_amount": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "$0.00",
                    "type": "dollar",
                    "decimals": 2,
                },
                "over_growth_percentage": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 4,
                },
                "growth_amount": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "$0.00",
                    "type": "dollar",
                    "decimals": 2,
                },
                "growth_percentage": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 4,
                },
            },
        ],
        "Ratio": [
            {
                "actual_number": True,
                "period_key": "20200401",
                "value_amount": {
                    "raw": 0.75,
                    "clean": 0.75,
                    "verbose": "75.0000%",
                    "type": "percentage",
                    "decimals": 2,
                },
                "growth_amount": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 2,
                },
                "growth_percentage": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 4,
                },
                "over_growth_amount": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 2,
                },
                "over_growth_percentage": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 4,
                },
            },
            {
                "actual_number": True,
                "period_key": "20200501",
                "value_amount": {
                    "raw": 0.5,
                    "clean": 0.5,
                    "verbose": "50.0000%",
                    "type": "percentage",
                    "decimals": 2,
                },
                "growth_amount": {
                    "raw": -0.25,
                    "clean": -0.25,
                    "verbose": "-25.0000%",
                    "type": "percentage",
                    "decimals": 2,
                },
                "growth_percentage": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 4,
                },
                "over_growth_amount": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 2,
                },
                "over_growth_percentage": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 4,
                },
            },
            {
                "actual_number": True,
                "period_key": "20210401",
                "value_amount": {
                    "raw": 0.5,
                    "clean": 0.5,
                    "verbose": "50.0000%",
                    "type": "percentage",
                    "decimals": 2,
                },
                "over_growth_amount": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 2,
                },
                "over_growth_percentage": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 4,
                },
                "growth_amount": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 2,
                },
                "growth_percentage": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 4,
                },
            },
            {
                "actual_number": True,
                "period_key": "20210501",
                "value_amount": {
                    "raw": 0.75,
                    "clean": 0.75,
                    "verbose": "75.0000%",
                    "type": "percentage",
                    "decimals": 2,
                },
                "over_growth_amount": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 2,
                },
                "over_growth_percentage": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 4,
                },
                "growth_amount": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 2,
                },
                "growth_percentage": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 4,
                },
            },
        ],
        "Days": [
            {
                "actual_number": True,
                "period_key": "20200401",
                "value_amount": {
                    "raw": 22,
                    "clean": 22,
                    "verbose": "22",
                    "type": "int",
                    "decimals": 2,
                },
                "growth_amount": {
                    "raw": 0,
                    "clean": 0,
                    "verbose": "0",
                    "type": "int",
                    "decimals": 2,
                },
                "growth_percentage": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 4,
                },
                "over_growth_amount": {
                    "raw": 0,
                    "clean": 0,
                    "verbose": "0",
                    "type": "int",
                    "decimals": 2,
                },
                "over_growth_percentage": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 4,
                },
            },
            {
                "actual_number": True,
                "period_key": "20200501",
                "value_amount": {
                    "raw": 14,
                    "clean": 14,
                    "verbose": "14",
                    "type": "int",
                    "decimals": 2,
                },
                "growth_amount": {
                    "raw": -8,
                    "clean": -8,
                    "verbose": "-8",
                    "type": "int",
                    "decimals": 2,
                },
                "growth_percentage": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 4,
                },
                "over_growth_amount": {
                    "raw": 0,
                    "clean": 0,
                    "verbose": "0",
                    "type": "int",
                    "decimals": 2,
                },
                "over_growth_percentage": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 4,
                },
            },
            {
                "actual_number": True,
                "period_key": "20210401",
                "value_amount": {
                    "raw": 14,
                    "clean": 14,
                    "verbose": "14",
                    "type": "int",
                    "decimals": 2,
                },
                "over_growth_amount": {
                    "raw": 0,
                    "clean": 0,
                    "verbose": "0",
                    "type": "int",
                    "decimals": 2,
                },
                "over_growth_percentage": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 4,
                },
                "growth_amount": {
                    "raw": 0,
                    "clean": 0,
                    "verbose": "0",
                    "type": "int",
                    "decimals": 2,
                },
                "growth_percentage": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 4,
                },
            },
            {
                "actual_number": True,
                "period_key": "20210501",
                "value_amount": {
                    "raw": 22,
                    "clean": 22,
                    "verbose": "22",
                    "type": "int",
                    "decimals": 2,
                },
                "over_growth_amount": {
                    "raw": 0,
                    "clean": 0,
                    "verbose": "0",
                    "type": "int",
                    "decimals": 2,
                },
                "over_growth_percentage": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 4,
                },
                "growth_amount": {
                    "raw": 0,
                    "clean": 0,
                    "verbose": "0",
                    "type": "int",
                    "decimals": 2,
                },
                "growth_percentage": {
                    "raw": 0.0,
                    "clean": 0.0,
                    "verbose": "0.0000%",
                    "type": "percentage",
                    "decimals": 4,
                },
            },
        ],
    },
    "column_index": ["20200401", "20200501", "20210401", "20210501"],
}
```
