import psycopg2
import time

class Connection:

    @staticmethod
    def get_connection():
        
        for _ in range(300):
            try:
                connection = psycopg2.connect(
                    dbname = "focuseconomics",
                    user = "admin",
                    password = "1234",
                    host = "postgres",
                    port = "5432"
                )
            #Operational Error deals with connection problems
            except:
                continue
