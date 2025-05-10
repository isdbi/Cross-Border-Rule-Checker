from pathlib import Path
import json
import uuid
import logging
from typing import List
from fastapi import HTTPException

from app.schemas.rules import (
    RuleCheckRequest,
    RuleCheckResponse,
    ComplianceResult,
    RiskSummary
)
from app.services.ai_agent import run_legal_agent
from app.utils.logging import audit_logger

logger = logging.getLogger(__name__)
RULES_FILE = Path(__file__).parent.parent.parent / "rules.json"

async def check_rules_ai(request: RuleCheckRequest) -> RuleCheckResponse:
    audit_id = str(uuid.uuid4())
    
    try:
        # Load and validate rules
        with open(RULES_FILE) as f:
            rules_data = json.load(f)
        
        if not isinstance(rules_data, dict):
            raise HTTPException(500, "Invalid rules format")

        country_rules = rules_data.get(request.country.upper(), [])
        if not country_rules:
            raise HTTPException(404, f"No rules for {request.country}")

        # Prepare structured input
        structured_rules = [
            {
                "rule_text": rule["rule"],
                "replacements": rule.get("replacements", []),
                "legal_source": rule.get("legal_source", "")
            }
            for rule in country_rules
        ]

        # Get AI analysis
        raw_results = await run_legal_agent(
            request.country.upper(),
            request.product_features,
            structured_rules
        )
        if not isinstance(raw_results, list):
            raise HTTPException(500, "Invalid AI response format")

        # Validate and parse results
        results = [ComplianceResult(**item) for item in raw_results]
        
        # Calculate risk
        risk_summary = RiskSummary(
            total_features=len(results),
            non_compliant=sum(1 for r in results if r.compliance == "Not Compliant"),
            needs_review=sum(1 for r in results if r.compliance == "Needs Review")
        )

        # Log success
        await audit_logger.log(
            audit_id=audit_id,
            risk_level="HIGH" if risk_summary.non_compliant > 0 else "MEDIUM",
            details="Analysis completed",
            features_count=risk_summary.total_features
        )

        return RuleCheckResponse(
            results=results,
            audit_id=audit_id,
            risk_summary=risk_summary
        )

    except HTTPException as he:
        await audit_logger.log(
            audit_id=audit_id,
            risk_level="ERROR",
            details=str(he),
            features_count=0
        )
        raise
    except Exception as e:
        await audit_logger.log(
            audit_id=audit_id,
            risk_level="CRITICAL",
            details=str(e),
            features_count=0
        )
        logger.exception("Critical error")
        raise HTTPException(500, "Processing failed")