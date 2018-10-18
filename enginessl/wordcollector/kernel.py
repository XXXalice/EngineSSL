class Kernel:
    def __init__(self, corpus):
        from gensim.models import KeyedVectors as kv
        try:
            self.model = kv.load_word2vec_format('./src/' + corpus, binary=True)
        except:
            print('[gensimError] Failed to load corpus.')
            exit()

    def get_sim(self, word, num):
        sims = self.model.most_similar(positive=[word], topn=num)
        words = [sim[0].replace('[','').replace(']','') for sim in sims]
        return words

    def get_notsim(self, word, num):
        sims = self.model.most_similar(negative=[word], topn=num)
        words = [sim[0].replace('[','').replace(']','') for sim in sims]
        return words
    
