import kernel

class WordCollector(kernel.Kernel):

    def __init__(self):
        super().__init__('wikipedia.bin')
        self.fnc = ['super().get_sim({},{})', 'super().get_notsim({},{})']

    def get_words(self, word, num, sim=False):
        if sim == False:
            word_query = "'" + word + "'"
            res = exec(self.fnc[1].format(word_query, num))
            return res



wc = WordCollector()
words = wc.get_words('月', 5)
print(words)