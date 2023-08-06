from DependencyParser.DependencyRelation cimport DependencyRelation


cdef class UniversalDependencyRelation(DependencyRelation):

    cdef object __universalDependencyType
