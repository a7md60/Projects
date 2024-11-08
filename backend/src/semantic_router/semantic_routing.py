
from src.model.models import call_llm
from src.semantic_router.prompts import (user_intent_identifiction_template, 
                                         conversational_chat_template,
                                         medical_assistance_tempalte,
                                         chat_end_template,
                                         other_medical_scenerio_template,
                                         book_appointment_template,
                                         assistance_prompt
                                        
                                         )
from langchain.prompts import PromptTemplate
import json


class Routing:
    def __init__(self, qdrant_client=None):
        self.qdrant_client = qdrant_client

    
    def route(self, query: str, chat_history: list, output_language: str):

        user_intent_prompt = PromptTemplate(template=user_intent_identifiction_template,input_variables=['text', 'chat_history'])

        route_path = call_llm(input_dict={"text":query, 'chat_history':chat_history },prompt=user_intent_prompt,return_json=True)
        print(route_path)
        if route_path['route_path']=="malicious_prompt":
            return self._malicious_prompt_handler(query, chat_history, output_language)
        
        if route_path['route_path'] == "conversational_chat":
            print(f"Path: {route_path['route_path']}")          
            return self._converstational_chat_handler(query, chat_history, output_language)

        if route_path['route_path'] == "medical_assistance":                      
            medical_assitance_routes = self._medical_assistance_handler(query, chat_history, output_language)

            if medical_assitance_routes['tool'] == "search_doctor":
                docs = self.qdrant_client.search_docs(query)
                format_query = "You are given list of docotors for the given disease with their contact suggest them in single line"
                medical_assitance_routes = self._medical_assistance_handler(format_query,chat_history, output_language, docs)
                return medical_assitance_routes
            else:
                return medical_assitance_routes
        
        if route_path['route_path'] == "chat_end":
            print(f"Path: {route_path['route_path']}")

            return self._chat_end_handler(query,chat_history, output_language)

            # if medical_assitance_routes['route_path']=="medical_scenerio":
            #     print(f"Path: {route_path['route_path']}")
          
            #     return self._other_medical_scenerios(query,chat_history)
            
            # if medical_assitance_routes['route_path'] == "book_appointment":
            #     print(f"Path: {route_path['route_path']}")
          
            #     return self._book_appointment(query,chat_history)


        


    def _malicious_prompt_handler(self, query: str, chat_history: list, output_language: str):
        return "Malicious Prompt Detected"

    def _medical_assistance_handler(self,query: str,chat_history: list, output_language, doctors=""):
        prompt = PromptTemplate(template=assistance_prompt,input_variables=['query','chat_history',"doctors",'output_language'])

        response = call_llm(input_dict={"query":query,"chat_history":chat_history,"doctors": doctors,"output_language":output_language},prompt=prompt,return_json=True,model_name="gpt-4")

        return response

    def _converstational_chat_handler(self,query: str, chat_history: list, output_language: str):

        prompt = PromptTemplate(template=conversational_chat_template,input_variables=['text','output_language'])

        response = call_llm(input_dict={"text":query,"chat_history":chat_history,'output_language':output_language},prompt=prompt)

        return response        
    
    def _chat_end_handler(self,query: str, chat_history: list, output_language: str):

        prompt = PromptTemplate(template=chat_end_template,input_variables=['text', 'output_language'])

        response = call_llm(input_dict={"text":query,"chat_history":chat_history, 'output_language' : output_language},prompt=prompt)

        return response

    # def _book_appointment(self,query: str, chat_history: list):
        
    #     docs = self.qdrant_client.search_docs(query)
    #     prompt = PromptTemplate(template=book_appointment_template,input_variables=['text','doctors_list_speciality',"chat_history"])

    #     response = call_llm(input_dict={"text":query,"doctors_list_speciality":docs,"chat_history":chat_history},prompt=prompt,return_json=True)

    #     return response


    # def _other_medical_scenerios(self,query: str, chat_history: list):

    #     prompt = PromptTemplate(template=other_medical_scenerio_template,input_variables=['text','chat_history'])

    #     response = call_llm(input_dict={"text":query,'chat_history':chat_history},prompt=prompt)

    #     return response
