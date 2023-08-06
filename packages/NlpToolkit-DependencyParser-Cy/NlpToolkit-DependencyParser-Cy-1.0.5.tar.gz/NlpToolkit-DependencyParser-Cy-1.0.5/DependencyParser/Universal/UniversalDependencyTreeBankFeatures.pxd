cdef class UniversalDependencyTreeBankFeatures:

    cdef dict featureList

    cpdef str getFeatureValue(self, str feature)
