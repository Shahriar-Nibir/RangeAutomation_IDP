from django.db import models

# Create your models here.


class Firer(models.Model):
    number = models.CharField(max_length=100, null=True, unique=True)
    name = models.CharField(max_length=100, null=True)
    rank = models.CharField(max_length=100, null=True)
    coy = models.CharField(max_length=100, null=True)
    unit = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.number


class Result(models.Model):
    firer = models.ForeignKey(Firer, null=True, on_delete=models.CASCADE)
    ret = models.CharField(max_length=100, null=True)
    date_created = models.DateField(auto_now_add=True)
    gp = models.PositiveIntegerField(null=True)
    fig2_ly = models.PositiveIntegerField(null=True)
    fig2_other = models.PositiveIntegerField(null=True)
    fig3 = models.PositiveIntegerField(null=True)
    ets = models.PositiveIntegerField(null=True)
    total = models.PositiveIntegerField(null=True)
    remark = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.firer.number + '-' + self.ret


class Detail(models.Model):
    number = models.PositiveIntegerField(null=True)
    target_1 = models.ForeignKey(
        Firer, related_name='target_1', on_delete=models.CASCADE, null=True, blank=True)
    target_2 = models.ForeignKey(
        Firer, related_name='target_2', on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.date.date())+'- No'+str(self.number)
