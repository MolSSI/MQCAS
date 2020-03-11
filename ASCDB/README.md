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

* The benchmark level of theory is heterogeneous and includes CCSD(T) and CASPT2. See issue #1.

## Manifest

* `add_dataset.py` adds the dataset to a Fractal server.
* `ASCDB.csv` contains the data.