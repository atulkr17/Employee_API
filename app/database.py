from databases import Database
from sqlalchemy import MetaData

DATABASE_URL =  "postgresql://postgres:Atul%402004@localhost:5432/podcast_db"

database = Database(DATABASE_URL)
metadata = MetaData()


