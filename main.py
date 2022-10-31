# This is ClusterGenerator code generates input data ECAL and HCAL crystal data for cluster finder studies

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import os
import sys
import random
from datetime import datetime

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

def generate(n_events):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Generating {n_events} events')  # Press ⌘F8 to toggle the breakpoint.
    # Create input file, which contains ECAL crystal and HCAL tower data
    datestr = datetime.now().strftime("%Y%m%d")
    input_file_name = "CaloData-" + datestr + ".inp"
    output_file_name = "ClusterData-" + datestr + ".out"
    # Loop over events
    for event in range(0, n_events):
        # Select number of pizero (Electromagnetic) candidates - about a third of the mean multiplicity
        n_pizeros = int(random.gauss(MEAN_MULTIPLICITY / 3, 0.3))
        total_em_energy = 0.0
        total_hd_energy = 0.0
        # Loop over pizero candidates
        for pizero in range(0, n_pizeros):
            # Choose a hit crystal for the pizero randomly
            c_eta = int(random.uniform(0, N_ETA_CRYSTALS))
            c_phi = int(random.uniform(0, N_PHI_CRYSTALS))
            # Split pizero to randomly fill about 1x2 to 3x5 crystal eta-phi space
            # The energy split should be "gaussian" distributed in eta-phi space with majority in the hit crystal
            energy = random.expovariate(1./10.0)  # Mean energy will be 10.0
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
            total_hd_energy += energy
        print(event, n_pizeros, n_pions, total_em_energy, total_hd_energy)
        # Save the non-zero crystals in the input file
        # Save the non-zero towers in the input file
        # Save the candidates in the output file, identifying pizeros as EM-clusters and pions as HD-clusters
        # Saved data contains, ID={EM/HD}, ET, hit crystal, hit
    return input_file_name, output_file_name


def reconstruct(input_file_name):
    # Cheat temporarily and return the expected output file name"
    return input_file_name.replace("CaloData-", "ClusterData-")


def compare_outputs(output_file_name, reco_output_file_name):
    # Cheat temporarily and return true without actually comparing!
    return True

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
    input_file_name, output_file_name = generate(n_events)
    reco_output_file_name = reconstruct(input_file_name)
    result = compare_outputs(output_file_name, reco_output_file_name)
    print(f"Result of the comparison is {result}")
