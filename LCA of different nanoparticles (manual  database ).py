import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------
# Define Base Fluid (Water) Properties
# ------------------------------
water_properties = {
    "emissions": {"CO2": 0.02, "CH4": 0.0005},
    "energy_use": [0.5, 0.8],
    "water_use": [0.008, 0.015],
    "toxicity_factors": {"Ag": 3000, "ZnO": 1500, "TiO2": 1.37e-7, "SiO2": 0, "CuO": 0, "Al2O3": 0, "TiO2-SiC": 1e-7},
    "heat_transfer": 1000
}

# ------------------------------
# Nanoparticle Database (LCA-based)
# ------------------------------
nanoparticles = {
    "Ag": {"emissions": {"CO2": 0.3, "CH4": 0.01}, "toxicity": 5000, "energy_use": [1.5, 1.8], "water_use": [0.01, 0.02], "cost_per_kg": 50},
    "ZnO": {"emissions": {"CO2": 0.1, "CH4": 0.002}, "toxicity": 1500, "energy_use": [1.2, 1.5], "water_use": [0.005, 0.01], "cost_per_kg": 20},
    "TiO2": {"emissions": {"CO2": 7.69e-7, "CH4": 0.0}, "toxicity": 1.37e-7, "energy_use": [0.7, 1.2], "water_use": [0.01, 0.015], "cost_per_kg": 5.0},
    "SiO2": {"emissions": {"CO2": 7.26, "CH4": 0.0}, "toxicity": 0.0, "energy_use": [5.0, 6.0], "water_use": [0.02, 0.025], "cost_per_kg": 1.0},
    "CuO": {"emissions": {"CO2": 1.2, "CH4": 0.0}, "toxicity": 0.8, "energy_use": [3.0, 4.0], "water_use": [0.015, 0.02], "cost_per_kg": 8.0},
    "Al2O3": {"emissions": {"CO2": 2.5, "CH4": 0.001}, "toxicity": 0.5, "energy_use": [4.0, 4.5], "water_use": [0.01, 0.02], "cost_per_kg": 4.0},
    "TiO2-SiC": {"emissions": {"CO2": 1.0, "CH4": 0.0}, "toxicity": 1e-7, "energy_use": [1.0, 1.5], "water_use": [0.01, 0.015], "cost_per_kg": 6.5}  # Hybrid nanofluid
}
# ------------------------------
# Swiss EGS Parameters (3.5 km depth, 50-year lifetime)
# ------------------------------
swiss_egs_lca = {
    "depth_km": 3.5,
    "plant_lifetime_years": 50,
    "drilling_energy_total_kWh": 10986111.11,
    "electricity_kWh": 9887500.00,
    "diesel_kWh_equivalent": 1098611.11,
    "conversion_efficiency": 0.15,
    "ghg_emission_range_gCO2_kWh": [30, 40]
}
# ------------------------------
# EGS Drilling Impact Analysis (Swiss Case: 3.5 km, 50 years)
# ------------------------------
print("\n--- EGS System LCA (Swiss Case: 3.5 km Depth, 50-Year Lifetime) ---")

# Total electricity generated (based on 15% efficiency over 50 years)
total_electricity_kWh = 0.15 * 3600 * 24 * 365 * swiss_egs_lca["plant_lifetime_years"]

# Energy intensity of drilling
drilling_energy_kWh = swiss_egs_lca["drilling_energy_total_kWh"]
per_kWh_drilling_energy = drilling_energy_kWh / total_electricity_kWh

# GHG emissions (average)
ghg_min = swiss_egs_lca["ghg_emission_range_gCO2_kWh"][0]
ghg_max = swiss_egs_lca["ghg_emission_range_gCO2_kWh"][1]
ghg_avg = (ghg_min + ghg_max) / 2

print(f"Total Drilling Energy Required: {drilling_energy_kWh:,.0f} kWh")
print(f"Total Estimated Electricity Output: {total_electricity_kWh:,.2e} kWh")
print(f"Drilling Energy Intensity: {per_kWh_drilling_energy:.5f} kWh per kWh_el")
print(f"Estimated GHG Emissions: {ghg_avg:.2f} g CO2-eq/kWh")

# Store for later comparison/plotting
egs_results = {
    "Carbon Footprint": ghg_avg / 1000,  # convert to kg CO2-eq/kWh
    "Cumulative Energy Demand": per_kWh_drilling_energy,
    "Toxicity (HTP+ETP)": 0.0,  # placeholder
    "Water Footprint": 0.0,     # placeholder
    "Cost": 0.0                 # placeholder
}

# ------------------------------
# LCA Calculation Functions
# ------------------------------
def calc_cf(base_emissions, nanoparticle_emissions, gwp):
    total_emissions = np.sum([base_emissions[gas] * gwp[gas] for gas in base_emissions])
    nanoparticle_emissions_total = np.sum([nanoparticle_emissions[gas] * gwp[gas] for gas in nanoparticle_emissions])
    return total_emissions + nanoparticle_emissions_total

def calc_ced(base_energy, nanoparticle_energy):
    return np.sum(base_energy) + np.sum(nanoparticle_energy)

def calc_toxicity(base_toxicity, nanoparticle_toxicity, nanoparticle_mass_fraction):
    return base_toxicity + nanoparticle_toxicity * nanoparticle_mass_fraction

def calc_wf(base_water, nanoparticle_water, nanoparticle_mass_fraction):
    return np.sum(base_water) + np.sum(nanoparticle_water) * nanoparticle_mass_fraction

def calc_cost(base_cost, nanoparticle_cost, nanoparticle_mass_fraction):
    return base_cost + nanoparticle_cost * nanoparticle_mass_fraction

# ------------------------------
# User Inputs (Nanoparticles)
# ------------------------------
def get_user_input():
    print("Enter the nanoparticle properties for your nanofluid:\n")

    nanoparticle_name = input("Enter nanoparticle name (e.g., Ag, ZnO, TiO2, SiO2, CuO, Al2O3, TiO2-SiC): ")
    nanoparticle_mass_fraction = float(input(f"Enter mass fraction of {nanoparticle_name} in nanofluid (0 - 1): "))

    if nanoparticle_name not in nanoparticles:
        print(f"Nanoparticle {nanoparticle_name} is not in the database. Please provide values manually.\n")
        nanoparticle_emissions = {
            "CO2": float(input(f"Enter CO2 emissions for {nanoparticle_name} (kg CO2/kg nanoparticle): ")),
            "CH4": float(input(f"Enter CH4 emissions for {nanoparticle_name} (kg CH4/kg nanoparticle): "))
        }
        nanoparticle_toxicity = float(input(f"Enter toxicity factor for {nanoparticle_name} (CTUh/e): "))
        nanoparticle_energy = [float(input(f"Enter energy usage (MJ) for {nanoparticle_name} (enter 2 values for lower and upper bounds): ")) for _ in range(2)]
        nanoparticle_water = [float(input(f"Enter water usage (m³) for {nanoparticle_name} (enter 2 values for lower and upper bounds): ")) for _ in range(2)]
        nanoparticle_cost = float(input(f"Enter cost of {nanoparticle_name} ($/kg): "))
    else:
        nanoparticle_emissions = nanoparticles[nanoparticle_name]["emissions"]
        nanoparticle_toxicity = nanoparticles[nanoparticle_name]["toxicity"]
        nanoparticle_energy = nanoparticles[nanoparticle_name]["energy_use"]
        nanoparticle_water = nanoparticles[nanoparticle_name]["water_use"]
        nanoparticle_cost = nanoparticles[nanoparticle_name]["cost_per_kg"]

    return nanoparticle_name, nanoparticle_mass_fraction, nanoparticle_emissions, nanoparticle_toxicity, nanoparticle_energy, nanoparticle_water, nanoparticle_cost

# ------------------------------
# Perform LCA and Display Results
# ------------------------------
def perform_lca():
    nanoparticle_name, nanoparticle_mass_fraction, nanoparticle_emissions, nanoparticle_toxicity, nanoparticle_energy, nanoparticle_water, nanoparticle_cost = get_user_input()

    GWP = {"CO2": 1.0, "CH4": 28.0}

    cf = calc_cf(water_properties["emissions"], nanoparticle_emissions, GWP)
    ced = calc_ced(water_properties["energy_use"], nanoparticle_energy)
    toxicity = calc_toxicity(water_properties["toxicity_factors"].get(nanoparticle_name, 0), nanoparticle_toxicity, nanoparticle_mass_fraction)
    wf = calc_wf(water_properties["water_use"], nanoparticle_water, nanoparticle_mass_fraction)
    cost = calc_cost(0.001, nanoparticle_cost, nanoparticle_mass_fraction)

    print("\n--- LCA Report for Nanofluid with", nanoparticle_name, "---")
    print(f"Carbon Footprint of the Nanofluid: {cf:.2e} kg CO2-eq/kg")
    print(f"Cumulative Energy Demand: {ced:.2f} MJ/kg")
    print(f"Toxicity (HTP+ETP): {toxicity:.2e} CTUh/e")
    print(f"Water Footprint: {wf:.4f} m³/kg")
    print(f"Cost of the Nanofluid: ${cost:.4f} per kg")

    results = {"Carbon Footprint": cf, "Cumulative Energy Demand": ced, "Toxicity (HTP+ETP)": toxicity, "Water Footprint": wf, "Cost": cost}
    
    # Global results
    global global_results
    global_results = results

    plt.bar(results.keys(), results.values(), color='royalblue')
    plt.ylabel('Values')
    plt.title(f'LCA of Nanofluid with {nanoparticle_name}')
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

# ------------------------------
# Compare Nanofluid vs EGS Baseline (Bar Chart)
# ------------------------------
if __name__ == "__main__":
    # Perform LCA
    perform_lca()

    # Compare Nanofluid vs EGS Baseline (Bar Chart)
    comparison_labels = list(global_results.keys())
    nanofluid_values = list(global_results.values())
    egs_values = [egs_results[label] for label in comparison_labels]

    x = np.arange(len(comparison_labels))
    width = 0.4

    plt.figure(figsize=(12, 7))
    plt.bar(x - width/2, nanofluid_values, width, label='Nanofluid', color='skyblue')
    plt.bar(x + width/2, egs_values, width, label='EGS Baseline (Swiss)', color='orange')

    plt.ylabel('Impact Value', fontsize=12)
    plt.title(f'LCA Comparison: Nanofluid vs Swiss EGS (3.5 km, 50 years)', fontsize=14)
    plt.xticks(x, comparison_labels, rotation=45, ha='right', fontsize=10)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()
