
# coding: utf-8

import pandas as pd

import sys


fn = sys.argv[1]

df = (pd.read_csv(fn)
        .drop(['Institution', 'Department'], axis=1)
        .rename(columns=lambda string: string.replace(' ', '_')))

USER_FIELDS = ['Last_name', 'First_name', 'ID_number', 'Email_address']

def clean_resps(df, resp_col = 'Response_1'):
    cols = [col for col in df.columns if not col.startswith('Response')]
    def make_response(row):
        resp = {'response': row[resp_col]}
        resp['user'] = dict(row[USER_FIELDS])
        return resp
    resps = [make_response(row) for i, row in df.iterrows()]
    return resps




import re
from jinja2 import evalcontextfilter, Markup, escape

_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', Markup('<br>\n'))
                          for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result



import jinja2

# TODO: make this loadable in any directory
loader = jinja2.FileSystemLoader('.')
env = jinja2.Environment(loader=loader)
env.filters['nl2br'] = nl2br


template = env.get_template('template.html')



qs = [col for col in df.columns if col.startswith('Response')]


for q in qs:
    resps = clean_resps(df, q)
    out = template.render(resps=resps, subject="Reading questions", headline=q)
    with open('%s.html' % q, 'w') as fl:
        fl.write(out)




