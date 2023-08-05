from os.path import dirname, join
from os import listdir, remove
from shutil import copyfile
from warnings import warn
import atexit, webbrowser

__all__ = ["htmlTable", "clearSlait"]

tables = []

tableInstances = []


def buildName():
    itr = 0
    while f"table{itr}.html" in listdir(join(dirname(__file__), "tables")):
        itr+=1
    
    tables.append(itr)
    return f"table{itr}"

def destroyAll():
    global tableInstances
    for e in tableInstances:
        e.delete()
    tableInstances=[]
    
    for itr in tables:
        remove(join(dirname(__file__), "tables", f"table{itr}.html"))

atexit.register(destroyAll)

def clearSlait():
    warn(f"html slait is the same for all interpreter instances clearing it may cause issues")
    global tableInstances
    for e in tableInstances:
        e.delete()
    tableInstances = []

    for f in listdir(join(dirname(__file__), "tables")):
        remove(join(dirname(__file__), "tables", f))

class htmlTable:
    """html table handler
    """
    _alive = False
    def __init__(self, inp, name="table", **kwargs):
        """create an html table form input with name name

        currently the input (inp) must be a list of lists of printable elements

        @param keyIdx: the position at witch the name of the name of the row is located tey are just bold
        @param keyIdx: the position at witch the name of the name of the Colum is located they are just bold
        """
        data = {
            "keyRowIdx": -1,
            "keyColIdx": -1,
            "border": 0,
            "encoding": "utf-8",
            "caption": "",
            }
        
        data.update(kwargs)



        tableInstances.append(self)
        self.name = buildName()
        self._encoding = data["encoding"]
        self._alive = True
        self.indentLvl = 3
        self.head = f"""<html>\n
    <head>
        <title>{name}</title>
    </head>

    <body>                        
        <table border="{data["border"]}">
        <meta charset="{data["encoding"]}"/>
        <caption>{data["caption"]}</caption>\n"""
        self.tail = """\t</table>
    </body>
</html>"""

        if isinstance(inp, list): self._buildFromList(inp, data)

        self.head+= self.tail
        self.cach()
    
    def cach(self):
        "temp save the file"
        with open(f"{dirname(__file__)}/tables/{self.name}.html", "w", encoding=self._encoding) as f:
            f.write(self.head)
    
    def indent(self):
        self.head += "\t"*self.indentLvl

    def _buildFromList(self, inp, data):
        
        def buildRow(row, handler="th"):
            self.indent()
            self.head += "<tr>\n"
            self.indentLvl+=1
            for idx, element in enumerate(row):
                self.indent()

                if idx== data["keyRowIdx"]: self.head += f"<th>{element}</th>\n"
                else: self.head += f"<{handler}>{element}</{handler}>\n"

            self.indentLvl-=1
            self.indent()
            self.head += "</tr>\n"
        
        for idx, row in enumerate(inp):
            buildRow(row, "th" if idx == data["keyColIdx"] else "td")

    def open(self):
        webbrowser.open(join(dirname(__file__), "tables", f"{self.name}.html"))
    
    def open_new(self):
        webbrowser.open_new(join(dirname(__file__), "tables", f"{self.name}.html"))

    def open_new_tab(self):
        webbrowser.open_new_tab(join(dirname(__file__), "tables", f"{self.name}.html"))
    
    def delete(self):
        self._alive=False
        tableInstances.remove(self)
        remove(join(dirname(__file__), "tables", f"{self.name}.html"))

    def copyFile(self, path):
        "copys the html file to path"
        copyfile(join(dirname(__file__), "tables", f"{self.name}.html"), path)
    
    def __str__(self):
        return f"htmlTable<active: {self._alive}, id: {self.name}, encoding: {self._encoding}>"
    __repr__=__str__