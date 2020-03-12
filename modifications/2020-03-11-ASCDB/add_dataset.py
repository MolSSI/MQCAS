#!/usr/bin/env Python # This line is needed only for unix-based systems.
# Written by Daniel Smith, Matthew Welborn, Pierpaolo Morgante.
# March 2020.
#
import qcportal as ptl
from qcfractal import FractalSnowflake
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dry-run", action="store_true")
args = parser.parse_args()

SNOWFLAKE = args.dry_run
if SNOWFLAKE:
    snowflake = FractalSnowflake()
    client = snowflake.client()
else:
    client = ptl.FractalClient.from_file()
print(client)

# The new subset you want to add.
dataset_name = "ASCDB"
# The tagline is a sentence that describes your database.
# For example, for ASCDB is
tagline = """A small database of statistically significant chemical properties ranging from transition metals
to artificial molecules coming from the three largest computational databases in the literature: MGCDB84, GMTKN55, and Minnesota 2015B"""
ds = ptl.collections.ReactionDataset(dataset_name, client=client)

# Add the paper
ds.data.metadata["citations"] = [
    ptl.models.Citation(
        bibtex="""
@article{morgante2019statistically,
  title={Statistically representative databases for density functional theory via data science},
  author={Morgante, Pierpaolo and Peverati, Roberto},
  journal={Physical Chemistry Chemical Physics},
  volume={21},
  number={35},
  pages={19092--19103},
  year={2019},
  publisher={Royal Society of Chemistry}
}
""",
        acs_citation="Morgante, P. &amp; Peverati, R. Statistically representative databases for density functional theory via data science. <em>Phys. Chem. Chem. Phys., </em><b>2019</b><i>, 21</i>, 19092-19103.",
        url="https://pubs.rsc.org/en/content/articlehtml/2019/cp/c9cp03211h",
        doi="10.1039/C9CP03211H",
    )
]

# The .csv file needed to build everything.
filename = "ASCDB.csv"
# We read the ASCDB.csv file. The encoding flag is optional,
# but necessary if the csv is generated (for example) with Microsoft Excel.
#
with open(filename, "r", encoding="utf-8-sig") as handle:
    rxns = [x.split(",") for x in handle.read().splitlines()]
# Where to find the geometry files (in .xyz)
gpath = "ACCDB/Geometries"
# We put names and reactions in the following lists:
contrib_name = []
contrib_value = []

for row in rxns:
    # Datapoint's name.
    name = row[0]
    # Datapoint's reference energy.
    energy = row[1]
    # Datapoint's reaction: from 2 to the end of the rxns list.
    rxn = row[2:]
    # This is used to handle the list.
    half = len(rxn) // 2
    molecules = rxn[:half]
    coefs = rxn[half:]
    rxn_data = []
    # This loop handles the definition of a reaction, putting together molecules
    # and stoichiometric coefficients.
    #
    for mol_name, coef in zip(molecules, coefs):
        mol = ptl.Molecule.from_file(gpath + "/" + mol_name + ".xyz")
        coef = float(coef)
        rxn_data.append((mol, coef))
    rxn = {"default": rxn_data}
    # We add the reaction to the dataset.
    ds.add_rxn(name, rxn)
    # We store the values to add in the "Contributed value" dictionary (see below).
    contrib_name.append(name)
    contrib_value.append(float(energy))
# Save the new subset.
ds.save()
#
# Adding a contributed value based on the ASCDB csv file and the molecules
# handled above.
#
contrib = {
    "name": "Benchmark",
    "theory_level": "CCSD(T), CASPT2, Experiment (see ref)",
    "values": contrib_value,
    "index": contrib_name,
    "theory_level_details": {"driver": "energy"},
    "units": "kcal / mol",
}
ds.units = "kcal/mol"
ds.set_default_benchmark("Benchmark")
ds.add_contributed_values(contrib)
ds.data.__dict__["tagline"] = tagline
ds.save()

# Test
ds = client.get_collection("ReactionDataset", dataset_name)
print(ds.list_values())
ds._ensure_contributed_values()
print(ds.get_values(native=False))
print(ds.data.metadata['citations'])
