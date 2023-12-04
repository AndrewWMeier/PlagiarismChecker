from googlesearch import search
import requests
from bs4 import BeautifulSoup

def get_website_content(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract text from paragraphs
        paragraphs = soup.find_all('p')
        text_content = ' '.join([paragraph.get_text() for paragraph in paragraphs])

        return text_content
    except Exception as e:
        print(f"An error occurred while fetching content: {e}")
        return None

def get_google_results(query, num_results=3):
    try:
        search_results = list(search(query, num_results=num_results))

        for i, result in enumerate(search_results, start=1):
            print(f"Result {i}:\n{result}")
            content = get_website_content(result)
            
            if content:
                print(f"Content:\n{content[:500]}\n...\n")  # Displaying the first 500 characters of content
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    user_query = input("Enter your search query: ")
    get_google_results(user_query)

