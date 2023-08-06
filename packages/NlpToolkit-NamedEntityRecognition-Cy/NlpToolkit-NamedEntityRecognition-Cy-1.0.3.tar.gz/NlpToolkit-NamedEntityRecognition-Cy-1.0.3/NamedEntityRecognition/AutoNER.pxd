from NamedEntityRecognition.Gazetteer cimport Gazetteer


cdef class AutoNER:

    cdef Gazetteer personGazetteer, organizationGazetteer, locationGazetteer
