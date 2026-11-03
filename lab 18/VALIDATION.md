# Validation evidence

Executed in the managed Windows workspace on 2026-11-03:

- `python -m unittest -v test_edgar.py`: **8 tests passed**. Includes Streamlit AppTest and the injected unsupported ROE.
- `python edgar.py COST`: attempted; blocked by outbound socket permissions, WinError 10013. No live financial output generated.
- SEC companyfacts retrieval through the web tool: unavailable for both company URLs.
- Bundled skill validator: unavailable because its optional `yaml` dependency is absent. Frontmatter and naming inspected directly instead.

Subsequent normal PowerShell downloads succeeded. The saved live reports were inspected, and `python verify_live.py` printed **All live COST and JPM classroom checks match.** COST and JPM memos were rewritten from the printed reports; both audit runs returned empty unsupported-number lists and bound their report hashes. All eight tests passed again after adding saved-report reload and memo refresh handling.

Synthetic fixture tests are labelled and isolated from runtime output. They demonstrate computation and missing-input behavior separately from the live verifier. The student's personal trust decision and fresh-chat comparison remain for the student to complete.

Streamlit was restarted successfully with `--server.address 127.0.0.1 --server.port 8519`; its startup log reported http://127.0.0.1:8519. Connection-refused troubleshooting and the requirement to keep the server process running are documented in README.md. The verified derived reports are now included in GitHub; raw SEC response caches and personal decision files are excluded.

The FAskills reference review added explicit evidence/unknowns/change-of-mind guidance to the skill and memos, and explained the cash-flow proxy and judgment framework in the app. Financial extraction and arithmetic were unchanged. Both memo number audits, the live verifier, and the eight existing tests were rerun successfully after these changes.
