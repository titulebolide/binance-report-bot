import requests
import numpy as np
import conf

def get_report(st):
    miner_data = requests.get(
        'https://api.ethermine.org/miner/'+str(conf.MINER_ADRESS)+'/dashboard'
    ).json()['data']

    report = {}
    report['worker_active'] = bool(miner_data['currentStatistics']['activeWorkers'])
    report['unpaid'] = miner_data['currentStatistics']['unpaid']/1e18
    report['unpaid_eur'] = report['unpaid']*st.getTicker('ETH')
    return report

def format_report(st,report):
    msg = "#### Mineur"
    msg += "\n- **Actif** : " + 'Oui' if report['worker_active'] else 'Non'
    msg += "\n- **Non payé** : {} ETH *({} €)*".format(
        round(report['unpaid'],5),
        round(report['unpaid_eur'], 2)
    )
    msg += "\n***"
    return msg
