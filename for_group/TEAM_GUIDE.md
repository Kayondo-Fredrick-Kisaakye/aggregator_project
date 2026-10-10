# Team Guide: How This Project Works

This is the simple version of the project for anyone who is seeing the code for the first time.

Think of this app as a mini data pipeline:

1. Get product data from a fake API
2. Get review data from a fake website
3. Clean the data
4. Calculate summary statistics
5. Save and print a final report

That is the whole project in one sentence.

---

## 1. What the app is trying to do

The project is a mock market research tool.

It simulates a real business flow where:

- a shop or app has a list of products
- each product has a name, price, and category
- each product also has a rating and number of reviews
- we want to find the best products and average prices by category

The app does not use a real database or a real internet service. Instead, it uses a local mock server that acts like a fake backend.

---

## 2. The big picture

The project is split into small files, each with one job.

### Core idea

- `mock_server.py` = fake backend that serves product and review data
- `api_fetcher.py` = fetches the product catalog from the backend
- `scraper.py` = fetches review details from the review pages
- `analyzer.py` = filters and calculates totals and averages
- `reporter.py` = creates the final report and saves it as JSON
- `main.py` = runs everything together
- `config.py` = central settings like URL and timeout values
- `data_models.py` = defines the structure of a Product

This is a very standard software design pattern:

- one file for configuration
- one file for fetching data
- one file for parsing data
- one file for logic
- one file for output

That makes the project easier to debug and easier to explain.

---

## 3. How the code flows from start to finish

### Step 1: App starts
The program begins in `main.py`.

It reads command-line arguments like:

```bash
python3 main.py --mode threads
```

or

```bash
python3 main.py --mode async
```

`--mode` tells Python whether to use:

- multiple threads
- asynchronous requests

### Step 2: Product list is fetched
`main.py` calls `fetch_all_products()` from `api_fetcher.py`.

This function does an HTTP GET request to the mock API at:

```python
http://localhost:8000/api/products
```

It gets back a list of products like:

```python
[
  {"id": 1, "name": "Freddie's Loaf", "price": 6500, "category": "Baked"},
  ...
]
```

### Step 3: Review data is fetched for each product
Now the app needs review information for each product.

That happens in two ways:

#### Threads mode
- `main.py` uses `ThreadPoolExecutor`
- it creates multiple threads
- each thread fetches reviews for one product

#### Async mode
- `main.py` uses `asyncio`
- many HTTP requests are started at the same time
- this is generally faster for I/O-heavy work

This is the part where the app shows off concurrency.

### Step 4: Product objects are created
Each product is turned into a `Product` object using the class in `data_models.py`.

This object stores:

- `id`
- `name`
- `price`
- `category`
- `avg_score`
- `review_count`

This is useful because the app can now work with clean data instead of raw dictionaries.

### Step 5: Data is analyzed
Once all products are collected, `main.py` calls functions from `analyzer.py`:

- `filter_products_with_reviews(products)`
  - removes products with zero reviews
- `calculate_avg_price_per_category(products)`
  - calculates average price per category
- `get_top_rated_products(products, top_n=5)`
  - sorts the data and keeps the top 5 highest-rated items

This is the logic that turns raw data into useful business insights.

### Step 6: Final report is generated
Finally, `reporter.py` prints the result to the terminal and saves it to `report.json`.

The output includes:

- total reviewed products
- average price per category
- top 5 highest-rated products

This answers questions like:

- Which category is the most expensive?
- Which products are the best rated?
- Which products should stand out in a market report?

---

## 4. What each file is responsible for

### `main.py`
This is the controller of the whole project.

It decides:

- which mode to run
- where to start the workflow
- when to analyze the data
- when to generate the report

So if someone asks, "Where does the project actually start?" the answer is `main.py`.

### `config.py`
This file stores the networking configuration.

It contains:

- `API_BASE_URL`
- `SCRAPER_BASE_URL`
- `REQUEST_TIMEOUT`

This is useful because the app can be configured from one place instead of hardcoding everything in many files.

### `api_fetcher.py`
This file handles the API side.

It reaches the fake product catalog and returns the raw JSON list.

The `lru_cache` decorator is used to cache repetitive requests, which helps avoid unnecessary duplicate calls.

### `scraper.py`
This file fetches the reviews of a single product page.

It uses BeautifulSoup to read the HTML and collect:

- average score
- total review count

This is the parser layer of the project.

### `mock_server.py`
This is the fake backend.

It runs a local HTTP server on port 8000 and serves:

- `/api/products` for product data
- `/reviews/<id>` for review HTML

Without this file, the app would have no data source to work with.

### `data_models.py`
This is the product blueprint.

The class `Product` stores the data in a clean and predictable structure.

This makes it much easier to pass values between functions.

### `analyzer.py`
This is the brain of the project.

It uses functional programming concepts like:

- `filter`
- `map`
- `reduce`

to do calculations and clean the dataset.

### `reporter.py`
This converts the analysis into a readable output.

It prints the final report and writes it as JSON so the results can be saved or reused later.

---

## 5. Why the code is split like this

This is one of the most important ideas in the project.

The app follows a clean separation of responsibilities:

- data retrieval
- data parsing
- data processing
- output generation

This is good software design because:

- each file is easier to understand
- bugs are easier to find
- features can be added without rewriting everything
- the project looks professional and structured

If everything lived in one giant file, the code would be messy and difficult to maintain.

---

## 6. Why threads and async were both used

The project is designed to show two ways to do parallel work.

### Threads mode
This uses Python's `ThreadPoolExecutor`.

It is useful when a task is waiting on network I/O, which is slow compared to CPU operations.

### Async mode
This uses `asyncio` and `aiohttp`.

It is also designed for I/O-bound work and can be more efficient for many simultaneous requests.

The teacher is probably checking whether we understand that concurrency exists and that network requests do not all have to run one by one.

---

## 7. The most important lesson in the project

The project is not just about scraping data.

The real lesson is:

- collect raw data
- make it structured
- process it
- derive insights
- present the result clearly

That is the general workflow of data-driven applications.

---

## 8. How to explain it in class in 1 minute

Use this simple speech:

> This project is a small data pipeline. We start with a fake backend that provides product data and review pages. The app fetches product information, then scrapes review details for each product. It turns that raw data into structured Product objects, filters out products without reviews, calculates averages by category, ranks the top-rated products, and finally prints and saves a report. We also built two execution styles: a threaded version and an async version, to show how parallel processing can be done in Python.

That is enough to sound confident and clear.

---

## 9. What to say when the teacher asks, “Why is this useful?”

Because this is a realistic example of how a data system works in real life:

- fetch raw inputs
- clean and transform them
- analyze them
- present them for decision-making

This same pattern is used in data engineering, analytics, and product reporting systems.

---

## 10. Quick reminder: how to run it

Start the mock server first:

```bash
python3 mock_server.py
```

Then run the app:

```bash
python3 main.py --mode threads
```

or

```bash
python3 main.py --mode async
```

If you need the dependencies installed:

```bash
pip install -r requirements.txt
```

---

## 11. Final takeaway

This project is a small but complete example of:

- fetching data
- parsing HTML
- structuring objects
- analyzing results
- generating a report

The real value is not only the code itself, but the fact that it shows how real software is built in layers.

That is the big picture.
