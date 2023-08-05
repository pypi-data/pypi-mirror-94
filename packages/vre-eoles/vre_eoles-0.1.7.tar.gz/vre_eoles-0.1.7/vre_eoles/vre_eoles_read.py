__all__ = [
    "read_LF_CIRED",
    "read_parc_eolien",
    "read_rte",
    "read_parc_solaire",
    "read_wind_power_power_curve",
    "read_LF_onshore",
    "read_vwf_power_curves",
]


def read_LF_CIRED(year, technic, directory_inputs):
    """
    reading of  an excel EOLES file
    
    Args:
    year (int): year must be in [2006,2012,...,2017]
        
    Returns:
        fe (dataframe): {year:nominal_pwer(GW)}
    """

    # Standard library import
    from pathlib import Path
    import datetime

    # 3rd party import
    import pandas as pd

    fe = pd.read_csv(
        directory_inputs / Path("vre_profiles" + str(year) + ".csv"), header=None
    )
    deb = datetime.datetime(year, 1, 1)
    fe.rename(columns={0: "Technic", 1: "Hour", 2: str(year)}, inplace=True)
    fe.query("Technic==@technic", inplace=True)
    fe.index = [deb + datetime.timedelta(hours=i) for i in range(len(fe))]
    fe.drop(["Technic", "Hour"], axis=1, inplace=True)

    return fe


def read_parc_eolien():

    """
    reading of  an excel RTE file downloaded from:
    https://www.statistiques.developpement-durable.gouv.fr/publicationweb/262
    
    Args:
        
    Returns:
        Pow_eol (dict): {year:nominal_pwer(GW)}
    """

    # Standard library import
    from pathlib import Path
    import os

    # 3rd party import
    import pandas as pd

    directory_eol = Path.home() / Path("CIRED-ENS")
    path = directory_eol / Path("Évolution du parc éolien.csv")

    Pow_eol = pd.read_csv(
        path, sep=";", parse_dates=["Date"], usecols=["Date", "Terrestre"]
    )
    Pow_eol.set_index("Date", inplace=True)
    Pow_eol = Pow_eol.dropna()
    Pow_eol = Pow_eol.resample("Y").mean()
    Pow_eol.index = Pow_eol.index.year
    Pow_eol = Pow_eol["Terrestre"].to_dict()

    return Pow_eol


def read_rte(year):
    """
    reading of  an excel RTE file downloaded from https://www.rte-france.com/eco2mix/telecharger-les-indicateurs
    Unzip the file and remame then yyyy.xlsx where yyyy stands for the 4 digits of the year.
    
    Args:
        year (int) : year of the RTE excel file to be read
    Returns:
        B (dataframe): datafame of the RTE file
    """

    # Standard library import
    from pathlib import Path
    import os

    # 3rd party import
    import pandas as pd

    directory_rte = Path.home() / Path("FRENCH_STAT/RTE_DATA")
    path = directory_rte / Path(str(year) + ".xlsx")

    A = pd.read_excel(
        path,
        skipfooter=1,  # skip the last line which is a comment
        parse_dates=[
            ["Date", "Heures"]
        ],  # concanenate columns Date and Heures as TimeStamp
        usecols="c:E,H:Q",
    )  # select columns
    A.drop([i for i in list(A.index)[1::2]], inplace=True)  # drop irrelevent rows
    index_ = [
        x for i, x in enumerate(A["Date_Heures"]) if i % 2 == 0
    ]  # resample every hour and convert in energy
    A.drop(columns=["Date_Heures"], inplace=True)
    B = A.groupby(A.index // 4).mean()
    B["Date_Heures"] = index_
    B.set_index("Date_Heures", inplace=True)
    return B


def read_parc_solaire():

    """
    WEB scrapping ot the wiki page : https://fr.wikipedia.org/wiki/%C3%89nergie_solaire_en_France and extract
    the table : Puissance photovoltaïque par région (MW)
    Valid 30/12/2020
    
    Args:
        
    Returns:
        Pow_sol (dict): {year:nominal_pwer(MW)}
    """

    # 3rd party imports
    import pandas as pd

    url = "https://fr.wikipedia.org/wiki/%C3%89nergie_solaire_en_France"

    tables = pd.read_html(url, header=0)

    headings = set(
        [
            "Région",
            "2008",
            "2009",
            "2010",
            "2011",
            "2012",
            "2013",
            "2014",
            "2015",
            "2016",
            "2017",
            "2018",
        ]
    )  # must be updated with wiki upgrade

    for (
        table
    ) in tables:  # find the table named "Puissance photovoltaïque par région (MW)"
        if set(table.columns.values) == headings:
            break

    Pow_sol = table.query('Région=="Total France"').to_dict("records")[0]
    del Pow_sol["Région"]
    Pow_sol = {
        int(key): int(str(value).replace("\xa0", "")) for key, value in Pow_sol.items()
    }  # data cleaning
    Pow_sol[2012] = 3727
    Pow_sol[2013] = 4366
    Pow_sol[
        2019
    ] = 9900  # https://www.statistiques.developpement-durable.gouv.fr/tableau-de-bord-solaire-photovoltaique-quatrieme-trimestre-2019
    return Pow_sol


def read_LF_onshore(year, directory_inputs):
    """
    reading of  an excel EOLES file
    
    Args:
        year (int): year must be in [2006,2012,...,2017]
        directory_inputs (string): directory containing the vre_path_profiles
        
    Returns:
        Pow_eol (dict): {year:nominal_pwer(GW)}
    """

    # Standard library imports
    from pathlib import Path
    import datetime

    # 3rd party imports
    import pandas as pd

    fe = pd.read_csv(
        directory_inputs / Path("vre_profiles" + str(year) + ".csv"), header=None
    )
    deb = datetime.datetime(2006, 1, 1)
    temps = [deb + datetime.timedelta(hours=i) for i in range(int(len(fe) / 3))]
    fe.rename(columns={0: "Technic", 1: "Hour", 2: str(year)}, inplace=True)
    fe.query('Technic=="onshore"', inplace=True)
    fe.index = temps
    fe.drop(["Technic", "Hour"], axis=1, inplace=True)

    return fe

def read_vwf_power_curves(root_inputs_vwf):

    # Standard library imports
    from pathlib import Path

    # 3rd party imports
    import pandas as pd

    Power_cuve00 = pd.read_csv(root_inputs_vwf / Path('Wind Turbine Power Curves ~ 5 (0.01ms with 0.00 w smoother).csv'),
                           index_col="speed")
    Power_cuve01 = pd.read_csv(root_inputs_vwf / Path('Wind Turbine Power Curves ~ 5 (0.01ms with 0.10 w smoother).csv'),
                           index_col="data$speed")
    Power_cuve02 = pd.read_csv(root_inputs_vwf / Path('Wind Turbine Power Curves ~ 5 (0.01ms with 0.20 w smoother).csv'),
                           index_col="data$speed")
    Power_cuve03 = pd.read_csv(root_inputs_vwf / Path('Wind Turbine Power Curves ~ 5 (0.01ms with 0.30 w smoother).csv'),
                           index_col="data$speed")
    Power_cuve04 = pd.read_csv(root_inputs_vwf / Path('Wind Turbine Power Curves ~ 5 (0.01ms with 0.40 w smoother).csv'),
                           index_col="data$speed")
                           
    return Power_cuve00, Power_cuve01, Power_cuve02, Power_cuve03, Power_cuve04
    
def read_wind_power_power_curve(constructor, turbine_type, file):

    """Returns the power curve of the WindPower Power_curves_20201224.xls database
    interpolated from 0 to 35 m/s with a step of 0.01 m/s. (vwf convention)
    
    Args:
        constructor (string): turbine manufacturer (ex: "Vestas")
        turbine_type (string): turbine model (ex:"V90/2000") 
        file (string): full path of the file Power_curves_20201224.xls
        
    Returns:
        wind_speed_interp (nparray): wind speed [0, 0.01, 0.02,...,35] in m/s
        pow_interp (nparray): turbine power at wind_speed_interp values
    """

    # Standard library imports
    from pathlib import Path
    
    # 3rd party import
    import pandas as pd
    import numpy as np
    from scipy.interpolate import interp1d

    dwp = pd.read_excel(file, sheet_name="Power_curves")
    rep = dwp.query(
        "(`Manufucturer Name`==@constructor) & (`Turbine Name`==@turbine_type)"
    )
    wind_speed = np.array(dwp.iloc[0][4:-2]).astype(float)
    power = np.array(rep.iloc[0][4:-2]).astype(float)

    #  interpolation
    wind_speed_interp = np.arange(0, 35.01, 0.01)
    f = interp1d(wind_speed, power, kind="linear")
    pow_interp = f(wind_speed_interp)

    return wind_speed_interp, pow_interp