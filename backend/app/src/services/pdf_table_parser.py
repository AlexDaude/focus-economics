import camelot
from typing import List, Optional, Dict, Any
from camelot.core import TableList, Table
from backend.app.src.enumerations.camelot_parsing_methods import CamelotParsingMethods



class PDFTableParser:
    """
    Class for parse a pdf and extract tables
    """
    def __init__(self, file: str):
        self.file = file
        self.tables = None

    def extract_tables(
                        self, 
                        method: CamelotParsingMethods = CamelotParsingMethods.STREAM, 
                        pages: str = "1", 
                        parallel = True
                    ) -> TableList:
        """
        Parse pdf and extract tables, class atribute tables is updated with the results.

        :param method: Method used for parsing the pdf
        :param pages: Pages to process, expected in string format with comma as delimiter
        :param parallel: Process pages in parallel using all available cpu cores.
        :return: Tables found within the file
        """
        self.tables = camelot.read_pdf(
                 self.file, 
                 flavor=method, 
                 pages=pages, 
                 parallel=parallel,
                )
        return self.tables
    
    
    def get_page_tables(self, pages: List[int]|int) -> List[Table]:
        """
        Get all the tables found in page

        :param pages: Pages where to search
        :return: Tables found in the given page
        """

        if not isinstance(pages, (int, List)):
            raise TypeError("Pages must be a int or a List of ints")
        
        if isinstance(pages, List) and not all(isinstance(p, int) for p in pages):
            raise TypeError("Pages must be a list of integers")
        
        if not self.tables:
            raise Exception("No tables were found")
        
        pages = [pages] if isinstance(pages, int) else pages

        related_tables = []
        for table in self.tables:
            if table.parsing_report["page"] in pages:
                related_tables.append(table)
        return related_tables
                
    

if __name__ == "__main__":
    file = r"backend\app\public\to_parse.pdf"
    pdf_table_parser = PDFTableParser(file)
 
    pdf_table_parser.extract_tables(
        method=CamelotParsingMethods.STREAM,
        pages="2",
        parallel=True,
        row_tol=2,
    
    )
    related_tables = pdf_table_parser.get_page_tables(2)
    print(related_tables[0].df)


            

    


    
        


