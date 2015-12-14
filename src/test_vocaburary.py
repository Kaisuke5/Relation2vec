import PMI
import pickle

if __name__=="__main__":
	c=PMI.Corpus()
	c.load_corpus()
	c.factorize(d=15)

