# fourier_duality.py
#
# Fourier-duality joint bound for the claims in Lee,
# "Digital to Wave: LGD In Situ Wave Memory-Human Wave Integrated
# Interface-Metaverse Hologram-Wave Affective AI"
# (Zenodo 21947108, DOI 10.5281/zenodo.21947108, 2026-08-15).
#
# The paper's §1/§3 claim requires BOTH of the following at the same
# time, on the same lattice site:
#   (a) the THz readout wave resolves the site (a0 = 0.356 nm), and
#   (b) the object's de Broglie matter wave addresses the site
#       coherently (a well-defined phase at that site).
#
# The two companion falsifications are the SAME wave principle --
# Fourier duality -- seen from opposite sides:
#   - Position space (Abbe limit): a wave of wavelength lam cannot
#     resolve features smaller than ~lam/2. A wave confined to
#     Delta-x has a spread in spatial frequency, Delta-k >= 1/(2
#     Delta-x); that is the Fourier uncertainty relation, and the
#     Abbe limit d = lam / (2 NA) is its optical form. The THz wave
#     (lam 100-1000 um) is far too LONG to resolve a 0.356 nm site:
#     it resolves only voxels of side d, each holding (d/a0)^3 sites.
#   - Momentum space (de Broglie wavelength): a particle of
#     momentum p has wavelength lam = h/p. The same Fourier
#     transform relates position and momentum (Delta-x * Delta-p >=
#     hbar/2). The matter wave is far too SHORT to address a site
#     coherently: its phase across one lattice spacing,
#     2 pi a0 / lam, is ~10^15-10^31 rad -- effectively random, so
#     no coherent 1:1 mapping of a matter wave onto the lattice is
#     possible.
# Both bounds are the wave principle that a wave can only address
# features comparable to its own wavelength. The THz wave is too
# long; the matter wave is too short. The sweet spot, lam ~ a0, is
# occupied by neither. The joint bound counts the lattice sites
# that satisfy BOTH conditions at once. For every macroscopic mass
# and every THz frequency, that count is zero.
#
# This module is SELF-CONTAINED: it recomputes both bounds from the
# paper's own numbers and standard constants (h, c, k_B, a0, the
# crystal size, the THz band). It does not import from the two
# companion repos; their verified numbers are reproduced here and
# cited in the report.
#
# Status: SYNTHETIC computation. A classical-physics bound applied
# to the paper's own numbers. No physical claim, no experiment, no
# medical claim. Fourier duality is the known wave principle, not a
# new physical law; it is applied here to unify the two bounds.
#
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

"""Fourier-duality joint bound: one wave principle, two failures.

Recomputes the Abbe diffraction bound (position space) and the
de Broglie matter-wave bound (momentum space) from the paper's own
numbers, then counts the lattice sites that satisfy BOTH at once.
For every macroscopic mass and every THz frequency the joint count
is zero: the THz wave cannot resolve a site, and the matter wave
cannot coherently address one. The joint bound is the logical AND
of the two falsifications.
"""

import math

import numpy as np

# ---------------------------------------------------------------------------
# Inputs: standard physics constants (exact SI definitions where noted)
# ---------------------------------------------------------------------------

PLANCK_H_J_S = 6.62607015e-34  # exact, SI definition
SPEED_OF_LIGHT_M_S = 299792458.0  # exact, SI definition
BOLTZMANN_KB_J_K = 1.380649e-23  # exact, SI definition
ELECTRON_MASS_KG = 9.1093837e-31
PROTON_MASS_KG = 1.67262192e-27

# ---------------------------------------------------------------------------
# Inputs: the paper's own stated values (Zenodo 21947108)
# ---------------------------------------------------------------------------

# LGD lattice pitch, paper section 1 (diamond lattice constant).
LATTICE_PITCH_M = 0.356e-9

# Crystal dimensions, paper section 1: 10 x 10 x 3 mm^3.
CRYSTAL_LX_M = 10e-3
CRYSTAL_LY_M = 10e-3
CRYSTAL_LZ_M = 3e-3

# Claimed stored capacity, paper section 1: 79.6 ZB.
# 1 ZB is taken as 10^21 bytes (decimal), as in the paper's own
# arithmetic: 79.6 ZB = 6.37e23 bits (79.6e21 bytes x 8 bits/byte).
CLAIMED_CAPACITY_BITS = 79.6e21 * 8.0

# THz readout band, paper section 3: 300 GHz - 3 THz.
FREQUENCIES_HZ = (300e9, 1e12, 3e12)

# Bits assumed per resolution voxel. 1000 is deliberately generous.
BITS_PER_VOXEL = (1, 10, 1000)

# CMB peculiar velocity, paper section 3.1-3.2: v ~ 370 km/s.
CMB_VELOCITY_M_S = 370e3

# Temperature for thermal velocities: 300 K (room temperature).
THERMAL_TEMPERATURE_K = 300.0

# Masses reported: electron, proton, and macroscopic masses.
MASSES_KG = {
    "electron": ELECTRON_MASS_KG,
    "proton": PROTON_MASS_KG,
    "1 kg": 1.0,
    "70 kg": 70.0,
    "1000 kg": 1000.0,
}

# Macroscopic masses (the fail criterion applies to these).
MACROSCOPIC_MASSES_KG = (1.0, 70.0, 1000.0)

# Pass/fail threshold: the claim FAILS if a bound is >= 10 orders of
# magnitude short, i.e. the relevant ratio is >= 1e10, even in the
# most generous case.
FAIL_RATIO_THRESHOLD = 1e10


# ---------------------------------------------------------------------------
# Position space: the Abbe diffraction bound (recomputed)
# ---------------------------------------------------------------------------

def thz_wavelength_m(freq_hz):
    """Vacuum wavelength (m) of the THz readout wave at freq_hz."""
    return SPEED_OF_LIGHT_M_S / float(freq_hz)


def abbe_resolution_m(freq_hz, na=1.0):
    """Abbe diffraction limit d = lambda / (2 * NA), in metres.

    Best case NA = 1. Smaller NA (realistic optics) only worsens d.
    """
    if na <= 0.0 or na > 1.0:
        raise ValueError("NA must be in (0, 1] for far-field optics")
    return thz_wavelength_m(freq_hz) / (2.0 * float(na))


def voxel_count(freq_hz, na=1.0):
    """Number of resolvable voxels in the crystal, V / d^3.

    Each voxel is one distinguishable position for the THz readout:
    at best, one (multiplexed) value per voxel. The crystal holds
    ~6.65e21 lattice sites; the readout distinguishes only ~10^3-10^6
    voxels, so the vast majority of sites are indistinguishable.
    """
    d = abbe_resolution_m(freq_hz, na)
    volume = CRYSTAL_LX_M * CRYSTAL_LY_M * CRYSTAL_LZ_M
    return volume / d ** 3


def sites_per_voxel(freq_hz, na=1.0):
    """Lattice sites inside one cubic resolution voxel, (d / a0)^3."""
    return (abbe_resolution_m(freq_hz, na) / LATTICE_PITCH_M) ** 3


def readable_capacity_bits(freq_hz, bits_per_voxel, na=1.0):
    """Diffraction-limited readable capacity in bits: voxels x bpv."""
    return voxel_count(freq_hz, na) * float(bits_per_voxel)


def claim_ratio_diffraction(freq_hz, bits_per_voxel, na=1.0):
    """Claimed capacity / diffraction-limited readable capacity."""
    return CLAIMED_CAPACITY_BITS / readable_capacity_bits(
        freq_hz, bits_per_voxel, na
    )


def worst_case_diffraction_ratio():
    """Smallest claim/capacity ratio over all frequencies and
    bits-per-voxel at NA = 1 -- the most generous case for the paper
    (3 THz, NA = 1, 1000 bits per voxel). Reproduces the companion
    repo's 2.65e14."""
    ratios = [
        claim_ratio_diffraction(f, bpv, 1.0)
        for f in FREQUENCIES_HZ
        for bpv in BITS_PER_VOXEL
    ]
    return min(ratios)


def best_case_readable_mb():
    """Most generous readable capacity, in megabytes.

    3 THz, NA = 1, 1000 bits per voxel. Reproduces the companion
    repo's 301 MB.
    """
    bits = readable_capacity_bits(3e12, 1000, 1.0)
    return bits / 8.0 / 1e6


def diffraction_verdict():
    """PASS/FAIL on the THz readout claim (Abbe bound).

    FAIL if the diffraction-limited capacity is >= 10 orders of
    magnitude below the claimed 79.6 ZB even in the most generous
    case. Returns "FAIL" or "PASS".
    """
    return (
        "FAIL"
        if worst_case_diffraction_ratio() >= FAIL_RATIO_THRESHOLD
        else "PASS"
    )


# ---------------------------------------------------------------------------
# Momentum space: the de Broglie matter-wave bound (recomputed)
# ---------------------------------------------------------------------------

def kinetic_energy_joules(mass_kg, velocity_m_s):
    """Relativistic kinetic energy E = (gamma - 1) m c^2, in joules.

    Computed in the numerically stable form E = m v^2 / (s (1 + s))
    with s = sqrt(1 - (v/c)^2), so that slow velocities do not
    underflow: at v/c ~ 1e-20 the naive (gamma - 1) is exactly 0.0
    in double precision, while this form returns 1/2 m v^2 to full
    precision.
    """
    m = float(mass_kg)
    v = float(velocity_m_s)
    if m <= 0.0:
        raise ValueError("mass must be positive")
    if not 0.0 <= abs(v) < SPEED_OF_LIGHT_M_S:
        raise ValueError("velocity must satisfy 0 <= |v| < c")
    beta_sq = (v / SPEED_OF_LIGHT_M_S) ** 2
    s = math.sqrt(1.0 - beta_sq)
    return m * v * v / (s * (1.0 + s))


def de_broglie_wavelength_m(mass_kg, velocity_m_s):
    """Relativistic de Broglie wavelength, in metres.

    lambda = h / sqrt(2 m E + E^2 / c^2), the paper's own formula
    (section 3.4), correctly stated there. E is the kinetic energy.
    """
    e = kinetic_energy_joules(mass_kg, velocity_m_s)
    m = float(mass_kg)
    p = math.sqrt(2.0 * m * e + e ** 2 / SPEED_OF_LIGHT_M_S ** 2)
    return PLANCK_H_J_S / p


def thermal_velocity_m_s(mass_kg, temperature_k=THERMAL_TEMPERATURE_K):
    """Root-mean-square thermal velocity v_rms = sqrt(3 k_B T / m)."""
    m = float(mass_kg)
    if m <= 0.0:
        raise ValueError("mass must be positive")
    return math.sqrt(3.0 * BOLTZMANN_KB_J_K * float(temperature_k) / m)


def wavelength_ratio_thz(freq_hz, mass_kg, velocity_m_s):
    """lambda_THz / lambda_matter (dimensionless).

    How many matter wavelengths fit across one THz wavelength.
    """
    lam = de_broglie_wavelength_m(mass_kg, velocity_m_s)
    return thz_wavelength_m(freq_hz) / lam


def phase_per_lattice_spacing_rad(mass_kg, velocity_m_s):
    """Phase across one lattice spacing, k * a0 = 2 pi a0 / lambda.

    In radians. For macroscopic masses this is astronomically large,
    so the phase at neighbouring lattice sites is effectively random
    -- no coherent 1:1 mapping of a matter wave onto the lattice is
    possible.
    """
    lam = de_broglie_wavelength_m(mass_kg, velocity_m_s)
    return 2.0 * math.pi * LATTICE_PITCH_M / lam


def worst_case_debroglie_ratio():
    """Smallest lambda_THz / lambda_matter over all macroscopic
    masses (>= 1 kg), all paper velocities (CMB 370 km/s and thermal
    at 300 K) and all THz frequencies -- the most generous case for
    the paper (1 kg, thermal, 3 THz). Reproduces the companion
    repo's 1.68e19."""
    ratios = [
        wavelength_ratio_thz(f, m, v)
        for f in FREQUENCIES_HZ
        for m in MACROSCOPIC_MASSES_KG
        for v in (
            CMB_VELOCITY_M_S,
            thermal_velocity_m_s(m),
        )
    ]
    return min(ratios)


def debroglie_verdict():
    """PASS/FAIL on the matter-wave hologram claim (de Broglie bound).

    FAIL if lambda_matter is >= 10 orders of magnitude below
    lambda_THz for every macroscopic mass at every paper velocity
    and every THz frequency. Returns "FAIL" or "PASS".
    """
    return (
        "FAIL"
        if worst_case_debroglie_ratio() >= FAIL_RATIO_THRESHOLD
        else "PASS"
    )


# ---------------------------------------------------------------------------
# The joint bound: Fourier duality, both conditions at once
# ---------------------------------------------------------------------------

def coherent_sites(mass_kg, velocity_m_s):
    """Lattice sites over which the matter-wave phase stays within
    1 radian: lam / (2 pi a0), as a continuous count.

    The phase changes by 2 pi a0 / lam per lattice spacing, so the
    phase stays within 1 rad over lam / (2 pi a0) spacings. A value
    below 1 means the phase does not stay coherent across even a
    single lattice site. For macroscopic masses this is ~10^-32 to
    ~10^-15: the phase is effectively random from site to site.
    For the electron at thermal velocity it is ~2.8 sites.
    """
    lam = de_broglie_wavelength_m(mass_kg, velocity_m_s)
    return lam / (2.0 * math.pi * LATTICE_PITCH_M)


def addressable_sites(mass_kg, velocity_m_s):
    """Integer count of coherently addressable lattice sites.

    floor(coherent_sites): the number of whole lattice sites over
    which the matter-wave phase stays within 1 radian. 0 for every
    macroscopic mass at every paper velocity -- the matter wave
    cannot coherently address even one site. (The electron at
    thermal velocity manages 2; an electron's wave cannot carry a
    macroscopic object's hologram, and the claim is about objects.)
    """
    return int(coherent_sites(mass_kg, velocity_m_s))


def joint_sites(freq_hz, mass_kg, velocity_m_s, na=1.0):
    """Lattice sites satisfying BOTH conditions at once.

    A site is jointly usable only if (a) the THz readout can
    distinguish it from its neighbours -- it lies in its own
    resolvable voxel, so at most one distinguishable site per
    voxel -- and (b) the matter wave can coherently address it.
    The joint count is the number of sites satisfying both, which
    is at most the smaller of the two individual counts (an
    intersection cannot exceed either side). It is 0 for every
    macroscopic mass at every THz frequency, because the matter
    wave coherently addresses 0 sites: the joint bound is the
    logical AND of the two falsifications, and the matter-wave
    side is the binding constraint.
    """
    addr = addressable_sites(mass_kg, velocity_m_s)
    if addr <= 0:
        return 0
    return min(int(voxel_count(freq_hz, na)), addr)


def joint_verdict():
    """PASS/FAIL on the joint (Fourier-duality) claim.

    FAIL if the joint count is zero for every macroscopic mass, at
    every paper velocity and every THz frequency -- i.e. no lattice
    site is both resolvable by the THz readout and coherently
    addressable by the matter wave. Returns "FAIL" or "PASS".
    """
    for f in FREQUENCIES_HZ:
        for m in MACROSCOPIC_MASSES_KG:
            for v in (
                CMB_VELOCITY_M_S,
                thermal_velocity_m_s(m),
            ):
                if joint_sites(f, m, v) > 0:
                    return "PASS"
    return "FAIL"


def illustrative_product():
    """Product of the two best-case shortfalls, ILLUSTRATIVE only.

    worst_case_diffraction_ratio() x worst_case_debroglie_ratio()
    ~ 2.65e14 x 1.68e19 ~ 4.5e33. This is NOT a single physical
    quantity: the two ratios are different kinds (a capacity
    shortfall vs a wavelength shortfall), so their product has no
    physical meaning on its own. It is shown only to convey the
    scale of the combined failure. The rigorous statement is the
    joint count (zero) and the logical AND (FAIL if either fails).
    """
    return worst_case_diffraction_ratio() * worst_case_debroglie_ratio()


def joint_table():
    """One row per (frequency, mass, velocity) with the joint chain.

    Each row has the resolvable voxel count, the coherent-sites
    measure, the integer addressable-site count, the joint count,
    and the two individual ratios.
    """
    rows = []
    names = ("electron", "proton", "1 kg", "70 kg", "1000 kg")
    for f in FREQUENCIES_HZ:
        for name in names:
            m = MASSES_KG[name]
            for label, v in (
                ("CMB 370 km/s", CMB_VELOCITY_M_S),
                ("thermal 300 K", thermal_velocity_m_s(m)),
            ):
                rows.append(
                    {
                        "freq_hz": float(f),
                        "mass_name": name,
                        "mass_kg": m,
                        "velocity_label": label,
                        "velocity_m_s": v,
                        "voxels": voxel_count(f),
                        "coherent_sites": coherent_sites(m, v),
                        "addressable_sites": addressable_sites(m, v),
                        "joint_sites": joint_sites(f, m, v),
                        "claim_ratio_diffraction_1000bpv": (
                            claim_ratio_diffraction(f, 1000, 1.0)
                        ),
                        "lambda_thz_over_lambda": wavelength_ratio_thz(
                            f, m, v
                        ),
                        "phase_per_site_rad": (
                            phase_per_lattice_spacing_rad(m, v)
                        ),
                    }
                )
    return rows


def main():
    """Print the Fourier-duality joint table and the verdict."""
    print("Fourier duality -- Lee, Digital to Wave Part II")
    print("Zenodo 21947108. One wave principle, two failures:")
    print("the THz wave is too LONG to resolve a site (Abbe),")
    print("the matter wave is too SHORT to address one (de Broglie).")
    print()
    print(
        f"{'freq':>7} {'mass':>9} {'velocity':>13} "
        f"{'voxels':>10} {'coherent':>10} {'addressable':>11} "
        f"{'joint':>6} {'phase/site':>12}"
    )
    for row in joint_table():
        print(
            f"{row['freq_hz']/1e12:>6.2f}T {row['mass_name']:>9} "
            f"{row['velocity_label']:>13} "
            f"{row['voxels']:>10.2e} "
            f"{row['coherent_sites']:>10.2e} "
            f"{row['addressable_sites']:>11d} "
            f"{row['joint_sites']:>6d} "
            f"{row['phase_per_site_rad']:>12.2e}"
        )
    print()
    print(
        f"Diffraction best case: {best_case_readable_mb():.0f} MB "
        f"readable vs 79.6 ZB claimed "
        f"(short by {worst_case_diffraction_ratio():.2e})."
    )
    print(
        f"de Broglie most generous case: lambda_THz/lambda = "
        f"{worst_case_debroglie_ratio():.2e} "
        f"(1 kg, thermal, 3 THz)."
    )
    print(
        f"Illustrative product of the two shortfalls: "
        f"{illustrative_product():.2e} "
        f"(illustrative only -- see the caveat in the code)."
    )
    print()
    print(
        f"Joint count for every macroscopic mass and frequency: 0. "
        f"No lattice site is both resolvable by THz and coherently "
        f"addressable by the matter wave."
    )
    print(f"VERDICT: {joint_verdict()} -- the joint claim fails "
          f"because both of its halves fail.")


if __name__ == "__main__":
    main()
