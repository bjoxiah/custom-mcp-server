from pydantic import BaseModel, Field
from typing import List


class TopicSentiment(BaseModel):
    topic: str = Field(..., alias="topic", description="Topic category of the article.")
    relevance_score: float = Field(..., alias="relevance_score", description="Relevance score for the topic.")


class TickerSentiment(BaseModel):
    ticker: str = Field(..., alias="ticker", description="Ticker symbol mentioned in the news.")
    relevance_score: float = Field(..., alias="relevance_score", description="Relevance score for the ticker.")
    ticker_sentiment_score: float = Field(..., alias="ticker_sentiment_score", description="Sentiment score for the ticker.")
    ticker_sentiment_label: str = Field(..., alias="ticker_sentiment_label", description="Sentiment label for the ticker.")


class NewsItem(BaseModel):
    title: str = Field(..., alias="title", description="Headline of the news article.")
    url: str = Field(..., alias="url", description="URL of the news article.")
    time_published: str = Field(..., alias="time_published", description="Timestamp the article was published.")
    authors: List[str] = Field(..., alias="authors", description="List of article authors.")
    summary: str = Field(..., alias="summary", description="Short text summary of the article.")
    banner_image: str = Field(..., alias="banner_image", description="URL of the banner image.")
    source: str = Field(..., alias="source", description="Source of the news article.")
    category_within_source: str = Field(..., alias="category_within_source", description="Category provided by the source.")
    source_domain: str = Field(..., alias="source_domain", description="Domain of the source website.")
    
    topics: List[TopicSentiment] = Field(..., alias="topics", description="Topic-level sentiment metadata.")
    
    overall_sentiment_score: float = Field(..., alias="overall_sentiment_score", description="Overall sentiment score of the article.")
    overall_sentiment_label: str = Field(..., alias="overall_sentiment_label", description="Overall sentiment label.")
    
    ticker_sentiment: List[TickerSentiment] = Field(..., alias="ticker_sentiment", description="Ticker-level sentiment metadata.")


class CompanySentiment(BaseModel):
    items: int = Field(..., alias="items", description="Number of items returned in the feed.")
    sentiment_score_definition: str = Field(..., alias="sentiment_score_definition", description="Explanation of sentiment score ranges.")
    relevance_score_definition: str = Field(..., alias="relevance_score_definition", description="Explanation of relevance score scale.")
    feed: List[NewsItem] = Field(..., alias="feed", description="List of news items returned.")
