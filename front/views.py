import logging
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from front.firstname import Firstname

logger = logging.getLogger(__name__)

@login_required()
@csrf_protect
def index(request):
  firstname = Firstname(request)
  if request.method == 'POST':
    logger.info(request.POST)
    firstname.votes(votes_list(request.POST))
  logger.info('list of firstnames')
  firstnames = firstname.next('F')
  logger.info(firstnames)
  context = {
    'firstnames': firstnames,
    'all_id': ','.join([f.get('id') for f in firstnames]),
  }
  return render(request, 'front/vote.html', context)

@login_required()
@csrf_protect
def history(request):
  firstname = Firstname(request)
  choices = firstname.list_votes()
  logger.info(f"choices: {choices.json}")
  context = {
    'choices': choices.json
  }
  return render(request, 'front/history.html', context)

@login_required()
def history_change_vote(request, vote_id):
  firstname = Firstname(request)
  logger.info(vote_id)
  firstname.change_vote(vote_id)
  return redirect('/history/')

def votes_list(data):
  logger.info('parse post data')
  all_id = data.get('all_id', '').split(',')
  logger.info(f"total: {len(all_id)}")
  checkboxes = []
  for checkbox in data.keys():
    if checkbox.startswith('id'):
      checkboxes.extend(data.get(checkbox).split(','))
  logger.info(f"validated: {len(checkboxes)}")
  return [{'id': id, 'choice': id in checkboxes} for id in all_id if id]
