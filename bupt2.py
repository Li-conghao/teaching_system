from playwright.sync_api import sync_playwright
from urllib.parse import urljoin
import os
import requests
BASE_URL = "https://is.bupt.edu.cn"
PAGE_URL = "https://is.bupt.edu.cn/xygk/szdw.htm"
SAVE_DIR = "images"
all_links = []
with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        args=[
            "--disable-blink-features=AutomationControlled"
        ]
    )
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/120.0.0.0 Safari/537.36"
    )
    page = context.new_page()
    page.goto(PAGE_URL, wait_until="domcontentloaded")
    page.wait_for_selector("#vsb_content", timeout=20000)
    img_srcs = page.eval_on_selector_all(
        "#vsb_content img",
        "imgs => imgs.map(img => img.getAttribute('src'))"
    )

    browser.close()

print(img_srcs)
for src in img_srcs:
    if not src:
        continue
    img_url = urljoin(BASE_URL, src)
    filename = os.path.basename(img_url)
    print("下载:", img_url)
    data = requests.get(img_url).content
    os.makedirs(SAVE_DIR, exist_ok=True)
    with open(os.path.join(SAVE_DIR, filename), "wb") as f:
        f.write(data)
