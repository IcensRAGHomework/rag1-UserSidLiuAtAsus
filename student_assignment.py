import json
import traceback

from model_configurations import get_model_configuration

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate,MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_functions_agent, create_openai_tools_agent

import json
import re

import calendarific
from langchain_core.tools import StructuredTool

gpt_chat_version = 'gpt-4o'
gpt_config = get_model_configuration(gpt_chat_version)

llm = AzureChatOpenAI(
        model=gpt_config['model_name'],
        deployment_name=gpt_config['deployment_name'],
        openai_api_key=gpt_config['api_key'],
        openai_api_version=gpt_config['api_version'],
        azure_endpoint=gpt_config['api_base'],
        temperature=gpt_config['temperature']
)

examples= [
        {"input": '[{"name":"NationalDay","description":"NationalDayisanationalholidayinTaiwan","country":{"id":"tw","name":"Taiwan"},"date":{"iso":"2024-10-10","datetime":{"year":2024,"month":10,"day":10}},"type":["Nationalholiday"],"primary_type":"Nationalholiday","canonical_url":"https://calendarific.com/holiday/taiwan/national-day","urlid":"taiwan/national-day","locations":"All","states":"All"},{"name":"Taiwan"sRetrocessionDay","description":"Taiwan"sRetrocessionDayisaobservanceinTaiwan","country":{"id":"tw","name":"Taiwan"},"date":{"iso":"2024-10-25","datetime":{"year":2024,"month":10,"day":25}},"type":["Observance"],"primary_type":"Observance","canonical_url":"https://calendarific.com/holiday/taiwan/taiwan-retrocession-day","urlid":"taiwan/taiwan-retrocession-day","locations":"All","states":"All"}]', "output": '{"Result": [{"date": "2024-10-10","name": "國慶日"},{"date": "2024-10-25","name": "光復節"}]}'}
    ]
example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}"),
        ("ai", "{output}"),
    ]
)

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)

class holidayRequest(BaseModel):
    country: str = Field(description="以2字母 iso code表示國家")
    year:int = Field(description="以yyyy表示年分")
    month:int = Field(description="以mm表示月份")

holiday_data = StructuredTool.from_function(
    func=get_holiday,
    name='Holiday_Calendar',
    description='特定年月份的節日有哪些',
    args_schema=holidayRequest
)

def generate_hw01(question):
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
                return(json_str)



def get_holiday(country: str, year:int, month:int):
    calapi = calendarific.v2('1OjpLyZIBMPMsVoHoxNvkZeAaFXWiGDJ')

    parameters = {
        # Required
        'country': country,
        'year':    year,
        'month':    month,
    }

    holidays = calapi.holidays(parameters)
    #decodeHoliday = json.dumps(holidays, ensure_ascii=False, indent=4)
    #print(decodeHoliday)
    return holidays
    

    
def generate_hw02(question):

    formal_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a restful api for calendar"),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
            ("human", "以{few_shot_prompt}為json範例格式回答, 不要有多餘json文字")
        ]
    )

    tools = [holiday_data]
    agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=formal_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools)
    return agent_executor.invoke({'input': question, 'few_shot_prompt': few_shot_prompt})['output']

    
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
    
generate_hw02("2024年台灣10月紀念日有哪些?")

