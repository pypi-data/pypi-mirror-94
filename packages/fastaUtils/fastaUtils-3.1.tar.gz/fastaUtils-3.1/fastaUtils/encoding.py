#!/usr/bin/env python
import numpy as np
import sys

def encodeInt(seq,profiledata):
  return [ profiledata.index[col][char] for col,char in enumerate(seq) ]

def encodeCategorical(data,profiledata):
#  index=[ profiledata.index[col][d]+profiledata.cumulative[col] for col,d in enumerate(data) ]
  index=[  ]
  for col,d in enumerate(data):
    try:
      index.append( profiledata.index[col][d]+profiledata.cumulative[col] ) 
    except:
      print("I do not know how to encode symbol {} in column {}. This position will remain empty.".format(d,col),file=sys.stderr)
  ret=np.zeros((profiledata.cumulative[-1],),dtype=bool)
  for idx in index:
    ret[idx]=True
  return ret
