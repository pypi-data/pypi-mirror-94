import typing

def _getData(table: typing.List[list], filler:str):
    "get data used for rendering more specificly: longest element longest collum lenth"
    longestElement = len(filler)
    longerstRow = 0
    if not isinstance(table, list): raise TypeError(f"parameter table must be type list not {type(table).__name__}")
    for row in table:
        if not isinstance(row, list): raise TypeError(f"parameter table must only contain lists no {type(row).__name__}'s")
        if longerstRow < len(row):
            longerstRow = len(row)


        for thingy in row:
            if not hasattr(thingy, "__str__"): raise TypeError(f"can't convert object of type {type(thingy).__name__} to str") # maybe
            if (longestElement < len(str(thingy))):
                longestElement = len(str(thingy))
    
    return longerstRow, longestElement+1


def _horizontalLine(longestElement:int, lenth:int, splitter:bool=False):
    if splitter: element = ("+" + "-"*longestElement + "-")*lenth + "+"
    else: element = "+" + "-"*longestElement*lenth + "-+"
    print(element)


def printRow(row:list, length:int, filler:str, longestElement:int, splitters:bool):
    "internaly print out 1 row"
    if splitters: 
        _horizontalLine(longestElement, length, splitters)
    print("|", end=" ")

    for idx in range(length):
        if idx < len(row):
            print(row[idx], end=" "*(longestElement- len(str(row[idx]))))
        else:
            print(filler, end=" "*(longestElement-len(filler)))
        
        if splitters: print("|", end=" ")
    if not splitters: print("|", end="")
    print()
    

def printTable(table:typing.List[list], renderInner=False, filler="") -> None:
    """given a table in 2d list form render a table containing those elements
    
    the first dimention of the list will beh rows and the second collums
    the list dose not have to be rectangular howerver the empties will be filled with the parameter filler"""
    longerstRow, longestElement = _getData(table, filler)

    if not renderInner: _horizontalLine(longestElement, longerstRow, renderInner)

    for row in table:
        printRow(row, longerstRow, filler, longestElement, renderInner)
    
    _horizontalLine(longestElement, longerstRow, renderInner)