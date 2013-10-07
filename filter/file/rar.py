import re

from filter.file.matcher import FileMatcherModule

class Matcher(FileMatcherModule):
   REGEXPS = [
      [".*part([\d]{1,2})\.rar$", ["1"]],   # Special rule, only allow
      ".*\.rar$",
      ".*\.r[0]{1,2}[0,1]$"
   ]
   
   def match(self, filename):
      fileNameMatch = None
      
      for regexp in self.REGEXPS:
         conditions = []
         
         # If the type is a dict
         if type(regexp).__name__ == 'list':
            conditions  = regexp[1]
            regexp      = regexp[0]
         
         # Compile the Regexp
         regexp = re.compile(regexp, re.IGNORECASE)
         
         match = re.match(regexp, filename)
         if match:
            if len(match.groups()) > 0:
               if self.matchRegexpWithConditions(match, conditions):
                  return match.group(0)
               else:
                  # The conditions did NOT match
                  return None
            else:
               fileNameMatch = match.group(0)
      
      if fileNameMatch != None:
         return fileNameMatch