import nltk

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""
        fp = open(positives)
        """except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)"""
        fn = open(negatives)
        """except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)"""
        # TODO
        self.positives = [i.strip() for i in fp.readlines() if not i.startswith(";") and i!='']
        self.negatives = [i.strip() for i in fn.readlines() if not i.startswith(";") and i!='']
        fp.close()
        fn.close()

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        self.score = 0
        tokenizer = nltk.TweetTokenizer(strip_handles=True, reduce_len=True)
        tweettokens = [i.lower() for i in tokenizer.tokenize(text) if len(i)>2]
        for token in tweettokens:
                if token in self.positives:
                    self.score = self.score + 1
                elif token in self.negatives:
                    self.score = self.score - 1
        #print(tweettokens, "\t score = ",self.score)
        # TODO
        return self.score
