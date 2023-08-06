#!/usr/bin/env python
import re
import sys

from fastaUtils.grammars import fasta_header_rules

default_int=-1
default_str='None'

def parse(x,type_,default):
  try:
    return type_(x)
  except:
    return default

def iterate_sequences(cmd_beg,cmd_main,cmd_end,sequences,**kwargs):
  for name, value in kwargs.items():
    exec("{} = {}".format(name, value))
  exec(cmd_beg)
  for NR,seq in enumerate(sequences):
    db,uid,name,descr,os,ox,gn,pe,sv,beg,end=parse_header(seq.header.strip())
    exec(cmd_main)
  exec(cmd_end)

class seqRecord:
  def __init__(self,header,sequence=""):
    self.header=header
    self.seq=sequence
  def append(self,sequence):
    self.seq+=sequence
  def __repr__(self):
    return "seqRecord object: {}; sequence length: {}".format(self.header,len(self.seq))
  def __str__(self):
    return ">{}\n{}".format(self.header,self.seq)

def parse_fasta(fastafile):
  s=None
  if fastafile is None:
    for line in sys.stdin:
      if line[0]=='>':
        if s is not None:
          yield s
        s=seqRecord(line.strip()[1:])
      else:
        s.append(line.strip())
    yield s
  else:
    with open(fastafile,'r') as infile:
      for line in infile:
        if line[0]=='>':
          if s is not None:
            yield s
          s=seqRecord(line.strip()[1:])
        else:
          s.append(line.strip())
      yield s

def parse_header(header):
  for r in fasta_header_rules:
    m=re.match(r,header)
    if m is not None:
      d=dict(m.groupdict(default='-'))
      return d.get('db',default_str), d.get('uid',default_str), d.get('name',default_str), d.get('descr',default_str), \
             d.get('os',default_str), parse(d.get('ox',default_int),int,default_int), d.get('gn',default_str), parse(d.get('pe',default_int),int,default_int), \
             parse(d.get('sv',default_int),int,default_int), parse(d.get('beg',default_int),int,default_int), parse(d.get('end',default_int),int,default_int)
  return default_str,default_str,default_str,default_str,default_str,default_int,default_str,default_int,default_int,default_int,default_int

def generate_header(db,uid,name,descr=default_str,os=default_str,ox=default_int,gn=default_str,pe=default_int,sv=default_int,beg=default_int,end=default_int):
  if db!=default_str and name!=default_str:
    if beg!=default_int and end!=default_int:
      header="{}|{}|{}/{}-{}".format(db,uid,name,beg,end)
    else:
      header="{}|{}|{}".format(db,uid,name)
  else:
    if beg!=default_int and end!=default_int:
      header="{}/{}-{}".format(uid,beg,end)
    else:
      header="{}".format(uid)
  if descr!=default_str:
    header+=" "+descr.strip()
  if gn!=default_str:
    header+=" OS={} OX={} GN={} PE={} SV={}".format(os,ox,gn,pe,sv)
  elif os!=default_str:
    header+=" OS={} OX={} PE={} SV={}".format(os,ox,pe,sv)
  return header
