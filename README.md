# Mehrdad Poorhassan (Dr. Metal)
### AI Systems Architecture & LLM Security Engineering
*Research · Architecture · Implementation · Reproducible Validation*

---

## Research and engineering pillars

| Pillar | Repository | Current implementation and evidence |
|---|---|---|
| **LLM Security Engineering** | [llm-security-and-streaming-benchmarks](https://github.com/sharr666/llm-security-and-streaming-benchmarks) | Omega-Stack v2.2 heuristic RAG quarantine prototype; runtime-injected HMAC verification; pattern-based L1-L4 detectors; 20 hand-authored smoke fixtures. The reported fixture score is not a generalization or production-security claim. Streaming examples are separate; the Parquet sample materializes each shard in memory. |
| **Declarative Prompt Systems** | [declarative-prompt-compilation-and-agentic-systems](https://github.com/sharr666/declarative-prompt-compilation-and-agentic-systems) | Typed AST validation, JSON-quoted canonical prompt IR, full SHA-256 fingerprint, exact-record split overlap checks, and bounded in-process memory stores. Five profile labels currently share one prompt grammar; semantic leakage and general contradiction reasoning are not solved. |


## Identifiers and profiles

The following identifiers and external profile names are listed by the account owner. Their issuer-side validity and current status have not been independently audited in this repository review.

- ORCID: `0009-0004-9269-3912`
- Zenodo records listed in project documentation: `10.5281/zenodo.23758690` and `10.5281/zenodo.23762055`
- Professional profiles: [LinkedIn](https://www.linkedin.com/in/dr-metal) · [Credly](https://credly.com/users/mehrdad-poorhassan)

## Credentials and learning records

The credential ledger reports **269 recorded entries** across four evidence categories:
- 21 professional certificates and specializations
- 113 individual course/credential records
- 104 modular course completions
- 31 platform skill badges

These are ledger counts, not an independently verified count of unique credentials. The accompanying 122-entry index includes cross-tier/master-certificate overlap; it must not be interpreted as 122 unique Tier-2 credentials. See [CREDENTIALS_PORTFOLIO.md](./CREDENTIALS_PORTFOLIO.md) for the itemized records and verification identifiers.

## Reproducibility and limitations

Each engineering repository includes a GitHub Actions workflow. Passing CI means the configured syntax, unit and smoke tests passed at that commit; it does not constitute independent scientific validation, security certification, or production readiness.

Research reports and benchmark datasets should be cited only within their stated scope. See the individual repository README and SECURITY policy for assumptions, limitations and licensing.
