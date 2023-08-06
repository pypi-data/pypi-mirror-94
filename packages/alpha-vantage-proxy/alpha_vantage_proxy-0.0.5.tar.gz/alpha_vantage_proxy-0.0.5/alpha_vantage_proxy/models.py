
import enum

class Record:

    def __init__(self):

        self.open = None
        self.close = None
        self.high = None
        self.low = None
        self.volume = None
        self.date = None
        self.time = None

    def __str__(self):
        return str(self.__dict__)

class TimeSeriesFunction(enum.Enum):
   
    INTRADAY = "TIME_SERIES_INTRADAY"
    INTRADAY_EXTENDED = "TIME_SERIES_INTRADAY_EXTENDED"
    DAILY = "TIME_SERIES_DAILY"
    DAILY_ADJUSTED = "TIME_SERIES_DAILY_ADJUSTED"
    WEEKLY = "TIME_SERIES_WEEKLY"
    WEEKLY_ADJUSTED = "TIME_SERIES_WEEKLY_ADJUSTED"
    MONTHLY = "TIME_SERIES_MONTHLY"
    MONTHLY_ADJUSTED = "TIME_SERIES_MONTHLY_ADJUSTED"

class TimeSeriesOutputSize(enum.Enum):

    COMPACT = "compact"
    FULL = "full"

class TimeSeriesDataType(enum.Enum):

    JSON = "json"
    CSV = "csv"

class IntradayInterval(enum.Enum):

    ONE_MINUTE = "1min"
    FIVE_MINUTE = "5min"
    FIFTEEN_MINUTE = "15min"
    THIRTY_MINUTE = "30min"
    SIXTY_MINUTE = "60min"