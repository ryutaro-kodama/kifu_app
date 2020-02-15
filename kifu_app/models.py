from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class LargeClass(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class MiddleClass(models.Model):
    large_class = models.ForeignKey(LargeClass, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class SmallClass(models.Model):
    middle_class = models.ForeignKey(MiddleClass, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    # order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Information(models.Model):
    date = models.DateTimeField()
    sente = models.CharField(max_length=50)
    gote = models.CharField(max_length=50)
    result = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)])
    #先手勝ち:0, 後手勝ち:1, 引き分け:2
    my_result = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)])
    #自分勝ち:0, 相手勝ち:1, 引き分け:2
    small_class = models.ForeignKey(SmallClass, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.date

class Kifu(models.Model):
    information = models.ForeignKey(Information, on_delete=models.CASCADE)
    number = models.IntegerField(validators=[MinValueValidator(0)])
    te = models.CharField(max_length=20)
    # comment = models.CharField(max_length=900)

    def __str__(self):
        return self.te