# unified_verdict.py
#
# Unified verdict + benefits architecture for the tests of Lee,
# "Digital to Wave: LGD In Situ Wave Memory-Human Wave Integrated
# Interface-Metaverse Hologram-Wave Affective AI"
# (Zenodo 21947108, DOI 10.5281/zenodo.21947108, 2026-08-15).
#
# This module brings together ALL five pieces of the falsification
# into one verdict and one benefits manifest:
#   1. Diffraction bound (Abbe, position space) -- the THz readout
#      cannot resolve a 0.356 nm site; best case 301 MB readable vs
#      79.6 ZB claimed (short by 2.65 x 10^14).
#   2. de Broglie bound (matter wavelength, momentum space) -- a
#      macroscopic object's matter wave is ~10^37 times too short
#      to couple to THz; most generous case short by 1.68 x 10^19.
#   3. Fourier-duality joint bound -- the symmetry unifying 1 and
#      2: no lattice site is both resolvable by THz and coherently
#      addressable by the matter wave. Joint count: 0.
#   4. Analog calibration robustness -- a bounded calibration
#      (Observer + Calibrator, delta in [-0.05, 0.05]) buys exactly
#      0.0223 orders; the best-calibrated gap is still 1.60 x 10^19.
#   5. Spooky stability -- the Omega-Genesis spooky correlation
#      over noisy copies of the log-gap state is 0.99999995 at
#      sigma = 0.01, and the verdict is stable 5/5 FAIL.
#
# This module is SELF-CONTAINED and runnable: it recomputes the
# diffraction bound, the de Broglie bound and the joint bound fresh
# here (importing only fourier_duality.py, in this package) from the
# paper's own numbers and standard constants. It does NOT import
# from the two companion repos. Where a number comes from a repo
# rather than a fresh computation here, it is stated as a cited
# constant with its source repo and commit:
#   - Calibration (piece 4): the improvement 0.0223 orders is the
#     analytic identity log10(1/0.95), computed here; it matches the
#     measured value in sparkainlp-x/digital-to-wave-2-debroglie
#     v0.2.0 (commit 190d726da24a855baa06284d50ff5adc9611625b). The
#     best-calibrated gap is the worst-case de Broglie ratio x 0.95.
#   - Spooky (piece 5): spooky = 0.99999995 at sigma = 0.01 and
#     verdict stability 5/5 FAIL are cited constants from
#     sparkainlp-x/digital-to-wave-2-debroglie v0.3.0 (commit
#     8dac0a0ce64d16cdec86568ae5e070b7448ff017). They are Monte Carlo
#     measurements, not closed forms, so they are cited rather than
#     recomputed here.
# The diffraction and de Broglie numbers are recomputed here and
# checked against the companion repos' verified values in the
# tests (within 1%).
#
# Status: SYNTHETIC computation. A classical-physics bound applied
# to the paper's own numbers. No physical claim, no experiment, no
# medical claim. Fourier duality is the known wave principle, not a
# new physical law.
#
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

"""Unified verdict and benefits architecture.

Aggregates the five pieces -- diffraction, de Broglie, Fourier-
duality joint bound, analog calibration robustness, spooky
stability -- into one verdict (FAIL) and a benefits manifest: for
each piece, the bound and its number, the robustness it proves,
the reusable template it provides for testing other wave-memory
claims, and the evidence value it carries.
"""

import math

import fourier_duality as fd

# ---------------------------------------------------------------------------
# Cited constants (from the companion repo, with source)
# ---------------------------------------------------------------------------

# Spooky stability, measured in
# sparkainlp-x/digital-to-wave-2-debroglie v0.3.0
# (commit 8dac0a0ce64d16cdec86568ae5e070b7448ff017):
# mean pairwise |dot| over 5 noisy copies of the log-gap state
# vector (10 standard cases at 1 THz, each (mass, velocity)
# perturbed by relative Gaussian noise, sigma = 0.01, seed 42).
# Verdict stable 5/5 FAIL at sigma = 0.01 (worst ratios
# 4.92e19-5.13e19) and at sigma = 0.05 (4.45e19-5.47e19).
# Cited here rather than recomputed: it is a Monte Carlo
# measurement, not a closed form. NOT comparable to the
# Omega-Genesis 0.9005 (same concept, different state and noise).
SPOOKY_SIGMA = 0.01
SPOOKY_CORRELATION_CITED = 0.99999995
SPOOKY_MIN_PAIRWISE_CITED = 0.99999992
SPOOKY_VERDICT_STABLE_CITED = "5/5"
SPOOKY_SOURCE = (
    "sparkainlp-x/digital-to-wave-2-debroglie v0.3.0, commit "
    "8dac0a0ce64d16cdec86568ae5e070b7448ff017"
)

# Analog calibration, measured in
# sparkainlp-x/digital-to-wave-2-debroglie v0.2.0
# (commit 190d726da24a855baa06284d50ff5adc9611625b):
# Observer (Yang, read-only) + Calibrator (Yin, one clipped scalar
# delta in [-0.05, 0.05], fractional velocity adjustment). The best
# delta is always -0.05. The improvement is the analytic identity
# log10(1/0.95), computed here; it matches the repo's measured
# 0.0223 exactly.
CALIBRATION_DELTA_MIN = -0.05
CALIBRATION_DELTA_MAX = 0.05
CALIBRATION_BEST_DELTA_CITED = -0.05
CALIBRATION_SOURCE = (
    "sparkainlp-x/digital-to-wave-2-debroglie v0.2.0, commit "
    "190d726da24a855baa06284d50ff5adc9611625b"
)

# Pass/fail threshold, same as the companion modules.
FAIL_RATIO_THRESHOLD = fd.FAIL_RATIO_THRESHOLD


# ---------------------------------------------------------------------------
# The five pieces
# ---------------------------------------------------------------------------

def piece_diffraction():
    """Piece 1: the Abbe diffraction bound (position space).

    Recomputed here. Returns a dict with the bound, its number and
    its verdict.
    """
    worst = fd.worst_case_diffraction_ratio()
    return {
        "name": "Diffraction bound (Abbe, position space)",
        "bound": (
            "A THz wave cannot resolve a 0.356 nm lattice site: "
            "Abbe limit d = lam / (2 NA)."
        ),
        "number": worst,
        "number_text": f"short by {worst:.2e} (best case)",
        "best_case": (
            f"{fd.best_case_readable_mb():.0f} MB readable vs "
            f"79.6 ZB claimed (3 THz, NA = 1, 1000 bits/voxel)"
        ),
        "verdict": fd.diffraction_verdict(),
    }


def piece_debroglie():
    """Piece 2: the de Broglie matter-wave bound (momentum space).

    Recomputed here. Returns a dict with the bound, its number and
    its verdict.
    """
    worst = fd.worst_case_debroglie_ratio()
    return {
        "name": "de Broglie bound (matter wavelength, momentum space)",
        "bound": (
            "A macroscopic object's matter wave is far too short "
            "to couple to THz or address a lattice site: "
            "lam = h / sqrt(2 m E + E^2 / c^2)."
        ),
        "number": worst,
        "number_text": f"short by {worst:.2e} (most generous case)",
        "best_case": (
            "1 kg, thermal, 3 THz: lambda_THz/lambda = "
            f"{worst:.2e}; 70 kg at 370 km/s: lambda = 2.56e-41 m, "
            "lambda_THz/lambda = 1.17e37, phase 8.74e31 rad/site"
        ),
        "verdict": fd.debroglie_verdict(),
    }


def piece_joint():
    """Piece 3: the Fourier-duality joint bound (the new symmetry).

    Recomputed here (fourier_duality.py). Returns a dict with the
    bound, its number and its verdict.
    """
    return {
        "name": "Fourier-duality joint bound (the symmetry)",
        "bound": (
            "One wave principle, two failures: the THz wave is too "
            "LONG to resolve a site and the matter wave is too "
            "SHORT to address one coherently. A site must satisfy "
            "BOTH at once."
        ),
        "number": 0,
        "number_text": "joint count: 0 sites",
        "best_case": (
            "For every macroscopic mass and THz frequency, no "
            "lattice site is both resolvable by THz and coherently "
            "addressable by the matter wave."
        ),
        "verdict": fd.joint_verdict(),
    }


def calibration_improvement_orders():
    """The calibration improvement, as the analytic identity.

    The best delta is -0.05, so the ratio scales by (1 + delta) =
    0.95 and the improvement in orders is log10(1/0.95) =
    0.022276... This is a mathematical identity, not a fitted
    number: it holds for every mass, velocity and frequency,
    because the calibrator is a pure multiplicative velocity
    scaling and the gap ratio is linear in velocity. It matches
    the companion repo's measured 0.0223 exactly.
    """
    return math.log10(1.0 / (1.0 + CALIBRATION_BEST_DELTA_CITED))


def piece_calibration():
    """Piece 4: analog calibration robustness.

    The improvement is computed here as the analytic identity
    log10(1/0.95); the best-calibrated gap is the worst-case de
    Broglie ratio scaled by 0.95. The design (Observer + Calibrator)
    and the measured best delta (-0.05) are cited from the
    companion repo v0.2.0.
    """
    worst = fd.worst_case_debroglie_ratio()
    improvement = calibration_improvement_orders()
    best_calibrated = worst * (1.0 + CALIBRATION_BEST_DELTA_CITED)
    return {
        "name": "Analog calibration robustness",
        "bound": (
            "A bounded calibration (Observer + Calibrator, delta in "
            "[-0.05, 0.05], fractional velocity adjustment) cannot "
            "close the gap."
        ),
        "number": best_calibrated,
        "number_text": (
            f"best-calibrated gap {best_calibrated:.2e} "
            f"(improvement {improvement:.4f} orders)"
        ),
        "best_case": (
            f"Best delta {CALIBRATION_BEST_DELTA_CITED:.2f}; "
            f"improvement exactly {improvement:.4f} orders in "
            f"every case; most generous case after calibration "
            f"still {best_calibrated:.2e}"
        ),
        "verdict": (
            "FAIL"
            if best_calibrated >= FAIL_RATIO_THRESHOLD
            else "PASS"
        ),
    }


def piece_spooky():
    """Piece 5: spooky stability (robustness to input noise).

    Cited constants from the companion repo v0.3.0 (Monte Carlo
    measurements, not closed forms). The spooky value is NOT
    comparable to the Omega-Genesis 0.9005 (same concept,
    different state and noise).
    """
    return {
        "name": "Spooky stability (robustness to input noise)",
        "bound": (
            "The FAIL is stable under random input noise, measured "
            "the Omega-Genesis way: mean pairwise |dot| over 5 "
            "noisy copies of the log-gap state vector."
        ),
        "number": SPOOKY_CORRELATION_CITED,
        "number_text": (
            f"spooky = {SPOOKY_CORRELATION_CITED:.8f} "
            f"at sigma = {SPOOKY_SIGMA}"
        ),
        "best_case": (
            f"Verdict stable {SPOOKY_VERDICT_STABLE_CITED} FAIL "
            f"at sigma = 0.01 and sigma = 0.05; max relative "
            f"spread 4.88% at sigma = 0.01"
        ),
        "verdict": "FAIL (stable)",
    }


def all_pieces():
    """The five pieces, in order."""
    return [
        piece_diffraction(),
        piece_debroglie(),
        piece_joint(),
        piece_calibration(),
        piece_spooky(),
    ]


def unified_verdict():
    """The unified verdict: FAIL if ANY of the five pieces fails.

    Pieces 1-4 are independent bounds on the claim (diffraction,
    de Broglie, joint, calibrated); each FAILs on its own. Piece 5
    (spooky) confirms the FAIL is stable under noise rather than
    adding an independent bound. The unified verdict is FAIL.
    """
    for piece in all_pieces():
        if piece["verdict"].startswith("FAIL"):
            return "FAIL"
    return "PASS"


# ---------------------------------------------------------------------------
# Benefits architecture
# ---------------------------------------------------------------------------

REUSABLE_TEMPLATE = [
    "1. State the claim and its numbers, from the paper itself "
    "(lattice pitch, crystal size, claimed capacity, velocities, "
    "frequency band). No invented inputs.",
    "2. Abbe bound: compute the diffraction-limited resolution "
    "d = lam / (2 NA), the voxel count, and the readable capacity. "
    "The claim fails here if capacity is >= 10 orders below the "
    "claim even in the most generous case.",
    "3. de Broglie bound: compute the relativistic matter "
    "wavelength lam = h / sqrt(2 m E + E^2 / c^2) and the phase "
    "per lattice spacing 2 pi a0 / lam. The claim fails here if "
    "lam is >= 10 orders below the readout wavelength for every "
    "macroscopic mass.",
    "4. Joint bound (Fourier duality): count the sites satisfying "
    "BOTH at once. The joint count is at most the smaller of the "
    "two individual counts; if either is zero, the joint is zero. "
    "The claim fails here if the joint count is zero.",
    "5. Bounded calibration: add an Observer (read-only) and a "
    "Calibrator (one clipped scalar, e.g. delta in [-0.05, 0.05]). "
    "Measure the best achievable gap. The verdict stands if the "
    "best-calibrated gap is still >= 10 orders short.",
    "6. Noisy-copy spooky: perturb the inputs (relative Gaussian "
    "noise), measure the spooky correlation (mean pairwise |dot| "
    "over 5 noisy copies of the log-gap state) and the verdict "
    "stability. The verdict stands if it is stable 5/5.",
    "7. Verdict: FAIL if any bound fails; report the robustness "
    "of the verdict (calibration + spooky) alongside it. Publish "
    "the negative result with the numbers, not just the verdict.",
]


def benefits_manifest():
    """The benefits manifest: what each piece contributes.

    Returns a dict with the five pieces, each carrying (a) the
    bound and its number, (b) the robustness it proves, (c) the
    reusable template step it provides, and (d) the evidence value
    (what a reader can cite), plus an overall summary and the full
    reusable template.
    """
    pieces = all_pieces()
    entries = [
        {
            "piece": pieces[0]["name"],
            "bound_and_number": (
                f"{pieces[0]['bound']} {pieces[0]['number_text']}. "
                f"{pieces[0]['best_case']}."
            ),
            "robustness": (
                "Proves the readout cannot work as described, "
                "parameter-independently: no choice of field "
                "strength, gain or coupling beats the diffraction "
                "limit."
            ),
            "template_step": REUSABLE_TEMPLATE[1],
            "evidence_value": (
                "Cite: the diffraction-limited readable capacity "
                "(301 MB best case vs 79.6 ZB claimed) and the "
                "2.65e14 shortfall."
            ),
        },
        {
            "piece": pieces[1]["name"],
            "bound_and_number": (
                f"{pieces[1]['bound']} {pieces[1]['number_text']}. "
                f"{pieces[1]['best_case']}."
            ),
            "robustness": (
                "Proves the storage carrier cannot work as "
                "described, parameter-independently: no choice of "
                "field strength, gain or coupling changes the de "
                "Broglie wavelength of a macroscopic mass."
            ),
            "template_step": REUSABLE_TEMPLATE[2],
            "evidence_value": (
                "Cite: the matter wavelength (2.56e-41 m for 70 kg "
                "at 370 km/s), the 1.17e37 ratio, the 8.74e31 rad "
                "phase per site, and the 1.68e19 most generous "
                "shortfall."
            ),
        },
        {
            "piece": pieces[2]["name"],
            "bound_and_number": (
                f"{pieces[2]['bound']} {pieces[2]['number_text']}. "
                f"{pieces[2]['best_case']}."
            ),
            "robustness": (
                "Proves the two failures are one failure: the claim "
                "needs the same site to satisfy both bounds at "
                "once, and no site does. The joint bound is "
                "stricter than either bound alone."
            ),
            "template_step": REUSABLE_TEMPLATE[3],
            "evidence_value": (
                "Cite: the joint count (0 sites) and the symmetry "
                "argument -- one wave principle (Fourier duality), "
                "two failures, opposite directions."
            ),
        },
        {
            "piece": pieces[3]["name"],
            "bound_and_number": (
                f"{pieces[3]['bound']} {pieces[3]['number_text']}. "
                f"{pieces[3]['best_case']}."
            ),
            "robustness": (
                "Proves the FAIL is robust to bounded calibration: "
                "the best calibration buys exactly 0.0223 orders "
                "(log10(1/0.95), a mathematical identity), while "
                "the gap is 19-37 orders."
            ),
            "template_step": REUSABLE_TEMPLATE[4],
            "evidence_value": (
                "Cite: the Observer + Calibrator design, the "
                "0.0223-order improvement, and the 1.60e19 "
                "best-calibrated gap."
            ),
        },
        {
            "piece": pieces[4]["name"],
            "bound_and_number": (
                f"{pieces[4]['bound']} {pieces[4]['number_text']}. "
                f"{pieces[4]['best_case']}."
            ),
            "robustness": (
                "Proves the FAIL is robust to random input noise: "
                "the log-gap state is almost unchanged by 1% noise "
                "(spooky 0.99999995) and the verdict holds 5/5."
            ),
            "template_step": REUSABLE_TEMPLATE[5],
            "evidence_value": (
                "Cite: the spooky correlation (0.99999995 at "
                "sigma = 0.01) and the 5/5 verdict stability. Not "
                "comparable to the Omega-Genesis 0.9005 (same "
                "concept, different state and noise)."
            ),
        },
    ]
    return {
        "pieces": entries,
        "reusable_template": list(REUSABLE_TEMPLATE),
        "unified_verdict": unified_verdict(),
        "summary": (
            "This package gives you one verdict (FAIL) supported "
            "five ways: two independent physical bounds "
            "(diffraction, de Broglie), their joint form (Fourier "
            "duality, joint count 0), and two robustness proofs "
            "(bounded calibration buys 0.0223 orders; spooky "
            "0.99999995, verdict 5/5). It also gives you a reusable "
            "template -- claim, Abbe, de Broglie, joint, bounded "
            "calibration, noisy-copy spooky, verdict -- for testing "
            "any other wave-memory claim the same way, with the "
            "same honesty standard: numbers, not adjectives."
        ),
    }


def main():
    """Print the five pieces, the unified verdict, and the summary."""
    print("Unified verdict -- Lee, Digital to Wave Part II")
    print("Zenodo 21947108. Five pieces, one verdict.")
    print()
    for i, piece in enumerate(all_pieces(), start=1):
        print(f"{i}. {piece['name']}")
        print(f"   {piece['bound']}")
        print(f"   {piece['number_text']}")
        print(f"   {piece['best_case']}")
        print(f"   Verdict: {piece['verdict']}")
        print()
    print(f"UNIFIED VERDICT: {unified_verdict()} -- the claim fails "
          f"on the diffraction bound, on the de Broglie bound, on "
          f"their joint form, and after the best bounded calibration; "
          f"and the failure is stable under input noise.")
    print()
    print("Benefits: " + benefits_manifest()["summary"])


if __name__ == "__main__":
    main()
