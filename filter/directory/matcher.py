import re

from filter import matchermodule

class MediaMatcherModule(mathermodule.MatcherModule):
   def matchDir(self, dir):
      for regexp in self.getRegexps():
         match = re.match(regexp, filename)
         if(match):
            return match.group(0)