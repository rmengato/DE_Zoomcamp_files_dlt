# -*- coding: utf-8 -*-
"""DEZoomcamp: dlt - Homework_rmengato.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1cd0xlj0kGL8iO7YORjbhDvS0tT9BMChh

# **Workshop "Data Ingestion with dlt": Homework**

---

## **Dataset & API**

We’ll use **NYC Taxi data** via the same custom API from the workshop:

🔹 **Base API URL:**  
```
https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api
```
🔹 **Data format:** Paginated JSON (1,000 records per page).  
🔹 **API Pagination:** Stop when an empty page is returned.

## **Question 1: dlt Version**

1. **Install dlt**:
"""

!pip install dlt[duckdb]

"""> Or choose a different bracket—`bigquery`, `redshift`, etc.—if you prefer another primary destination. For this assignment, we’ll still do a quick test with DuckDB.

2. **Check** the version:

"""

!dlt --version

"""or:"""

import dlt
print("dlt version:", dlt.__version__)

"""**Answer**:  
- Provide the **version** you see in the output.

## **Question 2: Define & Run the Pipeline (NYC Taxi API)**

Use dlt to extract all pages of data from the API.

Steps:

1️⃣ Use the `@dlt.resource` decorator to define the API source.

2️⃣ Implement automatic pagination using dlt's built-in REST client.

3️⃣ Load the extracted data into DuckDB for querying.
"""

import dlt
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.paginators import PageNumberPaginator


# your code is here
#print(help(dlt.resource))
#print(help(dlt.sources.helpers.rest_client))

@dlt.resource(name="rides")   # <--- The name of the resource (will be used as the table name)
def ny_taxi():
    client = RESTClient(
        base_url="https://us-central1-dlthub-analytics.cloudfunctions.net",
        paginator=PageNumberPaginator(
            base_page=1,
            total_path=None
        )
    )

    for page in client.paginate("data_engineering_zoomcamp_api"):    # <--- API endpoint for retrieving taxi ride data
        yield page   # <--- yield data to manage memory

"""
#based on dlt documentation for PageNumberPaginator
client = RESTClient(
    base_url="https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api",
    paginator=PageNumberPaginator(
        total_path="total_pages"
    )
)

@dlt.resource(name = "rides")
def ny_taxi():
    for page in client.paginate("/items", params={"size": 1000}):
        yield page


pipeline = dlt.pipeline(
    pipeline_name="ny_taxi_pipeline",
    destination="duckdb",
    dataset_name="ny_taxi_data"
)

"""

"""Load the data into DuckDB to test:





"""

load_info = pipeline.run(ny_taxi)
print(load_info)

"""

```
# Isto` está formatado como código`
```

Start a connection to your database using native `duckdb` connection and look what tables were generated:"""

import duckdb
from google.colab import data_table
data_table.enable_dataframe_formatter()

# A database '<pipeline_name>.duckdb' was created in working directory so just connect to it

# Connect to the DuckDB database
conn = duckdb.connect(f"{pipeline.pipeline_name}.duckdb")

# Set search path to the dataset
conn.sql(f"SET search_path = '{pipeline.dataset_name}'")

# Describe the dataset
conn.sql("DESCRIBE").df()



#get number of tables within ny_taxi_pipeline
#conn.sql("SELECT * FROM rides")

"""**Answer:**
* How many tables were created?

## **Question 3: Explore the loaded data**

Inspect the table `ride`:
"""

df = pipeline.dataset(dataset_type="default").rides.df()
df

"""**Answer:**
* What is the total number of records extracted?

## **Question 4: Trip Duration Analysis**

Run the SQL query below to:

* Calculate the average trip duration in minutes.
"""

with pipeline.sql_client() as client:
    res = client.execute_sql(
            """
            SELECT
            AVG(date_diff('minute', trip_pickup_date_time, trip_dropoff_date_time))
            FROM rides;
            """
        )
    # Prints column values of the first row
    print(res)

"""**Answer:**
* What is the average trip duration?

## **Submitting the solutions**

* Form for submitting: TBA

## **Solution**

We will publish the solution here after deadline.
"""
