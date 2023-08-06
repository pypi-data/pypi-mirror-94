from Dictionary.Word cimport Word


cdef class UniversalDependencyTreeBankSentence(Sentence):

    def __init__(self):
        super().__init__()
        self.comments = []

    cpdef addComment(self, str comment):
        self.comments.append(comment)

    def __str__(self) -> str:
        cdef str result
        cdef Word word
        result = ""
        for comment in self.comments:
            result += comment + "\n"
        for word in self.words:
            result += word.__str__() + "\n"
        return result
