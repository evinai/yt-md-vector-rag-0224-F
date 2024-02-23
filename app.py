import pymongo
import certifi
from dotenv import load_dotenv
import os
import requests

load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
HG_API_KEY = os.getenv("HUGGING_FACE")
HUGGING_FACE_URL = os.getenv('HUGGING_FACE_URL')

connection = "mongodb+srv://"+ USERNAME + ":" + PASSWORD + "@cluster0.xwgj9xw.mongodb.net/Configurations?retryWrites=true&w=majority"

client = pymongo.MongoClient(connection,tlsCAFile=certifi.where())

db = client.sample_mflix
collection = db.movies


def generate_embedding(text: str) -> list[float]:
    
    response = requests.post(
        HUGGING_FACE_URL,
        headers = {"Authorization": f"Bearer {HG_API_KEY}"},
        json={"inputs": text})

    if response.status_code != 200:
        raise ValueError(f"Request failed with status code {response.status_code}: {response.text}")
    
    return response.json()

# print(generate_embedding("freeCodecam is awesome"))

########## To generate embeddings
### for doc in collection.find({'plot':{"$exists": True}}).limit(50):
#     doc['plot_embedding_hf'] = generate_embedding(doc['plot'])
#     collection.replace_one({'_id': doc['_id']}, doc)


query = "imaginary characters from outer space at war"


results = collection.aggregate([
  {"$vectorSearch": {
    "queryVector": generate_embedding(query),
    "path": "plot_embedding_hf",
    "numCandidates": 100,
    "limit": 4,
    "index": "PlotSemanticSearch",
      }}
])

for document in results:
    print(f'Movie Name: {document["title"]},\nMovie Plot: {document["plot"]}\n')