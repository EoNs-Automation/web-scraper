import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime

def scrape_website():
    print("=== Web Scraper ===")
    print("Type 'quit' to exit.\n")

    while True:
        url = input("Enter website URL to scrape: ").strip()

        if url.lower() == "quit":
            print("Goodbye!")
            break

        if not url.startswith("http"):
            url = "https://" + url

        try:
            print("\nFetching page...")
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except Exception as e:
            print(f"Error fetching page: {e}\n")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        print("\nWhat would you like to extract?")
        print("1. All page text")
        print("2. All links")
        print("3. All headings (h1, h2, h3)")
        print("4. All images")

        choice = input("\nChoose an option (1-4): ").strip()

        script_folder = os.path.dirname(os.path.abspath(__file__))
        output_folder = os.path.join(script_folder, "scraped_data")
        os.makedirs(output_folder, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if choice == "1":
            text = soup.get_text(separator="\n", strip=True)
            filename = f"page_text_{timestamp}.txt"
            filepath = os.path.join(output_folder, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"\nSaved page text to:\n{filepath}\n")

        elif choice == "2":
            links = []
            for a in soup.find_all("a", href=True):
                href = a["href"]
                text = a.get_text(strip=True)
                links.append([text, href])

            filename = f"links_{timestamp}.csv"
            filepath = os.path.join(output_folder, filename)
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Link Text", "URL"])
                writer.writerows(links)
            print(f"\nFound {len(links)} links.")
            print(f"Saved to:\n{filepath}\n")

        elif choice == "3":
            headings = []
            for tag in ["h1", "h2", "h3"]:
                for heading in soup.find_all(tag):
                    headings.append([tag.upper(), heading.get_text(strip=True)])

            filename = f"headings_{timestamp}.csv"
            filepath = os.path.join(output_folder, filename)
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Type", "Text"])
                writer.writerows(headings)
            print(f"\nFound {len(headings)} headings.")
            print(f"Saved to:\n{filepath}\n")

        elif choice == "4":
            images = []
            for img in soup.find_all("img"):
                src = img.get("src", "")
                alt = img.get("alt", "")
                images.append([alt, src])

            filename = f"images_{timestamp}.csv"
            filepath = os.path.join(output_folder, filename)
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Alt Text", "Image URL"])
                writer.writerows(images)
            print(f"\nFound {len(images)} images.")
            print(f"Saved to:\n{filepath}\n")

        else:
            print("Invalid option.\n")


if __name__ == "__main__":
    scrape_website()