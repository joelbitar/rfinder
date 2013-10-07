from filter.media.matcher import MediaMatcherModule

class Matcher(MediaMatcherModule):
   REGEXPS = [
      ".*\.avi$"
   ]
   
   def match(self, filename):
      fileNameMatch = self.matchByFilename(filename)
      if fileNameMatch != None:
         return fileNameMatch