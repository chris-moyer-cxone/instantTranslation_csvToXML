from functools import total_ordering
from pprint import pprint

@total_ordering
class LangTerm:
    srcRowNum: int
    key: str
    value: str
    unique: bool
    def __init__(self, key, value, *_, srcRow:int=None, hashValue:bool=False, unique:bool=False) -> None:
        self.key = key
        self.value = value
        self.srcRowNum = 0 if srcRow is None else srcRow
        self.hashValue = hashValue
        self.unique = unique
    def __eq__(self, __o) -> bool:
        if __o is None and self is None: return True
        if __o is None and self is not None: return False
        return True if self.key == __o.key and self.value == __o.value else False

    def __gt__(self, __o) -> bool:
        if __o is None and self is None: return False
        if __o is None and self is not None: return True
        return True if self.key > __o.key else False
    
    def __repr__(self) -> str:
        return f"row: {self.srcRowNum} key: {self.key} value: {self.value}"
    
    def __hash__(self) -> int: 
        if self.unique: return hash(self.key, self.value, self.srcRowNum)
        elif self.hashValue: return hash(self.key, self.value)
        else: return hash(self.key)

class LangDict:
    langCode: str
    terms: list[LangTerm]
    def __init__(self, langCode, *_, terms:list=None) -> None:
        self.langCode = langCode
        self.terms = terms if terms != None else list()
    
    def __hash__(self) -> int: return hash(self.langCode)

    def applyUnique(self, level=0):
        '''Apply uniqueness level to all terms. 0: key only, 1: key + value, 2: key+value+srcRowNum'''
        if level == 0: 
            for term in self.terms:
                term.unique = False
                term.hashValue = False
        if level == 1: 
            for term in self.terms:
                term.unique = False
                term.hashValue = True
        if level == 2: 
            for term in self.terms:
                term.unique = True
                term.hashValue = False
    
    def getDuplicates(self)-> list:
        termCache = self.terms.copy()
        duplicateTerms = []
        tmpStack = []
        termCache.sort()
        for term in termCache:
            tmpStack.append(term)
            for compareTerm in termCache:
                if term == compareTerm: continue
                if term.key == compareTerm.key:
                    tmpStack.append(compareTerm)
            if len(tmpStack) > 1: duplicateTerms.extend(tmpStack)
            for term in duplicateTerms:
                termCache.remove(term)
            tmpStack = []
        return duplicateTerms
    
    def getSet(self):
        return set(self.terms)
    
    def sortByRowNum(key) -> list:
        '''Pass this as a key func to the list.sort method'''
        return key['srcRowNum']

    def printTerms(self, *_, silent=False, sep='\n'):
        builder = ''
        for term in self.terms:
            brick = f"{self.langCode}: {term.srcRowNum}, {term.key} : {term.value}{sep}"
            builder += brick
            if not silent: print(brick)
        return builder

# dict = LangDict('en', terms=[
#     LangTerm('test1', 'val1', srcRow=1),
#     LangTerm('test2', 'val2', srcRow=2),
#     LangTerm('test1', 'val3', srcRow=3)
# ])

# pprint(dict.getDuplicates())
