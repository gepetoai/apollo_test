from supabase import create_client
import logging

class SupabaseClient:

    def __init__(self, url:str, key:str):
        self.url = url
        self.key = key
        self.db = create_client(self.url, self.key)


    def insert(self, table_name:str, row:dict):
        try:
            return self.db.table(table_name).insert([row]).execute() 
        except Exception as e:
            logging.exception("Exception occurred")
    
    def get_system_prompt(self, table_name, name):
        try:
            prompt_data = self.db.table(table_name).select("*").eq("name", name).execute() 
            return prompt_data.data[0]['content']
        except Exception as e:
            logging.exception("Exception occurred")
    
    def insert_vector_row(self, row):
        try:
            return self.db.table("vdb").insert([row]).execute()
        except Exception as e:
            logging.exception("Exception occurred")
    
    def get_all_vectors_of_category(self, category):
        try:
            return self.db.table("vdb").select("*").eq("category", category).execute()
        except Exception as e:
            logging.exception("Exception occurred")

    def match_documents_knn(self, query_embedding, match_count):
        # Call the updated SQL function 'match_documents_knn'
        request = self.db.rpc('match_vdb_knn', {
            'query_embedding': query_embedding,
            'match_count': match_count
        })
        # Execute the request and get the result
        result = request.execute()
        return result