__all__ = [
    "stat_prod_electricite",
    "stat_prod_consommation",
    "prod_eolien_evolution_par_jour",
]




def stat_prod_electricite(year):

    
    #Local import
    from .vre_eoles_read import read_rte
    
    # 3rd party import
    import matplotlib.pyplot as plt
    
    
    format_date = lambda x : f'{x.year}/{x.month}/{x.day} à {x.hour}h'
    B = read_rte(year)
    fig=plt.figure(figsize=(10,10))
    B[["Fioul","Charbon","Gaz","Nucléaire","Eolien","Solaire","Hydraulique","Bioénergies"]] .sum().plot(kind='pie',fontsize=18)
    plt.ylabel("")
    plt.title(f"{year}")
    plt.show()
    
    cat = ["Fioul","Charbon","Gaz","Nucléaire","Eolien","Solaire","Hydraulique","Bioénergies"]
    print(f"Consommation et production d'énergie électrique pour l'année {year}\n")
    print(f"Consommation : {B['Consommation'].sum()/1.e6} TWh")
    prod = sum([x for x in B[cat] .sum()])
    for x in [(x[0],x[1]) for x in zip(cat,B[cat].sum())]:
        print(f'{x[0]} : {x[1]/1.e6} TWh, {round(100*x[1]/prod,3)} % ')
    
    
    tup = [(x[0],x[1]) for x in zip(B.index,B['Consommation'])]
    tup = sorted(tup, key=lambda x: x[1], reverse = True)
    print(f'En {year} la consommation maximale, en une heure, est de {tup[0][1]/1.e3 } GWh. Elle est advenue le {format_date(tup[0][0]) }')
    print(f'En {year} la consommation minimale, en une heure, est de {tup[-1][1]/1.e3 } GWh. Elle est advenue le {format_date(tup[-1][0]) }')
    return
    
def stat_prod_consommation(year):
    
    #Local import
    from .vre_eoles_read import read_rte
    
    # 3rd party import
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker  
    
    cat = 'Consommation'
    B = read_rte(year)
    BN = B[cat].resample('M').sum()/1.e6

    fig=plt.figure(figsize=(15,15))
    plt.subplot(2,2,1)
    ax = BN.plot(kind='bar')
    #ticklabels = [item.strftime('%m') for item in B.index]
    ticklabels = range(1,13)
    ticklabels = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
    ax.xaxis.set_major_formatter(ticker.FixedFormatter(ticklabels))
    plt.gcf().autofmt_xdate()
    plt.ylabel("TWh")
    plt.title(f'{cat} ({year})')

    plt.subplot(2,2,2)
    plt.hist(B['Consommation']/1.e3,bins=30,color='g')
    plt.xlabel("GWh")
    plt.ylabel("# heures")
    
    plt.subplot(2,2,4)
    plt.boxplot(B['Consommation']/1.e3)
    plt.ylabel("GWh")
    plt.show()
    
    return

def prod_eolien_evolution_par_jour(year,month):
    '''
    Draw electricity production vs time
    cat must be equal to : 'Fioul', 'Charbon', 'Gaz', 'Nucléaire', 'Eolien',
           'Solaire', 'Hydraulique', 'Pompage', 'Bioénergies'

    '''
    
    #Local import
    from .vre_eoles_read import read_rte
    
    # 3rd party import
    import matplotlib.pyplot as plt
    
    cat ='Eolien'
    B = read_rte(year)
    
    def numberOfDays(y, m):
      leap = 0
      if y% 400 == 0:
         leap = 1
      elif y % 100 == 0:
         leap = 0
      elif y% 4 == 0:
         leap = 1
      if m==2:
         return 28 + leap
      list = [1,3,5,7,8,10,12]
      if m in list:
         return 31
      return 30


    fig=plt.figure(figsize=(15,5))
    plt.subplot(1,2,1)
    dep = str(year)+'-' + str(month) +'-01'
    fin = str(year)+'-' + str(month) +'-'+ str(numberOfDays(year, month))
    B[dep:fin][cat].plot(style='or',ms=2)
    B['mean'] = B[dep:fin][cat].mean()
    B[dep:fin]['mean'].plot()
    plt.ylabel("MWh")
    plt.title(f'(a) {cat}')

    plt.subplot(1,2,2)
    B[dep:fin][cat].diff().plot(style='or',ms=2)
    plt.ylabel("MWh/h")
    plt.title(f'(b) {cat}')
    plt.show()
    
    return
