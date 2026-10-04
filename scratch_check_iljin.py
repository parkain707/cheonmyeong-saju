import urllib.parse
import re

with open(r'C:\Users\user\.gemini\antigravity\brain\d7671e34-1b04-4c8e-9116-8b835827c501\.system_generated\steps\2316\content.md', encoding='utf-8') as f:
    text = f.read()

# find 17일 around
pos = text.find('1993년 8월 17일')
if pos != -1:
    chunk = text[pos:pos+1000]
    # find all titles
    for m in re.finditer(r'title="([^"]+)"', chunk):
        print("title:", m.group(1))
    for m in re.finditer(r'href="([^"]+)"', chunk):
        print("href:", urllib.parse.unquote(m.group(1)))
