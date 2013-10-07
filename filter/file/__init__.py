from filter.file import rar, movie, other

modules = [rar, video, other]

def match(filename):
   
   print "Matching the file " + filename
   
   for module in modules:
      filenameMatch = module.Matcher().match(filename)
      if filenameMatch != None:
         print 'FOUND MATCH!!',
         print filenameMatch
         continue
         
   
   print "Match done \n"


def getFileName(fullpath):
   pass