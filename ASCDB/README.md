# ASCDB

## General Information

* Date: c. 3/11/2020
* Purpose: Microcosm of the ACCDB benchmark set
* Collection: ReactionDataset
* Name: ASCDB
* Number of Entries: 200
* Submitter: Pierpaolo Morgante (GH: PierMorgante)

## Generation Pipeline

1. Get the geometries: `git clone https://github.com/peverati/ACCDB.git`
2. Run `add_dataset.py`

## Notes

* Ref: P. Morgante, R. Peverati, "Statistically representative databases for density functional theory via data science", Phys. Chem. Chem. Phys. 2019, 21(35), 19092–19103. DOI:10.1039/C9CP03211H.
* The benchmark level of theory is heterogeneous and includes CCSD(T) and CASPT2. See issue #1.

## Manifest

* `add_dataset.py` adds the dataset to a Fractal server.
* `ASCDB.csv` contains the data.