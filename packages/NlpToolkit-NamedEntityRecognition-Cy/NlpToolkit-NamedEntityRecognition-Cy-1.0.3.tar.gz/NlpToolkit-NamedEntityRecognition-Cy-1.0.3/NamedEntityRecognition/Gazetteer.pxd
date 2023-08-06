cdef class Gazetteer:

    cdef set __data
    cdef str __name

    cpdef str getName(self)
    cpdef bint contains(self, str word)
