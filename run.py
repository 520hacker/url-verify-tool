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
