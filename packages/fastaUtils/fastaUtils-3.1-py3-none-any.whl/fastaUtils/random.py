#!/usr/bin/env python

import random

def generate_random_seq(profiledata):
  return "".join([ random.choices(profiledata.uniq[col],weights=profiledata.prob[col])[0] for col in range(len(profiledata.uniq)) ])

def generate_random_seq_with_template(profiledata,template,n_subs):
  cols=random.sample(range(len(template)),k=n_subs)
  newchars=[ random.choices(profiledata.uniq[col],weights=profiledata.prob[col])[0] for col in cols ]
  template=list(template)
  for col,char in zip(cols,newchars):
    template[col]=char
  return "".join(template)

def shuffle(seqs,columns=None,regions=None):
  if columns is None and regions is None:
    random.shuffle(seqs)
    return seqs

  import numpy as np
  x=np.array([[s for s in seq] for seq in seqs],dtype=str)
  if regions is not None:
    for r in range(len(regions)-1):
      np.random.shuffle(x[:,regions[r]+1:regions[r+1]])
  elif columns is not None:
    for col in columns:
      np.random.shuffle(x[:,col])
  seqs=["".join(x[i,:]) for i in range(x.shape[0])]
  return seqs
