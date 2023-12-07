class Comparison:
    def __init__(self, user_sentence, sample_sentence, similarity, url):
        self.user_sentence = user_sentence
        self.sample_sentence = sample_sentence
        self.similarity = score_calculator(user_sentence, sample_sentence)
        self.url = url
        
def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0

def score_calculator(user_sentence, sample_sentence):
    user_words = set(user_sentence.split())
    sample_words = set(sample_sentence.split())
    return jaccard_similarity(user_words, sample_words)

