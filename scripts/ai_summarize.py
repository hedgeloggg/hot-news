# scripts/ai_summarize.py
import os
import json
import time
from dashscope import Generation

def call_qwen(prompt):
    response = Generation.call(
        model='qwen-max',
        prompt=prompt,
        api_key=os.getenv('DASHSCOPE_API_KEY')
    )
    return response.output.text.strip()

def main():
    with open('output/raw_news.json') as f:
        news = json.load(f)
    
    report = "【全球社交热点日报】\n\n"
    for i, item in enumerate(news[:20], 1):
        prompt = f"""你是一个资深热点分析师。请用中文分析以下事件：
标题：{item['title']}
来源：{item['source']}

要求：
1. 用一句话概括核心事实（≤50字）
2. 指出主要讨论平台（如 X、Reddit、微博等）
3. 判断情绪倾向：□正面 □负面 □争议 □中性（选一个）
4. 提供一句深度洞察（≤60字）

格式严格如下：
【热度排名】#{i}
【事件标题】{item['title']}
【主要平台】...
【情绪倾向】...
【核心内容】...
【深度洞察】...
"""
        try:
            analysis = call_qwen(prompt)
            report += analysis + "\n────────────────\n\n"
            time.sleep(1)  # 避免 API 限流
        except Exception as e:
            print(f"AI Error: {e}")
            report += f"【热度排名】#{i}\n【事件标题】{item['title']}\n【分析失败】\n\n"
    
    with open('output/final_report.txt', 'w') as f:
        f.write(report)
    print("✅ AI analysis completed")

if __name__ == '__main__':
    main()
