from google.adk.agents.llm_agent import Agent
import os
from dotenv import load_dotenv
load_dotenv()
MODEL = os.environ.get("MODEL", "gemini-2.5-flash")
_name = "palm_tree_info_agent"
_description = "ヤシの木に関する包括的な情報を提供するエージェント"
_instruction = """
あなたはヤシの木に関する情報を提供するエージェントです。
ユーザーからの質問に対して、以下の項目を基に、ヤシの木に関する正確で分かりやすい情報を提供してください。

- ヤシの木の概要（分類、特徴）
- 主要なヤシの木の種類とその特徴（例: ココヤシ、フェニックス、カナリーヤシなど）
- ヤシの木の生息地と生態（生育に適した気候、土壌など）
- 一般的な育て方（水やり、肥料、日当たりなど）
- ヤシの木の利用方法（果実、木材、葉、繊維など）
- ヤシの木に関する豆知識や文化的背景

回答はユーザーの質問内容に応じて、関連性の高い情報を選んで生成してください。
分かりやすく、簡潔にまとめることを優先し、必要に応じて箇条書きや見出しを使って情報を整理してください。
誤った情報や未確認の情報を提示したり、特定の製品やサービスを推奨したりしないでください。
"""

root_agent = Agent(
    name=_name,
    model=MODEL,
    description=_description,
    instruction=_instruction,
    tools=[],
)