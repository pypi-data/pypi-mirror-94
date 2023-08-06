#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Import Modules
import re
import numpy as np
import pandas as pd
import requests
import warnings
from lxml import html
from finanzen_fundamentals.scraper import _make_soup
from . import statics


# Adjust Warnings Settings
warnings.simplefilter('once')


# Define Function to Check for Error
def _check_site(soup):
    message = soup.find("div", {"class": "special_info_box"})
    if message is not None:
        message_text = message.get_text()
        load_error = "Die gewünschte Seite konnte nicht angezeigt werden"
        if load_error in message_text:
            raise ValueError("Could not find Stock")


# Define Function to Extract GuV/Bilanz from finanzen.net
def get_fundamentals(stock: str, output = "dataframe"):
    
    # Parse User Input
    if output not in ["dataframe", "dict"]:
        raise ValueError("Please choose either 'dict' or 'dataframe' for input")
    
    # Convert name to lowercase
    stock = stock.lower()

    # Load Data
    soup = _make_soup("https://www.finanzen.net/bilanz_guv/" + stock)

    # Check for Error
    _check_site(soup)

    # Define Function to Parse Table
    def _parse_table(soup, signaler: str):
        table_dict = {}
        table = soup.find("h2", text=re.compile(signaler)).parent
        years = [int(x.get_text()) for x in table.find_all("th")[2:]]
        rows = table.find_all("tr")[1:]
        for row in rows:
            name = row.find("td", {"class": "font-bold"}).get_text()
            row_data = row.find_all("td")
            row_data = row_data[2:]
            row_data = [x.get_text() for x in row_data]
            row_data = [re.sub(r"\.", "", x) for x in row_data]
            row_data = [re.sub(",", ".", x) for x in row_data]
            row_data = [float(x) if x != "-" else None for x in row_data]
            table_dict[name] = dict(zip(years, row_data))
        return table_dict

    # Extract Stock Quote Info+
    try:
        quote_info = _parse_table(soup, "Die Aktie")
    except Exception:
        quote_info = None

    # Extract Key Ratios
    try:
        key_ratios = _parse_table(soup, "Unternehmenskennzahlen")
    except Exception:
        key_ratios = None

    # Extract Income Statement
    try:
        income_info = _parse_table(soup, "GuV")
    except Exception:
        income_info = None

    # Extract Balance Sheet
    try:
        balance_sheet = _parse_table(soup, "Bilanz")
    except Exception:
        balance_sheet = None

    # Extract Other Information
    try:
        other_info = _parse_table(soup, "sonstige Angaben")
    except Exception:
        other_info = None

    # Collect Fundamentals into single Directory
    fundamentals = {
        "Quotes": quote_info,
        "Key Ratios": key_ratios,
        "Income Statement": income_info,
        "Balance Sheet": balance_sheet,
        "Other": other_info
    }

    # Return Fundamentals if output is set to dict
    if output == "dict":
        return fundamentals
    else:
        df_list = []
        for f in fundamentals:
            for i in fundamentals[f]:
                df_tmp = pd.DataFrame({"Category": f, "Metric": i, 
                                       "Year": list(fundamentals[f][i].keys()),
                                       "Value": list(fundamentals[f][i].values())
                                      })
                df_list.append(df_tmp)
        fundamentals_df = pd.concat(df_list)
        return fundamentals_df
                


# Define Function to Extract Estimates
def get_estimates(stock: str, output = "dataframe"):
    
    # Check Input
    if output not in ["dataframe", "dict"]:
        raise ValueError("Please choose either 'dict' or 'dataframe' for input")
    
    # Convert Stock Name to Lowercase
    stock = stock.lower()

    # Load Data
    soup = _make_soup("https://www.finanzen.net/schaetzungen/" + stock)

    # Check for Error
    _check_site(soup)

    # Parse Table containing Yearly Estimates
    table_dict = {}
    table = soup.find("h1", text=re.compile("^Schätzungen")).parent
    years = table.find_all("th")[1:]
    years = [x.get_text() for x in years]
    rows = table.find_all("tr")[1:]
    for row in rows:
        fields = row.find_all("td")
        fields = [x.get_text() for x in fields]
        name = fields[0]
        row_data = fields[1:]
        row_data = [x if x != "-" else None for x in row_data]
        row_data = [re.sub("[^\d,]", "", x) if x is not None else x for x in row_data]
        row_data = [re.sub(",", ".", x) if x is not None else x for x in row_data]
        row_data = [float(x) if x is not None else x for x in row_data]
        table_dict[name] = dict(zip(years, row_data))

    # Return Estimates
    if output == "dict":
        return table_dict
    else:
        df_list = []
        for f in table_dict:
            df_tmp = pd.DataFrame({"Metric": f, 
                                   "Year": list(table_dict[f].keys()), 
                                   "Value": list(table_dict[f].values())
                                  })
            df_list.append(df_tmp)
        return pd.concat(df_list)


# Define Function to Search for Stocks
def search_stock(stock: str, limit: int = -1):
    # Convert Stock Name to Lowercase
    stock = stock.lower()

    # Make Request
    soup = _make_soup("https://www.finanzen.net/suchergebnis.asp?_search=" + stock)

    # Check for Error
    if soup.find("div", {"class": "red"}) is not None:
        if "kein Ergebnis geliefert" in soup.find("div", {"class": "red"}).get_text():
            return list()

    # Define Function to Extract Results
    result_list = []
    table_outer_div = soup.find("div", {"class": "table-responsive"})
    table = table_outer_div.find("table", {"class": "table"})
    rows = table.find_all("tr")
    for row in rows[1:]:
        cells = row.find_all("td")
        name = cells[0].get_text()
        link = cells[0].find("a")["href"]
        link = "https://www.finanzen.net" + link
        isin = cells[1].get_text()
        wkn = cells[2].get_text()
        result_list.append((name, link, isin, wkn))

    # Filter Result if limit was given
    if limit > 0:
        # Decrease limit if bigger than result
        result_len = len(result_list)
        if limit > result_len:
            limit = result_len
        result_list = result_list[0:limit]

    # Return Result List as formatted String
    names = []
    for result in result_list:
        stock_name = result[0]
        short_name = re.search("aktien/(.+)-aktie", result[1]).group(1)
        names.append({ 'name': stock_name, 'short_name': short_name, 'isin': result[2], 'wkn': result[3]})
    return names


### backster82 additional functions

def check_site_availability(url):
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


def get_parser(function, stock_name):
    base_url = "https://www.finanzen.net"

    functions = {
        "search": "/suchergebnis.asp?_search=",
        "stock": "/aktien/",
        "estimates": "/schaetzungen/",
        "fundamentals": "/bilanz_guv/",
        "index": "/index/"
    }

    if function not in functions:
        raise ValueError("Got unknown function %r in get_parser" % function)
        return 1

    check_site_availability(base_url)

    url = base_url + functions[function] + stock_name
    response = requests.get(url, verify=True)

    parser = html.fromstring(response.text)

    return parser


def get_estimates_lxml(stock: str, results=[]):
    
    # Raise DeprecationWarning
    warnings.warn("get_estimates_lxml() functionality now included in get_estimates().", 
                  DeprecationWarning)
    
    
    url = "https://www.finanzen.net/schaetzungen/" + stock

    xp_base_xpath = '//div[contains(@class, "box table-quotes")]//h1[contains(text(), "Schätzungen")]//..'
    xp_data = xp_base_xpath + '//table//tr'

    response = requests.get(url, verify=True)
    parser = html.fromstring(response.text)

    data_table = []

    header_row = 0

    for data_element in parser.xpath(xp_data):
        table_row = []
        for i in data_element:
            table_row.append(i.xpath('./text()')[0])

        if header_row != 0:
            for i in range(1, len(table_row)):
                if not table_row[i] == '-':
                    table_row[i] = table_row[i].replace(".", "").replace(",", ".")
                    table_row[i] = float(table_row[i].split(" ")[0])

        else:
            table_row[0] = "Estimation"
            header_row = 1

        data_table.append(table_row)
        dataframe = pd.DataFrame(list(map(np.ravel, data_table)))
        dataframe.columns = dataframe.iloc[0]
        dataframe.drop(dataframe.index[0], inplace=True)

    return dataframe


def get_fundamentals_lxml(stock: str, results=[]):
    
    # Raise DepreciationWarning
    warnings.warn("get_fundamentals_lxml() functionality now included in get_fundamentals().", 
                  DeprecationWarning)
    
    url = "https://www.finanzen.net/bilanz_guv/" + stock

    tables = ["Die Aktie",
              "Unternehmenskennzahlen",
              "GuV",
              "Bilanz",
              "sonstige Angaben"
              ]

    complete_data_set = []

    for table in tables:
        parser = get_parser("fundamentals", stock)

        xp_base = '//div[contains(@class, "box table-quotes")]//h2[contains(text(), "' + table + '")]//..'
        xp_head = xp_base + '//table//thead//tr'
        xp_data = xp_base + '//table//tbody'

        parsed_data_table = parser.xpath(xp_base)

        # drop second empty element in parsed_data_table
        # ToDo: find out why parser.xpath(xp_base) returns 2 elements
        # parsed_data_table.pop()

        for data_element in parsed_data_table:
            header_array = []
            table_data = []
            for i in data_element.xpath('.//table//thead//tr//th/text()'):
                header_array.append(i)

            table_data.append(header_array)

            # first table element is an checkbox so we'll drop it
            first_col = True
            for i in data_element.xpath('.//table//tr'):
                if not first_col:
                    data = i.xpath('.//td/text()')
                    for cnt in range(1, len(data)):
                        data[cnt] = data[cnt].replace(".", "").replace(",", ".")
                    table_data.append(data)
                else:
                    first_col = False

            dataframe = pd.DataFrame(list(map(np.ravel, table_data)))
            dataframe.columns = dataframe.iloc[0]
            dataframe.drop(dataframe.index[0], inplace=True)

            complete_data_set.append(dataframe)

    return pd.concat(complete_data_set, ignore_index=True)


def get_current_value_lxml(stock: str, exchange="TGT", results=[]):
    data_columns = [
        "name",
        "wkn",
        "isin",
        "symbol",
        "price",
        "currency",
        "chg_to_open",
        "chg_percent",
        "time",
        "exchange"
    ]

    url = "https://www.finanzen.net/aktien/" + stock + "-aktie" + statics.StockMarkets[exchange][
        'url_postfix']
    response = requests.get(url, verify=True)

    # sleep()
    parser = html.fromstring(response.text)
    summary_table = parser.xpath('//div[contains(@class,"row quotebox")][1]')

    i = 0

    summary_data = []

    for table_data in summary_table:
        raw_price = table_data.xpath(
            '//div[contains(@class,"row quotebox")][1]/div[contains(@class, "col-xs-5")]/text()')
        raw_currency = table_data.xpath(
            '//div[contains(@class,"row quotebox")][1]/div[contains(@class, "col-xs-5")]/span//text()')
        raw_change = table_data.xpath(
            '//div[contains(@class,"row quotebox")][1]/div[contains(@class, "col-xs-4")]/text()')
        raw_percentage = table_data.xpath(
            '//div[contains(@class,"row quotebox")][1]/div[contains(@class, "col-xs-3")]/text()')
        raw_name = table_data.xpath('//div[contains(@class, "col-sm-5")]//h1/text()')
        raw_instrument_id = table_data.xpath('//span[contains(@class, "instrument-id")]/text()')
        raw_time = table_data.xpath('//div[contains(@class,"row quotebox")]/div[4]/div[1]/text()')
        raw_exchange = table_data.xpath('//div[contains(@class,"row quotebox")]/div[4]/div[2]/text()')

        name = ''.join(raw_name).strip()
        time = ''.join(raw_time).strip()
        exchange = ''.join(raw_exchange).strip()

        instrument_id = ''.join(raw_instrument_id).strip()
        (wkn, isin) = instrument_id.split(sep='/')
        if 'Symbol' in isin:
            (isin, sym) = isin.split(sep='Symbol')
        else:
            sym = ""

        currency = ''.join(raw_currency).strip()

        summary_data = [
            name.replace('&nbsp', ''),
            wkn.replace(' ', '').replace("WKN:", ""),
            isin.replace(' ', '').replace("ISIN:", ""),
            sym.replace(' ', '').replace(":", ""),
            float(raw_price[0].replace(',', '.')),
            currency,
            float(raw_change[0].replace(',', '.').replace("±","")),
            float(raw_percentage[0].replace(',', '.').replace("±","")),
            time,
            statics.StockMarkets[exchange]['real_name']
        ]

    return pd.DataFrame(data=[summary_data], columns=data_columns)


def search_stock_lxml(stock: str, limit: int = -1, results=[]):
    indices = ["name", "fn_stock_name", "isin", "wkn"]
    df = pd.DataFrame(columns=indices)

    parser = get_parser("search", stock)

    table_xpath = '//div[contains(@class, "table")]//tr'
    summary_table = parser.xpath(table_xpath)

    if len(summary_table) == 0:
        raise ValueError("Site did find any entries for %r" % stock)

    skip_first_element = 0
    results = []

    for table_element in summary_table:
        # Todo: Find cause for the first element being [] []
        if skip_first_element == 0:
            skip_first_element = 1
        else:
            raw_name = ''.join(table_element.xpath('.//a/text()')).strip()
            raw_link = ''.join(table_element.xpath('.//a//@href')).strip()
            raw_isin = ''.join(table_element.xpath('.//td')[1].xpath('./text()')).strip()
            raw_wkn = ''.join(table_element.xpath('.//td')[2].xpath('./text()')).strip()

            fn_stock_name = raw_link.replace("/aktien/", "").replace("-aktie", "")

            if limit == 0:
                break
            elif limit > 0:
                limit = limit - 1
                df = df.append(pd.DataFrame(data=[[raw_name, fn_stock_name, raw_isin, raw_wkn]], columns=indices))
            else:
                df = df.append(pd.DataFrame(data=[[raw_name, fn_stock_name, raw_isin, raw_wkn]], columns=indices))

    return df
