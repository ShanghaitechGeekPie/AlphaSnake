from django.db import models

# Create your models here.


class Game(models.Model):
    # gid
    PENDING = 0
    READY = 1
    RUNNING = 2
    END = 3
    STATUS_CHOICE = (
        (PENDING, 'pending'),
        (READY, 'ready'),
        (RUNNING, 'running'),
        (END, 'end'),
    )
    # title = models.CharField(max_length=255, blank=False)
    status = models.IntegerField(choices=STATUS_CHOICE, default=PENDING)
    # step = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now=True)
    last_update_time = models.DateTimeField(null=True, default=None)
    # players = foreign key manager

    def __str__(self):
        return 'Game #{}'.format(self.id)


class Player(models.Model):
    # pid
    name = models.CharField(max_length=255, blank=False)
    join_time = models.DateTimeField(auto_now=True)
    # team = models.CharField(max_length=255, blank=False)
    game = models.ForeignKey(Game, on_delete=models.DO_NOTHING, null=True, default=None, related_name='players')
    cookie = models.CharField(max_length=255, blank=False)
    last_move = models.OneToOneField('Step', null=True, default=None)

    def __str__(self):
        return '[{} - {}]{}'.format(self.game, self.pid, self.name)
        # ordering = ['pid']


class Step(models.Model):
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    # step = models.IntegerField()
    choice = models.IntegerField()
    time_stamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '[{} - {}]{}'.format(self.game, self.pid, self.name)
        # ordering = ['step', 'player']
