from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class Ticker:
   def __init__(self,
               ticker: str,
               weight: int = 2):
      self.ticker = ticker
      self.count = 0
      self.bodies = []
      self.pos_count = 0
      self.neg_count = 0
      self.bullish = 0
      self.bearish = 0
      self.neutral = 0
      self.sentiment = 0
      self.weight = weight

   def analyze_sentiment(self):
      analyzer = SentimentIntensityAnalyzer()
      neutral_count = 0
      for text in self.bodies:
         sentiment = analyzer.polarity_scores(text)
         if (sentiment["compound"] > .005) or (sentiment["pos"] > abs(sentiment["neg"])):
            self.pos_count += 1
         elif (sentiment["compound"] < -.005) or (abs(sentiment["neg"]) > sentiment["pos"]):
            self.neg_count += 1
         else:
            neutral_count += 1

      self.bullish = int(self.pos_count / len(self.bodies) * 100)
      self.bearish = int(self.neg_count / len(self.bodies) * 100)
      self.neutral = int(neutral_count / len(self.bodies) * 100)
   
   @property
   def score(self):
      return (self.bullish - (self.bearish + self.neutral / self.weight)) / 100

   def __str__(self) -> str:
      return(f"{self.ticker} | {self.bullish} | {self.bearish} | {self.neutral} | {self.score}")
