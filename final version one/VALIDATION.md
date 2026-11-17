# Validation and AI use

- **Baseline.** Codex ran the packaged Python model with the committed Lab 15 engine and classroom assumptions in a fresh temporary folder on November 17, 2026. The run produced 6.51% expected return, 9.44% volatility, and 20.00% reserve eligibility.
- **Mandate check.** The engine filters a fully invested long-only grid in five-percentage-point steps by a 6.50% expected-return objective and a 3.00% eligible-reserve minimum. The baseline and stress clear both thresholds under the training eligibility flags. Full mandate review is unresolved.
- **Stress run.** Codex replayed the already documented Lab 15 change from 8.00% to 7.00% equity expected return and reproduced 6.53% expected return, 12.94% volatility, and 10.00% eligible reserves. [Before and after](output/results.md)
- **Locked record.** The new student-authored prediction and pre-run commit are pending. [Locked Changed-Input Record](docs/locked-changed-input.md)
- **AI use.** Codex inspected GitHub, packaged the existing engine, wrote the CLI and documentation, and replayed the documented stress. The Streamlit app was carried forward from Lab 15 and its runtime remains unverified for this package.
