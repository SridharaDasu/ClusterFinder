# This is ClusterGenerator code generates input data ECAL and HCAL crystal data for cluster finder studies

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import os
import sys
import random
from datetime import datetime
import numpy as np
from scipy import stats

MEAN_MULTIPLICITY = 9
MEAN_ET = 10
N_ETA_TOWERS = 5
N_PHI_TOWERS = 6

if "MEAN_MULTIPLICITY" in os.environ:
    N_ETA_TOWERS = os.environ["MEAN_MULTIPLICITY"]

if "N_ETA_TOWERS" in os.environ:
    N_ETA_TOWERS = os.environ["N_ETA_TOWERS"]

if "N_PHI_TOWERS" in os.environ:
    N_PHI_TOWERS = os.environ["N_PHI_TOWERS"]

N_ETA_CRYSTALS = N_ETA_TOWERS * 5
N_PHI_CRYSTALS = N_PHI_TOWERS * 5

N_TOWERS = N_ETA_TOWERS * N_PHI_TOWERS
N_CRYSTALS = N_ETA_CRYSTALS * N_PHI_CRYSTALS

def ecal_spread_selector():
    """
    Random output for selected spread space. 
    Higher Skewed data along phi direction are more likely.
    (eta_sprad, phi_spread) ---> ({1, 3}, {2, 5})
    (eta_sprad, phi_spread) is s.t. p(1, 5) > p(3, 2)

    TODO: write unittest for distribution check
    """

    # truncated normal distribution
    eta_lower, eta_upper = 1, 3.1
    phi_lower, phi_upper = 2, 5.1

    eta_mu, eta_sigma = 1, 1 #(3+1)//2 range 66%
    phi_mu, phi_sigma = 5, 1 #(5+2)//2 range 66%

    X_eta = stats.truncnorm((eta_lower - eta_mu) / eta_sigma, (eta_upper - eta_mu) / eta_sigma, loc=eta_mu, scale=eta_sigma)
    X_phi = stats.truncnorm((phi_lower - phi_mu) / phi_sigma, (phi_upper - phi_mu) / phi_sigma, loc=phi_mu, scale=phi_sigma)

    spread_eta, spread_phi = int(np.rint(X_eta.rvs())), int(np.rint(X_phi.rvs()))

    return spread_eta, spread_phi

def ecal_energy_spread(c_eta, c_phi, spread_energy):
    """
    energy split with major in and around the hit crystal (gaussian distributed)
    TODO: unittest to check index sanity
    """
    spread_eta, spread_phi = ecal_spread_selector()
    eta_indices, phi_indices = [] , []
    energy_spread = []

    #generating indices for filling space along eta
    if c_eta + spread_eta - 1 < N_ETA_CRYSTALS:
        # direct filling
        eta_indices = [x+c_eta for x in range(spread_eta)]
    else:
        # reverse order filling
        eta_indices = [x+c_eta for x in range(-spread_eta+1, 1)][::-1]
    
    #generating indices for filling space along phi
    if c_phi + spread_phi < N_PHI_CRYSTALS:
        # direct filling
        phi_indices = [x+c_phi for x in range(spread_phi)]
    else:
        # reverse order filling
        phi_indices = [x+c_phi for x in range(-spread_phi+1, 1)][::-1]
    
    # TODO: update to GD, there is 69%, 96%, ~100% distribution for GD
    gp_factor = 0.69
    for phi_idx in phi_indices:
        phi_energy = spread_energy*gp_factor
        eta_energy = phi_energy/spread_eta
        for eta_idx in eta_indices:
            # (eta, phi, energy_crytal)
            energy_spread.append((eta_idx, phi_idx, eta_energy))

        spread_energy -= spread_energy*gp_factor
        gp_factor*=0.9

    return energy_spread

def crytal_to_tower_map(c_eta, c_phi):
    # pass in crytal coordinates and returns tower coordinates
    h_eta = c_eta//N_ETA_TOWERS
    h_phi = c_phi//N_PHI_TOWERS

    return h_eta, h_phi

def hcal_spread_selector():
    # we need a static 3x3 shape
    return 3, 3

def hcal_energy_spread(h_eta, h_phi, spread_energy):
    """
    energy split with major in and around the hit tower (gaussian distributed)
    TODO: unittest to check index sanity
    """
    spread_eta, spread_phi = hcal_spread_selector()
    eta_indices, phi_indices = [] , []
    energy_spread = []

    #generating indices for filling space along eta
    if h_eta + spread_eta - 1 < N_ETA_TOWERS:
        # direct filling
        eta_indices = [x+h_eta for x in range(spread_eta)]
    else:
        # reverse order filling
        eta_indices = [x+h_eta for x in range(-spread_eta+1, 1)][::-1]
    
    #generating indices for filling space along phi
    if h_phi + spread_phi < N_PHI_TOWERS:
        # direct filling
        phi_indices = [x+h_phi for x in range(spread_phi)]
    else:
        # reverse order filling
        phi_indices = [x+h_phi for x in range(-spread_phi+1, 1)][::-1]
    
    # TODO: update to GD, there is 69%, 96%, ~100% distribution for GD
    gp_factor = 0.69
    for phi_idx in phi_indices:
        phi_energy = spread_energy*gp_factor
        eta_energy = phi_energy/spread_eta
        for eta_idx in eta_indices:
            # (eta, phi, energy_crytal)
            energy_spread.append((eta_idx, phi_idx, eta_energy))

        spread_energy -= spread_energy*gp_factor
        gp_factor*=0.9

    return energy_spread


def generate(n_events):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Generating {n_events} events')  # Press ⌘F8 to toggle the breakpoint.
    # Create input file, which contains ECAL crystal and HCAL tower data
    datestr = datetime.now().strftime("%Y%m%d")
    EM_file_name = "EMData-" + datestr + ".npy"
    HD_file_name = "HDData-" + datestr + ".npy"

    # Loop over events
    EM_data = []  # EM Data : MC Truth
    HD_data = []  # HD Data : MC Truth

    for event in range(0, n_events):
        # 25x30 Crystal Space
        event_input_data_EM = np.zeros((N_ETA_CRYSTALS, N_PHI_CRYSTALS))
        event_output_data_EM = np.zeros((N_ETA_CRYSTALS, N_PHI_CRYSTALS))

        # 5x6 Tower Space
        event_input_data_HD = np.zeros((N_ETA_TOWERS, N_PHI_TOWERS))
        event_output_data_HD = np.zeros((N_ETA_TOWERS, N_PHI_TOWERS))

        # Select number of pizero (Electromagnetic) candidates - about a third of the mean multiplicity
        n_pizeros = int(random.gauss(MEAN_MULTIPLICITY / 3, 0.3))
        total_em_energy = 0.0
        total_hd_energy = 0.0
        # Loop over pizero candidates
        for pizero in range(0, n_pizeros):
            # Choose a hit crystal for the pizero randomly
            c_eta = int(random.uniform(0, N_ETA_CRYSTALS))
            c_phi = int(random.uniform(0, N_PHI_CRYSTALS))

            energy = random.expovariate(1./10.0)
            # Split pizero to randomly fill about 1x2 to 3x5 crystal eta-phi space
            # The energy split should be "gaussian" distributed in eta-phi space with majority in the hit crystal
            energy_spread = ecal_energy_spread(c_eta, c_phi, energy)

            for energy_dist_idx in energy_spread:
                eta_idx, phi_idx, idx_energy = energy_dist_idx
                event_input_data_EM[eta_idx, phi_idx] += idx_energy
                event_output_data_EM[eta_idx, phi_idx] = 1

            total_em_energy += energy

        # Select number of charged pion (Hadronic) - about two thirds of the mean multiplicity
        n_pions = int(random.gauss(MEAN_MULTIPLICITY * 2 / 3, 0.3))
        # Loop over pion candidates
        for pion in range(0, n_pions):
            # Choose a hit crystal for the pion randomly
            c_eta = int(random.uniform(0, N_ETA_CRYSTALS))
            c_phi = int(random.uniform(0, N_PHI_CRYSTALS))
            # Deposit about 10% of the energy in the ECAL crystals as is done for the pizeros
            # Split pion to randomly fill the remaining energy in about 3x3 in HCAL tower eta-phi space
            energy = random.expovariate(1./10.0)  # Mean energy will be 10.0

            # assigning 0.1 percent energy to hit crystal in ECAL input
            em_energy = 0.1*energy
            event_input_data_EM[c_eta, c_phi] += em_energy
            total_em_energy+=em_energy

            event_output_data_EM[c_eta, c_phi] = 2

            hd_energy = 0.9*energy
            h_eta, h_phi = crytal_to_tower_map(c_eta, c_phi)
            # some code here for HCAL energy distribution
            energy_spread = hcal_energy_spread(h_eta, h_phi, energy)

            for energy_dist_idx in energy_spread:
                eta_idx, phi_idx, idx_energy = energy_dist_idx
                event_input_data_HD[eta_idx, phi_idx] += idx_energy
                event_output_data_HD[eta_idx, phi_idx] = 1

            total_hd_energy += hd_energy

        print(event, n_pizeros, n_pions, total_em_energy, total_hd_energy)

        # Saving as a 2-channel image (both input and output)
        EM_data.append(np.hstack((event_input_data_EM, event_output_data_EM)))
        HD_data.append(np.hstack((event_input_data_HD, event_output_data_HD)))

        # Save the non-zero crystals in the input file
        # Save the non-zero towers in the input file
        # Save the candidates in the output file, identifying pizeros as EM-clusters and pions as HD-clusters
        # Saved data contains, ID={EM/HD}, ET, hit crystal, hit
    
    with open(EM_file_name, 'wb') as f:
        np.save(f, np.array(EM_data))

    with open(HD_file_name, 'wb') as f:
        np.save(f, np.array(HD_data))

    return EM_file_name, HD_file_name

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    n_events = 1000
    if len(sys.argv) == 2:
        try:
            n_events = int(sys.argv[1])
        except Exception:
            print(f"Using n_events={n_events} - Error reading the argument {sys.argv[1]} as an integer.")
    elif len(sys.argv) == 1:
        print(f"Using n_events={n_events}")
    else:
        print(f"Command syntax: {sys.argv[0]} [<n_events>]")
    EM_file_name, HD_file_name = generate(n_events)
    #print(f"Result of the comparison is {result}")
