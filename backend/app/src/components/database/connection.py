from sqlalchemy import create_engine

class Connection:

    @staticmethod
    def get_connection():
        
        #wait until db is reachable
        for _ in range(1000):
            try:
                return create_engine("postgresql+psycopg2://admin:1234@postgres:5432/focuseconomics")
            except:
                continue
        
        raise Exception("Can't connect to the database")