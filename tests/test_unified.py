# test_unified.py
#
# Tests for the unified package (fourier_duality.py +
# unified_verdict.py) on Lee, Digital to Wave Part II,
# Zenodo 21947108.
#
# Exactly 5 tests:
#   1. The joint count is zero (< 1) for every macroscopic mass
#      and THz frequency.
#   2. The Fourier-duality module reproduces the two known
#      shortfalls (diffraction best case 301 MB / 2.65e14; de
#      Broglie most generous 1.68e19) within 1%.
#   3. The aggregator's unified verdict is FAIL and it lists all
#      five pieces.
#   4. The benefits manifest contains all five pieces and the
#      reusable template.
#   5. The joint bound is stricter than either bound alone: the
#      joint count (zero) is below both the resolvable-voxel count
#      and the addressable-site count (the continuous coherent-sites
#      measure, stated explicitly).
#
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import fourier_duality as fd
import unified_verdict as uv


def test_1_joint_count_is_zero_for_every_macroscopic_case():
    """The joint count is zero (< 1) for every macroscopic mass
    and THz frequency, at both paper velocities."""
    for f in fd.FREQUENCIES_HZ:
        for m in fd.MACROSCOPIC_MASSES_KG:
            for v in (
                fd.CMB_VELOCITY_M_S,
                fd.thermal_velocity_m_s(m),
            ):
                joint = fd.joint_sites(f, m, v)
                assert joint == 0, (f, m, v, joint)
                assert joint < 1
    # The joint verdict is FAIL.
    assert fd.joint_verdict() == "FAIL"


def test_2_reproduces_the_two_known_shortfalls():
    """The module reproduces the companion repos' verified numbers
    within 1%: diffraction best case 301 MB / 2.65e14, and de
    Broglie most generous 1.68e19."""
    # Diffraction: best case 3 THz, NA = 1, 1000 bits/voxel.
    assert math.isclose(
        fd.best_case_readable_mb(), 301.0, rel_tol=0.01
    ), fd.best_case_readable_mb()
    assert math.isclose(
        fd.worst_case_diffraction_ratio(), 2.65e14, rel_tol=0.01
    ), fd.worst_case_diffraction_ratio()
    # Spot values from the diffraction table.
    assert math.isclose(
        fd.voxel_count(1e12), 8.91e4, rel_tol=0.01
    ), fd.voxel_count(1e12)
    assert math.isclose(
        fd.voxel_count(3e12), 2.41e6, rel_tol=0.01
    ), fd.voxel_count(3e12)
    assert math.isclose(
        fd.claim_ratio_diffraction(1e12, 10, 1.0), 7.15e17, rel_tol=0.01
    ), fd.claim_ratio_diffraction(1e12, 10, 1.0)
    # de Broglie: most generous case 1 kg, thermal, 3 THz.
    assert math.isclose(
        fd.worst_case_debroglie_ratio(), 1.68e19, rel_tol=0.01
    ), fd.worst_case_debroglie_ratio()
    # Headline case: 70 kg at 370 km/s.
    lam = fd.de_broglie_wavelength_m(70.0, fd.CMB_VELOCITY_M_S)
    assert math.isclose(lam, 2.56e-41, rel_tol=0.01), lam
    assert math.isclose(
        fd.wavelength_ratio_thz(1e12, 70.0, fd.CMB_VELOCITY_M_S),
        1.17e37,
        rel_tol=0.01,
    )
    assert math.isclose(
        fd.phase_per_lattice_spacing_rad(70.0, fd.CMB_VELOCITY_M_S),
        8.74e31,
        rel_tol=0.01,
    )
    # Both individual verdicts are FAIL.
    assert fd.diffraction_verdict() == "FAIL"
    assert fd.debroglie_verdict() == "FAIL"


def test_3_unified_verdict_is_fail_with_all_five_pieces():
    """The aggregator's unified verdict is FAIL and it lists all
    five pieces, each with its own verdict."""
    assert uv.unified_verdict() == "FAIL"
    pieces = uv.all_pieces()
    assert len(pieces) == 5, len(pieces)
    names = [p["name"] for p in pieces]
    assert "Diffraction" in names[0]
    assert "de Broglie" in names[1]
    assert "Fourier-duality" in names[2]
    assert "calibration" in names[3].lower()
    assert "Spooky" in names[4]
    # Pieces 1-4 each FAIL on their own; piece 5 confirms the FAIL
    # is stable.
    assert pieces[0]["verdict"] == "FAIL"
    assert pieces[1]["verdict"] == "FAIL"
    assert pieces[2]["verdict"] == "FAIL"
    assert pieces[3]["verdict"] == "FAIL"
    assert pieces[4]["verdict"].startswith("FAIL")
    # The calibration piece reproduces the analytic identity.
    assert math.isclose(
        uv.calibration_improvement_orders(), 0.0223, rel_tol=0.01
    ), uv.calibration_improvement_orders()
    assert math.isclose(
        uv.calibration_improvement_orders(),
        math.log10(1.0 / 0.95),
        rel_tol=1e-12,
    )


def test_4_benefits_manifest_has_five_pieces_and_template():
    """The benefits manifest contains all five pieces and the
    reusable template (claim -> Abbe -> de Broglie -> joint ->
    bounded calibration -> noisy-copy spooky -> verdict)."""
    manifest = uv.benefits_manifest()
    assert manifest["unified_verdict"] == "FAIL"
    assert len(manifest["pieces"]) == 5, len(manifest["pieces"])
    for entry in manifest["pieces"]:
        for key in (
            "piece",
            "bound_and_number",
            "robustness",
            "template_step",
            "evidence_value",
        ):
            assert key in entry, key
            assert entry[key], entry["piece"]
    # The template has all seven steps, in order.
    template = manifest["reusable_template"]
    assert len(template) == 7, len(template)
    assert "Abbe" in template[1]
    assert "de Broglie" in template[2]
    assert "Joint" in template[3]
    assert "calibration" in template[4].lower()
    assert "spooky" in template[5].lower()
    assert "Verdict" in template[6]
    # The summary names the unified verdict and the template.
    assert "FAIL" in manifest["summary"]
    assert "template" in manifest["summary"].lower()


def test_5_joint_bound_is_stricter_than_either_alone():
    """The joint count (zero) is below both the resolvable-voxel
    count and the addressable-site count.

    The addressable-site comparison uses the CONTINUOUS
    coherent-sites measure lam / (2 pi a0): the number of lattice
    sites over which the matter-wave phase stays within 1 radian.
    For macroscopic masses this is a tiny positive number
    (~10^-32 to ~10^-15), i.e. less than one site is even
    coherently addressable, so the integer joint count (0) is
    strictly below it. The integer addressable-site count is
    floor(coherent_sites) = 0 for every macroscopic mass, which
    is what makes the joint count zero: the matter wave is the
    binding constraint. The joint bound requires BOTH conditions,
    so it can never exceed either individual count -- and here it
    equals the stricter one (0) while the other (voxels) is large.
    """
    for f in fd.FREQUENCIES_HZ:
        for m in fd.MACROSCOPIC_MASSES_KG:
            for v in (
                fd.CMB_VELOCITY_M_S,
                fd.thermal_velocity_m_s(m),
            ):
                joint = fd.joint_sites(f, m, v)
                voxels = fd.voxel_count(f)
                coherent = fd.coherent_sites(m, v)
                addressable = fd.addressable_sites(m, v)
                # Joint is zero.
                assert joint == 0, (f, m, v, joint)
                # Joint is strictly below the resolvable-voxel count.
                assert joint < voxels, (joint, voxels)
                assert voxels >= 2.40e3, voxels  # 2405 voxels at 300 GHz
                # Joint is strictly below the continuous coherent-sites
                # measure (a tiny positive number: < 1 site is even
                # coherently addressable).
                assert 0.0 < coherent < 1.0, (m, v, coherent)
                assert joint < coherent, (joint, coherent)
                # The integer addressable count is 0 -- the matter
                # wave is the binding constraint, and the joint
                # equals it.
                assert addressable == 0, (m, v, addressable)
                assert joint == addressable
    # The same holds for the most generous case specifically.
    joint = fd.joint_sites(3e12, 1.0, fd.thermal_velocity_m_s(1.0))
    assert joint == 0
    assert joint < fd.voxel_count(3e12)  # 2.41e6 voxels
    assert joint < fd.coherent_sites(1.0, fd.thermal_velocity_m_s(1.0))
