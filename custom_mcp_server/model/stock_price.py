from pydantic import BaseModel, Field
from datetime import date


class GlobalQuote(BaseModel):
    symbol: str = Field(..., alias="01. symbol", description="Ticker symbol.")
    open: float = Field(..., alias="02. open", description="Opening price for the trading day.")
    high: float = Field(..., alias="03. high", description="Highest price for the trading day.")
    low: float = Field(..., alias="04. low", description="Lowest price for the trading day.")
    price: float = Field(..., alias="05. price", description="Current trading price.")
    volume: int = Field(..., alias="06. volume", description="Trading volume.")
    latest_trading_day: date = Field(..., alias="07. latest trading day", description="Latest trading day date.")
    previous_close: float = Field(..., alias="08. previous close", description="Previous closing price.")
    change: float = Field(..., alias="09. change", description="Price change from previous close.")
    change_percent: str = Field(..., alias="10. change percent", description="Percent price change.")


class StockPrice(BaseModel):
    global_quote: GlobalQuote = Field(..., alias="Global Quote", description="Global quote market data.")
