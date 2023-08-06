---
title: 'The Pulsar Signal Simulator: A Python package for simulating radio signal data from pulsars'
tags:
  - Python
  - pulsars
  - astronomy
  - gravitational waves
  - pulsar timing arrays
authors:
  - name: Jeffrey S. Hazboun
    orcid: 0000-0003-2742-3321
    affiliation: 1
  - name: Brent Shapiro-Albert
    orcid: 0000-0002-7283-1124
    affiliation: 2, 3
  - name: Paul T. Baker
    orcid: 0000-0003-2745-753X
    affiliation: 4
  - name: Amelia M. Henkel
    orcid: 0000-0001-8688-5273
    affiliation: 5
  - name: Cassidy M. Wagner
    orcid: 0000-0002-1186-2082
    affiliation: 6
  - name: Jacob Hesse
    affiliation: 1
  - name: Paul R. Brook
    orcid: 0000-0003-3053-6538
    affiliation: 2, 3
  - name: Michael T. Lam
    orcid: 0000-0003-0721-651X
    affiliation: 7, 8
  - name: Maura A. McLaughlin
    orcid: 0000-0001-7697-7422
    affiliation: 2, 3
  - name: Nathan Garver-Daniels
    orcid: 0000-0001-6166-9646
    affiliation: 2, 3
affiliations:
 - name: Physical Sciences Division, University of Washington Bothell, 18115 Campus Way NE, Bothell, WA 98011, USA
   index: 1
 - name: Department of Physics and Astronomy, West Virginia University, P.O. Box 6315, Morgantown, WV 26506, USA
   index: 2
 - name: Center for Gravitational Waves and Cosmology, West Virginia University, Chestnut Ridge Research Building, Morgantown, WV 26505, USA
   index: 3
 - name: Department of Physics and Astronomy, Widener University, One University Place, Chester, PA 19013, USA
   index: 4
 - name: University of New Hampshire
   index: 5
 - name: Department of Astronomy, University of Illinois, 1002 West Green Street, Urbana IL 61802, USA
   index: 6
 - name: School of Physics and Astronomy, Rochester Institute of Technology, Rochester, NY 14623, USA
   index: 7
 - name: Laboratory for Multiwavelength Astrophysics, Rochester Institute of Technology, Rochester, NY 14623, USA
   index: 8
date: 6 August 2020
bibliography: paper.bib
aas-doi: 10.3847/xxxxx
aas-journal: Astrophysical Journal
---

# Summary

Pulsar observations have been a hallmark of radio astronomy since Jocelyn Bell Burnell
discovered the repeating signal from PSR B1919+21 in 1967 [@hewish1968]. Today, most radio frequency observatories include dedicated equipment for observations of pulsars, e.g., @arecibo2019, @gbt2019, @chime2019, @meertime2020.
The phenomenal precision of pulsar rotational periods has allowed for many notable observations stemming from strong field general relativity, including a Nobel Prize for the discovery of the first binary neutron star [@taylor1975], which led to the first evidence for gravitational waves [@taylor1982].

Pulsars continue to be used as probes of gravity as the constituents of pulsar timing arrays (PTAs). PTAs are collections of highly precise millisecond pulsars regularly
monitored for shifts in their pulse arrival times indicative of gravitational
waves in the nanohertz regime. See @ransom2019, @hobbs and @burke-spolaor for a review of
pulsar timing arrays and the astrophysics of nanohertz gravitational waves.

# Statement of Need

In order to use neutron stars as a galactic-scale gravitational wave observatory, it is important to understand the noise that affects the timing of radio pulses. The pulse times of arrival are modeled deterministically using aspects of the pulse profile, intrinsic flux, orbital parameters of the pulsar (if in a binary system), proper motion across the sky, effects of the interstellar medium (ISM), position of the observatory with respect to the solar system barycenter and various aspects of the telescope and backend processing.  Additionally, stochastic noise processes affect the times of arrival.

A number of `c`/`c++`-based packages exist which have pulsar signal simulation capabilities. The `SigProc` package [@sigproc2011] has long been publicly available for processing radio-based pulsar observation data and has a simulation module that uses a timing model to reproduce data in its native `fb` data structure. ``PSRCHIVE`` [@hotan2004; @VanStraten2012], another popular software package for processing radio data of pulsars,  has the ability to produce simulated pulsar profiles, but not as part of a full simulation pipeline. There are timing packages [@Luo2020; @tempo2] that can simulate noise/signals in the times of arrival of pulses, for instance to simulate gravitational wave signals, but these are a derivative data product making the injection of some noise processes and signals more difficult. The end-to-end simulation of ``PsrSigSim`` provides a way to study the covariances of the timing model and noise terms in a physically motivated and controlled manner using the basal data product output from radio observations.

``PsrSigSim`` is the first Python package for general-purpose simulation of radio telescope data from pulsar timing observations, based on the formalism presented in [@shapiroalbert2020pss].
It uses standard Python packages, such as ``NumPy`` [@numpy] and ``Astropy``
[@astropy], to simulate radio pulses from a neutron star and the effects of the interstellar material on the signal propagation. ``Signal`` objects are passed to ``Pulsar`` objects and `Telescope` objects to build a realistic pulsar signal from scratch. `ISM` objects use various signal-processing techniques, such as the Fourier shift theorem and convolution of pulse profiles with decaying exponentials, in order to simulate the frequency-dependent effects of the interstellar medium on pulse arrival times. ``PsrSigSim`` interfaces with various pulsar data standards, such as `PSRFITS` [@hotan2004], to build data products that can be passed to existing data-processing pipelines.

The modularity of the simulation allows enumerable options for investigating the processing of pulsar signals using the built-in features. It also allows users to add new physical effects with ease. The signals from different pulsars can be treated by the same telescope in order to investigate how various pulsars would look using a particular telescope configuration. A user can either use a provided telescope/backend, or build one with their own specifications.  This modularity also makes `PsrSigSim` an excellent tool for educating students about the physics of pulsar signals and how they are observed and processed.

The generic functionality, modularity and the ability to add user-defined signals/noise make `PsrSigSim` an useful tool for all pulsar researchers.

# Acknowledgements

JSH, BJS, PTB, PRB, MAM and MTL acknowledge subawards from the NSF NANOGrav Physics Frontier Center (NSF PFC-1430284). BJS acknowledges support from West Virginia University through the STEM Mountains of Excellence Fellowship. Finally, we thank Richard Prestage, Joseph D. Romano, Tim T. Pennucci and Paul B. Demorest for useful discussions.

# References
