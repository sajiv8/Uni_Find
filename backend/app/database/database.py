from sqlalchemy import create_engine
DATABASE_URL = "postgresql://user1:1234@localhost/unifind"
engine = create_engine(DATABASE_URL)

