from controllers.db_controller import Database


def main():
    db = Database()
    db.create_tables()


if __name__ == "__main__":
    main()
