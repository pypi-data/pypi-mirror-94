
import enum

class Node:

    def put(self, data):
        
        self.add(data)

        if self.isFull():
            self.calculate()

        self.store(data)

    def get(self):
        return self.value

class PredictionType(enum.Enum):
   
   BUY = "Buy"
   SELL = "Sell"
   HOLD = "Hold"
   NULL = None
