# Validation evidence

Executed in the managed Windows workspace on 2026-11-03:

- `python -m unittest -v test_edgar.py`: **8 tests passed**. Includes Streamlit AppTest and the injected unsupported ROE.
- `python edgar.py COST`: attempted; blocked by outbound socket permissions, WinError 10013. No live financial output generated.
- SEC companyfacts retrieval through the web tool: unavailable for both company URLs.
- Bundled skill validator: unavailable because its optional `yaml` dependency is absent. Frontmatter and naming inspected directly instead.

Synthetic fixture tests are labelled and isolated from runtime output. They demonstrate computation and missing-input behavior, not agreement with current EDGAR filings. `verify_live.py` is the separate live acceptance check. Final company memos and the student's personal decision remain pending live evidence and student review.
