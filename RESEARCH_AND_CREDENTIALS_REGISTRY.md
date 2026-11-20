# Research & Credentials Evidence Registry

**Maintainer:** Mehrdad Poorhassan (Dr. Metal)  
**ORCID claimed in repository:** [0009-0004-9269-3912](https://orcid.org/0009-0004-9269-3912)  
**Registry version:** 1.0.0  
**Inventory date:** 2026-11-20  
**Repository scope:** Public claims and identifiers currently listed in this profile repository.  
**Purpose:** A conservative index of claims, their canonical destinations, and the evidence still required before describing them as independently verified.

---

## 1. Verification policy

This registry distinguishes three separate questions:

1. **Listed here:** The identifier or claim appears in this GitHub repository.
2. **Destination reachable / record exists:** The canonical external destination resolves and exposes a record.
3. **Identity and claim verified:** The external record's metadata, creator/holder identity, title, version, date, and relationship to the cited GitHub project have been checked against primary-source evidence.

A GitHub link, badge, filename, or self-authored statement proves only that the claim is listed here. It does not, by itself, prove ownership, issuer validity, authorship, publication status, uniqueness, or cross-platform identity alignment.

### Status vocabulary

| Status | Meaning |
|---|---|
| `Listed — not independently verified` | Present in the current GitHub README or portfolio; external primary-source validation is pending. |
| `Partially verified` | Some attributes were checked, but one or more material attributes remain unverified. |
| `Verified` | Canonical primary source was inspected and the relevant identity and claim attributes matched. |
| `Conflict / needs reconciliation` | Sources contain inconsistent titles, counts, identifiers, dates, or scope. |
| `Not applicable` | The item is a local GitHub artifact rather than an external credential or research record. |

No item in this first inventory is promoted to **Verified** solely on the basis of GitHub content.

---

## 2. Research identity and profile identifiers

| Record | Identifier / canonical destination | What the repository claims | Current status | Required verification |
|---|---|---|---|---|
| Researcher identity | ORCID [0009-0004-9269-3912](https://orcid.org/0009-0004-9269-3912) | Researcher identifier for Mehrdad Poorhassan | Listed — not independently verified | Inspect the public ORCID record; match name, public works, and relevant identifiers. |
| OSF researcher profile | [OSF profile](https://osf.io/user/23uab) | Researcher profile associated with the author | Listed — not independently verified | Confirm profile ownership and public profile metadata. |
| OSF project | [OSF project y8j9g](https://osf.io/y8j9g/) | Project associated with the OSF DOI below | Listed — not independently verified | Inspect project metadata, contributors, registration/version state, and linked outputs. |
| OSF DOI | [10.17605/OSF.IO/Y8J9G](https://doi.org/10.17605/OSF.IO/Y8J9G) | DOI associated with the OSF project and a Philoprompts monograph in the README | Conflict / needs reconciliation | Confirm DOI landing-page metadata, title, creators, resource type, and whether the cited monograph is actually the deposited object. |

---

## 3. Zenodo research and software records

The following DOI destinations are transcribed from the current profile README. Their presence in this table is not a statement that the records' authorship, metadata, files, publication state, or project relationship have been independently validated.

| DOI | Canonical destination | GitHub-described relationship | Current status | Required verification |
|---|---|---|---|---|
| `10.5281/zenodo.24153117` | [Zenodo record](https://doi.org/10.5281/zenodo.24153117) | Archival DOI for this profile repository (`sharr666/sharr666`); also used by the README badge | Listed — not independently verified | Confirm record exists; inspect title, creators, version, files, license, and GitHub repository relation. |
| `10.5281/zenodo.23758690` | [Zenodo record](https://doi.org/10.5281/zenodo.23758690) | Listed for `llm-security-and-streaming-benchmarks` and for the report “Isolated Multi-Document Query Logic and Defense-in-Depth Architecture Against Distributed Indirect Prompt Injection in Agentic Workflows” | Conflict / needs reconciliation | Confirm whether this is one software record, one report, or a versioned record serving both roles; compare title, creators, files, and related identifiers. |
| `10.5281/zenodo.23762055` | [Zenodo record](https://doi.org/10.5281/zenodo.23762055) | Listed for `declarative-prompt-compilation-and-agentic-systems` and a systematic-survey technical report | Listed — publication state unconfirmed in README | Inspect record state, metadata, creators, files, and whether the cited title matches the archived object. |
| `10.5281/zenodo.24238946` | [Zenodo record](https://doi.org/10.5281/zenodo.24238946) | Listed for “How Ancient Scripts Break Modern Tokenizers: An Empirical Study on 563 Philoprompts” and the Hugging Face dataset | Listed — not independently verified | Confirm record metadata and files; compare title, creator, version, date, and dataset relationship with the Hugging Face repository. |

### DOI presentation rule

Use the canonical resolver form `https://doi.org/<DOI>` for DOI links. A DOI string without a hyperlink is not a broken identifier, but it is less usable for readers. A resolving DOI does not by itself prove that the record supports the surrounding claim.

---

## 4. Hugging Face dataset

| Dataset | Canonical destination | GitHub-described scope | Current status | Required verification |
|---|---|---|---|---|
| `Dr-Metal/philoprompts-v1` | [Hugging Face dataset](https://huggingface.co/datasets/Dr-Metal/philoprompts-v1) | Public dataset; README reports 563 rows in the `train` split, IDs `#0001–#0563`, and intentional gaps `#0146–#0148` | Conflict / needs reconciliation | Inspect dataset card, repository files, commit/revision, split configuration, row count, license, authorship metadata, and the documented gap decision. |

**Known reconciliation note from the GitHub README:** Older GitHub materials are reported to refer to a 234-entry corpus, while the README reports 563 public Hugging Face training rows. These values must not be presented as interchangeable. The 563-row figure is a dataset row count as stated in the README, not proof of 563 unique, independently validated prompts.

---

## 5. Selected credentials displayed in the profile README

These seven items are the selected examples displayed publicly in the README, not a complete audit of all entries in `CREDENTIALS_PORTFOLIO.md`.

| Credential | Issuer / platform stated in README | Credential identifier | Verification destination | Current status |
|---|---|---|---|---|
| Google Cybersecurity Professional Certificate | Google / Coursera | `9TMSJEXK7U9E` | [Coursera verification](https://www.coursera.org/verify/professional-cert/9TMSJEXK7U9E) | Listed — issuer verification pending |
| Google Data Analytics Professional Certificate | Google / Coursera | `RK5246370ZYI` | [Coursera verification](https://www.coursera.org/verify/professional-cert/RK5246370ZYI) | Listed — issuer verification pending |
| Google Prompting Essentials Specialization | Google / Coursera | `C2P8DXIFHHU4` | [Coursera verification](https://www.coursera.org/verify/specialization/C2P8DXIFHHU4) | Listed — issuer verification pending |
| Certified Ethical Hacking (v12) Specialization | LearnKartS / Coursera | `G75QPHDFMTSW` | [Coursera verification](https://www.coursera.org/verify/specialization/G75QPHDFMTSW) | Listed — issuer verification pending |
| Security and Ethical Hacking Specialization | University of Colorado Boulder / Coursera | `ENKTWY0WDCHI` | [Coursera verification](https://www.coursera.org/verify/specialization/ENKTWY0WDCHI) | Listed — issuer verification pending |
| Generative AI for Software Engineers & Developers Specialization | Edureka / Coursera | `EZMEIOPO5DT7` | [Coursera verification](https://www.coursera.org/verify/specialization/EZMEIOPO5DT7) | Listed — issuer verification pending |
| Career Essentials in Generative AI | Microsoft & LinkedIn | `9e9e0493783872d51508aec1fc079086464e6bb2a687f0d84dd374ce58e05627` | [LinkedIn Learning certificate](https://www.linkedin.com/learning/certificates/9e9e0493783872d51508aec1fc079086464e6bb2a687f0d84dd374ce58e05627) | Listed — issuer verification pending |

A credential identifier appearing in the portfolio is not equivalent to a successful issuer-side verification. Verification should capture the issuer's displayed title, holder name (where public), issue date, credential type, and current validity/status where provided.

---

## 6. Credential portfolio counting rules

The current `CREDENTIALS_PORTFOLIO.md` reports **269 recorded entries**, calculated as:

- 21 professional certificates / specializations;
- 113 individual course credential-ID entries;
- 104 modular course completions;
- 31 platform skill badges.

The same file explicitly states that the category total is **not deduplicated** and is not an issuer-verified count of unique credentials. Its itemized index contains **122 indexed records**, with rows 103–117 summarizing master certificates already represented in Tier 1.

Therefore:

- Use **“269 recorded entries across categories (not deduplicated)”** when describing the current portfolio ledger.
- Do not use **“269 unique certificates”**, **“269 verified credentials”**, or equivalent wording.
- Use **“122 indexed records”**, not “122 unique credentials”.
- Do not add the 122 index rows to the 269 category total.
- A future unique-credential count requires record-level deduplication using issuer + credential ID + credential type, with parent specializations and component courses kept distinct.

**Source of these counts:** [`CREDENTIALS_PORTFOLIO.md`](./CREDENTIALS_PORTFOLIO.md), read from the repository's `main` branch on 2026-11-20.

---

## 7. Professional profile links

The following profile links are listed in the current README. Their presence and URL syntax were confirmed in the repository content; ownership and account-to-person matching have not been independently established in this registry.

| Platform | Listed handle / URL | Current status |
|---|---|---|
| LinkedIn | [linkedin.com/in/dr-metal](https://www.linkedin.com/in/dr-metal/) | Listed — ownership not independently verified |
| X | [@Dr_Metal](https://x.com/Dr_Metal) | Listed — ownership not independently verified |
| Academia.edu | [DrMetal1](https://independent.academia.edu/DrMetal1) | Listed — ownership not independently verified |
| Kaggle | [drmetal](https://www.kaggle.com/drmetal) | Listed — ownership not independently verified |
| Hugging Face | [Dr-Metal](https://huggingface.co/Dr-Metal) | Listed — ownership not independently verified |

---

## 8. Reconciliation queue

The following items should be resolved before stronger public claims are made:

1. **Zenodo 23758690:** Determine whether the DOI is being used as a software archive, a technical report, or both; align the README's title and resource-type descriptions with the canonical record.
2. **Zenodo 23762055:** Confirm publication state and exact title/creator metadata before removing the current qualification.
3. **OSF DOI / project:** Confirm whether the DOI resolves to the same project and monograph described in the README.
4. **Zenodo 24238946 ↔ Hugging Face dataset:** Verify the paper-to-dataset relationship, exact dataset revision, authorship, and license scope.
5. **ORCID ↔ Zenodo ↔ OSF ↔ GitHub ↔ Hugging Face:** Verify identity and work-level links independently on each platform. Do not claim “100% alignment” until each identifier and relationship has direct evidence.
6. **Credential portfolio:** Validate the selected credentials first, then the full index; record issuer response and deduplication outcome without conflating courses, badges, and parent certificates.
7. **Profile links:** Confirm account ownership and canonical URLs for each professional network.

---

## 9. Verification log

| Date | Scope | Result |
|---|---|---|
| 2026-11-20 | GitHub `main`: `README.md` and `CREDENTIALS_PORTFOLIO.md` | Repository content and the claims transcribed into this registry were inspected through the GitHub integration. |
| 2026-11-20 | External primary-source records | Not completed in this registry-creation pass. All external records remain explicitly unverified or qualified pending direct inspection. |

**Next review:** Recheck every external record and update the status only with primary-source evidence. Record the checked URL, check date, matched fields, and any unresolved discrepancy.

---

## 10. Scope and limitations

This registry is an evidence index, not a certification authority, identity proof, or guarantee of external service availability. It does not claim that every credential, profile, DOI, or dataset was checked. No private account data was accessed. No code, tests, or external repository payloads were executed as part of creating this document.
