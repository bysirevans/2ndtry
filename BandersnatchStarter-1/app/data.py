from os import getenv
from certifi import where
from dotenv import load_dotenv
from MonsterLab import Monster
from pandas import DataFrame
from pymongo import MongoClient

class Database:
    def __init__(self):
        load_dotenv()
        client = MongoClient("mongodb+srv://bysire:blackburn200@cluster0.sfeqpsg.mongodb.net/", tlsCAFile=where())["bandersnatch"]
        self.collection = client.get_collection('Name')
    
    def seed(self, amount=1000):
        if amount == 1:
            record = Monster().to_dict()
            return self.collection.insert_one(record).acknowledged
        if amount > 1:
            records = [Monster().to_dict() for i in range(amount)]
            return self.collection.insert_many(records).acknowledged

    def reset(self):
        result = self.collection.delete_many({})
        return result.deleted_count

    def count(self) -> int:
        return self.collection.count_documents({})

    def dataframe(self) -> DataFrame:
        cursor = self.collection.find({})
        df = DataFrame(list(cursor))
        return df

    def html_table(self) -> str:
        df = self.dataframe()
        html_table = df.to_html(index=False)
        return html_table

if __name__ == "__main__":
    db=Database()
    db.seed(1000)
    print(db.html_table())