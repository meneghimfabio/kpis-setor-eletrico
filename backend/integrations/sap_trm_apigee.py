"""
Cliente de Integração Apigee -> SAP TRM / FI.
Garante a regra de ouro: Somente Park / Planejado (Zero Post definitivo).
"""
import os
import uuid
from typing import Dict, Any
from decimal import Decimal

class SapTrmApigeeClient:
    def __init__(self):
        self.apigee_base_url = os.getenv("APIGEE_GATEWAY_URL", "https://api.corporate.energy/sap/v4")
        self.client_id = os.getenv("APIGEE_CLIENT_ID", "sati-ccee-agent-client-id")
        self.client_secret = os.getenv("APIGEE_CLIENT_SECRET", "mock-secret")
        self.agent_principal = "SATI_AGENT_CCEE_GUARANTEES"

    def _get_oauth_token(self) -> str:
        """Autenticação OAuth 2.0 no Apigee."""
        return "mock_secure_oauth_bearer_token"

    def create_parked_guarantee_document(
        self,
        company_code: str,
        ccee_agent_code: str,
        amount: Decimal,
        currency: str = "BRL",
        text_memo: str = ""
    ) -> Dict[str, Any]:
        """
        Gera um Parked Document (Documento Pré-editado no SAP FI/TRM).
        NÃO debita nem transfere fundos; apenas cria a provisão para conferência do tesoureiro.
        """
        token = self._get_oauth_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "X-Agent-Principal": self.agent_principal,
            "X-Audit-Context": "SATI_CCEE_PRE_MARKET_ALLOCATION",
            "Content-Type": "application/json"
        }

        # Simulação controlada de id único gerado pelo SAP Gateway
        mock_sap_doc = f"PARK-2026-{abs(hash(ccee_agent_code + str(amount))) % 1000000:06d}"
        
        payload = {
            "CompanyCode": company_code,
            "DocumentType": "ZG",  # Tipo de Documento de Garantia Financeira CCEE
            "DocumentDate": "2026-10-02",
            "PostingDate": "2026-10-02",
            "Status": "PARKED",    # Regra Imutável: Somente PARKED
            "Currency": currency,
            "HeaderMemo": f"SATI CCEE [{ccee_agent_code}] - {text_memo}",
            "Items": [
                {
                    "ItemNo": 1,
                    "Account": "21151000", # Conta Transitória de Garantias Regulatórias CCEE
                    "Amount": float(amount),
                    "DebitCreditCode": "S", # Débito
                    "CostCenter": "CC_TESOURARIA"
                },
                {
                    "ItemNo": 2,
                    "Account": "11120000", # Conta de Provisão / Bloqueio de Caixa
                    "Amount": float(amount),
                    "DebitCreditCode": "H", # Crédito
                    "AllocationReference": f"CCEE-{ccee_agent_code}"
                }
            ]
        }

        return {
            "sap_document_number": mock_sap_doc,
            "status": "PARKED_SUCCESS",
            "company_code": company_code,
            "ccee_agent_code": ccee_agent_code,
            "amount": float(amount),
            "currency": currency,
            "maker_checker_status": "PENDING_APPROVAL",
            "message": "Documento pré-editado (Parked) criado com sucesso no SAP TRM/FI. Aguardando liberação do Tesoureiro no Fiori."
        }
