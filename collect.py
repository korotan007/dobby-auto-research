#!/usr/bin/env python3
"""Dobby: free RSS research collector. Standard library only."""
import datetime as dt
import json
import pathlib
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "data"
OUT.mkdir(exist_ok=True)
TOPICS = {
    "government_bids": ["官公庁 入札 公告 清掃 設備管理", "政府 調達 業務委託 入札公告"],
    "ai_business": ["生成AI 副業 SNS 収益化", "note クリエイター 収益化 AI"],
    "reuse": ["リユース 買取 業界 ニュース", "古物商 貴金属 買取 市場"],
}
HEADERS = {"User-Agent": "DobbyResearchBot/1.0 (RSS reader)"}

def fetch(query):
    params = urllib.parse.urlencode({"q": query, "hl": "ja", "gl": "JP", "ceid": "JP:ja"})
    url = "https://news.google.com/rss/search?" + params
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=18) as response:
        raw = response.read(1_500_000)
    root = ET.fromstring(raw)
    result = []
    for item in root.findall("./channel/item")[:15]:
        def value(name):
            return (item.findtext(name) or "").strip()
        link = value("link")
        if link.startswith("https://"):
            result.append({"title": value("title"), "url": link, "published": value("pubDate"), "source": value("source")})
    return result

def main():
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    for topic, queries in TOPICS.items():
        path = OUT / (topic + ".json")
        try:
            previous = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
        except (ValueError, OSError):
            previous = {}
        old = {x["url"]: x for x in previous.get("items", []) if x.get("url")}
        merged = dict(old)
        errors = []
        for query in queries:
            try:
                for item in fetch(query):
                    merged[item["url"]] = item
            except Exception as exc:
                errors.append(f"{query}: {type(exc).__name__}: {str(exc)[:150]}")
        # Do not overwrite a successful snapshot with empty data on network errors.
        if not merged and errors:
            print(f"{topic}: failed: {errors}")
            continue
        items = list(merged.values())[-150:]
        new_count = sum(x["url"] not in old for x in items)
        # Keep files stable if nothing new was found.
        if new_count or not path.exists():
            path.write_text(json.dumps({"topic": topic, "updated_at_utc": now, "items": items}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{topic}: {len(items)} stored, {new_count} new; errors={errors}")

if __name__ == "__main__":
    main()
