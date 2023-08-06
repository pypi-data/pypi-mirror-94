cdef class Gazetteer:

    def __init__(self, name: str, fileName: str):
        """
        A constructor for a specific gazetteer. The constructor takes name of the gazetteer and file name of the
        gazetteer as input, reads the gazetteer from the input file.

        PARAMETERS
        ----------
        name : str
            Name of the gazetteer. This name will be used in programming to separate different gazetteers.
        fileName : str
            File name of the gazetteer data.
        """
        cdef str line
        cdef list lines
        self.__name = name
        self.__data = set()
        inputFile = open(fileName, "r", encoding="utf8")
        lines = inputFile.readlines()
        for line in lines:
            self.__data.add(line.strip())

    cpdef str getName(self):
        """
        Accessor method for the name of the gazetteer.

        RETURNS
        -------
        str
            Name of the gazetteer.
        """
        return self.__name

    cpdef bint contains(self, str word):
        """
        The most important method in Gazetteer class. Checks if the given word exists in the gazetteer. The check
        is done in lowercase form.

        PARAMETERS
        ----------
        word : str
            Word to be search in Gazetteer.

        RETURNS
        -------
        bool
            True if the word is in the Gazetteer, False otherwise.
        """
        lowerMap = {
            ord(u'I'): u'ı',
            ord(u'İ'): u'i',
        }
        return word.translate(lowerMap).lower() in self.__data
