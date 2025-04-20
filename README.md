# LCA-Eaposys-
The following Python script is based on a manual database due to the unavailability of specific data. The numbers used in the script are approximate and can be modified if new data becomes available. This script is designed to test the impact of different nanoparticles on water-based nanofluids, with varying nanoparticle mass fractions ranging from 0 to 1.
Purpose
This Python script is designed to perform a Life Cycle Assessment (LCA) of water-based nanofluids, focusing on the environmental impact of different nanoparticles. It evaluates key environmental impact factors, including carbon footprint, energy demand, toxicity, water usage, and cost. The script is particularly useful for assessing the sustainability of nanofluid formulations used in applications such as geothermal energy systems.

How It Works
The script allows the analysis of various nanofluid compositions by calculating the LCA impacts for different nanoparticles (e.g., Copper, Aluminum) and their respective mass fractions ranging from 0 to 1. The script provides outputs such as:

Carbon Footprint: CO₂ and CH₄ emissions associated with the nanofluid.

Energy Demand: The range of energy required to produce the nanofluid.

Toxicity: Human toxicity potential (HTP) and ecotoxicity potential (ETP) for the nanofluid.

Water Footprint: The total water consumption for producing the nanofluid.

Cost: The cost of the nanofluid based on nanoparticle price.

Manual Database
The script is based on a manual database due to the unavailability of detailed data for the nanoparticles. The numbers provided are approximate and can be modified when new data is available. The current database includes nanoparticles like Copper (Cu) and Aluminum (Al), and the mass fraction of the nanoparticles in the nanofluid can be adjusted to test different formulations.

LCA Calculation Functions
Several functions are defined within the script to compute the different aspects of the LCA:

calc_cf: Calculates the carbon footprint (CO₂ and CH₄ emissions).

calc_ced: Calculates the cumulative energy demand for producing the nanofluid.

calc_toxicity: Calculates the human toxicity potential (HTP) and ecotoxicity potential (ETP) for the nanofluid.

calc_wf: Calculates the water footprint of the nanofluid.

calc_cost: Computes the cost of the nanofluid based on the nanoparticle cost and mass fraction.

Usage
You can easily modify the script to test different nanoparticle combinations and mass fractions. The script takes the mass fraction of the nanoparticle as input, runs the LCA calculations, and prints the results.
Conclusion
This script provides an efficient and modular way of conducting a Life Cycle Assessment for nanofluids, helping to identify the most sustainable formulations for energy applications like geothermal systems. Its flexibility allows for use with a wide range of nanofluids and energy contexts.
