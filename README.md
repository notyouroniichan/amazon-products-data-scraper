
# Amazon.in Product Scraping Bot

This project is designed to scrape product data from Amazon India based on specific search queries. The script uses ```undetected_chromedriver```, ```Selenium```, and ```BeautifulSoup``` to extract product details such as product name, price, rating, company, and additional product options. The extracted data is stored in CSV format for further analysis or use.


## Objective

The primary goal of this script is to automate the process of gathering detailed information about products listed on Amazon, such as :

- **Page Number :** The page number from where the data is scraped.
- **Company :** The brand or company name associated with the product.
- **Product Name :** The name of the product being sold.
- **Price :** The price of the product.
- **Sponsored :** Information on whether the product is sponsored.
- **Ratings :** The user ratings (out of 5 stars).
- **Number of Global Ratings :** Total number of user ratings for the product.
- **Number of Product Options :** Additional number options such as colors, patterns, or variants available for the product.
- **Delivery Type :** Whether the product qualifies for free delivery or not.
## Steps and Approach

1. ***Set Up the Environment :***
    
    - The script uses ```undetected_chromedriver``` to initialize the Chrome WebDriver. The reason for using this library is to bypass bot detection mechanisms on Amazon, allowing for uninterrupted scraping of data.
    - The Chrome options are set to run headless (without opening a browser window), ensuring faster and more efficient scraping.

2. ***Short Names Input :***

    - Product queries (short names) are read from a file named ```Short_Names.txt```. The script expects this file to contain product search terms, which will be used to generate Amazon search URLs.
    - The names are cleaned by removing single or double quotes and splitting them into a list.

3. ***Web Scraping Using Selenium :***

    - The script navigates to Amazon search result pages for each product query using Selenium.
    - For each search query, it scrapes the first three pages of results. On each page, it identifies all product listings by targeting specific HTML elements (using XPath).
    - For each product listing, the script extracts relevant details like : *Company name, Product name, Price, Ratings, Product options, Number of global ratings, Delivery type, Sponsored*

4. ***BeautifulSoup for HTML Parsing :***
For certain elements like product ratings and additional options, the script uses ```BeautifulSoup``` to parse the HTML content (```outerHTML```). This helps extract data that may not be accessible directly through Selenium's ```find_element``` methods.

5. ***Error Handling :***

    - The script is equipped with basic error handling to ensure that it continues running even if some elements are missing or there's an issue while extracting specific data. If a product lacks certain information, the script safely assigns a default value (e.g., "No product name" or "No price").
    - All exceptions are logged to assist with debugging if the script fails to extract some product data.

6. ***Storing Results in CSV :***
Once the scraping is done, the data is stored in CSV format using ```pandas```. Each query generates a separate CSV file named after the search term, making it easy to identify and organize the results.


## Run the code
Navigate to your root folder and open a terminal

- **Install dependencies :** Install the required libraries by running
```
pip install undetected-chromedriver selenium beautifulsoup4 pandas
```

- **Run the Script :** In terminal run the following command
```
python main.py
```

- **Output :**
    The script will generate CSV files for each product search term. Each CSV file will contain the scraped product data, including the product name, price, ratings, etc.
## Key Functions

- ```setup_driver()```: Sets up and returns a headless Chrome WebDriver for scraping.
- ```read_short_names()```: Reads the list of product search queries from ```Short_Names.txt```.
- ```scrape_product_info()```: Handles the scraping of data for a single product search query, processing multiple pages.
- ```scrape_page()```: Extracts product information from individual pages of search results.
- ```extract_product_data()```: Extracts individual product details from a product listing using XPath.
- ```parse_html()```: Parses specific HTML content using ```BeautifulSoup``` to extract data like ratings and product options.
## Error Handling and Improvements

- **Error handling :** Each function has basic error handling to catch and log exceptions. This ensures that the script continues execution even if some elements fail to load or data is missing.
- **Efficiency :** The script runs headlessly and minimizes waiting times between requests, but could be further optimized by handling asynchronous requests or parallelizing the scraping process for larger datasets.
- **Scalability :** Currently, the script is set to scrape three pages of results for each query. This can easily be adjusted by modifying the loop in the ```scrape_product_info()``` function.
- **Parallel Processing :** To scrape larger datasets, consider implementing multithreading or multiprocessing to handle multiple queries simultaneously.
- **Dynamic User Input :** Allow the user to input search queries directly from the terminal or GUI rather than reading from a file.


> This tool helps you easily gather information about products on Amazon. You can use it to compare different items or analyze product data.