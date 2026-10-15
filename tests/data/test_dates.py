import json
from pathlib import Path
from data_rules import classify

def test_reference_dataset():
    root=Path(__file__).resolve().parents[2]
    data=json.loads((root/'data/articles.json').read_text(encoding='utf-8'))
    expected=['accepted','duplicate','accepted','accepted','rejected','accepted',
              'rejected','accepted','rejected','rejected','rejected','rejected']
    assert classify(data)==expected
