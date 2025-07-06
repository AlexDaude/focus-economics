from typing import List
import os
import pandas as pd
from backend.app.src.services.pdf_table_parser import PDFTableParser
from backend.app.src.services.data_frame_parser import DataFrameParser
from backend.app.src.components.database.connection import Connection





def process_and_save_page_2_and_3(file: str, dst: str, pages: List[int] = [2,3]) -> pd.DataFrame:
    """
    Run code
    """

    os.makedirs(dst, exist_ok=True)
        
    # parse pages
    pages_str = [str(p) for p in pages]
    pdf_table_parser = PDFTableParser(file)
    pdf_table_parser.extract_tables(pages=",".join(pages_str))


    # parse dataframes

    for p in pages:

        unprocessed_tables = pdf_table_parser.get_page_tables(p)

        for ut in unprocessed_tables:

            data_frame_parser = DataFrameParser(p, ut.df)
            #camelot sometimes joins tables wrongly, here they're divided
            cleaned_dfs = data_frame_parser.split_tables()
        
            for i, df in enumerate(cleaned_dfs):
                file_name = f"page-{str(p)} table-{str(i)}.csv"
                dst_file = os.path.join(dst, file_name)
                df.to_csv(dst_file, index=False)



def process_and_aggregate_page_2(file: str, src: str, dst: str) -> pd.DataFrame:
    """
    Run code
    """

    os.makedirs(dst, exist_ok=True)

    dfs = []
    for f in os.listdir(src):
        if f.find("page-2") != -1:
            full_path = os.path.join(src, f)
            tmp_df = pd.read_csv(full_path)
            tmp_df.columns = tmp_df.columns[1:].insert(0,"Asset")
            dfs.append(tmp_df)

    joined_df = pd.concat(dfs, axis=0)
    df = joined_df[["Asset", "1M", "3M", "6M", "12M", "YTD", "QTD"]]

    df = df.sort_values(
        by="12M",
        ascending=False
    )   

    #save sorted
    file_name = "page-2 asset-performance.csv"
    dst_path = os.path.join(dst, file_name)
    df.to_csv(dst_path)

    print("------------- Top 3 assets - Last 12M -------------\n")
    print(df.head(3)[["Asset","12M"]])
    print("\n\n------------- Worst 3 assets - Last 12M -------------\n")
    print(df.tail(3)[["Asset","12M"]])





def process_and_save_pages_16_to_19(file: str, dst: str, pages: List[int] = [16,17,18,19]) -> pd.DataFrame:
    """
    Run code
    """

    os.makedirs(dst, exist_ok=True)

    # parse pages
    pages_str = [str(p) for p in pages]
    pdf_table_parser = PDFTableParser(file)
    pdf_table_parser.extract_tables(pages=",".join(pages_str))
    
    # parse dataframes

    for p in pages:

        unprocessed_tables = pdf_table_parser.get_page_tables(p)

        for ut in unprocessed_tables:

            data_frame_parser = DataFrameParser(p, ut.df)
            #camelot sometimes joins tables wrongly, here they're divided
            cleaned_dfs = data_frame_parser.split_tables()

            for i, df in enumerate(cleaned_dfs):
                file_name = f"page-{str(p)} table-{str(i)}.csv"
                dst_file = os.path.join(dst, file_name)
                df.to_csv(dst_file, index=False)


def store_data(src: str):

    connection = Connection.get_connection()

    for file in os.listdir(src):
        file_path = os.path.join(src, file)
        df = pd.read_csv(file_path)
        df.to_sql(
            file,
            con=connection
        )

if __name__ == "__main__":
    
    RESULTS = r"backend/results"
    file = r"backend/app/public/to_parse.pdf"
    process_and_save_page_2_and_3(file, r"backend/results/pages_2_3")
    process_and_aggregate_page_2(file, r"backend/results/pages_2_3", r"backend/results/page_2_asset_performance")
    process_and_save_pages_16_to_19(file, r"backend/results/pages_16_to_19")
    store_data(RESULTS)
