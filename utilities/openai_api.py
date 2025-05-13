from openai import OpenAI
import os
from dotenv import load_dotenv

def openai_api(flavors, mains, staples):
    load_dotenv()

    print("目前 OpenAI KEY：", os.getenv("OPENAI_API_KEY"))  # 暫時 debug 用

    try:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        prompt = f'''
        我這邊有三組字詞，分別是：
        口味: {', '.join(flavors)}
        主餐: {', '.join(mains)}
        主食: {', '.join(staples)}
        可否幫我從這三個字詞中隨機各挑出一個詞，並將這三個詞組成適合Google Map搜尋的詞語，ex:炭烤豬肉飯，總共隨機十次，回傳成由逗號分開不要空格的字串。
        '''

        response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0.8,
        max_tokens=200,
        )

        return response.choices[0].message.content.split(",")
    
    except Exception as e:
        print("⚠️ OpenAI 呼叫錯誤：", str(e))  # <== 印出錯誤訊息
        raise