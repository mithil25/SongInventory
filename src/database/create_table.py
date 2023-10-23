from database.db_config import db


class Table:
    @staticmethod
    def create_tables(models):
        try:
            db.create_tables(models)
            print("Tables created successfully")
        except Exception as e:
            print("Exception while creating tables:", e)
        finally:
            db.close()  # Always close the database connection
