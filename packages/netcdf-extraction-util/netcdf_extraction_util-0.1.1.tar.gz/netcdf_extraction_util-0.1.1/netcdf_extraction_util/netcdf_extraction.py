import xarray as xr
import numpy as np


def extract_from_netcdf(input_nc: str, reach_id: str):
    """
    Extract the data for a reach from the input NetCDF file. The result will be written as CSV as
    reach_id.csv.

    :param input_nc: name of the NetCDF file (from NZWaM output)
    :param reach_id: ID of the reach to extract
    :return: None
    """
    output_file_csv = "{}.csv".format(reach_id)
    DS = xr.open_dataset(input_nc)
    # TODO: this is hardcoded to work with NZWaM output
    variable_name = "mod_streamq"
    # See if we have that reach
    reach_location = DS.rchid.values == reach_id
    if (~reach_location).all():
        print("Reach not found, try an existing reach on the input file from: ", DS.rchid.values)
        exit(1)

    index_rch = np.argmax(DS.rchid.values == reach_id)
    print("Reach found...")
    # TODO: the dimensions of the variable are hardcoded for NZWaM output
    values = DS[variable_name][:, index_rch, 0, 0].to_dataframe()
    # Cleaning the column names
    values.rename(columns={"time": "date", variable_name: "flow"}, inplace=True)

    values.to_csv(output_file_csv)
    print("Writing file {}".format(output_file_csv))


