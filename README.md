# Digital to Wave Part II — Unified Verdict

One verdict, five ways, for the claims in Lee, "Digital to Wave:
LGD In Situ Wave Memory–Human Wave Integrated Interface–Metaverse
Hologram–Wave Affective AI" (Zenodo 21947108, DOI
10.5281/zenodo.21947108, 2026-08-15).

## The claim under test

Paper §1 (readout) + §3 (hologram mapping): a THz wave reads out /
reconstructs data stored at individual LGD lattice sites
(a₀ = 0.356 nm) on a "1:1 basis" (79.6 ZB in a 10 × 10 × 3 mm³
crystal), and an object's de Broglie matter wave couples to THz and
is stored as a hologram mapped 1:1 onto the same lattice. The claim
requires the SAME site to be both resolvable by the THz readout and
coherently addressable by the matter wave.

## The symmetry: Fourier duality

The Abbe diffraction limit and the de Broglie wavelength are the
same Fourier duality seen from opposite sides. A wave of wavelength
λ cannot resolve features smaller than ~λ/2 (position space); a
particle of momentum p has wavelength λ = h/p (momentum space).
A wave can only address features comparable to its own wavelength.
The THz wave (λ 100–1000 µm) is too LONG to resolve a 0.356 nm
site. The matter wave (λ ~10⁻⁴¹ m for a macroscopic mass) is too
SHORT to address one coherently — its phase across a single lattice
spacing is ~10³¹ rad, effectively random. The sweet spot, λ ~ a₀,
is occupied by neither. One wave principle, two failures, opposite
directions.

## The five pieces

1. **Diffraction bound (Abbe).** Best case 301 MB readable vs
   79.6 ZB claimed — short by **2.65 × 10¹⁴**. FAIL.
2. **de Broglie bound (matter wavelength).** Most generous case
   (1 kg, thermal, 3 THz) short by **1.68 × 10¹⁹**; 70 kg at
   370 km/s: λ = 2.56×10⁻⁴¹ m, λ_THz/λ = 1.17×10³⁷, phase
   8.74×10³¹ rad/site. FAIL.
3. **Fourier-duality joint bound.** No lattice site is both
   resolvable by THz and coherently addressable by the matter wave.
   Joint count: **0**. FAIL.
4. **Analog calibration robustness.** A bounded calibration
   (Observer + Calibrator, δ ∈ [−0.05, 0.05]) buys exactly
   **0.0223 orders** (log10(1/0.95), a mathematical identity);
   best-calibrated gap still **1.60 × 10¹⁹**. FAIL stands.
5. **Spooky stability.** Omega-Genesis spooky correlation
   **0.99999995** at σ = 0.01; verdict stable **5/5 FAIL**.
   The FAIL is robust to input noise. (Not comparable to the
   Omega-Genesis 0.9005 — same concept, different state and noise.)

## Verdict

**FAIL.** The claim fails on the diffraction bound, on the de
Broglie bound, on their joint form, and after the best bounded
calibration; and the failure is stable under input noise.

## Benefits

See `BENEFITS.md` for the full manifest: for each piece, the bound
and its number, the robustness it proves, the reusable template step
it provides, and the evidence value (what a reader can cite). The
reusable template — claim, Abbe, de Broglie, joint, bounded
calibration, noisy-copy spooky, verdict — tests any other
wave-memory claim the same way.

## Run it

```sh
python fourier_duality.py   # prints the joint table and the verdict
python unified_verdict.py   # prints the five pieces and the unified verdict
python -m pytest tests/ -v     # 5 tests, all must pass
```

This package is self-contained: it recomputes the diffraction, de
Broglie and joint bounds fresh here from the paper's own numbers
and standard constants. It does not import from the companion repos;
where a number comes from a repo (calibration, spooky), it is stated
as a cited constant with its source commit (see
`unified_verdict.py`).

## Layout

- `fourier_duality.py` — the joint bound (recomputed Abbe + de
  Broglie + joint count + illustrative product, caveated).
- `unified_verdict.py` — the aggregator: five pieces, unified
  verdict, benefits manifest.
- `tests/test_unified.py` — exactly 5 tests.
- `reports/unified.md` — one-page report with the symmetry, the
  joint bound, the five pieces, the unified verdict, the benefits,
  and the honest caveats.
- `BENEFITS.md` — the benefits manifest + the reusable template.
- `pyproject.toml` — package metadata (version 0.1.0, AGPL-3.0-only).
- `VERSION` — 0.1.0. `CHANGELOG.md` — release notes.
- `CITATION.cff`, `.zenodo.json`, `NOTICE` — citation and attribution
  metadata (DOI pending: no Zenodo record yet).
- `MODULES.sha256` — SHA-256 checksums of the modules, tests and
  report.
- `LICENSE` — GNU Affero General Public License v3 (AGPL-3.0-only).

## Credits

- **Mun Seok Lee** — author of the Part II paper under test
  ("Digital to Wave: LGD In Situ Wave Memory–Human Wave Integrated
  Interface–Metaverse Hologram–Wave Affective AI", Zenodo 21947108).
  The claims, equations and numbers tested here are his; the test,
  the computation and the verdict are not his and he has not reviewed
  or endorsed this software.
- **Jean-François Brisson (Spark AI NLP)** — author of this unified
  test, the deep analysis behind it, and the FAIL verdict.
- **Omega-Genesis (Untitled7, Colab notebooks)** — source of the
  "spooky" concept cited in piece 5: mean pairwise |dot| over 5
  noisy copies of a state (measured 0.9005 there). The concept is
  reused; the value is not comparable (different state, different
  noise).
- **Inspiration — Jack Sarfatti and Klee Irwin ("THE EMPIRE WAVE",
  OSF DOI 10.17605/OSF.IO/5AT2W), shared by Jered Mcclain** — their
  "digital wave" (emergent spacetime / digital physics) is an
  inspiration for the digital-wave exploration, not the theory under
  test. It shares words, not physics, with Lee's Digital-to-Wave
  (phase-based signal and computing). The falsification in this
  package targets Lee's Part II claims specifically; it makes no
  claim about Sarfatti and Irwin's work, and they have not reviewed
  or endorsed this software.
- **Companion work:** `sparkainlp-x/digital-to-wave-2-thz-validity`,
  which validity-checked the §2 human-wave-interface equations
  (dimensional error, impossible intensities, χ⁽²⁾ = 0 in bulk water);
  `sparkainlp-x/digital-to-wave-2-diffraction`, which falsified the
  THz readout by the Abbe diffraction limit (readable capacity short
  by ~10¹⁴–10¹⁷); and `sparkainlp-x/digital-to-wave-2-debroglie`,
  which falsified the matter-wave hologram (λ ~10³⁷ too short),
  added the analog calibration (0.0223 orders) and the spooky
  stability (0.99999995). This package unifies those three repos'
  results under one symmetry and one verdict.

## Status and limits

SYNTHETIC computation. A classical-physics bound applied to the
paper's own numbers. No physical claim, no experiment, no medical
claim. Fourier duality is the known wave principle, not a new
physical law; it is applied here to unify the two bounds. The
illustrative product of the two shortfalls (~4.45×10³³) is shown
only for scale — it is not a single physical quantity. The rigorous
statements are the joint count (0) and the logical AND.

## License

AGPL-3.0-only. Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP).
