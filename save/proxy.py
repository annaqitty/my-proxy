import requests

# List of proxy source URLs for European countries
proxy_urls = [
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=DE&ssl=yes&anonymity=all",  # Germany
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=FR&ssl=yes&anonymity=all",  # France
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=IT&ssl=yes&anonymity=all",  # Italy
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=ES&ssl=yes&anonymity=all",  # Spain
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=GB&ssl=yes&anonymity=all",  # United Kingdom
    "https://proxify.io/api/proxies?country=DE&protocol=http",  # Germany
    "https://proxify.io/api/proxies?country=FR&protocol=http",  # France
    "https://proxify.io/api/proxies?country=IT&protocol=http",  # Italy
    "https://proxify.io/api/proxies?country=ES&protocol=http",  # Spain
    "https://proxify.io/api/proxies?country=GB&protocol=http",  # United Kingdom
    "https://www.free-proxy-list.net/"  # General list, can filter by country later if needed
]

def fetch_proxies(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        return response.text
    except requests.RequestException as e:
        print(f"An error occurred with URL {url}: {e}")
        return None

def save_proxies(proxy_lists):
    with open("europe_proxies.txt", "w") as file:
        for proxies in proxy_lists:
            if proxies:
                file.write(proxies + "\n")

def main():
    proxy_lists = []
    for url in proxy_urls:
        proxies = fetch_proxies(url)
        if proxies:
            proxy_lists.append(proxies)

    if proxy_lists:
        save_proxies(proxy_lists)
        print("Proxy list saved to europe_proxies.txt")
    else:
        print("Failed to fetch proxy list from all sources")

if __name__ == "__main__":
    main()
