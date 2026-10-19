import os
from  openai import OpenAI
client=OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com"

)
knowledge="""
我今年20岁了，
是一名大学生，
我的生活似乎3点一线，
国庆节有5天假期，
正在学习ai
"""
chunks=[line.strip()  for line in knowledge.strip().split("\n") if line.strip()]

def retrieve(question,chunks):
    scored=[]
    for  chunk in chunks:
        score=sum(1 for ch in question if ch in  chunk )
        scored.append((score,chunk))
    scored.sort(reverse=True)
    return [chunk for score ,chunk in scored[:2]]

question =input("问点什么：")
relevant=retrieve(question,chunks)
context="\n".join(relevant)

prompt=f"""请根据下面的资料回答问题。如果资料里没有答案，就说"资料里没有"。
资料:
{context}
问题:
{question}
"""
response=client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role":"user","content":prompt}])
print("AI:",response.choices[0].message.content)
    