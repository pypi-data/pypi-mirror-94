from xml.etree.ElementTree import Element

from DependencyParser.Turkish.TurkishDependencyTreeBankWord cimport TurkishDependencyTreeBankWord


cdef class TurkishDependencyTreeBankSentence(Sentence):

    def __init__(self, sentenceNode: Element):
        """
        Given the parsed xml node which contains information about a sentence, the method constructs a
        TurkishDependencyTreeBankSentence from it.

        PARAMETERS
        ----------
        sentenceNode : Element
            Xml parsed node containing information about a sentence.
        """
        super().__init__()
        for wordNode in sentenceNode:
            word = TurkishDependencyTreeBankWord(wordNode)
            self.words.append(word)

    cpdef int maxDependencyLength(self):
        """
        Calculates the maximum of all word to related word distances, where the distances are calculated in terms of
        index differences.

        RETURNS
        -------
        int
            Maximum of all word to related word distances.
        """
        cdef int maxLength, i
        cdef TurkishDependencyTreeBankWord word
        maxLength = 0
        for i in range(len(self.words)):
            word = self.words[i]
            if word.getRelation() is not None and word.getRelation().to() - i > maxLength:
                maxLength = word.getRelation().to() - i
        return maxLength
