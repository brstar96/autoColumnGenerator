import datetime
import urllib
import requests
import openai

from requests_html import HTMLSession
from pytz import timezone

def get_time():
    now = datetime.datetime.now(timezone('Asia/Seoul'))
    nowDate = now.strftime('%Y-%m-%d')
    nowTime = now.strftime('%H-%M-%S')
    current_time = now.strftime("%Y_%m_%d_%H_%M_%S")

    return current_time

# code from https://blog.naver.com/htk1019/223003764130
def get_source(url):
    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)

def get_results(query):
    
    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.co.uk/search?q=" + query)
    
    return response

def parse_results(response): # parse the results from the response object
    
    css_identifier_result = ".tF2Cxc"
    css_identifier_title = "h3"
    css_identifier_link = ".yuRUbf a"
    css_identifier_text = ".VwiC3b"
    
    results = response.html.find(css_identifier_result)

    output = []
    
    for result in results:

        item = {
            'title': result.find(css_identifier_title, first=True).text,
            'link': result.find(css_identifier_link, first=True).attrs['href'],
            'text': result.find(css_identifier_text, first=True).text
        }
        
        output.append(item)
        
    return output

def get_gpt_text(gpt_prompt, temp=0.5, max_tokens=256, top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0):
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=gpt_prompt,
      temperature=temp,
      max_tokens=max_tokens,
      top_p=top_p,
      frequency_penalty=frequency_penalty,
      presence_penalty=presence_penalty
    )
    
    return response['choices'][0]['text']