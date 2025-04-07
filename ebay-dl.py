#PROJECT 3

import argparse
import requests
from bs4 import BeautifulSoup
import json


def parse_itemprice(text):
    '''
    Price will contain the price of the item in cents, stored as an integer (you should never use floats to store monetary values, 
    because floats can't be represented exactly in computers); if there are multiple prices listed (e.g. $54.99 to $79.99), then you 
    may select either price.

    >>> parse_itemprice('$150.00')
    15000
    >>> parse_itemprice('$198.50 to $1,529.85')
    19850
    >>> parse_itemprice('$1,234.56')
    123456
    '''
    if 'to' in text: #indicating a price range
        lower_price = text.split(' to ')[0]
    else:
        lower_price = text
    cleaned = '' #remove any commas or dollar signs
    for char in lower_price:
        if char.isdigit() or char == '.': #if char is a number or decimal
            cleaned += char
    if cleaned: #convert the extracted string to a float and then multiply by 100 to get cents
        return int(float(cleaned) * 100)
    else:
        return None

    
def parse_itemshipping(text):
    '''
    Shipping will contain the price of shipping the item in cents, stored as an integer; if the item has free shipping, 
    then this value should be 0.
    
    >>> parse_itemshipping('Free delivery in 2 days')
    0
    >>> parse_itemshipping('Free Delivery')
    0
    >>> parse_itemshipping('Freight')
    0
    >>> parse_itemshipping('$10.50 shipping')
    1050
    >>> parse_itemshipping('+$4.99 shipping estimate')
    499
    '''
    if "Free Delivery" in text or "Free delivery" in text or "Freight" in text:
        return 0

    shipping_type = ''.join([char for char in text if char.isdigit() or char == '.'])
    if shipping_type:
        try:
            return int(float(shipping_type) * 100)
        except ValueError:
            return None
    return None


def parse_itemssold(text):
    '''
    Takes as input a string and returns the number of items sold, as specified in the string.
    
    >>> parse_itemssold('38 sold')
    38
    >>> parse_itemssold('14 watchers')
    0
    >>> parse_itemssold('Almost gone')
    0
    '''
    numbers = ''
    for char in text:
        if char in '1234567890': #if char is a number
            numbers += char
    if 'sold' in text:
        return int(numbers)
    else:
        return 0


# This if statement says only run the code below when the python file is run "normally," where normally means not in the doctests
if __name__ == '__main__':


    # Get command line arguments
    parser = argparse.ArgumentParser(description='Download information from ebay and convert to JSON.')
    parser.add_argument('search_term')
    parser.add_argument('--num_pages', default=10)
    args = parser.parse_args()
    print('args.search_term=', args.search_term)
    #in terminal type: python3 Project3/ebay-dl.py hammer
    #output: args.search_term= hammer

    # List of all items found in all ebay webpages
    items = []

    # Loop over the ebay webpages
    #for page_number in range(1,11):
    for page_number in range(1,int(args.num_pages)+1):

        # Build the URL
        url = 'https://www.ebay.com/sch/i.html?_nkw='
        url += args.search_term 
        url += '&_sacat=0&_from=R40&_pgn=' 
        url += str(page_number)
        print('url=', url)

        # Download the html
        r = requests.get(url)
        status = r.status_code
        print('status=', status)
        html = r.text

        # Process the html
        soup = BeautifulSoup(html, 'html.parser') 

        # Loop over the items in the page 
        tags_items = soup.select('.s-item')
        for tag_item in tags_items:

            # Extracted items
            item_name = None
            tags_name = tag_item.select('.s-item__title')
            for tag in tags_name:
                item_name = tag.text

            item_price = 0
            tags_price = tag_item.select(".s-item__price")
            for tag in tags_price:
                item_price = parse_itemprice(tag.text)

            item_status = ''
            tags_status = tag_item.select('.s-item__subtitle')
            for tag in tags_status:
                item_status = tag.text

            item_shipping = ''
            tags_shipping = tag_item.select('.s-item__logisticsCost') + tag_item.select('.s-item__freeXDays')
            for tag in tags_shipping:
                item_shipping = parse_itemshipping(tag.text)

            freereturns = False
            tags_freereturns = tag_item.select('.s-item__free-returns')
            for tag in tags_freereturns:
                freereturns = True

            items_sold = None
            tags_itemssold = tag_item.select('.s-item__hotness')
            for tag in tags_itemssold:
                items_sold = parse_itemssold(tag.text)
                print('tag=', tag)

            item = {
                'item_name': item_name,
                'item_price': item_price,
                'item_status': item_status,
                'item_shipping': item_shipping,
                'free_returns': freereturns,
                'items_sold': items_sold,

            }
            items.append(item)


        print('len(tags_items)=', len(tags_items))
        print('len(items)=', len(items))


    # Write the json to a file
    filename = args.search_term+'.json'
    with open(filename, 'w', encoding='ascii') as f:
        f.write(json.dumps(items)) #converts a list/dictionary into a json string


