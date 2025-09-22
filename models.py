from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ResearchRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000, description="Research question")
    user_id: str = Field(..., min_length=1, description="User identifier")
    include_live_data: bool = Field(default=True, description="Include live data sources")
    max_sources: int = Field(default=10, ge=1, le=50, description="Maximum number of sources to use")

class Citation(BaseModel):
    source: str = Field(..., min_length=1, description="Source name")
    title: str = Field(..., min_length=1, description="Citation title")
    url: Optional[str] = Field(None, description="Source URL")
    page_number: Optional[int] = Field(None, ge=1, description="Page number")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    excerpt: str = Field(..., min_length=1, description="Text excerpt")

class KeyTakeaway(BaseModel):
    insight: str = Field(..., min_length=1, description="Key insight")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    sources: List[str] = Field(..., min_items=1, description="Source references")
    category: str = Field(..., min_length=1, description="Category of insight")

class ResearchReport(BaseModel):
    id: str = Field(..., min_length=1, description="Report identifier")
    question: str = Field(..., min_length=1, description="Research question")
    summary: str = Field(..., min_length=1, description="Report summary")
    key_takeaways: List[KeyTakeaway] = Field(..., min_items=1, description="Key insights")
    citations: List[Citation] = Field(..., description="Source citations")
    sources_used: List[str] = Field(..., description="Sources used")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="Generation timestamp")
    user_id: str = Field(..., min_length=1, description="User identifier")
    credits_used: int = Field(..., ge=0, description="Credits consumed")
    freshness_score: float = Field(..., ge=0.0, le=1.0, description="Information freshness score")

class UsageStats(BaseModel):
    user_id: str
    total_questions: int
    total_reports: int
    credits_remaining: int
    credits_used: int
    last_activity: datetime

class DocumentInfo(BaseModel):
    filename: str
    file_type: str
    size: int
    processed_at: datetime
    chunks: int
    user_id: str

class DataSource(BaseModel):
    name: str
    type: str
    last_updated: datetime
    status: str
    description: str

class BillingEvent(BaseModel):
    user_id: str
    event_type: str  # "research", "upload", "premium"
    credits_used: int
    timestamp: datetime
    description: str

class LiveDataItem(BaseModel):
    id: str
    title: str
    link: str
    summary: str
    timestamp: datetime
    source: str
    category: str
