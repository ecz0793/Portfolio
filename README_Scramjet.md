# Aerodynamic Optimization Project — Numerical Simulation of Compressible Internal Flow in a Scramjet

**Authors:** Etienne CRZ
**Course:** LU3ME104 — Sorbonne Université

## Overview

This project studies and optimizes the aerodynamics of an internal flow problem inside a simplified **scramjet** (supersonic combustion ramjet) inlet configuration.

Unlike a classical ramjet, which slows incoming air to subsonic speed before combustion and typically operates between Mach 3 and Mach 6, a scramjet keeps the airflow supersonic (Mach > 1) throughout the engine. This project focuses specifically on the **inlet section**, modeled as a simplified 2D geometry defined by 8 coordinate points and 5 boundary segments (m1–m5).

The flow is modeled as an **inviscid perfect gas**, so viscous effects are neglected and the **Euler equations** are solved. This choice lets the study focus on shock-wave dynamics rather than boundary-layer effects.

The project is split into two phases:

1. **Direct problem** — mesh generation (Gmsh), spatial convergence validation, and flow simulation with sensitivity analysis to flight conditions (Mach number, angle of attack) and geometry.
2. **Adjoint optimization** — using the continuous adjoint method to compute flow sensitivities and attempt a shape optimization of the inlet's upper wall, aiming to minimize total pressure loss at the outlet.

Simulations are performed with **SU2** (open-source CFD solver).

## Geometry

The inlet is modeled as a 2D domain with 8 points forming 5 boundary segments:

- **m1** — upstream vertical inflow boundary
- **m2** — solid walls (slip / Euler boundary conditions)
- **m3** — upper wall (design surface targeted by the optimization)
- **m4** — compression ramp segment
- **m5** — outlet section

## Part 1 — Direct Problem

### 1. Reference case

The reference case is an inflow at **Mach 2** with zero angle of attack. Slip (Euler) wall conditions are applied since viscous effects are neglected.

An oblique shock wave forms at the compression ramp, producing a sharp drop in Mach number together with a sudden rise in pressure and density. This initial shock reflects off the lower wall, generating a "diamond" shock-train pattern that propagates downstream through the channel — the classic behavior of supersonic flow in a converging duct, which compresses the air before it reaches the combustion chamber.

### 2. Spatial convergence study

A mesh convergence study was performed with **Gmsh**, comparing three refinement levels:

| Mesh | Characteristic length (lc) |
|------|------------------------------|
| Mesh 1 | 0.2 |
| Mesh 2 | 0.1 |
| Mesh 3 | 0.05 |

The outlet pressure coefficient profiles were compared across the three meshes. As refinement increases, the pressure gradients (marking shock position and intensity) become sharper and more stable, converging toward a consistent profile. Mesh 1 was retained as the reference mesh, offering the best trade-off between resolving shocks accurately and keeping computational cost manageable for the rest of the study.

### 3. Sensitivity to flight conditions (Mach number & angle of attack)

**Mach number:** Increasing the incoming Mach number from 2 to 4 significantly changes the pressure field. Higher Mach numbers weaken the relative shock strength, shift shock reflection points further downstream, and reduce the pressure coefficient overall (due to the much larger dynamic pressure of the freestream at higher speed).

**Angle of attack:** Increasing the angle of attack raises the effective compression angle at the lower ramp, intensifying the initial shock, while potentially generating an expansion wave on the upper inlet surface. This creates an asymmetric flow structure that strongly perturbs the overall compression ratio and mass flow capture — showing that the inlet performance is highly sensitive to incidence angle.

### 4. Geometric sensitivity — ramp angle

The angle between points 6 and 7 (part of the m4/m3 junction) was also studied. Moving point 6 from its initial position (x = 0.907, y = 0.254, ramp angle ≈ 6°) to x = 1.5 produces a new ramp angle of ≈ 4.5°. This geometric change shifts the pressure jump and displaces the entire shock train, confirming that the flow topology is highly sensitive to even small geometric variations.

### Motivation for optimization

The direct-problem analysis shows that the scramjet's internal flow is crossed by multiple shock reflections, producing a highly non-uniform pressure profile at the outlet. Since combustion efficiency requires the delivered air to be as uniform as possible while retaining maximum total pressure, and since shock position/intensity are extremely sensitive to wall geometry, manual trial-and-error shape design is impractical. This motivates a mathematically rigorous shape-optimization approach — the **adjoint method**.

## Part 2 — Adjoint-Based Optimization

### 1. Role of the adjoint method

Computing the gradient of a cost function with respect to design variables via finite differences requires one additional flow simulation per design variable, which becomes prohibitively expensive. The **adjoint method** avoids this: by introducing Lagrange multipliers (the adjoint variables), the gradient of the cost function with respect to *all* design variables is obtained by solving a single additional system (the adjoint equations), independent of the number of design variables.

The optimization problem is formulated without major geometric constraints. The objective is to maximize total pressure recovery in the engine. The cost function `J` to minimize is the quadratic deviation of total pressure over the outlet surface `S`:

```
J = ∫_S  1/2 (p - p∞)² dS
```

The optimizer's goal is to minimize outlet pressure non-uniformity by modifying the boundary shape (the wall geometry).

### 2. Adjoint solution & sensitivity analysis

SU2 computes the adjoint state starting from the converged direct-problem solution.

- **Adjoint density profile:** Sensitivity is systematically negative along the outlet section, with a sharp transition around Y = 0.30, dropping to values near -1900. This indicates that the upper part of the channel is the most sensitive region to density variations, reflecting the shock/expansion structures identified in the direct problem.
- **Surface sensitivity on m3 (upper wall):** Shows large-amplitude sensitivity, with strong negative influence near the inlet (X ≈ 0) and mid-duct (X ≈ 1.0), and a positive-sensitivity zone near the end of the ramp (X ≈ 1.5). This indicates m3 is a powerful control surface, with the optimizer expected to adjust its curvature primarily at these locations.
- **Surface sensitivity on m4:** Adjoint density values are less extreme than on m3 (between -1270 and -1150), but the surface sensitivity peaks at a very high, narrow spike (~+500,000 around X = 1.17). This points to m4 being a highly localized, "nervous" transition zone — any small change there disproportionately affects outlet pressure, but the effect is very localized rather than distributed.

**Conclusion:** Optimizing **m3** (rather than m4) is more relevant, since it governs the global shock structure over the full duct length and its sensitivity curve (alternating positive/negative) offers a complete control lever over the initial compression, whereas m4's influence is too localized to meaningfully improve global performance.

### 3. Optimization strategy & setup

The design variables are the coordinates of the m3 (upper wall) surface points. A **Hicks-Henne shape function** parametrization is used to link mesh node displacements to a restricted set of control variables, ensuring a smooth, aerodynamically consistent wall deformation. A gradient-descent algorithm, driven by `OPT_ACCURACY` and the `OPT_OBJECTIVE` penalty, iterates to minimize the cost functional.

Optimization parameters used (`inlet.cfg`):

```
OPT_GRADIENT_FACTOR = 1E3
OPT_RELAX_FACTOR    = 1E-6
OPT_OBJECTIVE       = SURFACE_TOTAL_PRESSURE * 1E-9
OPT_ITERATIONS      = 100
OPT_BOUND_UPPER     = 0.1
OPT_BOUND_LOWER     = -0.1
OPT_CONSTRAINT      = NONE
OPT_ACCURACY        = 1E-10
```

### 4. Result: no geometric deformation observed

Comparing the 1st, 5th, 9th, and final optimization iterations, **no visible change in geometry or the flow field occurs** — the first and last designs are identical. The optimizer failed to deform the upper wall.

**Suspected causes:**

1. **Gradient/objective scaling:** The `OPT_OBJECTIVE` penalty factor may be mismatched with the actual order of magnitude of pressure in the domain, resulting in numerically negligible gradients. The optimizer then incorrectly concludes it has already reached a local minimum.
2. **Precision settings (`OPT_ACCURACY`):** An overly restrictive stopping tolerance or maximum per-iteration deformation step may have prevented the solver from perceptibly modifying the mesh.

## Conclusions

- The direct-problem study successfully characterized a complex "diamond" shock-train system inside the scramjet inlet at Mach 2, and showed the flow topology is highly sensitive to Mach number, angle of attack, and ramp geometry.
- The adjoint analysis correctly identified the **upper wall (m3)** as the most relevant lever for controlling the global shock structure.
- However, the **shape-optimization phase did not converge to a visible geometric change** — the initial and final designs remained identical despite applying the adjoint-based gradient method.

### Difficulties encountered

The main difficulty was mastering the complexity of the SU2 solver's configuration, in particular understanding the interaction between numerical settings such as gradient and relaxation factors, and translating mathematical sensitivities into actual geometric deformations.

### Limitations

- Modeling the fluid as inviscid (Euler equations) neglects viscous effects and shock/boundary-layer interactions, which are critical phenomena in a real scramjet.
- The rigid optimization parametrization — particularly the `OPT_ACCURACY` tolerance and the allowed deformation step — likely froze the geometry at its initial state, preventing the optimizer from converging to an improved design.

## Tools & Methods

- **Gmsh** — mesh generation
- **SU2** — Euler flow solver, continuous adjoint solver, and gradient-based shape optimization
- **Hicks-Henne shape functions** — geometric parametrization for smooth wall deformation
