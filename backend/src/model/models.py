
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
import json
import re


def call_llm(input_dict:dict , prompt: PromptTemplate, model_name: str = "gpt-3.5-turbo-16k-0613",return_json = False):

    model = ChatOpenAI(temperature=0,openai_api_key=os.getenv("OPENAI_KEY"),model=model_name)
    chain = LLMChain(llm=model, prompt=prompt)
    response = chain.run(**input_dict)
    print(response)
    if return_json:
        try:
            return json.loads(response)
        except:
            return match_pattern(response)
    return response
    
    

def match_pattern(response):
    pattern = r'({[^}]+})'
    match = re.search(pattern, response)
    if match:
        return json.loads(match.group(0))
    
    return None
