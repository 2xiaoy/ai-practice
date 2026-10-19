import os
import json
from datetime import datetime
from openai import OpenAI
client=OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com"

)
def calculate(a,b,op):
    if op=="+":return a+b
    if op == "-": return a - b
    if op == "*": return a * b
    if op == "/": return a / b

def get_weather(city):
    fake={"北京": "晴，25度", "上海": "小雨，22度", "广州": "多云，28度"}
    return  fake.get(city,"没有这个城市的数据")

def get_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

tools=[
    {
        "type":"function",
        "function":{
            "name":"calculate",
            "description":"计算两个数的加减乘除",
            "parameters":{
                "type":"object",
                "properties":{
                    "a":{"type":"number"},
                    "b":{"type":"number"},
                    "op":{"type":"string","description":"+ - * /"}
                },
            "required":["a","b","op"]
        }
    }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询某个城市的天气",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string", "description": "城市名"}},
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "获取当前时间",
            "parameters": {"type": "object", "properties": {}}
            }
        },
    
]

tool_map={"calculate":calculate,"get_weather":get_weather,"get_time":get_time}
messages=[]

while True:
    user_input=input("你：")
    if user_input==("退出"):
        break
    messages.append({"role":"user","content":user_input})

    while True:
        response=client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools
    )
        message=response.choices[0].message

        if message.tool_calls:
            messages.append(message)
            for tool_call in message.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                print(f"调用工具:{name},参数:{args}")
                result = tool_map[name](**args)
                print(f"     结果：{result}")
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })

        else :
            print("AI：", message.content)
            messages.append({"role": "assistant", "content": message.content})
            break
