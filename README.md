# Project 3: Webscraping

## What my ebay-dl.py file does:
This project focuses on collecting and analyzing eBay marketplace data for specific keywords. Using a Python script (ebay-dl.py), I automated the process of scraping item listings from the first 10 pages of eBay search results for given search terms. The script extracts relevant details about each item—such as the name, price (in cents), item status (Brand New, Pre-owned, etc.), shipping cost, whether or not the item has free returns, and the number of items sold. It then compiles this information into a structured JSON file. My repository includes three of these files, each corresponding to one of the keywords I searched: "beach chair," "sunglasses," and "swimsuit." These files were generated by running the script with each keyword as input.


## How to run my ebay-dl.py file:
```
python3 Project3/ebay-dl.py 'beach chair'
python3 Project3/ebay-dl.py 'sunglasses'
python3 Project3/ebay-dl.py 'swimsuit'
```

## Learn more about this project:
Visit the project instructions page [here](https://github.com/mikeizbicki/cmc-csci040/tree/2025spring/project_03_webscraping).