# Project Description

A simple interface to interact with the ethereum ETL data stored in public Google BigQuery datasets. Requires a GCP Project to interact with the data.

# Setup and Installation

Firstly you must have set up a GCP project to interact with the public google BigQuery datasets using Python. To do this follow the instructions located under quick setup [here](https://pypi.org/project/google-cloud-bigquery/).


Next, install this module from PyPi.

```
pip install erc721
```

That's it, once this is setup you should be able to interact with the provided functions.

# Interactions

There are a few simple interactions provided:

```python
get_all_collection_transfers_sql(nft_token_address)
```

This fetches all of the transfers and sales for a single ERC721 token. For example to get all transfers for BAYC, pass the token address "0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d" as a string to the function.

This will extract all of the sales and transfer data for that desired collection and return it as a pandas dataframe.

Additionally a highwatermark (of the blocknumber) can be passed to this function to allow for faster batch processing from past that point only. The function will return a second value which is a new highwatermark of the highest block number returned.

```python
get_all_sales(all_data=None, collection_address=None)
```

This fetches all of the sales data and returns it as a pandas dataframe. This can either be called alone by being passed a collection address (for BAYC: collection_address="0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d") or if you have already extracted data using get_all_collection_transfers, the result of this can be passed.

```python
get_all_transfers(all_data=None, collection_address=None)
```

Working in the same way as the above function, this function returns all of the transfers (without any payment).

```python
get_all_sales_and_transfers(all_data=None, collection_address=None)
```

Working in the same way as the two above functions, this function returns two arguments all sales and all transfers respectively as two separate pandas dataframes.