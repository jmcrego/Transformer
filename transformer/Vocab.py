# -*- coding: utf-8 -*-

import sys
import os
import logging
from collections import defaultdict

def sentencepiece2vocab(ifile, ofile):
  vocab = defaultdict()
  vocab['<pad>'] = 0 #### this does not appear in sentencepiece
  vocab['<unk>'] = 1
  vocab['<bos>'] = 2
  vocab['<eos>'] = 3

  with open(ifile,'r') as f:
    for l in f:
      tok = l.rstrip()
      if tok.find('\t') >= 0:
        tok = tok.split('\t')[0]
      if tok == '<pad>' or tok == '<unk>' or tok == '<s>' or tok == '</s>' or tok == '<bos>' or tok == '<eos>' or tok == '<blank>':
        continue
      if tok in vocab:
        logging.warning('Repeated entry: {} [skipping]'.format(tok))
        continue
      if ' ' in tok or len(tok) == 0:
        logging.warning('Bad entry: {} [skipping]'.format(tok))
        continue
      vocab[tok] = len(vocab)

  with open(ofile,'w') as f:
    for wrd,key in sorted(vocab.items(), key=lambda item: item[1], reverse=False):
      f.write(wrd+'\n')

  logging.info('Read vocab from {} ~ Written into {} ({} entries)'.format(ifile, ofile, len(vocab)))


##############################################################################################################
### Vocab ####################################################################################################
##############################################################################################################
class Vocab():
  def __init__(self, file, token): 
    super(Vocab, self).__init__()

    if not os.path.exists(file):
      logging.error('Missing {} vocab file'.format(file))
      sys.exit()

    self.token = token
    self.idx_pad = 0 
    self.str_pad = '<pad>'
    self.idx_unk = 1 
    self.str_unk = '<unk>'
    self.idx_bos = 2
    self.str_bos = '<bos>'
    self.idx_eos = 3
    self.str_eos = '<eos>'
    self.tok_to_idx = defaultdict()
    self.idx_to_tok = []

    with open(file,'r') as f: 
      for l in f:
        tok = l.rstrip()
        if len(self.idx_to_tok) == 0 and tok != '<pad>':
          logging.error('idx=0 must be <pad>')
          sys.exit()
        elif len(self.idx_to_tok) == 1 and tok != '<unk>':
          logging.error('idx=1 must be <unk>')
          sys.exit()
        elif len(self.idx_to_tok) == 2 and tok != '<bos>':
          logging.error('idx=2 must be <bos>')
          sys.exit()
        elif len(self.idx_to_tok) == 3 and tok != '<eos>':
          logging.error('idx=3 must be <eos>')
          sys.exit()
        if tok in self.tok_to_idx:
          logging.error('Repeated entry {}'.format(tok))
          sys.exit()

        self.idx_to_tok.append(tok)
        self.tok_to_idx[tok] = len(self.tok_to_idx)
    logging.debug('Read Vocab ({} entries) from file {}'.format(len(self.idx_to_tok), file))


  def __len__(self):
    return len(self.idx_to_tok)

  def __iter__(self):
    for tok in self.idx_to_tok:
      yield tok

  def __contains__(self, s): ### implementation of the method used when invoking : entry in vocab
    if type(s) == int: ### testing an index
      return s>=0 and s<len(self)    
    return s in self.tok_to_idx ### testing a string

  def __getitem__(self, s): ### implementation of the method used when invoking : vocab[entry]
    if type(s) == int: ### input is an index, i want the string
      if s not in self:
        logging.error("Key \'{}\' not found in vocab".format(s))
        sys.exit()
      return self.idx_to_tok[s] ### s exists in self.idx_to_tok
    ### input is a string, i want the index
    if s not in self: 
      print(s,self.idx_unk)
      return self.idx_unk
    print(s,self.tok_to_idx[s])
    return self.tok_to_idx[s]

