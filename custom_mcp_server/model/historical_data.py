from typing import Dict
from pydantic import BaseModel, Field, RootModel

class MetaData(BaseModel):
    information: str = Field(..., alias="1. Information", description="Description of the data series")
    symbol: str = Field(..., alias="2. Symbol", description="Stock ticker symbol")
    last_refreshed: str = Field(..., alias="3. Last Refreshed", description="Date of the most recent data point")
    time_zone: str = Field(..., alias="4. Time Zone", description="Time zone of the data")

class MonthlyDataPoint(BaseModel):
    open: float = Field(..., alias="1. open", description="Opening price of the stock for the month")
    high: float = Field(..., alias="2. high", description="Highest price of the stock for the month")
    low: float = Field(..., alias="3. low", description="Lowest price of the stock for the month")
    close: float = Field(..., alias="4. close", description="Closing price of the stock for the month")
    volume: int = Field(..., alias="5. volume", description="Trading volume for the month")

# Pydantic v2 RootModel for dynamic dictionary
class MonthlyTimeSeries(RootModel[Dict[str, MonthlyDataPoint]]):
    """
    Mapping of date (YYYY-MM-DD) to MonthlyDataPoint.
    """

class HistoricalData(BaseModel):
    meta_data: MetaData = Field(..., alias="Meta Data", description="Metadata about the time series")
    monthly_time_series: MonthlyTimeSeries = Field(..., alias="Monthly Time Series", description="Monthly stock prices and volumes")
