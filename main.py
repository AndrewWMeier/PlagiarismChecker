from googlesearch import search
import requests
from bs4 import BeautifulSoup
import hashlib
from nltk.tokenize import sent_tokenize
import nltk
from Source import Source
from Comparison import Comparison


nltk.download('punkt')


# extracts paragraphs from website urls, this is called by the get_google_results function
def get_website_content(url):
    try:
        print(f"\nFetching {url}...")
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # extract text from paragraphs
        paragraphs = soup.find_all('p')
        text_content = ' '.join([paragraph.get_text()
                                for paragraph in paragraphs])

        return text_content
    except Exception as e:
        print(f"An error occurred while fetching content: {e}")
        return None


# searches google for the query and returns objects containing clean sentences from the sources and the url of the first 3 results
def get_google_results(query, num_results=3):
    try:
        search_results = list(search(query, num_results=num_results))
        # initialize the array to store the Source objects
        all_sources = []
        # limit to num_results
        for i, result in enumerate(search_results[:num_results], start=1):
            # print(f"Result {i}:\n{result}")
            content = get_website_content(result)
            if content:
                # clean up the content and create a source object
                cleaned_content = data_cleanup(content)
                source = Source(cleaned_content, result)
                all_sources.append(source)
                source.set_url(result)
        return all_sources

    except Exception as e:
        print(f"An error occurred: {e}")


# data cleanup function
def data_cleanup(text):
    # to lowercase and remove unnecessary spacing
    text = text.lower()
    text = text.replace("\n", "")
    # Use NLTK to tokenize the text into sentences
    sentences = nltk.sent_tokenize(text)
    return sentences


# compare the user query with the text samples
def compare_sentences(user_query, sources):
    result = []
    for source in sources:
        for sentence_sample in source.get_sentences():
            for sentence_user in user_query:
                # Compare sentence_user with sentence_sample
                # print(f"Comparison Result for Sentence {k+1} (User) vs Sentence {j+1} (Sample {i+1}):")
                # print(f"User Sentence: {sentence_user}")
                # print(f"Sample Sentence: {sentence_sample}")
                # print("-----------------------------------------------------------------")
                comparison = Comparison(
                    sentence_user, sentence_sample, None, source.get_url())

                if (__name__ == '__main__'):
                    print(f"\nSimilarity score: {comparison.similarity}")
                    print(f"User Sentence: {sentence_user}")
                    print(f"Sample Sentence: {sentence_sample}")
                    print(f"Source URL: {comparison.url}")
                    print(
                        "-----------------------------------------------------------------\n")
                else:
                    # return as json object
                    result.append(dict(
                        similarity=comparison.similarity,
                        user_sentence=sentence_user,
                        sample_sentence=sentence_sample,
                        source_url=comparison.url
                    ))

    if (__name__ != '__main__'):
        return result


if __name__ == '__main__':
    # get user input and create a list of text samples from google
    user_query = input("Enter text to analyze:")
    text_samples = get_google_results(user_query)

    # clean up the user query
    user_query = data_cleanup(user_query)

    # compare the user query with the text samples
    compare_sentences(user_query, text_samples)
