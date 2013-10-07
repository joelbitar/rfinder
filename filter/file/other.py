from filter.file.matcher import FileMatcherModule

class Matcher(FileMatcherModule):
   REGEXPS = [
      ".*\.iso$"
   ]
   
   def match(self, filename):
      fileNameMatch = self.matchByFilename(filename)
      if fileNameMatch != None:
         return fileNameMatch