from google.cloud import bigquery

transactions_table_id = "bigquery-public-data.crypto_ethereum.transactions"
token_transfers_table_id = "bigquery-public-data.crypto_ethereum.token_transfers"

def get_all_collection_transfers_sql(nft_token_address, highwatermark=None):
    """
    Function to get all transfers of a specific ERC721 token
    :param nft_token_address: ERC721 token address
    :return all_data_df: DataFrame with all sales and transfers of the ERC721 token
    """
    client = bigquery.Client()
    
    if not highwatermark:
        query = f"""
        SELECT transactions.value, transactions.`hash`, transactions.gas, 
        token_transfers.*
        FROM {token_transfers_table_id}
        FULL OUTER JOIN {transactions_table_id}
        ON token_transfers.transaction_hash = transactions.hash
        WHERE token_address = "{nft_token_address}";
        """
    else:
        query = f"""
        SELECT transactions.value, transactions.`hash`, transactions.gas, 
        token_transfers.*
        FROM {token_transfers_table_id}
        FULL OUTER JOIN {transactions_table_id}
        ON token_transfers.transaction_hash = transactions.hash
        WHERE token_address = "{nft_token_address}" AND token_transfers.block_number > {highwatermark} AND transactions.block_number > {highwatermark};
        """
    
    # get all BAYC transactions
    all_data_df = (
        client.query(query)
        .result()
        .to_dataframe(
            create_bqstorage_client=True,
        )
    )
    
    # convert wei to ether
    all_data_df["ether"] = all_data_df["value"] / 10 ** 18
    # rename value_1 to token id of ERC721 token
    all_data_df.rename({"value_1": "token_id"}, inplace=True)
    
    # drop duplicate or renamed/revalued columns
    all_data_df.drop(columns=["value"], inplace=True)
    all_data_df.drop(columns=["hash"], inplace=True)
    all_data_df.drop(columns=["value_1"], inplace=True)
    
    new_highwatermark = all_data_df["block_number"].max()
    
    return all_data_df, new_highwatermark


def get_all_sales(all_data=None, collection_address=None, highwatermark=None):
    """
    Take a dataframe of all sales or a collection address of an ERC721 token and output a dataframe
    with the sales data for that specific ERC721 token
    :param all_data: DataFrame with all sales and transfers of an ERC721 token
    :param collection_address: ERC721 token address
    :return all_erc721_sales: Return dataframe containing all sales data for the desired ERC721 token
    """
    if all_data:
        all_erc721_sales = all_data[all_data["ether"] != 0]
        return all_erc721_sales
    if collection_address:
        all_data = get_all_collection_transfers_sql(collection_address, highwatermark=highwatermark)
        all_erc721_sales = all_data[all_data["ether"] != 0]
        return all_erc721_sales
    return "Either all_data or collection_address must not be null."


def get_all_transfers(all_data=None, collection_address=None, highwatermark=None):
    """
    Take a dataframe of all transfers or a collection address of an ERC721 token and output a dataframe
    with the transfer data for that specific ERC721 token
    :param all_data: DataFrame with all sales and transfers of an ERC721 token
    :param collection_address: ERC721 token address
    :return all_erc721_transfers: Return dataframe containing all transfer data for the desired ERC721 token
    """
    if all_data:
        all_erc721_transfers = all_data[all_data["ether"] == 0]
        return all_erc721_transfers
    if collection_address:
        all_data = get_all_collection_transfers_sql(collection_address, highwatermark=highwatermark)
        all_erc721_transfers = all_data[all_data["ether"] == 0]
        return all_erc721_transfers
    return "Either all_data or collection_address must not be null."

def get_all_sales_and_transfers(collection_address=None, all_data=None, highwatermark=None):
    """
    Take a collection address of an ERC721 token and output a dataframe
    with the transfer and sales data for that specific ERC721 token
    :param collection_address: ERC721 token address
    :return all_erc721_sales: Return dataframe containing all sales data for the desired ERC721 token
    :return all_erc721_transfers: Return dataframe containing all transfer data for the desired ERC721 token
    """
    if collection_address:
        all_data = get_all_collection_transfers_sql(collection_address, highwatermark=highwatermark)
        all_erc721_sales = get_all_sales(all_data, None)
        all_erc721_transfers = get_all_transfers(all_data, None)
        return all_erc721_sales, all_erc721_transfers
    if all_data:
        all_erc721_sales = get_all_sales(all_data, None)
        all_erc721_transfers = get_all_transfers(all_data, None)
        return all_erc721_sales, all_erc721_transfers
    return "Either all_data or collection_address must not be null."
    
        
    
def get_all_sales_of_value(max, min=0, sales_data=None, collection_address=None, highwatermark=None):
    """
    Get all sales of tokens which are of a certain value
    :param max: Maximum value of the token
    :param min: Minimum value of the token (default = 0)
    :param sales_data: DataFrame with all sales of an ERC721 token
    :return all_erc721_sales: Return dataframe containing all sales data for the desired ERC721 token
    """
    if sales_data:
        filtered_erc721_sales = sales_data[(sales_data["ether"] <= max) & (sales_data["ether"] >= min)]
        return filtered_erc721_sales
    if collection_address:
        all_erc721_sales = get_all_sales(collection_address=collection_address, highwatermark=highwatermark)
        filtered_erc721_sales = all_erc721_sales[(all_erc721_sales["ether"] <= max) & (all_erc721_sales["ether"] >= min)]
        return filtered_erc721_sales
        
    return "sales_data or collection_address must not be null."
