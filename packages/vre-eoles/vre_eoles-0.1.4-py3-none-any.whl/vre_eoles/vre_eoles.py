__all__ = [
    "french_wind_turbine_analysis",
    "wind_pca",
    "plot_wind_pca",
    "vre_computation",
    "vre_aggregation",
]


def french_wind_turbine_analysis(year, root_vwf, root_county, mode="max", EOLES=False):

    """
    This routine for a selected year :
        - plots the french counties using the contours extracted from depfr-txt.zip 
        downloaded from  https://melusine.eu.org/syracuse/jms/depfr/ 
        - plots the location (red dots) of the french wind farms using the WindPower file Windfarms_France_20201220.xls
        - plots for each county the location (blue star) of the most powerful wind farm.
        - builds a dataframe df with 
        index county Insee code | Latitude |Longitude|Total power|Manufacturer|Model|Hub height|
        where Latitude, Longitude, Total power, Manufacturer, Model, Hub height are given for the largest file in the county
    
    Arguments:
        year (int): the working year
        root_vwf (path): root of the WindPower file Windfarms_France_20201220.xls
        root_county (path): root of county contours downloaded from https://melusine.eu.org/syracuse/jms/depfr/ . 
          Download depfr-txt.zip (1.23 Mo – 6 juin 2010), put the unzipped files in yout Path home/depfr-txt
        mode (string): mode = 'max' in each county we select the wind farm with the greatest power capacity
                       mode = 'min' in each county we select the wind farm with the lowest power capacity
                       mode = 'median' in each county we select the wind farm with the median power capacity
                       (default = 'max')
        EOLES (boolean) : if True we use EOLES condition hub height = 80, tubine = Vestas V80 2000
                       
    Returns:
        df (dataframe): countyInsee code|Latitude|Longitude|Total power|Manufacturer|Model|Hub height| for the french metropolitan wind farm
        median_hub_height (float): median value of the hubs height
        df_offshore (dataframe): countyInsee code|Latitude|Longitude|Total power|Manufacturer|Model|Hub height| for the french offshore wind farm
    """

    # Standard library imports
    from pathlib import Path
    import os
    import re

    os.environ["PROJ_LIB"] = str(
        Path.home() / Path("Anaconda3/pkgs/proj4-5.2.0-ha925a31_1/Library/share")
    )

    # 3rd party imports
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    import adjustText as aT
    from adjustText import adjust_text
    from mpl_toolkits.basemap import Basemap
    from matplotlib.collections import PolyCollection
    from matplotlib.patches import Polygon
    import warnings

    warnings.filterwarnings("ignore")

    def extract_year(x):
        try:
            year = x.split("/")[0]

        except:
            year = x

        return int(year)

    def lim_departement(dep):

        """
        parse the files ##-nom_departement.txt where xx is the departement identifier (ex Isère ## = 38)
        """

        v = root_county / Path(dep)
        file = open(v, "r", encoding="utf8")
        lines = file.readlines()
        file.close()

        lat = []  # list of county contor latitudes
        lon = []  # list of county contor longitudes
        for i, y in enumerate(lines[9].split(",")[0:-1]):  # skip 9 lines
            if i % 2 == 1:
                lon.append(float(y))
            elif i == 0:  # corection of a bug in the txt file
                lat.append(float(y))
            else:
                lat.append(float(y[2:]))
        x, y = m(lat, lon)
        return x, y, m(*[float(x) for x in lines[2].split(",")[0:-1]])

    # read the wind farm data file and select
    wind_farm = pd.read_excel(
        root_vwf, sheet_name="Windfarms", parse_dates=["Commissioning date"]
    )

    wind_farm.drop(0, axis=0, inplace=True)
    wind_farm_offshore = wind_farm.query(
        'Status=="Approved" &  \
                                          Area=="Offshore"'
    )
    wind_farm = wind_farm.query('`Commissioning date` != "#ND"')
    wind_farm["year"] = wind_farm["Commissioning date"].apply(extract_year)
    wind_farm = wind_farm.query("year <= @year")

    # build the dictionary d = {'county Insee code : nominal total power of the most powerfull county wind farm}
    d = {}
    gps_selected_farm = {}
    selected_farm = {}
    for (
        x
    ) in (
        wind_farm.Area.unique()
    ):  # look for all different counties equiped with wind farm

        if ("Offshore" not in x) & (
            "2B" not in x
        ):  # eliminate offshore and retain french metropolitan county

            num_county = re.findall("\d{1,3}", x)[0]

            wind_farm_county = wind_farm.query(
                '(`Total power` !="#ND") &    \
                                                ( Status == "Production") &  \
                                                (Area==@x)'
            )

            total_power = wind_farm_county["Total power"].sum()

            d[num_county] = total_power

            if int(num_county) < 96:  # select the largest county wind farm

                if mode == "max":
                    idx_pow_max = wind_farm_county["Total power"].astype(float).argmax()
                    idx_pow_index = wind_farm_county.index[idx_pow_max]
                    color_selected_farm = "b"
                elif mode == "min":
                    idx_pow_min = wind_farm_county["Total power"].astype(float).argmin()
                    idx_pow_index = wind_farm_county.index[idx_pow_min]
                    color_selected_farm = "k"
                elif mode == "median":
                    wind_farm_median_pow = np.percentile(
                        wind_farm_county["Total power"], 50, interpolation="nearest"
                    )
                    idx_pow_median = list(wind_farm_county["Total power"]).index(
                        wind_farm_median_pow
                    )
                    idx_pow_index = wind_farm_county["Total power"].index[
                        idx_pow_median
                    ]
                    color_selected_farm = "g"

                gps_selected_farm[num_county] = (
                    wind_farm_county.loc[idx_pow_index, "Latitude"],
                    wind_farm_county.loc[idx_pow_index, "Longitude"],
                )

                if EOLES:  # we choose EOLES conditions
                    selected_farm[num_county] = (
                        wind_farm_county.loc[
                            idx_pow_index, "Latitude"
                        ],  # Latitude of the largest county wind farm
                        wind_farm_county.loc[
                            idx_pow_index, "Longitude"
                        ],  # Longitude of the largest county wind farm
                        total_power,
                        "Vestas",  # Manufacturer of the largest county wind farm
                        "V80/2000",  # Turbine of the largest county wind farm
                        80,
                    )  # Hub height of the largest county wind farm

                else:

                    selected_farm[num_county] = (
                        wind_farm_county.loc[
                            idx_pow_index, "Latitude"
                        ],  # Latitude of the largest county wind farm
                        wind_farm_county.loc[
                            idx_pow_index, "Longitude"
                        ],  # Longitude of the largest county wind farm
                        total_power,
                        wind_farm_county.loc[
                            idx_pow_index, "Manufacturer"
                        ],  # Manufacturer of the largest county wind farm
                        wind_farm_county.loc[
                            idx_pow_index, "Turbine"
                        ],  # Turbine of the largest county wind farm
                        wind_farm_county.loc[idx_pow_index, "Hub height"],
                    )  # Hub height of the largest county wind farm

    french_total_power = sum(d.values())

    # draw the France map
    m = Basemap(
        urcrnrlat=51.5,
        llcrnrlat=42,
        urcrnrlon=9,
        llcrnrlon=-5.5,
        suppress_ticks=True,
        rsphere=(6378137.00, 6356752.3142),
        resolution="h",
        projection="merc",
        lat_0=(51.5 + 42.0) / 2,
        lon_0=(9 - 5.5) / 2,
    )

    fig = plt.figure(figsize=(15, 15))
    verts = []
    total_power = []
    for f in os.listdir(root_county):

        if (
            (f[0:2] != "2A") and (f[0:2] != "2B") and int(f[0:2]) < 97
        ):  # select only french metropolitan counties

            x, y, c = lim_departement(f)
            plt.plot(
                x,
                y,
                color="k",
                alpha=0.7,
                linewidth=1,
                solid_capstyle="round",
                zorder=60,
            )
            verts.append(list(zip(x, y)))

            try:  # the county is equipped with wind farm
                total_power.append(d[f[0:2]])
                prod = round(100 * d[f[0:2]] / french_total_power, 2)
            except:
                total_power.append(0)
                prod = 0

            ax = plt.gca()  # get current axes instance
            if int(f[0:2]) <= 90:
                ax.text(
                    c[0],
                    c[1],
                    str(prod) + "%",
                    fontsize=12,
                    fontweight="bold",
                    ha="center",
                    va="top",
                    color="k",
                )

    poly = PolyCollection(
        verts,
        array=np.array(total_power),
        cmap=plt.cm.get_cmap("viridis"),
        edgecolors="none",
    )

    # plot wind farm locations
    w_onshore = wind_farm.query(
        '(Status == "Production")  &  \
                                  (Area != "Offshore")     &  \
                                  (Latitude !="#ND")       &  \
                                  (Longitude !="#ND")      &  \
                                  (`Total power` !="#ND")'
    )

    w_onshore = w_onshore.query(
        "(Latitude > 42)  &  (Latitude < 52) &  (Longitude < 14)"
    )

    lat = np.array(w_onshore["Latitude"])
    long = np.array(w_onshore["Longitude"])
    pw = (np.array(w_onshore["Total power"]) / 500).astype(int)
    x, y = m(long, lat)
    plt.scatter(x, y, s=pw, c="r")

    # plot location of the selected farm per county
    long, lat = zip(*list(gps_selected_farm.values()))
    long = list(long)
    lat = list(lat)
    x, y = m(lat, long)
    plt.scatter(x, y, s=50, c=color_selected_farm, marker="*", alpha=0.8)

    # plot offshore wind farm location in production
    w_offshore = wind_farm_offshore.query(
        '(Status == "Production") &  \
                                           (Area=="Offshore")'
    )
    w_offshore = w_offshore.query(
        "(Latitude > 42)  &  (Latitude < 52) &  (Longitude < 14)"
    )
    lat = np.array(w_offshore["Latitude"])
    long = np.array(w_offshore["Longitude"])
    x, y = m(long, lat)
    _ = plt.scatter(x, y, s=100, c="r")

    # plot offshore wind farm location planned
    w_offshore = wind_farm_offshore.query(
        '(Status == "Approved") &  \
                                           (Area=="Offshore")'
    )
    w_offshore = w_offshore.query(
        "(Latitude > 42)  &  (Latitude < 52) &  (Longitude < 14)"
    )
    lat = np.array(w_offshore["Latitude"])
    long = np.array(w_offshore["Longitude"])
    pw = (np.array(w_offshore["Total power"]) / 500).astype(int)
    x, y = m(long, lat)
    _ = plt.scatter(x, y, s=0.8 * pw, c="g")

    df = pd.DataFrame.from_dict(selected_farm).T
    df.columns = [
        "Latitude",
        "Longitude",
        "Total power",
        "Manufacturer",
        "Model",
        "Hub height",
    ]

    hub_height = [float(x) for x in df["Hub height"] if x != "#ND"]
    per_cent_height = 100 * len(hub_height) / len(df["Hub height"])
    median_hub_height = np.median(hub_height)

    _ = plt.title(
        f"year = {year}, \
                total power = {sum(total_power)/1.e6:.2f} Gw, \
                number of farms = {len(wind_farm)}, \
                median hub height = {median_hub_height:.2f} m  \
                {per_cent_height:.1f}% of known hub heigth \n  \
                selection mode : {mode},  number of equipped counties : {len(df)}"
    )
    plt.axis("off")

    # build offshore farms data frame
    farm_offshore = {}
    w_offshore = wind_farm_offshore.query('(Area=="Offshore")')
    w_offshore = w_offshore.query(
        "(Latitude > 42)  &  (Latitude < 52) &  (Longitude < 14)"
    )
    for idx in w_offshore.index:
        farm_offshore[w_offshore.loc[idx, "Name"]] = [
            w_offshore.loc[idx, "Latitude"],
            w_offshore.loc[idx, "Longitude"],
            w_offshore.loc[idx, "Total power"],
            "Siemens",
            "SWT-4.0-130",
            120,
        ]
    df_offshore = pd.DataFrame.from_dict(farm_offshore).T
    df_offshore.columns = [
        "Latitude",
        "Longitude",
        "Total power",
        "Manufacturer",
        "Model",
        "Hub height",
    ]
    df_offshore.index = [str(x) for x in (200 + np.arange(0, len(df_offshore), 1))]

    return df, median_hub_height, df_offshore


def wind_pca(X):

    import numpy as np
    import matplotlib.pyplot as plt

    # Build a square symetric correlation matrix of rank  N_var
    Cor = np.dot(X, X.T)

    # Compute the eigenvalues and eigenvectors
    lbd, Eigen_vec = np.linalg.eig(Cor)
    # print(np.matmul(Cor,Eigen_vec)-np.matmul(Eigen_vec,np.eye(N_var)*lbd))

    # sort by decreasing value of eigenvalues
    w = sorted(list(zip(lbd, Eigen_vec.T)), key=lambda tup: tup[0], reverse=True)
    vp = np.array([x[0] for x in w])
    L = np.array([x[1] for x in w]).reshape(np.shape(Eigen_vec)).T

    F = np.real(np.matmul(X.T, L))
    Eigen_vec = np.real(Eigen_vec)

    labels = ["PC" + str(x) for x in range(1, 10)]
    plt.bar(x=range(1, 10), height=vp[0:9], tick_label=labels, color="turquoise")
    plt.title("Scree plot")
    return F


def plot_wind_pca(F, df, wind, year):

    import matplotlib.pyplot as plt
    from adjustText import adjust_text

    txt_optimisation = True

    dic_region = {
        "Rhone Alpes": [
            "01",
            "03",
            "07",
            "15",
            "26",
            "38",
            "42",
            "43",
            "63",
            "73",
            "74",
        ],
        "Bourgogne Franche Comte": ["21", "25", "39", "58", "70", "71", "89", "90"],
        "Bretagne": ["22", "29", "35", "56"],
        "Centre Val de Loire": ["18", "28", "36", "37", "41", "45"],
        "Grand Est": ["08", "10", "51", "52", "54", "55", "57", "67", "68", "88"],
        "Haut de France": ["02", "59", "60", "62", "80"],
        "Ile de France": ["75", "77", "78", "91", "92", "93", "94", "95"],
        "Normandie": ["14", "27", "50", "61", "76"],
        "Nouvelle Aquitaine": [
            "16",
            "17",
            "19",
            "23",
            "24",
            "33",
            "40",
            "47",
            "64",
            "79",
            "86",
            "87",
        ],
        "Occitanie": [
            "09",
            "11",
            "12",
            "30",
            "31",
            "32",
            "34",
            "46",
            "48",
            "65",
            "66",
            "81",
            "82",
        ],
        "Pays de Loire": ["44", "49", "53", "72", "85"],
        "PACA": ["04", "05", "06", "13", "83", "84"],
    }
    dic_color = {
        "Rhone Alpes": "b",
        "Bourgogne Franche Comte": "r",
        "Bretagne": "y",
        "Centre Val de Loire": "c",
        "Grand Est": "g",
        "Haut de France": "m",
        "Ile de France": "gray",
        "Normandie": "k",
        "Nouvelle Aquitaine": "orange",
        "Occitanie": "gold",
        "Pays de Loire": "olive",
        "PACA": "aqua",
    }
    inv = {}
    for x, y in dic_region.items():
        for k in y:
            inv[k] = dic_color[x]

    c = []
    for county in wind.columns:
        c.append(inv[county[0:2]])

    plt.figure(figsize=(15, 15))

    idx_dep = {int(x[0:2]): i for i, x in enumerate(wind.columns)}
    for region in dic_region.keys():
        idx = [
            idx_dep[int(x[0:2])] for x in wind.columns if x[0:2] in dic_region[region]
        ]

        X = [F[i][0] for i in idx]
        Y = [F[i][1] for i in idx]

        plt.scatter(
            X,
            Y,
            c=dic_color[region],
            s=(df.T.values[2][idx] / 7000).astype(int),
            label=region,
            alpha=0.6,
        )

    plt.legend(loc=5, bbox_to_anchor=(0.3, 0.5))
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.title(f"Wind PCA analysis ({year})")

    if not txt_optimisation:
        for idx, sample in enumerate(wind.columns):
            plt.annotate(sample[0:2], (F[:, 0][idx], F[:, 1][idx]), size=15, c=c[idx])

    else:
        texts = []
        for idx, sample in enumerate(wind.columns):
            texts.append(
                plt.text(
                    F[:, 0][idx],
                    F[:, 1][idx],
                    sample[0:2],
                    size=11,
                    fontweight="bold",
                    c=c[idx],
                )
            )
        adjust_text(texts, save_steps=False)


def vre_aggregation(year, root_outputs, root, new_turbine=False):

    """
    This routine aggregates all the excel files in three files:
        - the first contains the loading rate matrix MxN with 8760 rows (number of hours in a year) and
          N columns corresponfing the the counties
        - the second contains the wind speed matrix MxN with 8760 rows (number of hours in a year) and
          N columns corresponfing the the counties
        - the third contains, for each county, the meta parameters provided to the ninja api.
        
    Args:
        - year (int): The current year 
        - root_outputs (string): the root containing the files to aggregates
    """

    # Standard library imports
    from pathlib import Path
    import os
    import re

    # 3rd party imports
    import pandas as pd
    from scipy.interpolate import interp1d

    #  interpolation
    if new_turbine:
        df_turbine = pd.read_excel(
            root / Path("Vestas_V110_2000_w02.xlsx"), index_col="Unnamed: 0"
        )
        wind_speed = df_turbine["speed"].values
        power = df_turbine["power"].values
        f = interp1d(wind_speed, power, kind="cubic")

    for idx, file in enumerate(os.listdir(root_outputs)):
        sub_str = re.findall(
            "^\d{1,3}.xlsx", file
        )  # filter the files with the right format ##.xlsx

        if len(sub_str):  # is a valid file found?
            num_county = sub_str[0].split(".xlsx")[
                0
            ]  # county Insee code (ex 38 for Isère) or 2## for offshore
            dg = pd.read_excel(
                root_outputs / Path(sub_str[0]), index_col="Unnamed: 0"
            )  # store the vre
            dg.columns = [
                str(num_county),
                str(num_county) + "_wind",
            ]  # store the wind speed

            if new_turbine:
                pow_interp = f(dg[str(num_county) + "_wind"])
                dg[str(num_county)] = pow_interp

            if idx == 0:
                vre_new = dg[str(num_county)]
                wind = dg[str(num_county) + "_wind"]
            else:
                vre_new = pd.merge(
                    vre_new, dg[str(num_county)], right_index=True, left_index=True
                )
                wind = pd.merge(
                    wind,
                    dg[str(num_county) + "_wind"],
                    right_index=True,
                    left_index=True,
                )

    dict_metadata = {}
    for idx, file in enumerate(os.listdir(root_outputs)):
        sub_str = re.findall("^\d{1,3}_metadata.xlsx", file)
        if len(sub_str):
            num_county = sub_str[0].split(".xlsx")[
                0
            ]  # county Insee code (ex 38 for Isère) or 2## for offshore
            dg = pd.read_excel(root_outputs / Path(sub_str[0]), index_col="Unnamed: 0")
            dict_metadata[num_county] = [
                dg.loc["params", "lat"],
                dg.loc["params", "lon"],
                dg.loc["params", "date_from"],
                dg.loc["params", "date_to"],
                dg.loc["params", "height",],
                dg.loc["params", "turbine"],
            ]

    df_metadata = pd.DataFrame.from_dict(dict_metadata)
    df_metadata.index = ["lat", "lon", "date_from", "date_to", "height", "turbine"]

    return vre_new, wind, df_metadata


def vre_computation(year, vre_new, df, root_inputs_eoles, wind_farm_type="onshore"):

    # Standard library import
    import datetime

    # Local import
    from .vre_eoles_read import read_LF_CIRED
    from .vre_eoles_read import read_parc_eolien
    from .vre_eoles_read import read_rte
    

    # 3rd party import
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    fe = read_LF_CIRED(year, wind_farm_type, root_inputs_eoles)

    per_cent_power_county = df["Total power"].values.astype(float)
    per_cent_power_county = per_cent_power_county / sum(per_cent_power_county)

    # computation of the load time at the France scale
    VRE = np.sum(
        vre_new.values.astype(float) * per_cent_power_county, axis=1
    )  # beware the broadcasting

    deb = datetime.datetime(year, 1, 1)
    temps = [deb + datetime.timedelta(hours=i) for i in range(int(len(VRE)))]
    VRE = pd.DataFrame(VRE, index=temps, columns=["vre"])
    VRE = pd.merge(VRE, fe, right_index=True, left_index=True)

    if wind_farm_type == "onshore":
        P_eol = read_parc_eolien()  # build rte vre
        vre_rte = read_rte(year)
        vre_rte = vre_rte["Eolien"] / P_eol[year]
        VRE = pd.merge(VRE, vre_rte, right_index=True, left_index=True)
        VRE.columns = ["This sudy", "EOLES", "RTE"]
        ax = VRE.resample("M").mean().plot(kind="bar")
        _ = ax.set_xticklabels(
            [
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul",
                "Aug",
                "Sep",
                "Oct",
                "Nov",
                "Dec",
            ],
            rotation=0,
            fontsize=12,
        )
        plt.ylabel("Capacity Factor")
        plt.title(
            f"Onshore, year : {year} \n  \
                  This sudy = {100*VRE['This sudy'].mean():.1f}% RTE = {100*VRE['RTE'].mean():.1f}% EOLES = {100*VRE['EOLES'].mean():.1f}%"
        )
        plt.legend(loc=9)
    else:
        VRE.columns = ["This sudy", "EOLES"]
        ax = VRE.resample("M").mean().plot(kind="bar")
        _ = ax.set_xticklabels(
            [
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul",
                "Aug",
                "Sep",
                "Oct",
                "Nov",
                "Dec",
            ],
            rotation=0,
            fontsize=12,
        )
        plt.title(
            f"Offshore, year : {year} \n  \
                  This sudy = {100*VRE['This sudy'].mean():.1f}% EOLES = {100*VRE['EOLES'].mean():.1f}%"
        )
        plt.ylabel("Capacity Factor")
        plt.legend(loc=9)

    return VRE
