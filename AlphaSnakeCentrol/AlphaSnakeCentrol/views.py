import json
import os
import base64

from django.db import transaction
from django.db.models import F
from django.http.response import HttpResponse, HttpResponseBadRequest

from db.models import Game, Player, Step

from .WaitOnce import WaitUntilRecv
import logging


logger = logging.getLogger(__name__)

GAME_THRESHOLD = 4


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

    sock_conn = WaitUntilRecv('init', lambda x: x['gid'] == gid)

    if game.players.count() >= GAME_THRESHOLD:
        game.status = Game.READY
        game.save()

    sock_conn.wait()

    return HttpResponse(json.dumps({
        'pid': player.id,
        'cookie': cookie,
        'map': sock_conn.msg['map']
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

    sock_conn = WaitUntilRecv('judged', lambda x: x['gid'] == gid)
    sock_conn.wait()

    status = sock_conn.msg['status']
    status = [s for pid, s in status if pid == player.id][0]
    # May have error indexing, throw http500 anyway.

    if status == 2:
        Game.objects.filter(id=gid).update(winner=player)

    return HttpResponse(json.dumps({
        'map': sock_conn.msg['map'],
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
    # logger.debug('Player last moves at {}: {} {}'.format(
    #              game.last_update_time,
    #              list(game.players.values_list('id', 'last_move__choice', 'last_move__time_stamp')),
    #              moves))
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


# def check_step(game, step):
#     if game.step != step:
#         return
#     currect_steps = Step.objects.filter(player__game = game, step = step)
#     all_players = Player.objects.filter(game = game)

#     if len(all_players) != len(currect_steps):
#         for player in all_players:
#             if player.status:
#                 try:
#                     temp = all_players.get(player = player)
#                     continue
#                 except Step.DoesNotExist:
#                     currect_time = time.time()
#                     if currect_time - game.timeStamp <= 10:
#                         return
#                     else:
#                         player.status = False
#                         player.save()

#     for currect_step in currect_steps:
#         if (currect_step.x < 0) or \
#             (currect_step.y < 0) or \
#             (currect_step.x > 99) or \
#             (currect_step.y > 99):
#             currect_step.player.status = False
#             currect_step.player.save()
#             continue
#         if len(Step.objects.filter(x = currect_step.x, y = currect_step.y, player__game = game)) > 1:
#             currect_step.player.status = False
#             currect_step.player.save()

#     game.step = step + 1
#     game.save()

# def default(request):
#     pass

# def info(request):
#     try:
#         gameid = request.GET['gameid']
#         game = Game.objects.get(id = gameid)
#         command = request.GET['command']
#         if command == 'register':
#             id = request.GET['id']
#             name = request.GET['name']
#             team = request.GET['team']
#             try:
#                 tplayer = Player.objects.get(game = game, pid = id)
#                 tplayer.name = name
#                 tplayer.team = team
#                 tplayer.status = True
#             except:
#                 tplayer = Player(
#                     name = name,
#                     team = team,
#                     game = game,
#                     pid = id,
#                     status = True,
#                     x = 0,
#                     y = 0,
#                 )
#             tplayer.save()
#             tplayer.random()
#             return HttpResponse(json.dumps({
#                 'code': 'success',
#             }))
#         elif command == 'check':
#             id = request.GET['id']
#             if game.start:
#                 return HttpResponse(json.dumps({
#                     'num': len(game.player_set.all()),
#                     'start_position': [{
#                         'id': player.pid,
#                         'position': {
#                             'x': player.x,
#                             'y': player.y,
#                         },
#                     } for player in game.player_set.all()],
#                     'code': 'success',
#                 }))
#             else:
#                 return HttpResponse(json.dumps({
#                     'code': 'failed',
#                 }))
#         elif command == 'all':
#             return HttpResponse(json.dumps({
#                 'players': [{
#                     'name': player.name,
#                     'team': player.team,
#                 } for player in game.player_set.all()],
#                 'code': 'success',
#             }))
#     except:
#         return HttpResponse(json.dumps({
#             'code': 'error',
#         }))

# def submit(request):
#     try:
#         choiceMat = {
#             '0': [0, 1],
#             '1': [1, 0],
#             '2': [0, -1],
#             '3': [-1, 0],
#         }

#         gameid = request.GET['gameid']
#         id = request.GET['id']
#         command = request.GET['command']

#         # check if the game and player exists
#         game = Game.objects.get(id = gameid)
#         player = Player.objects.get(game = game, pid = id)

#         # check snake is dead already
#         if player.status == False:
#             raise

#         # check this step haven't be decided
#         try:
#             Step.objects.get(player = player, step = game.step)
#             raise
#         except Step.DoesNotExist:
#             pass

#         # initialize the new step object
#         tstep = Step(
#             player = player,
#             step = game.step,
#             choice = command,
#             x = player.x,
#             y = player.y,
#         )
#         if game.step != 0:
#             tprestep = Step.objects.get(player = player, step = game.step - 1)
#             tstep.choice = command
#             tstep.x = tprestep.x + choiceMat[command][0]
#             tstep.y = tprestep.y + choiceMat[command][1]

#         tstep.save()
#         return HttpResponse(json.dumps({
#             'step': game.step,
#             'code': 'success',
#         }))
#     except:
#         return HttpResponse(json.dumps({
#             'code': 'error',
#         }))

# def get_step(request):
#     try:
#         gameid = request.GET['gameid']
#         step = int(request.GET.get('step', -1))

#         game = Game.objects.get(id = gameid)

#         if step == -1:
#             players = Player.objects.filter(game = game)

#             steps = []

#             for i in players:
#                 tsteps = Step.objects.filter(player = i)
#                 steps.append({
#                     'id': i.pid,
#                     'steps': [
#                         {
#                             'choice': i.choice,
#                             'x': i.x,
#                             'y': i.y,
#                             'step': i.step,
#                         }
#                         for i in tsteps
#                     ]
#                 })

#             return HttpResponse(json.dumps({
#                 'step': steps,
#                 'code': 'success',
#             }))

#         else:

#             if step == game.step:
#                 check_step(game, step)

#             if step >= game.step:
#                 return HttpResponse(json.dumps({
#                     'code': 'not allowed',
#                 }))

#             players = Player.objects.filter(game = game)

#             status = []
#             steps = []

#             for i in players:
#                 status.append(i.status)
#                 try:
#                     tstep = Step.objects.get(player = i, step = step)
#                     steps.append(tstep.choice)
#                 except Step.DoesNotExist:
#                     steps.append(-1)

#             return HttpResponse(json.dumps({
#                 'status': status,
#                 'step': steps,
#                 'code': 'success',
#             }))
#     except:
#         return HttpResponse(json.dumps({
#             'code': 'error',
#         }))
