from show import ShowAnalyzer
from movie import MovieAnalyzer
from music import MusicAnalyzer

class SortAdapter(object):
    def __init__(self, obj):
        self.obj = obj

class AnalyzerSorter(SortAdapter):
    def __lt__(self, other):
        return self.obj.confidence < other.obj.confidence


def analyze(file):
   analyzers = [
      MusicAnalyzer(file),
      ShowAnalyzer(file),
      MovieAnalyzer(file)
   ]

   analyzer_that_won = max(analyzers, key = AnalyzerSorter)
   return analyzer_that_won


   