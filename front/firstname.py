import logging
import requests
from jellyfish import jaro_winkler

class BackApi():

  def __init__(self, request):
    self.logger = logging.getLogger(__name__)
    self.base_url = f"{request.scheme}://{request.get_host()}/api"
    self.  headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Token {request.user.auth_token}',
  }

  def _get_url(self, path):
    return f"{self.base_url}/{path}"

class Firstname(BackApi):

  def next(self, sex, limit = 20):
    params = {
      'sex': sex,
      'limit': limit,
    }
    r = requests.get(self._get_url('firstnames/metaphones/'), params = params, headers = self.headers)
    firstnames = self._split_if_needed(r.json())
    self.logger.info(len(firstnames))
    return firstnames[:limit]

  def vote(self, id, choice):
    data = {
      'firstname': id,
      'choice': choice,
      }
    requests.post(self._get_url('votes/'), json = data, headers = self.headers)

  def votes(self, votes):
    data = [{
      'firstname': v.get('id'),
      'choice': v.get('choice'),
      } for v in votes]
    requests.post(self._get_url('votes/'), json = data, headers = self.headers)

  def change_vote(self, id):
    requests.patch(self._get_url(f"history/{id}/change_vote/"), headers = self.headers)

  def list_votes(self):
    return requests.get(self._get_url('history/'), headers = self.headers)

  def _split_if_needed(self, data):
    splitted = []
    while data:
      splitted.append(self._as_one(data[0], data))
    return splitted

  def _as_one(self, o, l):
    ids = []
    firstnames = []
    for f in l:
      if jaro_winkler(o.get('firstname'), f.get('firstname')) > 0.88:
        ids.append(str(f.get('id')))
        firstnames.append(f.get('firstname'))
        l.remove(f)
    return {'id': ','.join(ids), 'firstname': ', '.join(firstnames), 'sex': o.get('sex')}

class Vote(BackApi):

  def list(self):
    r = requests.get(self._get_url('votes/'), json = data, headers = self.headers)
