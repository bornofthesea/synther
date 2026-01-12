import pandas as pd
import os
from pathlib import Path

# Load data
stellar_data = pd.read_csv("abundances.csv")

# Create output directory
os.makedirs("com", exist_ok=True)

TEMPLATE = """#!/bin/csh -f
date

#Parametres

foreach BLABLA (\\
mod-smc-{star_name}.asc\\
)

set Etoile     = '{star_name}'
set deltalam   = '0.02'
set MODEL      = ${{BLABLA}}
set PARAMETERFILE = 'parameter.dat'
set METALLIC   = '{fe_h}'
set TURBVEL    = '{vmicro}'

set Fe_ab = {Fe_ab}

set lam_min    = '{lam_min}'
set lam_max    = '{lam_max}'
set SUFFIX     = _${{lam_min}}-${{lam_max}}.spec
set result     = {star_name}x{file_suffix}.spec

#Abonds
{abundance_blocks}

#######################################################################

# TO CREATE THE OPACITY
source BabsmaMaster

# TO RUN THE MODEL
../exec-gf-v19.1/bsyn_lu <<EOF
'LAMBDA_MIN:'     '${{lam_min}}'
'LAMBDA_MAX:'     '${{lam_max}}'
'LAMBDA_STEP:'    '${{deltalam}}'
'INTENSITY/FLUX:' 'Flux'
'COS(THETA)    :' '1.00'
'ABFIND        :' '.false.'
'MODELOPAC:' 'contopac/${{MODEL}}opac'
'RESULTFILE :' 'syntspec/${{result}}'
'METALLICITY:'    '${{METALLIC}}'
'ALPHA/Fe   :'    '0.40'
'HELIUM     :'    '0.00'
'R-PROCESS  :'    '0.00'
'S-PROCESS  :'    '0.00'
'INDIVIDUAL ABUNDANCES:'   '63'
4  $Be_ab
6  $C_ab
7  $N_ab
8  $O_ab
11 $Na_ab
12 $Mg_ab
13 $Al_ab
14 $Si_ab
15 $P_ab
16 $S_ab
19 $K_ab
20 $Ca_ab
21 $Sc_ab
22 $Ti_ab
23 $V_ab
24 $Cr_ab
25 $Mn_ab
26 $Fe_ab
27 $Co_ab
28 $Ni_ab
29 $Cu_ab
30 $Zn_ab
32 $Ge_ab
33 $As_ab
34 $Se_ab
38 $Sr_ab
39 $Y_ab
40 $Zr_ab
41 $Nb_ab
42 $Mo_ab
44 $Ru_ab
45 $Rh_ab
46 $Pd_ab
47 $Ag_ab
48 $Cd_ab
50 $Sn_ab
56 $Ba_ab
57 $La_ab
58 $Ce_ab
59 $Pr_ab
60 $Nd_ab
62 $Sm_ab
63 $Eu_ab
64 $Gd_ab
65 $Tb_ab
66 $Dy_ab
67 $Ho_ab
68 $Er_ab
69 $Tm_ab
70 $Yb_ab
71 $Lu_ab
72 $Hf_ab
73 $Ta_ab
74 $W_ab
75 $Re_ab
76 $Os_ab
77 $Ir_ab
78 $Pt_ab
79 $Au_ab
82 $Pb_ab
83 $Bi_ab
90 $Th_ab
92 $U_ab

'ISOTOPES : ' '5'
6.012 0.925
6.013 0.025
8.016 0.925
8.017 0.020
8.018 0.005
'NFILES   :' '10'
linelists/atomsMasseron.dat
linelists/12C12C_15000-17500_P-BR.bsyn
linelists/12C13C_15000-17500_P-BR.bsyn
linelists/turbomolec-20180901_woC2-0607.012014CN
linelists/hitran.combined.acm.eav.ME4957.OH-IR.bsyn
linelists/12C16O_Hitran.bsyn
linelists/12C17O_Hitran.bsyn
linelists/12C18O_Hitran.bsyn
linelists/13C16O_Hitran.bsyn
linelists/Hlinedata
'SPHERICAL:'  'F'
  30
  300.00
  15
  1.30
EOF
########################################################################
date
end
"""

# Wavelength ranges for each suffix
wavelength_ranges = {
    "a": (15600, 16800),
    "b": (15000, 16000),
}

for _, star in stellar_data.iterrows():
    star_name = star["Name"]
    fe_h = star["FE_H"]
    vmicro = star["VMICRO"]
    
    # Get required abundances
    Fe_ab = star["Fe_ab"]
    C_ab = star["C_ab"]
    N_ab = star["N_ab"]
    O_ab = star["O_ab"]
    Mg_ab = star["Mg_ab"]
    
    # Generate abundance blocks (foreach loops)
    abundance_blocks = []
    for col in stellar_data.columns:
        if col.endswith("_ab"):
            value = star[col]
            abundance_blocks.append(f"foreach {col} ({value})")
    
    for suffix, (lam_min, lam_max) in wavelength_ranges.items():
        file_content = TEMPLATE.format(
            star_name=star_name,
            fe_h=fe_h,
            vmicro=vmicro,
            Fe_ab=Fe_ab,
            C_ab=C_ab,
            N_ab=N_ab,
            O_ab=O_ab,
            Mg_ab=Mg_ab,
            abundance_blocks="\n".join(abundance_blocks),
            lam_min=lam_min,
            lam_max=lam_max,
            file_suffix=suffix,
        )
        
        filename = f"com/APO{star_name}{suffix}.com"
        with open(filename, "w") as f:
            f.write(file_content)
        
        print(f"Generated: {filename}")