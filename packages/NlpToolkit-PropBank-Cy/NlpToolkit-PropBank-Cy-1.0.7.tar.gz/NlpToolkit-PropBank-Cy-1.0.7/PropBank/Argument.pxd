cdef class Argument(object):

    cdef str __argumentType
    cdef str __id

    cpdef initWithId(self, str argumentType, str _id)
    cpdef str getArgumentType(self)
    cpdef str getId(self)
