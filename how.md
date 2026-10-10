# How the Aggregator Project Works

This document explains what we built, how we debugged it, and why the project is structured the way it is.

## 1. The project goal

This app is meant to:

- fetch product data from a mock API
- fetch product review information from a mock review page
- clean and analyze the results
- generate a summary report

The project simulates a real-world data pipeline, but keeps everything local so it can run without internet access.

---

## 2. What we started with

The project had these files:

- `main.py` — application entry point
- `config.py` — URLs and timeout settings
- `api_fetcher.py` — fetches product list from API
- `scraper.py` — fetches reviews from review pages
- `mock_server.py` — local fake API and review site
- `data_models.py` — Product model
- `analyzer.py` — filtering and summary logic
- `reporter.py` — print and save the final report

At first, the app had several errors due to wrong variable names, function names, and code placed outside its proper execution block.

---

## 3. The debugging journey

### Problem 1: `args` was not defined
The main issue was that the app did this:

```python
if args.profile:
```

but `args` was never created, because the parser and `parse_args()` call were not correctly placed inside `main()`.

This caused:

```python
NameError: name 'args' is not defined
```

### Problem 2: wrong function names
The code called functions that did not exist or had different names:

- `execute.map(...)` instead of `executor.map(...)`
- `run_threaded_mode()` instead of `run_thread_mode()`
- `_fetch_and_scrape_async(...)` instead of `fetch_and_scrape_async(...)`

This is a common Python mistake: you know the intention, but the names do not match the actual function definitions.

### Problem 3: `hepl` typo
This line had a typo:

```python
parser.add_argument("--mode", ..., hepl="Execution mode")
```

`hepl` should be `help`.

### Problem 4: wrong HTML ID name
The async scraper looked for:

```python
id="review__count"
```

but the mock server was serving:

```html
<span id="review-count">...</span>
```

The mismatch meant the app could not read the review count, although in this project the server is consistent and the fix was needed for correctness.

### Problem 5: port 8000 already in use
When we started the mock server again, Python raised:

```python
OSError: [Errno 98] Address already in use
```

This means another process was already listening on port 8000.

The fix was:

```bash
fuser -k 8000/tcp
```

Then start the server again.

---

## 4. What we fixed

We corrected the project by:

- parsing CLI arguments inside `main()`
- using the correct functions and variable names
- keeping the async scraper consistent with the mock HTML
- ensuring profile code only runs after argument parsing
- starting the server on a clean port

After that, the app ran successfully in both modes:

- `--mode threads`
- `--mode async`

---

## 5. How the app works

### Step 1: server starts
The mock server provides fake data:

- `/api/products` returns a list of products
- `/reviews/<id>` returns HTML with review score and review count

This simulates a real API and website backend.

### Step 2: app starts from `main.py`
`main.py` is the entry point.

It reads command-line arguments:

```bash
python3 main.py --mode async
```

This tells Python which execution style to use.

### Step 3: data is fetched
There are two modes:

#### Threads mode
Uses multiple threads to fetch each product’s review details in parallel.

#### Async mode
Uses `asyncio` and `aiohttp` to fetch many review pages concurrently without blocking.

This is useful because network requests are slow compared to CPU work.

### Step 4: product objects are created
The `Product` class in `data_models.py` stores data like:

- `id`
- `name`
- `price`
- `category`
- `avg_score`
- `review_count`

This is a clean, lightweight structure to hold product data.

### Step 5: analysis happens
`analyzer.py` removes products with zero reviews and calculates:

- valid products with reviews
- average price by category
- top-rated products

The functions are simple but important:

- `filter_products_with_reviews()`
- `calculate_avg_price_per_category()`
- `get_top_rated_products()`

### Step 6: report is generated
`reporter.py` prints a summary to the console and writes it to `report.json`.

This makes the project useful as a real data workflow: fetch, process, analyze, display.

---

## 6. Why we did it this way

### 1. Because Python programs need structure
The biggest lesson is that Python executes top-to-bottom. If something depends on `args` or a function name, it must exist before that line runs.

This is why code was moved into `main()`.

### 2. Because real projects use separate responsibilities
Each file has one job:

- config for configuration
- API fetcher for HTTP calls
- scraper for HTML parsing
- analyzer for logic
- reporter for output

This makes it easier to add features, debug errors, and reuse pieces.

### 3. Because concurrency is useful in real data workflows
Fetching data from many URLs is slower than processing the data itself. Threading and async help run work in parallel.

That is why both modes exist in `main.py`.

### 4. Because mock servers teach us real architecture
This project simulates a real system using local fake endpoints. That makes it perfect for learning without needing a production backend.

---

## 7. How to run it

Start the server first:

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

Optional profiling:

```bash
python3 main.py --mode async --profile
```

---

## 8. Beginner-friendly summary

Think of the app like this:

1. The fake website gives us data.
2. The app asks for that data.
3. It reads product ratings from review pages.
4. It turns that into Python objects.
5. It filters and analyzes the data.
6. It prints a final report.

This is the same core idea behind many real Python projects: fetch data, clean it, analyze it, and produce results.

---

## 9. Final lesson

The most important lesson from our debugging is this:

> Python does not guess what you mean. Names must match exactly, and code must be in the right place.

That is why the project was fixed by checking:

- function names
- variable names
- placement of code
- matching server IDs and URLs
- port availability

Once those are aligned, the project works smoothly.

If you keep practicing this pattern, you will get much faster at spotting bugs in Python projects.
