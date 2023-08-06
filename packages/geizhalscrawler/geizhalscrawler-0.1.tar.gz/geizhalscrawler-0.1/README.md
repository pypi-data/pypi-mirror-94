# geizhalscrawler

The geizhalscrawler library will give you the best price of a product from Geizhals.eu website.
This information can be used in automations, e.g. to notify you when a price drops.


## Install

```bash
pip install geizhalscrawler
```

## Usage

```python
from geizhalscrawler import Geizhals

# setup the product data
ID_or_URL = 'https://geizhals.de/ducky-one-2-sf-pbt-dkon1967st-bdepdazt1-a2194110.html'

# the id of the product is also valid
#ID_or_URL = 2194110

# possible values: AT/EU/DE/UK/PL
locale = 'DE'

# parse the data
obj = Geizhals(ID_or_URL, locale)
device = obj.parse()

# print the available product information
print(device)
```

Get the `product_id` from the geizhals website of your chosen product by opening the *Price History* in a new browser tab (right-click on the price history > open in new tab).
The URL of this site reveals the ID, e.g. `https://geizhals.de/?phist=2194110` with a `product_id` of `2194110`.
