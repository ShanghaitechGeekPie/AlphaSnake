import json

from django.http.response import HttpResponse

from db.models import Game, Player, Step

def check_step(game, step):
    if game.step != step:
        return
    currect_steps = Step.objects.filter(player__game = game, step = step)
    all_players = Player.objects.filter(game = game)

    if len(all_players) != len(currect_steps):
        for player in all_players:
            if player.status:
                try:
                    temp = all_players.get(player = player)
                    continue
                except Step.DoesNotExist:
                    currect_time = time.time()
                    if currect_time - game.timeStamp <= 10:
                        return
                    else:
                        player.status = False
                        player.save()

    for currect_step in currect_steps:
        if (currect_step.x < 0) or \
            (currect_step.y < 0) or \
            (currect_step.x > 99) or \
            (currect_step.y > 99):
            currect_step.player.status = False
            currect_step.player.save()
            continue
        if len(Step.objects.filter(x = currect_step.x, y = currect_step.y, player__game = game)) > 1:
            currect_step.player.status = False
            currect_step.player.save()

    game.step = step + 1
    game.save()

def default(request):
    pass

def info(request):
    try:
        gameid = request.GET['gameid']
        game = Game.objects.get(id = gameid)
        command = request.GET['command']
        if command == 'register':
            id = request.GET['id']
            name = request.GET['name']
            team = request.GET['team']
            try:
                tplayer = Player.objects.get(game = game, pid = id)
                tplayer.name = name
                tplayer.team = team
                tplayer.status = True
            except:
                tplayer = Player(
                    name = name,
                    team = team,
                    game = game,
                    pid = id,
                    status = True,
                    x = 0,
                    y = 0,
                )
            tplayer.save()
            tplayer.random()
            return HttpResponse(json.dumps({
                'code': 'success',
            }))
        elif command == 'check':
            id = request.GET['id']
            if game.start:
                return HttpResponse(json.dumps({
                    'num': len(game.player_set.all()),
                    'start_position': [{
                        'id': player.pid,
                        'position': {
                            'x': player.x,
                            'y': player.y,
                        },
                    } for player in game.player_set.all()],
                    'code': 'success',
                }))
            else:
                return HttpResponse(json.dumps({
                    'code': 'failed',
                }))
        elif command == 'all':
            return HttpResponse(json.dumps({
                'players': [{
                    'name': player.name,
                    'team': player.team,
                } for player in game.player_set.all()],
                'code': 'success',
            }))
    except:
        return HttpResponse(json.dumps({
            'code': 'error',
        }))

def submit(request):
    try:
        choiceMat = {
            '0': [0, 1],
            '1': [1, 0],
            '2': [0, -1],
            '3': [-1, 0],
        }

        gameid = request.GET['gameid']
        id = request.GET['id']
        command = request.GET['command']

        # check if the game and player exists
        game = Game.objects.get(id = gameid)
        player = Player.objects.get(game = game, pid = id)

        # check snake is dead already
        if player.status == False:
            raise

        # check this step haven't be decided
        try:
            Step.objects.get(player = player, step = game.step)
            raise
        except Step.DoesNotExist:
            pass

        # initialize the new step object
        tstep = Step(
            player = player,
            step = game.step,
            choice = command,
            x = player.x,
            y = player.y,
        )
        if game.step != 0:
            tprestep = Step.objects.get(player = player, step = game.step - 1)
            tstep.choice = command
            tstep.x = tprestep.x + choiceMat[command][0]
            tstep.y = tprestep.y + choiceMat[command][1]

        tstep.save()
        return HttpResponse(json.dumps({
            'step': game.step,
            'code': 'success',
        }))
    except:
        return HttpResponse(json.dumps({
            'code': 'error',
        }))

def get_step(request):
    try:
        gameid = request.GET['gameid']
        step = int(request.GET.get('step', -1))

        game = Game.objects.get(id = gameid)

        if step == -1:
            players = Player.objects.filter(game = game)

            steps = []

            for i in players:
                tsteps = Step.objects.filter(player = i)
                steps.append({
                    'id': i.pid,
                    'steps': [
                        {
                            'choice': i.choice,
                            'x': i.x,
                            'y': i.y,
                            'step': i.step,
                        }
                        for i in tsteps
                    ]
                })

            return HttpResponse(json.dumps({
                'step': steps,
                'code': 'success',
            }))

        else:

            if step == game.step:
                check_step(game, step)

            if step >= game.step:
                return HttpResponse(json.dumps({
                    'code': 'not allowed',
                }))

            players = Player.objects.filter(game = game)

            status = []
            steps = []

            for i in players:
                status.append(i.status)
                try:
                    tstep = Step.objects.get(player = i, step = step)
                    steps.append(tstep.choice)
                except Step.DoesNotExist:
                    steps.append(-1)

            return HttpResponse(json.dumps({
                'status': status,
                'step': steps,
                'code': 'success',
            }))
    except:
        return HttpResponse(json.dumps({
            'code': 'error',
        }))
