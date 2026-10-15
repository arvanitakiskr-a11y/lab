import sys
import httpx
mode=sys.argv[1] if len(sys.argv)>1 else 'normal'
r=httpx.post('http://127.0.0.1:8000/training/mode',json={'mode':mode}, trust_env=False)
print(r.status_code,r.text)
r.raise_for_status()
