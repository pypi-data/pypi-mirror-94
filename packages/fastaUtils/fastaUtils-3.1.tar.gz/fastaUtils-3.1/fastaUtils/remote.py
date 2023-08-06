from datetime import date
import os
import gzip
import shutil
import requests
import time

def download_file(url,local_filename):
  if local_filename is None:
    local_filename = url.split('/')[-1]
  # NOTE the stream=True parameter below
  with requests.get(url, stream=True) as r:
    r.raise_for_status()
    with open(local_filename, 'wb') as f:
      for chunk in r.iter_content(chunk_size=1024*64): 
        if chunk: # filter out keep-alive new chunks
          f.write(chunk)
          f.flush()
  return local_filename

def uniprot(folder=None):
  if folder is None:
    try:
      folder=os.environ['UNIPROTFOLDER']
    except:
      raise RuntimeError("The environment variable UNIPROTFOLDER must be defined")
  if not os.path.isdir(folder):
    os.mkdir(folder)
  
  current_release=os.path.join(folder,"current_release")
  today = date.today()
  folder=os.path.join(folder,today.strftime("%Y%m%d"))
  if not os.path.isdir(folder):
    os.mkdir(folder)
  
  url_uniprot_sprot="https://ftp.expasy.org/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.fasta.gz"
  download_file(url_uniprot_sprot,os.path.join(folder,"uniprot_sprot.fasta.gz"))
  with gzip.open(os.path.join(folder,"uniprot_sprot.fasta.gz"), 'rb') as f_in:
    with open(os.path.join(folder,"uniprot_sprot.fasta"), 'wb') as f_out:
      shutil.copyfileobj(f_in, f_out)
  
  url_uniprot_trembl="https://ftp.expasy.org/databases/uniprot/current_release/knowledgebase/complete/uniprot_trembl.fasta.gz"
  download_file(url_uniprot_trembl,os.path.join(folder,"uniprot_trembl.fasta.gz"))
  with gzip.open(os.path.join(folder,"uniprot_trembl.fasta.gz"), 'rb') as f_in:
    with open(os.path.join(folder,"uniprot_trembl.fasta"), 'wb') as f_out:
      shutil.copyfileobj(f_in, f_out)
  os.remove(os.path.join(folder,"uniprot_trembl.fasta.gz"))
  os.remove(os.path.join(folder,"uniprot_sprot.fasta.gz"))
  os.remove(current_release)
  os.symlink(folder, current_release)

def uniprot_metadata(query_ids,outfile,chunk_size=200):
  def chunks(l, n):
    for i in range(0, len(l), n):
      yield l[i:i + n]  
  headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)     Chrome/37.0.2049.0 Safari/537.36'}

  if os.path.isfile(outfile):
    os.remove(outfile)
    
  output=""
  n=0
  for ids in chunks(query_ids,chunk_size):
    n+=1
    m=0
    query= 'id:'+'+OR+'.join(ids)+''+"&format=tab&columns=id,entry name,reviewed,protein names,genes,length,lineage(all),created"
    query_str="https://www.uniprot.org/uniprot/?query={}".format(query)
    print("batch {}".format(n),end="\r")
    response=""
    resp=False
    while not resp:
      try:
        response = requests.get(query_str)
        if response.ok:
          resp=True
        else:
          raise ValueError("not ok")
      except:
        m+=1
        print("batch {}: retry {}".format(n,m),end="\r")
        time.sleep(5)
        pass
    output=response.text 
    with open(outfile,'a') as out:
      out.write(output)
  
def metaclust(folder=None):
  if folder is None:
    try:
      folder=os.environ['METACLUSTFOLDER']
    except:
      raise RuntimeError("The environment variable METACLUSTFOLDER must be defined")
  if not os.path.isdir(folder):
    os.mkdir(folder)
  
  current_release=os.path.join(folder,"current_release")
  today = date.today()
  folder=os.path.join(folder,today.strftime("%Y%m%d"))
  if not os.path.isdir(folder):
    os.mkdir(folder)


  url_metaclust="https://metaclust.mmseqs.org/current_release/metaclust_nr.fasta.gz"
  download_file(url_metaclust,os.path.join(folder,"metaclust-nr.fasta.gz"))
  with gzip.open(os.path.join(folder,"metaclust-nr.fasta.gz"), 'rb') as f_in:
    with open(os.path.join(folder,"metaclust-nr.fasta"), 'wb') as f_out:
      shutil.copyfileobj(f_in, f_out)
  os.remove(os.path.join(folder,"metaclust-nr.fasta.gz"))
  os.symlink(folder, current_release)
