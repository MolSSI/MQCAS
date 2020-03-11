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
dataset_name = "TODO"
ds = ptl.collections.ReactionDataset(dataset_name, client=client)

# Add the paper
ds.data.metadata["citations"] = [
    ptl.models.Citation(
        bibtex="""
TODO
""",
        acs_citation="TODO",
        url="TODO",
        doi="TODO",
    )
]

# TODO list:
# 1. add entries to the dataset
# 2. add contributed values
# 3. call ds.save()
# Where to find the geometry files (in .xyz)
# We put names and reactions in the following lists: