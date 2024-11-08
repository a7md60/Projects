from qdrant_client import QdrantClient
import uuid
from qdrant_client.models import Distance, VectorParams, PointStruct
from src.model.tokenizer import Tokenizer

class QdrantUtils:

    def __init__(self,path: str = "./KB-Vector-Store/"):
        # self.client = QdrantClient(host="localhost", port=6333)

        self.client = QdrantClient(path=path)  # Persists changes to disk
        self.vector_size = 384
        self.tokenizer = Tokenizer() 
        self.collection_name = "medical_assistant_db"


    def is_collection_exits(self,collection_name: str):
        collections = [collection.name for collection in self.client.get_collections().collections]

        if collection_name in collections:
            return True
        
        return False

    def upsert_vectors(self,collection_name: str, vectors_to_upsert: list):
       
       if vectors_to_upsert:

            try:

                if self.is_collection_exits(collection_name):
                    print("Upserting in existing")
                    points = []
                    for data in vectors_to_upsert:
                        points.append(PointStruct(id=str(uuid.uuid4()),payload=data['metadata'],vector=data['values']))

                    self.client.upsert(collection_name=collection_name,points=points)

                else:
                    # Create New Collection
                    print("creating a collection")
                    self.client.create_collection(collection_name=collection_name,
                            vectors_config=VectorParams(size=self.vector_size,distance=Distance.COSINE))
                    
                    points = []
                    for data in vectors_to_upsert:
                        vector = data['vector']
                        points.append(PointStruct(id=str(uuid.uuid4()),payload=data['metadata'],vector=vector))
                    print(points)
                    self.client.upsert(collection_name=collection_name,points=points)

            except Exception as e:
                print(f"Exception Occured {e}")
            

    def search_docs(self,query: str, limit: int =10):

        vector = self.tokenizer.create_embedding(query)
        
        docs = self.client.search(collection_name=self.collection_name,
                           query_vector=vector,
                           limit=limit)

        documents = [doc.payload for doc in docs]
        
        return documents