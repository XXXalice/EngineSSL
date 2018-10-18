import kernel

class WordCollector(kernel.Kernel):

    def __init__(self):
        super().__init__('wikipedia.bin')

    def get_words(self, word, num, sim=False):
        if sim == False:
            res = super().get_notsim(word, num)
        else:
            res = super().get_sim(word, num)
        return res




wc = WordCollector()
words = wc.get_words('月', 5)
print(words)