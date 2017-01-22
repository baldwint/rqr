
# coding: utf-8

import pandas as pd

import sys
fn = sys.argv[1]

userfields = {
    'Last_name': 'lastname',
    'First_name': 'firstname',
    'ID_number': 'idnumber',
    'Email_address': 'email',
}

df = (pd.read_csv(fn)
        .drop(['Institution', 'Department'], axis=1)
        .rename(columns=lambda string: string.replace(' ', '_'))
        .rename(columns=userfields))

def clean_resps(df, resp_col = 'Response_1'):
    def make_response(row):
        resp = {'response': row[resp_col]}
        resp['user'] = dict(row[list(userfields.values())])
        return resp
    resps = [make_response(row) for i, row in df.iterrows()]
    return resps

from .templating import env
template = env.get_template('template.html')

qs = [col for col in df.columns if col.startswith('Response')]

for q in qs:
    resps = clean_resps(df, q)
    out = template.render(resps=resps, subject="Reading questions", headline=q)
    with open('%s.html' % q, 'w') as fl:
        fl.write(out)




