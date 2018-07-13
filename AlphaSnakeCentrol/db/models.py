from django.db import models

# Create your models here.

class Game(models.Model):
    title = models.CharField(max_length = 255, blank = False)
    start = models.BooleanField(default = False)
    step = models.IntegerField(default = 0)
    timeStamp=models.DateTimeField(auto_now=True,verbose_name='时间戳')

    def __unicode__(self):
        return '{}'.format(self.title)

class Player(models.Model):
    name = models.CharField(max_length = 255, blank = False)
    team = models.CharField(max_length = 255, blank = False)
    game = models.ForeignKey(Game, on_delete=models.DO_NOTHING)
    pid = models.IntegerField()
    status = models.BooleanField(default = True)
    x = models.IntegerField()
    y = models.IntegerField()

    def random(self):
        import random
        x = random.randint(5, 94)
        y = random.randint(5, 94)
        self.x = x
        self.y = y
        self.save()

    def __unicode__(self):
        return '[{} - {}]{}'.format(self.game, self.pid, self.name)
        ordering = ['pid']

class Step(models.Model):
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    step = models.IntegerField()
    choice = models.IntegerField()
    x = models.IntegerField()
    y = models.IntegerField()

    def __unicode__(self):
        return '[{} - {}]{}'.format(self.game, self.pid, self.name)
        ordering = ['step', 'player']
