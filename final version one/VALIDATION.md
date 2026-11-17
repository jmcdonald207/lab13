# Validation and AI use

Codex downloaded all four Yahoo Finance adjusted-close series and ran the full and recent windows plus the VT override on November 17, 2026. The acquisition code requires 61 valid calendar-month observations per fund. The optimizer evaluates a fully invested long-only five-percentage-point grid against the 6.50% annual return hurdle and 3% SGOV reserve minimum. All four reported runs pass those modeled checks.

Changing the estimation window moved VT from 45% to 15%. Holding full-window covariance fixed and lowering VT's expected return to 9.55% raised its weight to 50% and portfolio volatility from 6.74% to 7.48%. [Run output](output/results.md)

Codex implemented and ran the CLI. Browser runtime and human cold run are pending. The AI-assisted stress replay is separate from the student's pending AI-off prediction and pre-run commit. [Locked record](docs/locked-changed-input.md)
