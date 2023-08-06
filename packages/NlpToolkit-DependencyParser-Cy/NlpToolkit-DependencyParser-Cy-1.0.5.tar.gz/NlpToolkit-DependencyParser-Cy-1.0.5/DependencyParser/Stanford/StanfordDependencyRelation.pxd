from DependencyParser.DependencyRelation cimport DependencyRelation


cdef class StanfordDependencyRelation(DependencyRelation):

    cdef int __toIG
    cdef object __stanfordDependencyType
