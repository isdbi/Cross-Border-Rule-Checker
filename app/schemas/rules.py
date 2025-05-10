from pydantic import BaseModel
from typing import List, Literal

class ComplianceResult(BaseModel):
    feature: str
    compliance: Literal["Compliant", "Not Compliant", "Needs Review"]
    justification: str

class RiskSummary(BaseModel):
    total_features: int
    non_compliant: int
    needs_review: int

class CrossBorderAnalysis(BaseModel):
    compatibility_score: int
    critical_issues: List[str]
    recommended_changes: List[str]

class RuleCheckRequest(BaseModel):
    country: str
    product_features: List[str]

class RuleCheckResponse(BaseModel):
    results: List[ComplianceResult]
    risk_summary: RiskSummary
    audit_id: str

class CrossBorderRequest(BaseModel):
    source_country: str
    target_country: str
    product_design: dict

class CrossBorderResponse(BaseModel):
    analysis: CrossBorderAnalysis
    audit_id: str