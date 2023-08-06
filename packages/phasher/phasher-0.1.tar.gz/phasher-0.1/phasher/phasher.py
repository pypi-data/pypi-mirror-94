#Compare file hashes of different formats quickly
import hashlib
import sys, getopt
 
def main(argv):
   filein = ""
   hash = ""
   compareh=""
   try:
      opts, args = getopt.getopt(argv,"hi:t:c:",["filepath=","hashtype=,compare="])
   except getopt.GetoptError:
      print ('phasher.py -i <filein> -t <hash type (MD5, SHA1, SHA256, SHA512)> -c <compared hash>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('phasher.py -i <filein> -t <hash type> -c <compared hash>')
         sys.exit()
      elif opt in ("-i", "--filepath"):
         filein = arg
      elif opt in ("-t", "--hashtype"):
         hash = arg
      elif opt in ("-c", "--compare"):
         compareh = arg
   print 'Input file is ', filein
   print 'Hash type is ', hash

   if hash.lower() == 'md5':
	   hasher = hashlib.md5()
   elif hash.lower() == 'sha1':
	   hasher = hashlib.sha1()
   elif hash.lower() == 'sha256':
	   hasher = hashlib.sha256()
   elif hash.lower() == 'sha512':
	   hasher = hashlib.sha512()
   else:	#spit out md5 if error
	   hasher = hashlib.md5()
   with open(filein, 'rb') as afile:
       buf = afile.read()
       hasher.update(buf)
   hout=hasher.hexdigest()   
   print(hout)
   
   if compareh==hout:
      print("HASH IS A MATCH")
   else:
      print("HASH IS NOT A MATCH")

if __name__ == "__main__":
   main(sys.argv[1:])
   
