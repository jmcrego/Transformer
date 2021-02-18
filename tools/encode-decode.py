# -*- coding: utf-8 -*-
import sys
import os
import glob
from Preprocessor import SentencePiece, Space
from Tools import create_logger, isbinary

if __name__ == '__main__':

  fmod = None
  fin = None
  do = 'encode'
  in_type = 'int'
  out_type = 'str'
  prog = sys.argv.pop(0)
  usage = '''usage: {} -do STRING -model FILE
   -do           STRING : encode OR decode ({})
   -model          FILE : input model/vocab
   -i              FILE : input file (stdin)
   -in_type      STRING : int OR str when sentencepiece/decode ({})
   -out_type     STRING : int OR str when sentencepiece/encode ({})
   -h                   : this help
'''.format(prog,do,in_type,out_type)

  while len(sys.argv):
    tok = sys.argv.pop(0)
    if tok=='-h':
      sys.stderr.write(usage)
      sys.exit()
    elif tok=='-i' and len(sys.argv)>=0:
      fin = sys.argv.pop(0)
    elif tok=='-do' and len(sys.argv)>=0:
      do = sys.argv.pop(0)
    elif tok=='-model' and len(sys.argv)>=0:
      fmod = sys.argv.pop(0)
    elif tok=='-in_type' and len(sys.argv)>=0:
      in_type = sys.argv.pop(0)
    elif tok=='-out_type' and len(sys.argv)>=0:
      out_type = sys.argv.pop(0)
    else:
      sys.stderr.write('error: unparsed {} option\n'.format(tok))
      sys.stderr.write(usage)
      sys.exit()

  if fmod is None or not os.path.exists(fmod):
    sys.stderr.write('error: missing or unreachable -model file\n')
    sys.exit()

  create_logger('stderr','info')
  preprocessor = 'sentencepiece' if isbinary(fmod) else 'space'

  if preprocessor == 'space':
    mod = Space(fmod=fmod)
  else:
    mod = SentencePiece(fmod=fmod)

  if do == 'encode':
    if preprocessor == 'space':
      in_type = 'str'
      out_type = 'int'
    else:
      in_type = 'str'

    _, lines = mod.encode(fin=fin, in_type='str', out_type=out_type)
    for l in lines:
      if out_type == 'str':
        print(' '.join(l))
      else:
        print(' '.join([str(x) for x in l]))

  elif do == 'decode':
    if preprocessor == 'space':
      in_type = 'int'
      out_type = 'str'
    else:
      out_type = 'str'

    _, lines = mod.decode(fin=fin, in_type=in_type, out_type=out_type)
    for l in lines:
      print(' '.join(l))
