# Question
urls.txt 里面是逐行保存的网址列表，但是有一些网站已经打不开了，现在我们需要写带来来验证这些网址，并提取中依然能访问的网址列表
请使用python，读取urls.txt,去除空行和重复，使用多线程，逐一请求这些网址，保存页面的标题信息，并把能够正常访问的地址和页面标题以markdown格式生成为结果文件urls_alive.txt

# ChatGPT
以下是一个使用Python的示例代码，它可以读取urls.txt文件中的网址列表，并使用多线程逐一验证这些网址是否可以访问。如果可以访问，它将提取页面的标题信息，并将可访问的网址和标题以Markdown格式保存在urls_alive.txt文件中。

python 
```
import requests
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup

def get_title(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string.strip() if soup.title else 'No Title'
        return url, title
    except (requests.RequestException, ValueError, AttributeError):
        return None

def process_urls(urls):
    results = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_title, url) for url in urls]
        for future in futures:
            result = future.result()
            if result is not None:
                results.append(result)
    return results

def save_results(results):
    with open('urls_alive.txt', 'w', encoding='utf-8') as file:
        for url, title in results:
            file.write(f"[{title}]({url})\n")

def main():
    urls = set()
    with open('urls.txt', 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                urls.add(line)
    results = process_urls(urls)
    save_results(results)

if __name__ == '__main__':
    main()
```

请确保你已经安装了Python的requests库、BeautifulSoup库和concurrent.futures库。你可以使用pip命令来安装它们：

```
pip install requests beautifulsoup4
```

将以上代码保存到一个Python文件（例如url_checker.py），并将urls.txt放在同一目录下。运行Python脚本后，将会生成名为urls_alive.txt的文件，其中包含可访问的网址和对应的标题信息。