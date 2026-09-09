import logging
from typing import Dict, Any
from langchain.agents import initialize_agent, AgentType
from langchain_community.llms import Ollama # Configured for Llama-3-8b
from langchain.tools import Tool

logger = logging.getLogger(__name__)

class ArbiterOrchestrator:
    def __init__(self):
        self.is_ready = True
        # Initialize Llama-3-8B via local Ollama instance (or substitute with API)
        self.llm = Ollama(model="llama3:8b")

    def fast_eval(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Guard clauses and instantaneous heuristic checks."""
        if not payload.get("entity_id") or not payload.get("cryptographic_signature"):
            raise ValueError("Invalid payload: Missing ID or Signature.")
            
        is_suspicious = len(payload["cryptographic_signature"]) < 10 or payload.get("metadata", {}).get("tamper_flag") == True
        return {"is_suspicious": is_suspicious}

    def deep_eval_react_loop(self, payload: Dict[str, Any], fast_results: Dict[str, Any]):
        """LangChain ReAct loop. Agent decides which tools to invoke based on context."""
        logger.info(f"Initiating ReAct loop for {payload['entity_id']}")
        
        # Lazy Loading Tools as LangChain custom tools
        from app.tools.nlp_processor import analyze_text_metadata
        from app.tools.fusion_engine import apply_rrf_scoring
        from app.tools.risk_engine import calculate_dynamic_risk
        from app.tools.db_gateway import persist_risk_record
        
        tools = [
            Tool(
                name="VectorEmbeddings",
                func=analyze_text_metadata,
                description="Generates dense embeddings for asset metadata."
            ),
            Tool(
                name="RiskMultiplier",
                func=lambda x: calculate_dynamic_risk(50.0, 0.6, not fast_results["is_suspicious"], payload.get("metadata")),
                description="Calculates dynamic risk multiplier based on RRF scores."
            ),
            Tool(
                name="DatabaseUpdate",
                func=lambda x: persist_risk_record(payload["entity_id"], {"data": x}),
                description="Persists final risk calculations to MongoDB and triggers adaptive learning."
            )
        ]

        # Initialize the ReAct Agent
        agent = initialize_agent(
            tools, 
            self.llm, 
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
            verbose=True,
            handle_parsing_errors=True
        )

        prompt = f"""
        Analyze this asset: {payload['entity_id']} with metadata {payload['metadata']}.
        1. Use VectorEmbeddings to check semantic drift.
        2. Use RiskMultiplier to calculate the final score capped at 100.
        3. Use DatabaseUpdate to save the result.
        """
        
        try:
            agent.run(prompt)
            logger.info("ReAct loop completed successfully.")
        except Exception as e:
            logger.error(f"ReAct agent failure: {e}")