
from rolling_technical_indicators.calc import *
from rolling_technical_indicators.model import Node

class BollingerBands(Node):

    def __init__(self, config):

        period = config.bollingbandPeriod
        
        self.smoothedTypical = SimpleMovingAverage(period)
        self.stdev = StandardDeviation(period)
        self.value = None

    def isFull(self):
        return self.smoothedTypical.isFull() and self.stdev.isFull()

    def calculate(self):
        smoothedValue = self.smoothedTypical.get()
        stdevValue = self.stdev.get()

        upperBandValue = smoothedValue + 2*stdevValue
        lowerBandValue = smoothedValue - 2*stdevValue

        self.value = (lowerBandValue, upperBandValue)

    def add(self, record):

        typical = (record.close + record.high + record.low) / 3
        self.smoothedTypical.put(typical)
        self.stdev.put(typical)

class ADX(Node):

    def __init__(self, period):

         period = config.adxPeriod

        self.smoothedAbs = SmoothedMovingAverage(period)
        self.plusDM = SmoothedMovingAverage(period)
        self.minusDM = SmoothedMovingAverage(period)
        self.avgTrueRange = AverageTrueRange(period)
        self.yesterdayHigh = None
        self.yesterdayLow = None

    def add(self, record):

        if self.yesterdayHigh != None and self.yesterdayLow != None:

            upMove = record.high - self.yesterdayHigh
            downMove = self.yesterdayLow - record.low

            self.plusDM.put( upMove if upMove > downMove and upMove > 0 else 0 )
            self.minusDM.put( upMove if downMove > upMove and downMove > 0 else 0 )

        self.yesterdayHigh = record.high
        self.yesterdayLow = record.low
        self.avgTrueRange.put(record)


    def calculate(self):

        plusDI = 100 * self.plusDM.get() / self.avgTrueRange.get()
        minusDI = 100 * self.minusDM.get() / self.avgTrueRange.get()

        self.smoothedAbs.put( abs( (plusDI - minusDI) / (plusDI + minusDI) ) )

    def get(self):
        return self.smoothedValue.get()
