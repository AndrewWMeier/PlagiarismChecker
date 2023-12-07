class Source:
    def __init__(self, sentences, url):
        self.sentences = sentences
        self.url = url

    def set_url(self, url):
        self.url = url

    def set_sentences(self, sentences):
        self.sentences = sentences

    def get_url(self):
        return self.url

    def get_sentences(self):
        return self.sentences
        
        

    