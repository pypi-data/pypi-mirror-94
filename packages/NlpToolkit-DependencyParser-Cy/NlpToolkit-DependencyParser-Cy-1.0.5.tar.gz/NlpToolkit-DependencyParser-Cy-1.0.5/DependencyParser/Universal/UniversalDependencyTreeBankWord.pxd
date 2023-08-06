from Dictionary.Word cimport Word
from DependencyParser.Universal.UniversalDependencyRelation cimport UniversalDependencyRelation
from DependencyParser.Universal.UniversalDependencyTreeBankFeatures cimport UniversalDependencyTreeBankFeatures


cdef class UniversalDependencyTreeBankWord(Word):

    cdef int id
    cdef str lemma
    cdef object upos
    cdef str xpos
    cdef UniversalDependencyTreeBankFeatures features
    cdef UniversalDependencyRelation relation
    cdef str deps
    cdef str misc

    cpdef int getId(self)
    cpdef str getLemma(self)
    cpdef object getUpos(self)
    cpdef str getXPos(self)
    cpdef UniversalDependencyTreeBankFeatures getFeatures(self)
    cpdef str getFeatureValue(self, str featureName)
    cpdef UniversalDependencyRelation getRelation(self)
    cpdef str getDeps(self)
    cpdef str getMisc(self)
