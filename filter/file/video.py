from filter.file.matcher import FileMatcherModule

class Matcher(FileMatcherModule):
   REGEXPS = [
      ".*\.avi$",
      ".*\.mkv$",
      ".*\.mp4$",
      ".*\.mpeg$",
      ".*\.xvid$",
      ".*\.divx$",
      ".*\.avi\.part"
   ]
   
   def match(self, filename):
      fileNameMatch = self.matchByFilename(filename)
      if fileNameMatch != None:
         return fileNameMatch