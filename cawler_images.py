import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def crawl(url, domain, visited_urls, image_urls):
    if len(visited_urls) >= 100:
        return
    if url in visited_urls:
        return
    visited_urls.add(url)
    print(f"Vizitez pagina: {url}")
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except Exception as e:
        print(f"Eroare la accesarea {url}: {e}")
        return
    soup = BeautifulSoup(response.text, 'html.parser')

  
    for img in soup.find_all('img'):
        src = img.get('src')
        if src:
            full_img_url = urljoin(url, src)
            if domain in full_img_url:
                image_urls.add(full_img_url)

  
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            full_link = urljoin(url, href)
            parsed = urlparse(full_link)
            if parsed.netloc == domain:
                crawl(full_link, domain, visited_urls, image_urls)  


start_url = 'https://dentamax.ro/'  
parsed_domain = urlparse(start_url).netloc
visited_urls = set()  
image_urls = set()  

crawl(start_url, parsed_domain, visited_urls, image_urls)

print("\nImagini găsite:")
for idx, img_url in enumerate(sorted(image_urls), 1):
    print(f"{idx}. {img_url}")

print(f"\nTotal pagini vizitate: {len(visited_urls)}")
print(f"Total imagini găsite: {len(image_urls)}")