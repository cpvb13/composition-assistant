import re
import webbrowser

import requests

from secrets import ACCESS_TOKEN


def get_backup_ids(file="raw_queue.txt"):
    with open(file) as f:
        text = f.read()
        return re.findall(r"/composition/(.+)\?", text)


def get_backup_code(id):
    params = {"access_token": ACCESS_TOKEN}
    r = requests.get(f"https://okpy.org/api/v3/backups/{id}", params=params)
    messages = r.json()["data"]["messages"]
    out = None
    for message in messages:
        if "typing_test.py" in message["contents"]:
            if out is not None:
                raise Exception("Multiple typing_test.py found???")
            out = message["contents"]["typing_test.py"]

    if out is None:
        raise Exception("No typing_test.py found!!!")

    return out


def submit_comment(id, line, message):
    params = {"access_token": ACCESS_TOKEN}
    data = {"filename": "typing_test.py", "line": line, "message": message}
    r = requests.post(f"https://okpy.org/api/v3/backups/{id}/comment/", params=params, data=data)
    assert r.status_code == 200, "fail"


def submit_grade(id, score, message):
    params = {"access_token": ACCESS_TOKEN}
    data = {"bid": id, "kind": "composition", "score": score, "message": message}
    r = requests.post(f"https://okpy.org/api/v3/score/", params=params, data=data)
    assert r.status_code == 200, "fail"
    webbrowser.open(f"https://okpy.org/admin/composition/{id}")
