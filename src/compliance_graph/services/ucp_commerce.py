class UCPCommerceService:
    def __init__(self):
        pass

    def create_checkout_session(self, plan: str, customer_id: str) -> dict:
        return {
            "session_id": f"ucp_ses_{hash(plan + customer_id) % 100000}",
            "plan": plan,
            "customer_id": customer_id,
            "amount": 99.99 if plan == "enterprise" else 29.99,
            "currency": "USD",
            "status": "created"
        }

    def list_plans(self) -> list[dict]:
        return [
            {"id": "community", "name": "Community", "price": 0, "features": ["basic_scan", "5_devices"]},
            {"id": "professional", "name": "Professional", "price": 29.99, "features": ["full_scan", "50_devices", "api_access"]},
            {"id": "enterprise", "name": "Enterprise", "price": 99.99, "features": ["quantum_scan", "unlimited_devices", "api_access", "pqc_audit", "zk_proofs"]},
        ]
