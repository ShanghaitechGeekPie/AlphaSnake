import json
import os
import base64

from django.db import transaction
from django.db.models import F
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render

from db.models import Game, Player, Step

from .NotificationCenter import NotificationCenter

import logging


SOCKET_SERVER_URL = os.environ['SOCKET_SERVER_URL']

logger = logging.getLogger(__name__)

GAME_THRESHOLD = 4


noticenter_init = NotificationCenter(SOCKET_SERVER_URL, 'init')
noticenter_judged = NotificationCenter(SOCKET_SERVER_URL, 'judged')


def postinit(request):
    if request.method != 'POST' or 'name' not in request.POST:
        return HttpResponseBadRequest()

    cookie = base64.b64encode(os.urandom(12)).decode()
    player = Player(name=request.POST['name'], cookie=cookie)
    player.save()

    with transaction.atomic():
        game, _ = Game.objects.select_for_update() \
            .filter(status=Game.PENDING, player_count__lt=GAME_THRESHOLD) \
            .order_by('create_time')[:1].get_or_create()
        logger.debug('Game updating.')
        game.player_count = F('player_count') + 1
        game.save()

    logger.debug('Game update success.{}'.format(game.player_count))

    player.game = game
    player.save()
    logger.debug('Player update success.')
    gid = game.id

    msg, evt = noticenter_init.listen(gid)

    if game.players.count() >= GAME_THRESHOLD:
        game.status = Game.READY
        game.save()

    evt.wait()
    msg = msg[0]

    return HttpResponse(json.dumps({
        'pid': player.id,
        'cookie': cookie,
        'local_id': sorted(msg['players']).index(player.id) + 1,
        'map': msg['map'],
    }))


def postgo(request):
    if request.method != 'POST' or 'pid' not in request.POST \
            or 'cookie' not in request.POST or 'move' not in request.POST:
        return HttpResponseBadRequest()

    step = Step(choice=request.POST['move'])
    step.save()

    update_res = Player.objects.filter(id=request.POST['pid'], cookie=request.POST['cookie']) \
        .update(last_move=step)
    if not update_res:
        return HttpResponseBadRequest()

    player = Player.objects.get(id=request.POST['pid'])

    step.player = player
    step.save()
    gid = player.game.id

    msg, evt = noticenter_judged.listen(gid)
    evt.wait()
    msg = msg[0]

    status = msg['status']
    status = [s for pid, s in status if pid == player.id][0]
    # May have error indexing, throw http500 anyway.

    if status == 2:
        Game.objects.filter(id=gid).update(winner=player)

    return HttpResponse(json.dumps({
        'map': msg['map'],
        'status': status
    }))


def getready(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()
    # TODO: check localhost
    game = Game.objects.filter(status=Game.READY).order_by('create_time').first()
    if not game:
        return HttpResponse(json.dumps(None))
    # Maybe null but is just we need

    players = game.players.values_list('id', flat=True)
    return HttpResponse(json.dumps({'id': game.id, 'players': list(players)}))


def getmove(request):
    if request.method != 'POST' or 'gid' not in request.POST:
        return HttpResponseBadRequest()
    game = Game.objects.filter(id=request.POST['gid']).first()
    if not game:
        return HttpResponse('[]')

    moves = list(game.players.filter(last_move__time_stamp__gte=game.last_update_time)
                 .values_list('id', 'last_move__choice'))
    return HttpResponse(json.dumps(moves))


def updategame(request):
    # TODO: check localhost
    if request.method != 'POST' or 'gid' not in request.POST or 'time' not in request.POST:
        return HttpResponseBadRequest()
    update_fields = {'last_update_time': request.POST['time']}
    if 'status' in request.POST:
        update_fields['status'] = request.POST['status']
    Game.objects.filter(id=request.POST['gid']).update(**update_fields)
    return HttpResponse('')


def homepage(request):
    return render(request, 'index.html')
