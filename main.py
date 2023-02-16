import os
from enum import Enum
from typing import Optional
from fastapi import FastAPI
from utils import *


PATH = os.path.dirname(os.path.abspath(__file__)) + '/'
os.environ['OPENAI_API_KEY'] = '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'
current_time = get_time()
openai.api_key = os.getenv('OPENAI_API_KEY')
app = FastAPI()

def get_report(topic, temp=0.5, max_tokens=1000, top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0):  
    print('topic: ', topic)
    goog_src = parse_results(get_results(topic))
    gpt_prompt = "plz write news report about " + topic + " and the contents should includes "
    print('gpt_prompt: ', gpt_prompt)
    report = ""

    for i in range(2):
        for j in range(len(goog_src)):
            gpt_prompt = gpt_prompt + goog_src[j]['text'] + "\n"
            
        report = report + get_gpt_text(gpt_prompt=gpt_prompt, max_tokens=max_tokens) 
        goog_src = parse_results(get_results(report))
        gpt_prompt = "plz write news report about " + topic + " and the contents should includes "
        
    return report

@app.get("/report/{prompt}")
def read_item(prompt: str):
    report = get_report(prompt).replace('\n', '')
    print('report: ', report, len(report))
    return {"imput_prompt":prompt, "output_report": report, "report_length": len(report)} 