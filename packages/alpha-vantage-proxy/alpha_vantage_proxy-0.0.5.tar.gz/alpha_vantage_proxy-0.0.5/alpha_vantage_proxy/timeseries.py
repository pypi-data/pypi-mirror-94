
import requests
from alpha_vantage_proxy.models import *

class TimeSeries:

    def setFunction(self, function):
        self.function = function
        return self

    def intraday(self):
        return self.setFunction(TimeSeriesFunction.INTRADAY)

    def intradayExtended(self):
        return self.setFunction(TimeSeriesFunction.INTRADAY_EXTENDED)

    def daily(self):
        return self.setFunction(TimeSeriesFunction.DAILY)

    def dailyAdjusted(self):
        return self.setFunction(TimeSeriesFunction.DAILY_ADJUSTED)

    def weekly(self):
        return self.setFunction(TimeSeriesFunction.WEEKLY)

    def weeklyAdjusted(self):
        return self.setFunction(TimeSeriesFunction.WEEKLY_ADJUSTED)

    def monthly(self):
        return self.setFunction(TimeSeriesFunction.MONTHLY)

    def monthlyAdjusted(self):
        return self.setFunction(TimeSeriesFunction.MONTHLY_ADJUSTED)

    def setSymbol(self, symbol):
        self.symbol = symbol
        return self

    def setOutputSize(self, outputsize):
        self.outputsize = outputsize
        return self

    def compact(self):
        return self.setOutputSize(TimeSeriesOutputSize.COMPACT)

    def full(self):
        return self.setOutputSize(TimeSeriesOutputSize.FULL)

    def setDataType(self, datatype):
        self.datatype = datatype
        return self

    def json(self):
        return self.setDataType(TimeSeriesDataType.JSON)

    def csv(self):
        return self.setDataType(TimeSeriesDataType.CSV)

    def setKey(self, apikey):
        self.apikey = apikey
        return self

    def setInterval(self, interval):
        self.interval = interval
        return self

    def oneMin(self):
        return self.setInterval(IntradayInterval.ONE_MINUTE)

    def fiveMin(self):
        return self.setInterval(IntradayInterval.FIVE_MINUTE)

    def fifteenMin(self):
        return self.setInterval(IntradayInterval.FIFTEEN_MINUTE)

    def thirtyMin(self):
        return self.setInterval(IntradayInterval.THIRTY_MINUTE)

    def sixityMin(self):
        return self.setInterval(IntradayInterval.SIXITY_MINUTE)

    def setAdjusted(self, flag):
        self.adjusted = flag
        return self

    def adjusted(self):
        return self.setAdjusted(True)

    def unadjusted(self):
        return self.setAdjusted(False)

    def get(self):

        url = self.build()
        response = requests.get(url)   
        data = self.clean(response)

        return data

    def build(self):

        url = "https://www.alphavantage.co/query?"

        for key in self.__dict__:
            value = self.__dict__[key] if type(self.__dict__[key]) == str else self.__dict__[key].value
            url += key + "=" + value + "&"

        url = url[:-1]

        return url


    def clean(self, response):

        data = response.content.decode("utf-8").split("\n")
        del data[0]
        del data[-1]
        data.reverse()

        records = []
        for row in data:

            row = row.split(",")
            recordObj = Record()

            recordObj.date = row[0].split(" ")[0]
            recordObj.time = row[0].split(" ")[1]
            recordObj.open = float(row[1])
            recordObj.high = float(row[2])
            recordObj.low = float(row[3])
            recordObj.close = float(row[4])
            recordObj.volume = int(row[5])

            records.append(recordObj)

        return records
        

    def __str__(self):
        return str(self.__dict__)
