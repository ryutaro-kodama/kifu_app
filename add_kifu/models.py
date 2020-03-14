from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class HistoryList(models.Model):
    game_id = models.CharField(max_length=10)
    my_result = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)])
    #自分勝ち:0, 相手勝ち:1, 引き分け:2
    save_limit = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.game_id