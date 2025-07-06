from typing import List
import pandas as pd
from backend.app.src.schemas.page_schemas import pages_table_schema
from backend.app.src.services.pdf_table_parser import PDFTableParser

class DataFrameParser:
    def __init__(self, page: int, df: pd.DataFrame):
        self.df = df
        if page not in pages_table_schema:
            raise Exception("Schema not defined for the given page")
        self.headers = pages_table_schema[page]["headers"]
        self.parsed_dataframe = self.parse_dataframe()

    def parse_dataframe(self):
        """
        Clean dataframe, removing empty rows defined as it through a threshold, and set the header.

        """
        header_idx = None       
        threshold_empty_rows = 5 #to define what is an empty row
        empty_rows = []
        
        df = self.df.copy()

        for idx, row in df.iterrows():
            if not header_idx and row[1] in self.headers:
                header_idx = idx
            
            count = 0
            for v in row.to_list():
                if v == "":
                    count+=1
                if count == threshold_empty_rows:
                    empty_rows.append(idx)
                    break;

        

        if not header_idx:
            raise Exception("Header was not found")
        
        df.columns = df.iloc[header_idx]
        df.drop(index=range(header_idx+1), inplace=True)
        df.drop(index=[r for r in empty_rows if r > header_idx], inplace=True)
        df.reset_index(drop=True, inplace=True)

        return df


    def can_be_divided(self) -> bool:
        """
        Check if additional headers are found in the dataframe.
        Meaning tables were wrongly joined
        """
        headers_found = []
        for idx, row in self.parsed_dataframe.iterrows():
        
            if row.iloc[1] in self.headers:
                headers_found.append(idx)
            
            if headers_found:
                return True
            
        return False
        

    def split_tables(self) -> List[pd.DataFrame]:
        """
        If parsed dataframe contains multiple headers, return all tables
        with it's own set of headers. 
        """
        if not self.can_be_divided():
            return [self.parsed_dataframe]
        
        headers_found = []
        for idx, row in self.parsed_dataframe.iterrows():
            if row.iloc[1] in self.headers:
                headers_found.append(idx)
        
        dfs = []
        current = 0
        for h in headers_found:
            t = self.parsed_dataframe.iloc[current:h].copy()
            dfs.append(t)
            current = h
        dfs.append(self.parsed_dataframe.iloc[current:].copy())
        
        for df in dfs[1:]: #1st already has header correctly
            df.reset_index(drop=True, inplace=True)
            df.columns = df.iloc[0]
            df.drop(0, inplace=True)

            #unamed cols
            col_to_delete = []
            for col in df.columns:
                if col.find("unamed") != -1:
                    col_to_delete.append(col)
            
            df = df[[col for col in df.columns if col not in col_to_delete]]

        return dfs
             





if __name__ == "__main__":
    file = r"backend\app\public\241025 Unicredit Macro & Markets Weekly Focus - python.pdf"
    page = 18
    table_parser = PDFTableParser(file)
    table_parser.extract_tables(pages=f"{page}")
    df = table_parser.get_page_tables(page)[0].df
    data_frame_parser = DataFrameParser(page, df)
    print(data_frame_parser.split_tables()[0])
