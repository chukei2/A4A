import os
import json
import http.client
import sys

def generate_pr_description():
    api_key = os.getenv("GEMINI_API_KEY")
    diff = os.getenv("DIFF_CONTENT", "").strip()

    fallback = {"title": "Manual PR Update", "body": "Updated via GitHub Action"}

    if not api_key or not diff:
        print(json.dumps(fallback, ensure_ascii=False))
        return

    prompt = f"""
以下はコミットメッセージの一覧です。
日本語で Pull Request のタイトルと説明文を生成してください。

# 出力形式（厳守）
- JSONのみを出力すること
- 形式: {{"title": "...", "body": "..."}}
- 余計な文章、コードフェンス（```）、Markdownは禁止

# コミット一覧
{diff}
""".strip()

    conn = http.client.HTTPSConnection("generativelanguage.googleapis.com")
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}

    try:
        conn.request(
            "POST",
            f"/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}",
            json.dumps(payload),
            headers,
        )
        res = conn.getresponse()
        body = res.read().decode("utf-8")

        if res.status != 200:
            print(json.dumps(fallback, ensure_ascii=False))
            return

        data = json.loads(body)
        text = data["candidates"][0]["content"]["parts"][0]["text"].strip()

        # コードフェンス掃除
        text = text.replace("```json", "").replace("```", "").strip()

        try:
            obj = json.loads(text)
            title = str(obj.get("title", fallback["title"]))
            body = str(obj.get("body", fallback["body"]))
            print(json.dumps({"title": title, "body": body}, ensure_ascii=False))
        except Exception:
            print(json.dumps(fallback, ensure_ascii=False))

    except Exception:
        print(json.dumps(fallback, ensure_ascii=False))

if __name__ == "__main__":
    generate_pr_description()
