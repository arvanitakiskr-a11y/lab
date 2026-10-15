"""Small HTTP helper: python probe.py GET /sites, etc. Only loopback is used."""
import json, sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError
method, path = sys.argv[1:3]
body = json.loads(sys.argv[3]) if len(sys.argv)>3 else None
headers={'X-Demo-Token':'alpha-demo','Content-Type':'application/json','Idempotency-Key':'probe-1'}
r=Request('http://127.0.0.1:8000'+path,data=None if body is None else json.dumps(body).encode(),headers=headers,method=method)
try:
    with urlopen(r) as res: print(res.status, res.read().decode())
except HTTPError as e:
    print(e.code,e.read().decode())
