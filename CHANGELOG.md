# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] - 2026-11-13

### Results (SYNTHETIC; no physical, biological or safety claim)

- **Unified verdict: FAIL.** The paper's §1/§3 claim — a THz wave
  reads out data at individual LGD lattice sites 1:1, and an
  object's de Broglie matter wave couples to THz and is stored as
  a hologram mapped 1:1 onto the same lattice — fails five ways:
  diffraction (best case 301 MB readable vs 79.6 ZB claimed,
  short by 2.65 × 10¹⁴), de Broglie (most generous case short by
  1.68 × 10¹⁹; 70 kg at 370 km/s: λ = 2.56 × 10⁻⁴¹ m,
  λ_THz/λ = 1.17 × 10³⁷, phase 8.74 × 10³¹ rad/site), Fourier-
  duality joint bound (joint count 0 sites), analog calibration
  (best buys exactly 0.0223 orders; best-calibrated gap still
  1.60 × 10¹⁹), spooky stability (0.99999995 at σ = 0.01, verdict
  stable 5/5 FAIL).
- **The symmetry:** Fourier duality unifies the two falsifications.
  The THz wave is too LONG to resolve a site (Abbe) and the matter
  wave is too SHORT to address one coherently (de Broglie). One
  wave principle, two failures, opposite directions. The joint
  count — sites satisfying both — is 0 for every macroscopic mass
  and THz frequency.
- **Illustrative product:** 2.65 × 10¹⁴ × 1.68 × 10¹⁹ ≈ 4.45 × 10³³.
  Caveated as illustrative only (the two ratios are different
  kinds); the rigorous statements are the joint count (0) and the
  logical AND.

### Added

- `fourier_duality.py`: recomputed Abbe + de Broglie bounds,
  coherent-sites measure λ/(2πa₀), addressable-site count, joint
  count, joint verdict, illustrative product (caveated).
- `unified_verdict.py`: aggregator (five pieces, unified verdict),
  `benefits_manifest()` and the reusable template (claim, Abbe,
  de Broglie, joint, bounded calibration, noisy-copy spooky,
  verdict).
- `tests/test_unified.py`: exactly 5 tests, 5/5 pass.
- `reports/unified.md`: one-page report with the symmetry, the
  joint bound, the five pieces, the unified verdict, the benefits,
  and the honest caveats.
- `BENEFITS.md`: the benefits manifest + the reusable template.
- `pyproject.toml`, `VERSION`, `CHANGELOG.md`, `CITATION.cff`,
  `.zenodo.json`, `NOTICE`, `MODULES.sha256`, `.gitignore`.
