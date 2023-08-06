from DependencyParser.Universal.UniversalDependencyPosType import UniversalDependencyPosType


cdef class UniversalDependencyTreeBankWord(Word):

    def __init__(self, id: int, name: str, lemma: str, upos: UniversalDependencyPosType, xpos: str,
                 features: UniversalDependencyTreeBankFeatures, relation: UniversalDependencyRelation, deps: str,
                 misc: str):
        super().__init__(name)
        self.id = id
        self.lemma = lemma
        self.upos = upos
        self.xpos = xpos
        self.deps = deps
        self.features = features
        self.relation = relation
        self.misc = misc

    cpdef int getId(self):
        return self.id

    cpdef str getLemma(self):
        return self.lemma

    cpdef object getUpos(self):
        return self.upos

    cpdef str getXPos(self):
        return self.xpos

    cpdef UniversalDependencyTreeBankFeatures getFeatures(self):
        return self.features

    cpdef str getFeatureValue(self, str featureName):
        return self.features.getFeatureValue(featureName)

    cpdef UniversalDependencyRelation getRelation(self):
        return self.relation

    cpdef str getDeps(self):
        return self.deps

    cpdef str getMisc(self):
        return self.misc

    def __str__(self) -> str:
        return self.id.__str__() + "\t" + self.name + "\t" + self.lemma + "\t" + self.upos.__str__() + "\t" + \
               self.xpos + "\t" + self.features.__str__() + "\t" + self.relation.to().__str__() + "\t" + \
               self.relation.__str__().lower() + "\t" + self.deps + "\t" + self.misc
