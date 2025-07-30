# for convenience, a copy of the 1.0 data is included in this repository
# path is relative to the notebook file
data_path = "../data/"

# chart directory, relative to notebook file
chart_dir = "../charts"

# To run against latest pgp metadata, load by URL from pgp-metadata repo
# data_path = "https://github.com/princetongenizalab/pgp-metadata/raw/main/data/"
pgp_csv_paths = {
    "documents": f"{data_path}documents.csv",
    "fragments": f"{data_path}fragments.csv",
    "sources": f"{data_path}sources.csv",
    "footnotes": f"{data_path}footnotes.csv",
    "people": f"{data_path}people.csv",
    "places": f"{data_path}places.csv",
}
