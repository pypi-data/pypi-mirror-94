QUERY FACTORY
=============

This tool should help organizing SQL queries into python projects.


USAGE
-----

You should seperate query template in a yaml file as in the following example:

```yaml
# template.yaml
description: |
  This is a simple query for demonstration purpose.

variables:
  start_date:
    description: UTC datetime string to gather data from (inclusive)
    required: true
  end_date:
    description: UTC datetime string to gather data to (exclusive)
    required: true
  category_id:
    description: Category id to filter on. If null, filter won't apply.
    required: false
    default: null
  market:
    description: Market scope (either 'pro' or 'part').
    required: false
    default: part

query_template: |
  SELECT *
  FROM db.table
  WHERE event_date >= {{ start_date }}
  AND event_date < {{ end_date }}
  AND market = {{ market }}
  {% if category_id %}
  AND category_id = {{ category_id }}
  {% endif %}
  LIMIT = 100;

```

Then get your factory up and run some queries:
```python
from query_factory import SQLQueryFactory

# factory setup.
factory = SQLQueryFactory("/path/to/template.yaml")
```

Factory carries some information about template as:
```python
>>> set(factory.required_variables)
{'end_date', 'start_date'}

>>> set(factory.optional_variables)
{'category_id'}

>>> factory.describe("start_date")
'UTC datetime string to gather data from (inclusive)'
```

Here is how you can variabilize your queries using a factory as define above:
```python
import pandas as pd

connection = connect_to_sql_query_engine()

data_2020_02_01 = pd.read_sql(
    factory(
        start_date="2020-02-01",
        end_date="2020-02-02"
    ),
    con=connection
)
data_2020_02_02_filtered_on_categ1 = pd.read_sql(
    factory(
        start_date="2020-02-02", 
        end_date="2020-02-03", 
        category_id="categ_1"
    ),
    con=connection
)
```
