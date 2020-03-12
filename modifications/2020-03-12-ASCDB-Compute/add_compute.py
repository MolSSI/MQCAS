import qcfractal.interface as ptl
import itertools
import qcengine
from tqdm import tqdm

client = ptl.FractalClient.from_file()


def is_semiempirical(method):
    return method.lower() in {"hf-3c", "pbe-3c", "pm6", "xtb"}


bases = ["sto-3g", "def2-svp", "def2-tzvp", "aug-cc-pvdz", "aug-cc-pvtz"]
methods = [
    "hf-3c",
    "pbe-3c",
    "hf",
    "b3lyp",
    "b2plyp",
    "pbe",
    "m06-2x",
    "m06-l",
    "pbe0",
    "wb97",
    "wb97x",
    "scan",
    "mp2",
]
ed_suffixes = ["", "-d3", "-d3m", "-d3bj", "-d3mbj"]

ds = client.get_collection("ReactionDataset", "ASCDB")
for method in tqdm(methods):
    try:
        if is_semiempirical(method):
            ds.compute(
                program="psi4", method=method, basis=None, tag="molssi_small",
            )
        else:
            for basis, ed_suffix in itertools.product(bases, ed_suffixes):
                d3method = method + ed_suffix
                if ed_suffix != "":
                    try:
                        qcengine.programs.empirical_dispersion_resources.from_arrays(
                            d3method
                        )
                    except qcengine.exceptions.InputError:
                        continue
                if basis == "sto-3g":
                    tag = "molssi_small"
                elif basis in {"def2-svp", "aug-cc-pvdz"}:
                    tag = "molssi_medium"
                else:
                    tag = "molssi_large"
                ds.compute(
                    program="psi4", method=d3method, basis=basis, tag=tag,
                )
    except KeyError:
        continue
