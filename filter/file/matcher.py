import re

from filter import matchermodule

class FileMatcherModule(matchermodule.MatcherModule):
   def matchByFilename(self, filename):
      for regexp in self.getRegexps():
         match = re.match(regexp, filename)
         if(match):
            return match.group(0)
            
         