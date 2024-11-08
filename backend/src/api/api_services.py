from src.semantic_router.semantic_routing import Routing
from src.utils.qdrant_utils import QdrantUtils
from src.model.tokenizer import Tokenizer
from src.utils.topic_extraction import TopicExtraction
import pandas as pd
import numpy as np



class Services:

    def __init__(self,qdrant_client = None):
        self.tokenizer = Tokenizer()
        self.semantic_router = Routing(qdrant_client)
        self.qdrant_client = qdrant_client
        self.topic_extractor = TopicExtraction()

    async def route_user_query(self, query: str,chat_history: list, output_language:str):
        return self.semantic_router.route(query, chat_history, output_language)
        

    async def topic_extraction(self, query: str):
        return self.topic_extractor.extract(query)

    async def upsert_vectors(self,file_path,collection_name):

        # Prepare Doc
        try:
            df = pd.read_csv(file_path)
            specialities_texts = df["Speciaplty"].tolist()
            array = np.unique(np.array(specialities_texts))
            print(array)
            word_embeddings = {}
            for word in array:
                word_embedding = self.tokenizer.create_embedding(word)
                word_embeddings[word] = word_embedding

            #Prepare metadata
            metadata = df.to_dict(orient="records")
            
            vectors_to_upsert = []
            for item in metadata:
                embedding = word_embeddings[item['Specialty']]
                item['text'] = item['Specialty']
                vectors_to_upsert.append({"values":embedding,"metadata":item})

            self.qdrant_client.upsert_vectors(collection_name=collection_name,
                                            vectors_to_upsert=vectors_to_upsert)
        except Exception as e:
            print(f"Exception {e}")
            return {"status":"400"}
        return {"status":"200"}
    

    
        
