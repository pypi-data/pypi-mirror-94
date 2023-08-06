from DependencyParser.DependencyRelation cimport DependencyRelation


cdef class TurkishDependencyRelation(DependencyRelation):

    cdef int __toIG
    cdef object __turkishDependencyType

    cpdef int toIG(self)
    cpdef object getTurkishDependencyType(self)
