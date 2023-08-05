__all__ = [
    "request_vwf_wind",
    "vwf_api",
]


"""
Tranlation of the WinPower turbine names to the ninja ones .

"""

wp2wvf = {
    "Acciona AW-1500 77": "Acciona AW77 1500",  # ok
    "Alstom Power 110": "Alstom Eco 110",  # ok
    "Ecotecnia 80 1.6": "Alstom Eco 80",  # nok
    "Enercon E48 800": "Enercon E48 800",  # ok
    "Enercon E70 2000": "Enercon E70 2000",  # ok
    "Enercon E70 2300": "Enercon E70 2300",  # ok
    "Enercon E82 2000": "Enercon E82 2300",  # nok
    "Enercon E82 2300": "Enercon E82 2300",  # ok
    "Fuhrländer FL 2500 100": "Nordex N100 2500",  # ok
    "Fuhrländer FL 2500 90": "Nordex N80 2500",  # ok
    "GE Energy 1.5s": "GE 1.5sl",  # nok
    "Gamesa G80 2000": "Gamesa G80 2000",  # ok
    "Gamesa G90 2000": "Gamesa G90 2000",  # ok
    "Leitwind LTW77-1500": "Acciona AW77 1500",  # ok
    "Nordex N100 2500": "Nordex N100 2500",  # ok
    "Nordex N80 2500": "Nordex N80 2500",  # ok
    "Nordex N90 2300": "Nordex N90 2300",  # ok
    "Nordex N90 2500": "Nordex N90 2500",  # ok
    "Repower MM70": "REpower MM70 2000",  # ok
    "Repower MM82": "REpower MM82 2000",  # ok
    "Repower MM92": "REpower MM92 2000",  # ok
    "Senvion MM82 2050": "REpower MM82 2000",  # nok
    "Senvion MM92 2050": "REpower MM92 2000",  # nok
    "Siemens SWT-2.3-93": "Siemens SWT 2.3 101",  # nok
    "Siemens SWT-3.0-101": "Siemens SWT 3.0 101",  # ok
    "Vestas V100 1800": "Vestas V100 1800",  # ok
    "Vestas V100 2000": "Vestas V100 2000",  # ok
    "Vestas V112 3000": "Vestas V112 3000",  # ok
    "Vestas V52 850": "Vestas V52 850",  # ok
    "Vestas V66 1750": "Vestas V66 1750",  # ok
    "Vestas V80 2000": "Vestas V80 2000",  # ok
    "Vestas V90 2000": "Vestas V80 2000",  # nok
    "Vestas V90 3000": "Vestas V90 3000",  # ok
    "Winwind WWD-1-64": "Vestas V52 850",  # nok
    "Nordex N117 2400": "Nordex N90 2500",  # ok
    "Gamesa G97 2000": "Gamesa G90 2000",  # nok
    "Enercon E101 3050": "Enercon E101 3000",  # nok
    "Enercon E92 2350": "Enercon E92 2350",  # ok
    "Vestas V112 3300": "Vestas V112 3300",  # ok
    "GE Energy 2.75-100": "GE 2.75 103",  # nok
    "Vestas V110 2000": "Vestas V100 2000",  # ok
    "Vestas V117 3300": "Vestas V112 3300",  # ok
    "Senvion MM100": "REpower MM70 2000",  # ok
    "Vestas V126 3300": "Vestas V112 3300",  # ok
    "Enercon E82 2350": "Enercon E92 2350",  # ok
    "Enercon E115 3000": "Enercon E101 3000",  # ok
    "Enercon E103 2350": "Enercon E92 2350",  # ok
    "Siemens SWT-3.0-113": "Siemens SWT 3.0 101",  # ok
    "Senvion 3.0M122": "Vestas V112 3000",  # nok
    "Siemens SWT-3.2-113": "Siemens SWT 3.6 107",  # ok
    "Nordex N117 3000": "Nordex N131 3000",  # ok
    "Vestas V100 2200": "Vestas V100 2000",  # ok
    "Senvion 3.4M122 NES": "Vestas V112 3300",  # ok
    "Enercon E82 3000": "Enercon E82 3000",  # ok
    "Nordex #ND": "Nordex N131 3000",  # ok
    "Vestas V105 3600": "Vestas V112 3300",  # ok
    "Vestas V112 3450": "Vestas V112 3300",  # nok
    "Nordex N131": "Nordex N131 3000",  # ok
    "Vestas V126 3450": "Vestas V112 3300",  # nok
    "Vestas V136 3450": "Vestas V112 3300",  # nok
    "Vestas V117 3450": "Vestas V112 3300",  # nok
    "Ecotecnia 100": "Enercon E101 3000",  # nok
    "GE Energy 2.5xl": "Nordex N90 2500",  # nok
    "Goldwind S50 750": "Goldwind GW82 1500",  # nok
    "GE Energy 1.5sl": "GE 1.5sl",  # ok
    "Gamesa G114 2000": "Gamesa G90 2000",  # nok
    "DDIS DDIS60": "Enercon E48 800",  # nok
    "Enercon E53 800": "Enercon E53 800",  # ok
    "Enercon E82 2050": "Enercon E82 1800",  # nok
    "Siemens SWT-1.3-62": "Siemens SWT 1.3 62",  # ok
    "Bonus B62 1300": "Bonus B62 1300",  # ok
    "Enercon E66 2000": "Enercon E66 2000",  # ok
    "Nordex N60 1300": "Nordex N60 1300",  # ok
    "Repower MD77": "REPower MD77 1500",  # ok
    "WES WES250": "Vestas V29 225",  # nok
    "Winwind WWD-3-103": "Enercon E101 3000",
    "Siemens SWT-4.0-130": "Siemens SWT 4.0 130",
}


def request_vwf_wind(args, token):

    '''
    send a request to ninja api
    
    Args
        args (dict): {"lat":Latitude
                      "lon"]:Longitude
                      "date_from": yyyy-mm-dd
                      "date_to": yyyy-mm-dd
                      "raw": "true"
                      "capacity":1.0
                      "height": hub height
                      "turbine": turbine type
                      "format": "json"
                      
        token (string) : your ninja API token
    
    returns:
        data (dataframe): date| wind speed [ FC
        
        metadata (dataframe): conains the args values
        
        status (boolean): True theexchangz with ninja has been successfull False otherwise
        
    '''

    # Standard library imports
    import requests
    import json as json

    # 3rd party import
    import pandas as pd

    
    api_base = "https://www.renewables.ninja/api/"

    data = None
    metadata = None
    status = True

    s = requests.session()

    # Send token header with each request
    s.headers = {"Authorization": "Token " + token}
    url = api_base + "data/wind"

    r = s.get(url, params=args)

    try:
        parsed_response = json.loads(r.text)
        data = pd.read_json(json.dumps(parsed_response["data"]), orient="index")
        metadata = parsed_response["metadata"]
    except:
        status = False

    return data, metadata, status


def vwf_api(df, year, root_outputs, token, median_hub_height=80, EOLES=False):
    """
    This function automates the access to  ninja via its API taking into account ninja access restrition:

        - Anonymous users are limited to a maximum of 5 requests per day.

        - To increase this limit to 50 per hour, please register for a free user account.

        - In addition to the hourly limit, there is a burst limit, currently set to 6/minute for both anonymous and registered users, to prevent a fast succession of individual requests overloading the server.

        - If you need a higher limit, e.g. for automated access via the API, please contact ninja webmaster.

    Arguments:
        df (dataframe): index Insee county code|Latitude (°)|Longitue (°)|Total power (kW)|Manufacture|Model|Hub height (m)
        year (int): year of the analysis
        
        root_outputs (path): path of outputs directory
        
        token (string): your ninja API token (see https://www.renewables.ninja/profile )
        
        median_hub_height (real): height to be used if the hub height is unknown
        
    Returns:
        files: stored in root_outputs as:
            ##.xlsx where ## stands for the county Insee code with Timedate|electricity|wind_speed|
            ##_metadata.xls is the metadata returns by the ninja api

    """

    # Standard library imports
    import os
    import re
    import time
    from pathlib import Path
    
    # 3rd party imports
    import vre_eoles as vre
    import pandas as pd

    test = False

    def turbine_name(county,):

        try:
            turbine_type = (
                df.loc[county, "Manufacturer"]
                + " "
                + str(df.loc[county, "Model"].replace("/", " "))
            )
        except:
            turbine_type = (
                df.loc[county, "Manufacturer"] + " " + str(df.loc[county, "Model"])
            )
        turbine_name = wp2wvf[turbine_type]

        return turbine_name

    # build the list of existing file name ##.xlsx ## is county identifier
    files = []
    for file in os.listdir(root_outputs):
        sub_str = re.findall("\d{1,3}.xlsx", file)
        if len(sub_str):
            files.append(sub_str[0])

    turbine_type = []
    list_args = {}

    idx = 0
    for county in df.index:
        if idx == 49:
            break  # to comply with the request hour limit
        args = {}  # dict to provide to the ninja API

        args["lat"] = df.loc[county, "Latitude"]
        args["lon"] = df.loc[county, "Longitude"]
        args["date_from"] = str(year) + "-01-01"
        args["date_to"] = str(year) + "-12-31"
        args["raw"] = "true"
        args["capacity"] = 1.0
        if EOLES:
            args["height"] = 80
            args["turbine"] = "Vestas V90 2000"
        else:
            height = df.loc[county, "Hub height"]
            if height == "#ND":
                height = median_hub_height  # if the height is unknown we take the median value
            # of the known heights
            args["height"] = height
            args["turbine"] = turbine_name(county)
        args["format"] = "json"
        list_args[county] = args

        if (not test) & (not (county + ".xlsx" in files)):
            print(county + ".xlsx", end=" ", flush=True)
            idx += 1
            data, metadata, status = request_vwf_wind(args, token)
            if (
                status
            ):  # if the request succeeds we save the results into two excel files
                data.to_excel(root_outputs / Path(str(county) + ".xlsx"))
                meta_data = pd.DataFrame.from_dict(metadata).T
                meta_data.to_excel(root_outputs / Path(str(county) + "_metadata.xlsx"))
            else:
                print("ERREUR :", county)
            time.sleep(11)  # to comply with the burst limit
