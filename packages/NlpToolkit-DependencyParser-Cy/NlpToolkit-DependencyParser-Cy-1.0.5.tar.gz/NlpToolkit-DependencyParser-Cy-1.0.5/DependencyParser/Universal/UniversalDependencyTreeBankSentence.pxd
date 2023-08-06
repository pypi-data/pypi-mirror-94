from Corpus.Sentence cimport Sentence


cdef class UniversalDependencyTreeBankSentence(Sentence):

    cdef list comments

    cpdef addComment(self, str comment)
