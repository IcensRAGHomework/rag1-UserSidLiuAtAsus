import json
import traceback

from model_configurations import get_model_configuration

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage

import json
import re

gpt_chat_version = 'gpt-4o'
gpt_config = get_model_configuration(gpt_chat_version)

def generate_hw01(question):
    llm = AzureChatOpenAI(
            model=gpt_config['model_name'],
            deployment_name=gpt_config['deployment_name'],
            openai_api_key=gpt_config['api_key'],
            openai_api_version=gpt_config['api_version'],
            azure_endpoint=gpt_config['api_base'],
            temperature=gpt_config['temperature']
    )
    message = HumanMessage(
            content=[
                {"type": "text", "text": question},
            ]
    )
    response = llm.invoke([message])
    contents = response.content.splitlines()
    year = contents[0][0:4]

    for content in contents:
        if len(content) > 1:
            if (ord(content[0]) <= 0x39 and ord(content[0]) > 0x30) and (ord(content[1]) == 0x2e):
                Date = re.match(r'.*\D(\d+)月(\d+)日.*',content, re.M|re.I)
                month = Date.group(1)
                day = Date.group(2)
                Time = year + '-' + month + '-' + day
                NameMatch1 = re.match(r'.*\*\*(.*)\*\*.*',content, re.M|re.I)
                index = NameMatch1.group(1).find('-')
                if index != -1:
                    NameMatch2 = re.match(r'.*\*\*(.*) - (.*)\*\*.*',content, re.M|re.I)
                    Name = NameMatch2.group(2)
                else:
                    Name = NameMatch1.group(1)
                data = {'Result':[{'date': Time, 'name': Name}]}
                json_str = json.dumps(data, ensure_ascii=False, indent=4)
                print(json_str)

    return response
    
def generate_hw02(question):
    pass
    
def generate_hw03(question2, question3):
    pass
    
def generate_hw04(question):
    pass
    
def demo(question):
    llm = AzureChatOpenAI(
            model=gpt_config['model_name'],
            deployment_name=gpt_config['deployment_name'],
            openai_api_key=gpt_config['api_key'],
            openai_api_version=gpt_config['api_version'],
            azure_endpoint=gpt_config['api_base'],
            temperature=gpt_config['temperature']
    )
    message = HumanMessage(
            content=[
                {"type": "text", "text": question},
            ]
    )
    response = llm.invoke([message])
    
    return response

#generate_hw01("2024年台灣10月紀念日有哪些?")
#data = {'info':[{'name': 'John', 'age': 30, 'city': '北京'}]}
#json_str = json.dumps(data, ensure_ascii=False, indent=4)
#print(json_str)