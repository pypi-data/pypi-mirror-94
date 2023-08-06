from Corpus.Corpus cimport Corpus
from Corpus.Sentence cimport Sentence


cdef class NERCorpus(Corpus):

    cpdef addSentence(self, Sentence s)
