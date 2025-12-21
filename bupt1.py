from playwright.sync_api import sync_playwright
from urllib.parse import urljoin
import os
save_dir = "bupt_news_content"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
url = "https://zsb.bupt.edu.cn/zyjs/gjxy_bjyddxmlnwxy_1.htm"
all_links = []

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
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
    page.goto(url, wait_until="domcontentloaded")
    page.wait_for_selector("ul.list_box_wz_list li a", timeout=15000)
    page.wait_for_timeout(1000)
    links_data = page.eval_on_selector_all(
        "ul.list_box_wz_list a",
        "els => els.map(a => ({href: a.getAttribute('href'), title: a.textContent.trim()}))"
    )
    for item in links_data:
        if item['href']:
            full_link = urljoin(url, item['href'])
            all_links.append({
                'url': full_link,
                'title': item['title']
            })
            print(f"链接: {full_link}")
            print(f"标题: {item['title']}")
            print("-" * 50)
    browser.close()

for index, item in enumerate(all_links):
    url = item['url']
    title = item['title']
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False,
                args=["--disable-blink-features=AutomationControlled"]
            )
            page = browser.new_page()
            page.goto(url, wait_until="domcontentloaded")
            page.wait_for_selector("div.v_news_content", timeout=15000)
            content_text = page.locator("div.v_news_content").inner_text()
            filename = f"{title}.txt"
            file_path = os.path.join(save_dir, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content_text)
            print(f"\n已保存文件: {file_path}")
            browser.close()
    except Exception as e:
        print(f"\n处理 {url} 时出错: {str(e)}")
        continue
print(f"\n文件保存目录: {os.path.abspath(save_dir)}")