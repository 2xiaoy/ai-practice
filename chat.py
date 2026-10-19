import os
from  openai import OpenAI
client=OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com"

)
messages=[]

while True:
    user_input=input("你:")
    if user_input=="退出":
        break
    messages.append({"role":"user","content":user_input})
    response=client.chat.completions.create(
    model="deepseek-chat",
    messages=messages
    )
    reply=response.choices[0].message.content
    print("AI:",reply)
    messages.append({"role":"assistant","content":reply})