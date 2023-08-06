from lark import Lark, Transformer,Token
import re

## Fasta related grammars ##
fasta_header1=re.compile(r"(?P<db>\w+)\|(?P<uid>\w+)\|(?P<name>\w+)(?:/(?P<beg>\d+)-(?P<end>\d+))?(?P<descr>.+) OS=(?P<os>.+) OX=(?P<ox>\d+) (?:GN=(?P<gn>.+) )?PE=(?P<pe>\d+) SV=(?P<sv>\d+)") # UNIPROT
fasta_header2=re.compile(r"(?P<db>\w+)\|(?P<uid>\w+)\|(?P<name>\w+)(?:/(?P<beg>\d+)-(?P<end>\d+))?(?P<descr>.+)?")                                                                              # UNIPROT without key-value fields
fasta_header3=re.compile(r"(?P<uid>[^ /]+)(?:/(?P<beg>\d+)-(?P<end>\d+))?(?P<descr>.+)?")                                                                                                       # general match >NAME/beg-end DESCR
fasta_header_rules=[fasta_header1,fasta_header2,fasta_header3]


## AWK related grammars and utils ##
AWK_GRAMMAR="""

beginblock : "\BEGIN"block
mainblock : condition block | condition | block
endblock : "\END"block

program : [beginblock] mainblock [endblock]

condition : /[^{}\\\]+/

code : (/[^{}\\\]+/|block)+
block : "{"(code|block)+"}"

%import common.ESCAPED_STRING
%import common.SIGNED_NUMBER
%import common.WS
%ignore WS
"""

class awkParsing:
  def __init__(self):
    self.codestring={"beginblock":"","mainblock":"","endblock":""}
  def build(self,tree,level=0):
    for subtree in tree.children:
      branch=subtree.data
      if branch=="mainblock":
        data=[c.data for c in subtree.children]
        if "condition" not in data or len(self.visit(subtree.children[data.index("condition")],level=0)[:-1].strip())==0:
          self.codestring[branch]="if True:\n"
        else:
          self.codestring[branch]="if("+self.visit(subtree.children[data.index("condition")],level=0)[:-1]+"):\n"
        if "block" not in data:
          self.codestring[branch]+="  print(seq)\n"
        else:
          self.codestring[branch]+=self.visit(subtree.children[data.index("block")],level=1)
      else:
        self.codestring[branch]=self.visit(subtree,level=-1)
    return self.codestring
    
  def visit(self,tree,level,string=""):
    if type(tree)==Token:
      return "".join(["  "*level+value.strip()+"\n" for value in str(tree).strip().split(';')])
    for subtree in tree.children:
      if type(subtree)==Token:
        string+="".join(["  "*level+value.strip()+"\n" for value in str(subtree).strip().split(';')])
      elif subtree.data=="code":
        string=self.visit(subtree,level,string)
      elif subtree.data=="block":
        if len(string):
          string=string[:-1]+":\n"
        string=self.visit(subtree,level+1,string)
    return string

awk_parser = Lark(AWK_GRAMMAR, start="program")
awk_tree = awkParsing()

##
