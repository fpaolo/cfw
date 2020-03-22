class TwitterInfo:
    """ Class to store twitter info for health/government """
    country_list =['AU', 'CA', 'CH', 'CN', 'CN-HK',
                   'DE', 'ES', 'FR', 'IN', 'IT',                    'JA',
                   'KR', 'NZ', 'SE', 'UK', 'US']
    hlt_users = {'IT':"DPCgov", 
                 "UK":"DHSCgovuk", 
                 "DE":"rki_de", 
                 "ES":"SaludPublicaEs",
                 "FR":"MinSoliSante",
                 "US":"CDCgov", 
                 "AU":"healthgovau",
                 "NZ":"minhealthnz",
                 "CA":"GovCanHealth",
                 "CH":"BAG_OFSP_UFSP",
                 "IN":"PIB_India",  # "MoHFW_INDIA",
                 "SE":"Folkhalsomynd",
                 "KR":"TheKoreaHerald",
                 "CN":"PDChina",
                #  "CN-HK":None,  # "SCMPNews"
                #  "JA":None,   #"japantimes"
            } 
    hlt_keys_ANY = {'IT':['diretta'], 
                    "UK":['update', 'testing'], 
                    "DE":['pressebriefing', 'aktuelle'], 
                    "ES":['casos', 'actualizados', 'datos'],
                    "FR":['direct', "Point de situation"],
                    "US":['briefing'],
                    "AU":["update"],
                    "NZ":["update"],
                    "CA":["update", "broadcast", "live"],
                    "CH":["CoronaInfoCH", "bilan actuel",
                          "Point de Presse", "cas", "positifs"],
                    "IN":["cases", "number", "tested"],
                    "SE":["Uppdaterade", "pressträff"],
                    "KR":['breaking'],
                    "CN":['Chinese mainland'],
                    # "CN-HK":None,
                    # "JA":None
                    }  
    hlt_keys_ALL = dict.fromkeys(hlt_users)
    for _k in hlt_keys_ALL.keys():
        hlt_keys_ALL[_k] = None # hlt_keys_ANY[_k]
    # hlt_keys_ALL['ES'] = ["actualizados"]
    # hlt_keys_ALL['CH'] = ["CoronaInfoCH"]
    # hlt_keys_ALL['SE'] = None
    hlt_match_covid = dict.fromkeys(hlt_users)
    for _k in hlt_match_covid.keys():
        hlt_match_covid[_k] = True

    gov_users = {'IT':"Palazzo_Chigi",
                'UK':"10DowningStreet",
                "DE":"RegSprecher",
                "ES":"desdelamoncloa",
                'FR':"Elysee",
                "US":"whitehouse",
                "AU":"ScottMorrisonMP",
                "NZ":"govtnz",
                "CA":"CanadianPM",
                "CH":"BR_Sprecher",
                "IN":"narendramodi",
                "SE":"swedense",
                "KR":"TheBlueHouseENG",   # TheBlueHouseKR
                #  "CN":None,
                #  "CN-HK":None,
                "JA":"JPN_PMO"}

    gov_keys_ANY = {'IT':['diretta', 'live', 'broadcast'], 
                "UK":['watch live'], 
                "DE":['konferenz'], 
                "ES":['live', 'directo'],
                "FR":['direct', "Point de situation","adresse"],
                "US":['live', 'press','briefing'],
                "AU":["update"],
                "NZ":["update"],
                "CA":["update", "broadcast", "live"],
                "CH":["stampa"],
                "IN":["CoronaVirusUpdates"],
                "SE":["Uppdaterade", "pressträff"],
                "KR":['breaking'],
                # "CN":None,
                # "CN-HK":None,
                "JA":['update']}
  
    gov_keys_ALL = dict.fromkeys(gov_users)
    for _k in gov_keys_ALL.keys():
        gov_keys_ALL[_k] = None
    gov_match_covid = dict.fromkeys(gov_users)
    for _k in gov_match_covid.keys():
        gov_match_covid[_k] = True
    gov_match_covid['IT'] = False
    gov_match_covid['AU'] = False
    gov_match_covid['IN'] = False
    gov_match_covid['SE'] = False

    def __init__(self):
        pass 


