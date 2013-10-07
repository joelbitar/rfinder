from filter.media.matcher import MediaMatcherModule

class Matcher(MediaMatcherModule):
   REGEXPS = [
      ".*/(.*)\.s(\d{2})e(\d{2})\..*",    # One episode
      ".*/(.*)\.s([\d]{2})\..*"           # A series
   ]
   
   def getShowData(self, match):
      
      episode = None
      
      if len(match.groups()) > 2:
         episode  = match.group(3)
      
      return {
              show      : match.group(1),
              season    : match.group(2),
              episode   : episode
      }
   
   def match(self, dirname):
      fileNameMatch = self.matchByFilename(dirname)
      
      for regexp in self.getRegexps():
         match = re.match(regexp, dirname)
         
         if match:
            return self.getShowData(match)
         
      
      return None