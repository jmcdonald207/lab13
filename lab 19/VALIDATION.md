# Validation and limits

Validated on November 5, 2026 in the managed Windows workspace.

- The existing Lab 18 Streamlit process started at port 8519. COST was also loaded through Streamlit AppTest as part of building the extension.
- The Lab 19 app loads COST and JPM without exceptions, displays three memo editors, and flags an unsupported number injected into every investor's editor.
- Six automated tests cover the known COST answer recomputed from included SEC source observations; the 5% probe; missing growth, R&D, cash-flow pairs, revenue tags, and zero equity; exact inclusive boundaries; both saved reports matching source recomputation; six clean memo audits; and numeric injection into each app memo.
- `prepare_sources.py` confirmed the committed source subsets reproduce reports identical to the complete Lab 18 caches. These remain saved snapshots, not a new live download. Manifest SHA-256 hashes identify the inputs.
- `review_memos.py` found no unprinted numbers in any of the six memos. Memos were reviewed for meaning and units and bound to report hashes. Audit limitations are described in README.
- COST liabilities/equity, growth, all seven checks, and missing R&D match the supplied answer. Expected values exist only in the test; runtime reports are calculated from SEC observations.
- The skill threshold was temporarily changed to 5 and COST recomputed: growth passed and R&D remained not known. It was restored to 15. A separate CLI probe report preserves that result without overwriting the baseline.
- Lab 19 Streamlit started successfully at http://127.0.0.1:8520. The bundled skill validator could not run because its optional `yaml` module is absent; skill frontmatter, lowercase names, reference paths, and instruction consistency were inspected directly instead.

Exact failed NVIDIA retrieval command, run from the repository root:

```powershell
python -c "import sys,json;sys.path.insert(0,'lab 19');import edgar;from pathlib import Path;f=edgar.fetch('https://data.sec.gov/api/xbrl/companyfacts/CIK0001045810.json',edgar.DEFAULT_AGENT);Path('lab 19/output/NVDA_companyfacts.json').write_text(json.dumps(f),encoding='utf-8');print('Downloaded NVDA SEC facts')"
```

Exact terminal exception:

```text
urllib.error.URLError: <urlopen error [WinError 10013] An attempt was made to access a socket in a way forbidden by its access permissions>
```

The browser retrieval route was also unavailable. No NVIDIA financial result was created. Final selection is FNCL/JPM with a verified issuer holdings source and existing SEC cache, not an assertion that NVDA does not file a 10-K. Future refreshes require functioning outbound SEC access. Partner exercises and the Brightspace quiz were not performed.
