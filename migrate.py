from database import engine, Base

import models


def migrate():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")


if __name__ == "__main__":
    migrate()