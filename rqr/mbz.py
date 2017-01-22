
import tarfile

from lxml import objectify
from lxml.cssselect import CSSSelector

def handle_null(input):
    if input == '$@NULL@$':
        return '-'
    else:
        return str(input)

def build_user_table(uf):
    xml = objectify.parse(uf)
    sel_users = CSSSelector('user')

    USER_FIELDS = ['firstname', 'lastname', 'email', 'idnumber']
    users = {}
    for usr in sel_users(xml):
        id = int(usr.attrib['id'])
        assert id not in users
        users[id] = {k: usr.find(k) for k in USER_FIELDS}

    return users


def build_response_table(qf):
    xml = objectify.parse(qf)

    sel_attempts = CSSSelector('attempt')
    sel_question_attempts = CSSSelector('question_attempt')

    attempts = []
    for att in sel_attempts(xml):
        uid = int(att.userid)
        qatts = {}
        for qatt in sel_question_attempts(att):
            qid = int(qatt.questionid)
            resp = handle_null(qatt.responsesummary)
            assert qid not in qatts
            qatts[qid] = resp
        attempts.append((uid, qatts))
    return attempts

def parse_backup(fn):
    with tarfile.open(fn, 'r:gz') as fl:
        # user file
        uf = fl.extractfile('users.xml')
        users = build_user_table(uf)

        # quiz file
        is_quiz = lambda fname: fname.endswith('quiz.xml')
        q, = filter(is_quiz, fl.getnames())
        qf = fl.extractfile(q)

        atts = build_response_table(qf)
        return users, atts


if __name__ == "__main__":

    import sys
    fn = sys.argv[1]

    users, atts = parse_backup(fn)

    from collections import defaultdict
    qs = defaultdict(list)

    for uid,qatts in atts:
        for qid,resp in qatts.items():
            qs[qid].append({'response': resp, 'user': users.get(uid)})

    from .templating import env
    template = env.get_template('template.html')

    for q,resps in qs.items():
        out = template.render(resps=resps, subject="Reading questions", headline=q)
        with open('%s.html' % q, 'w') as fl:
            fl.write(out)
