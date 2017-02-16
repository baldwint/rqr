
def main():

    import sys
    fn = sys.argv[1]

    import os
    bn = os.path.splitext(fn)[0]

    from .mbz import parse_backup
    qname, users, questions, atts = parse_backup(fn)

    from collections import defaultdict
    qs = defaultdict(list)

    for uid,qatts in atts:
        for qid,resp in qatts.items():
            qs[qid].append({'response': resp, 'user': users.get(uid)})

    from .templating import env
    template = env.get_template('template.html')


    qs = [dict(resps=resps, **questions.get(q)) for q,resps in sorted(qs.items())]
    out = template.render(title=qname, questions=qs, subject="Reading questions")
    with open(bn + '.html', 'w') as fl:
        fl.write(out)

if __name__ == "__main__":
    main()
