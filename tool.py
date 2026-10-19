import os
import json 
from openai import  OpenAI

client =OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com"
)
def calculate(a,b,op):
    if op=="+":
        return a+b 
    elif op=="-":
        return a-b 
    elif op=="*":
        return a*b
    elif op=="/":
        return a/b 

tools=[
    {
        "type":"function",
        "function":{
            "name":"calculate",
            "description":"计算两个数的加减乘除",
            "parameters":{
                "type":"object",
                "properties":{
                    "a":{"type": "number","description":"第一个数"},
                    "b":{"type": "number","description":"第二个数"},
                    "op":{"type":"string","description":"运算符，只能是+ - * /"}
            },
            "required":["a","b","op"]
        }
    }
    }
]
messages=[{"role": "user","content":"帮我算一下1234乘以5687等于多少"}]

response=client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    tools=tools
)
message= response.choices[0].message

if  message.tool_calls:
    tool_call=message.tool_calls[0]
    args=json.loads(tool_call.function.arguments)
    print("AI 想调用:",tool_call.function.name)
    print("AI 传的参数:",args)
    
    result=calculate(args["a"],args["b"],args["op"])
    print("实际的计算结果:",result)

    messages.append(message)
    messages.append({
        "role":"tool",
        "tool_call_id":tool_call.id,
        "content":str(result)
    })

    final=client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools
    )
    print("AI最终回答:",final.choices[0].message.content)
