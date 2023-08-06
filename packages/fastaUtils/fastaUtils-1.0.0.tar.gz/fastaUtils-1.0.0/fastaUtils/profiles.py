#!/usr/bin/env python

from collections import defaultdict

def parse_profile(infile):
  profile=[]
  with open(infile,'r') as freqfile:
    for line in freqfile:
      line=line.strip()
      if line[0]=="#":
        continue
      freq=parse_profile_line(line)
      profile.append(freq)
  return profile

def parse_profile_line(profileline):
  tok=profileline.split()
  freq=dict(d.split(':') for d in tok)
  return defaultdict(lambda:0, {key:float(val) for key,val in freq.items()})

class profile_data:
  def __init__(self,profile):
    self.uniq=[list(col.keys()) for col in profile]
    self.prob=[list(col.values()) for col in profile]
    self.index=[{key:idx for idx,key in enumerate(col.keys())} for col in profile]
    self.cumulative=[0]
    for i in range(len(self.uniq)):
      self.cumulative.append(self.cumulative[i]+len(self.uniq[i]))
