import json


class AuditLogger:
    async def log(
        self,
        audit_id: str,
        risk_level: str,
        details: str,
        features_count: int = 0
    ):
        """Unified logging method"""
        entry = {
            "audit_id": audit_id,
            "risk_level": risk_level.upper(),
            "details": details,
            "features": features_count
        }
        print(f"[AUDIT] {json.dumps(entry)}")

audit_logger = AuditLogger()