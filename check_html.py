import urllib.request

html = urllib.request.urlopen('http://localhost:8088/').read().decode('utf-8')
print("webtoon-intro-section:", "webtoon-intro-section" in html)
print("tab-btn-webtoon:", "tab-btn-webtoon" in html)
print("webtoon-cta-banner:", "webtoon-cta-banner" in html)
print("HTML length:", len(html))
