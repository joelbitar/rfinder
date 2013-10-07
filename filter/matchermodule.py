import re

class MatcherModule(object):
   def getRegexps(self):
      for regexp in self.REGEXPS:
         yield re.compile(regexp, re.IGNORECASE)
         
   def matchRegexpWithConditions(self, match, conditions):
      for i in range(len(match.groups())):
         if match.group(i + 1) != conditions[i]:
            return False
      
      return True
   