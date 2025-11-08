APP_INFO = {
    "name": "Cyb_browser",
    "icon": "🌐",
    "description": "Browse the internet"
}

from core import utils
import requests
from bs4 import BeautifulSoup

def launch():
    utils.clear_console()
    utils.Print_Typing(utils.Colors.col_text("Welcome to Cyber_Browser\n", color_code=utils.Colors.BRIGHT_MAGENTA), fast=False)
    url = input("\nEnter URL (or 'q' to quit) > ").strip()
    while True:
        if url.lower() in ("q", "quit", "exit"):
            utils.clear_console()
            break
        if not url.startswith("http"):
            url = "https://" + url
            utils.clear_console()
            fetch_and_display(url)

def fetch_and_display(url):
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            )
        }

        utils.Print_Typing(f"Fetching {url} ...\n", fast=False)
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(res.text, "html.parser")

        title = soup.title.string if soup.title else "(No title)"
        utils.Print_Typing(utils.Colors.col_text(f"\n{title}\n", utils.Colors.BRIGHT_GREEN), fast=False)

        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        # Prefer article or main content
        article = soup.find("article") or soup.find("main")

        if article:
            paragraphs = [p.get_text(strip=True) for p in article.find_all("p") if p.get_text(strip=True)]
        else:
            paragraphs = [p.get_text(strip=True) for p in soup.find_all("p") if p.get_text(strip=True)]

        # Combine and trim long text
        text = "\n\n".join(paragraphs[:20])  # temporary limit
        if not text:
            text = "(No readable content found)"

        utils.Print_Typing(utils.Colors.col_text("\n--- Content ---\n", utils.Colors.BRIGHT_CYAN), fast=False)
        #print(text)

                # --- Display content with pagination ---
        utils.Print_Typing(utils.Colors.col_text("\n--- Content ---\n", utils.Colors.BRIGHT_CYAN), fast=False)

        lines = text.splitlines()
        page_size = 25  # number of lines per "page"
        total_lines = len(lines)

        current = 0
        while current < total_lines:
            end = current + page_size
            for line in lines[current:end]:
                print(line)
            current = end

            if current < total_lines:
                cmd = input(utils.Colors.col_text("\n[Press Enter to continue, 'q' to quit reading] ", utils.Colors.BRIGHT_MAGENTA)).strip().lower()
                if cmd in ("q", "quit", "exit"):
                    break
            else:
                print(utils.Colors.col_text("\n[End of Page]", utils.Colors.BRIGHT_MAGENTA))

        # Placeholder for readable text extraction (coming next)
        #print("\n[Page fetched successfully — content extraction coming soon]")

    except requests.exceptions.HTTPError as e:
        print(utils.Colors.col_text(f"\nHTTP Error: {e}", utils.Colors.RED))
    except requests.exceptions.ConnectionError:
        print(utils.Colors.col_text("\nConnection failed — check your internet.", utils.Colors.RED))
    except Exception as e:
        print(utils.Colors.col_text(f"\nError: {e}", utils.Colors.RED))
