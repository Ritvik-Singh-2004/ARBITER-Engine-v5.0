# Arbiter Engine: AI & Blockchain Risk Assessment System

A major academic project developed for Dr. A.P.J. Abdul Kalam Technical University (AKTU). Arbiter is a highly secure, decentralized API microservice designed to assess the authenticity of physical assets via JSON metadata payloads, bypassing the need for optical scanning. 

## System Architecture

Arbiter employs a dual-stage evaluation pipeline to ensure end-user safety and rigorous background analysis:
1. **Fast-Eval (Sub-millisecond):** Instantly runs heuristic guard clauses on incoming JSON payloads. Returns a `quick_flag` to the client, triggering immediate UI waiting animations for potentially tampered assets.
2. **Deep-Eval (LangChain ReAct + Llama-3-8B):** Offloaded to a background thread, a LangChain ReAct agent orchestrates specific tools to evaluate the asset:
   - Extracts dense entity embeddings using **Llama-3-8B**.
   - Fuses semantic drift scores with keyword databases using **Reciprocal Rank Fusion (RRF)**.
   - Calculates a dynamic risk multiplier (capped at 100).
   - Commits critical risk events to a **Blockchain Ledger** and updates user trust scores in **MongoDB**.
   - Adjusts future baseline weights via **Adaptive Learning** feedback loops.

## Deployment
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000