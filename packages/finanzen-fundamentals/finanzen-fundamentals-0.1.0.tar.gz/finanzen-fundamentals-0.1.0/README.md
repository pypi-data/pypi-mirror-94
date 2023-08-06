# Finanzen-Fundamentals
Finanzen-Fundamentals is a Python package that can be used to retrieve fundamentals of stocks. The data is fetched from [finanzen.net](https://www.finanzen.net), a German language financial news site. Note that the api is English but all data will be returned in German.

# Installation
You can easily install finanzen-fundamentals via pip: `pip install finanzen-fundamentals`

If you choose to download the source code, make sure that you have the following dependencies installed:
* requests
* BeautifulSoup
* lxml
* pandas
* numpy

You can install all of them by running: `pip install requests bs4 lxml pandas numpy`.

# Usage
## Import
After you successfully installed the package, you can include it in your projects by importing it.

```import finanzen_fundamentals.stocks as ff```

## Retrieve Fundamentals
You can retrieve the fundamentals of a single stock by running: 

```bmw_fundamentals = ff.get_fundamentals("bmw")```

This will fetch the fundamentals of BMW and save it into a Pandas DataFrame called bmw_fundamentals.
The data is split into the following categories:
* Quotes
* Key Ratios
* Income Statement
* Balance Sheet
* Other

Optionally, you can add the argument `output = "dict"`. Instead of a Pandas DataFrame, you will receive a dictionary. Every category will hold another dictionary.

```bmw_fundamentals = ff.get_fundamentals("bmw", output = "dict")```

You can also fetch estimates for expected values by using:

```bmw_estimates = ff.get_estimates("bmw")```

Again, the data will be saved as a Pandas DataFrame. If you want to receive the data as a dictionary, you could use `output = "dict"` again.

```bmw_estimates = ff.get_estimates("bmw", output = "dict")```

Note that we use stock names not stock symbols when fetching data. You can search for stock names by using

```ff.search_stock("bmw", limit = 3)```

This will return the three most matching stock names for your search. You can increase the limit to 30. If you don't give a parameter, all available data will be returned (up to 30).

## Alternative Implementation
Thanks to the contribution of [backster82](https://github.com/backster82), there is also a xml based alternative to the preceeding functions. All of the following functions will return a Pandas DataFrame. Note that get_fundamentals and get_estimates now incorporates the functionallity of the alternative implementation. Hence, you will receive deprecation warning upon using these functions.

You can obtain fundamentals like so:

```bmw_fundamentals = ff.get_fundamentals_lxml("bmw")```

Estimates can be loaded via:

```bmw_estimates = ff.get_estimates_lxml("bmw")```

Additionally, you can also load the current stock price for a vast selection of stock exchanges. For example, you can retrieve the current stock prices for BMW by using the following line of code:

```bmw_price = ff.get_current_value_lxml("bmw")```

This will give you the current price at Tradegate. However, you can change the stock exchange by entering its symbol for the "exchange" argument. If you want to obtain the current price of BMW stocks at the Frankfurt Stock Exchange, you can use the following command:

```bmw_price_frankfurt = ff.get_current_value_lxml("bmw", exchange = "FSE")```

You can find all available exchanges by inspecting the StockMarkets dictionary in `finanzen_fundamentals.statics`.


