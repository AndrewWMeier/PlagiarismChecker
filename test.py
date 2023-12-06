from googlesearch import search
import requests
from bs4 import BeautifulSoup
import hashlib

#extracts paragraphs from website urls, this is called by the get_google_results function
def get_website_content(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        #extract text from paragraphs
        paragraphs = soup.find_all('p')
        text_content = ' '.join([paragraph.get_text() for paragraph in paragraphs])

        return text_content
    except Exception as e:
        print(f"An error occurred while fetching content: {e}")
        return None
    
#searches google for the query and returns the content of the first 3 results
def get_google_results(query, num_results=3):
    try:
        search_results = list(search(query, num_results=num_results))
        #initlize the array to store the paragraphs of each website
        all_content = []
        for i, result in enumerate(search_results, start=1):
            # print(f"Result {i}:\n{result}")
            content = get_website_content(result)
            if content:
                all_content.append(content)
                # print(f"Content:\n{content[:500]}\n...\n")  # Displaying the first 500 characters of content
        return all_content
    except Exception as e:
        print(f"An error occurred: {e}")

#creates a set of shingles for each text sample
def generate_shingles(text, shingle_size):
    shingles = set()
    words = text.split()
    for i in range(len(words) - shingle_size + 1):
        shingle = " ".join(words[i:i + shingle_size])
        shingles.add(shingle)
    return shingles

#creates a signature for each text sample
def minhash(shingles, num_hash_functions):
    hash_functions = [hashlib.md5, hashlib.sha1, hashlib.sha256]  # 3 hash functions
    signatures = []

    for hash_function in hash_functions[:num_hash_functions]:
        min_hash = float('inf')
        for shingle in sorted(shingles):  # Sort the shingles before hashing
            hash_value = int(hash_function(shingle.encode()).hexdigest(), 16)
            min_hash = min(min_hash, hash_value)
        signatures.append(min_hash)

    return signatures


#calculates jaccard similarity
def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union

#calculates the similarity score between the text sample and each of the possible matches
def plagiarism_score(text, possible_matches, shingle_size=8, num_hash_functions=3):
    text_shingles = generate_shingles(text, shingle_size)
    text_signature = minhash(text_shingles, num_hash_functions)

    scores = []
    for match in possible_matches:
        match_shingles = generate_shingles(match, shingle_size)
        match_signature = minhash(match_shingles, num_hash_functions)
        similarity = jaccard_similarity(set(text_signature), set(match_signature))
        scores.append(similarity)

    return scores

#converts the text to lowercase and removes newlines
def data_cleanup(text):
    text = text.lower()
    text = text.replace("\n", "")
    return text



#using the functions above to test the plagiarism score function

#get user input and create a list of text samples
user_query = input("Enter text to analyze: ")
text_samples = get_google_results(user_query)

#clean up the text samples
for i in range(len(text_samples)):
    text_samples[i] = data_cleanup(text_samples[i])

#clean up the user query
user_query = data_cleanup(user_query)

#test the plagiarism score function
scores = plagiarism_score(user_query, text_samples)
print("-----------------------------------------------------------------")
print(text_samples[0])
print("-----------------------------------------------------------------")
print(text_samples[1])
print("-----------------------------------------------------------------")
print(text_samples[2])
print("-----------------------------------------------------------------")
print(scores)



