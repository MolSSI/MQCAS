import qcportal as ptl

client = ptl.FractalClient.from_file()

ds = client.get_collection("ReactionDataset", "ASCDB")
ds.data.__dict__["tagline"] = (
    "A small database of statistically significant chemical properties ranging from "
    "transition metals to artificial molecules coming from the three largest computational databases in the literature: "
    "MGCDB84, GMTKN55, and Minnesota 2015B."
)
ds.save()
