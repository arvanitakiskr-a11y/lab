from datetime import datetime, timedelta
REFERENCE = datetime.fromisoformat('2026-10-08T12:00:00+00:00')
def classify(records):
    seen = set(); result = []
    for r in records:
        try:
            if type(r.get('feed_id')) is not int or not isinstance(r.get('external_id'), str) or not r['external_id'].strip():
                raise ValueError('bad key')
            if not isinstance(r.get('title'), str) or not r['title'].strip():
                raise ValueError('bad title')
            dt = datetime.fromisoformat(r['published_at'].replace('Z', '+00:00'))
            if dt.tzinfo is None or not REFERENCE-timedelta(days=7) <= dt <= REFERENCE:
                raise ValueError('bad time')
            key = (r['feed_id'], r['external_id'])
            result.append('duplicate' if key in seen else 'accepted')
            seen.add(key)
        except (ValueError, KeyError, TypeError, AttributeError):
            result.append('rejected')
    return result
