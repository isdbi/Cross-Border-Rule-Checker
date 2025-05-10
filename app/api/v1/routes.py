from fastapi import APIRouter
from app.services.check import check_rules_ai
from app.schemas.rules import RuleCheckRequest, RuleCheckResponse

router = APIRouter(prefix="/v1/compliance", tags=["Compliance"])

@router.post(
    "/check",
    response_model=RuleCheckResponse,
    summary="Shariah Compliance Check",
    description="Analyzes financial product features against Islamic finance rules"
)
async def compliance_check(request: RuleCheckRequest):
    return await check_rules_ai(request)