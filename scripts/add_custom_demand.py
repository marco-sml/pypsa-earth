import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

from _helpers import configure_logging, create_logger

if __name__ == "__main__":
    if "snakemake" not in globals():
        from _helpers import mock_snakemake

        snakemake = mock_snakemake("add_custom_demand")

logger = create_logger(__name__)
configure_logging(snakemake)

# --- Load inputs ---
base_demand = pd.read_csv(snakemake.input.base_demand, index_col=0, parse_dates=True)
regions = gpd.read_file(snakemake.input.bus_regions)
add_demand_df = pd.read_csv(snakemake.input.additional_demand)

# --- Create GeoDataFrame from input CSV ---
geometry = [Point(xy) for xy in zip(add_demand_df["lon"], add_demand_df["lat"])]
additional = gpd.GeoDataFrame(add_demand_df.drop(columns=["lat", "lon"]), geometry=geometry, crs=regions.crs)

# --- Spatial join: assign each demand point to a bus region ---
matched = gpd.sjoin(additional, regions, how="left", predicate="within")

unmatched = matched[matched["name"].isnull()]
if not unmatched.empty:
    logger.warning(f"{len(unmatched)} demand point(s) could not be matched to any region.")
    logger.warning("Unmatched entries:\n" + unmatched.to_string(index=False))

# --- Prepare additional demand ---
snapshots = base_demand.index
add_matrix = pd.DataFrame(0.0, index=snapshots, columns=base_demand.columns)

# Handle static vs time-varying demand
if "demand_mw" in matched.columns:
    for _, row in matched.iterrows():
        if row["name"] in add_matrix.columns:
            add_matrix[row["name"]] += row["demand_mw"]
else:
    # time-varying demand (columns = timestamps)
    matched = matched.set_index("name").drop(columns=["index_right", "geometry"])
    matched = matched.T
    add_matrix.update(matched)

# --- Combine base + additional ---
demand_custom = base_demand.add(add_matrix, fill_value=0.0)
demand_custom.to_csv(snakemake.output.profiles)

# --- Export demand mapping ---
mapping_summary = add_matrix.sum().reset_index()
mapping_summary.columns = ["bus", "added_demand_MWh"]
mapping_summary.to_csv(snakemake.output.mapping, index=False)

logger.info("Custom demand successfully added and mapping exported.")
