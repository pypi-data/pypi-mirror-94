NetCDF extraction util
----------------------

This is a simple script to extract time-series from a NetCDF file to a Comma Separated Value (CSV) file.

To use:

    netcdf_extraction_util <input_netcdf_file> <selected_reach>

This will produce a <selected_reach>.csv file with columns date and flow for the selected reach. If the
reach does not exist on <input_netcdf_file>, the script will error and show you the available reaches.


