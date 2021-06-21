from django.db import models

# Create your models here.


class Firer(models.Model):
    number = models.CharField(max_length=100, null=True, unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    rank = models.CharField(max_length=100, null=True, blank=True)
    coy = models.CharField(max_length=100, null=True, blank=True)
    unit = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.number


class Detail(models.Model):
    number = models.PositiveIntegerField(null=True)
    target_1 = models.ForeignKey(
        Firer, related_name='target_1', on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.date)+'- No'+str(self.number)


class Fire(models.Model):
    detail = models.ForeignKey(
        Detail, null=True, blank=True, on_delete=models.CASCADE)
    new_target = models.BooleanField(default=False, blank=True)
    hits = models.PositiveIntegerField(null=True, blank=True)
    fired = models.ImageField(null=True, blank=True)
    detected = models.ImageField(null=True, blank=True)


class Result(models.Model):
    firer = models.ForeignKey(Firer, null=True, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True, blank=True)
    fire = models.OneToOneField(
        Fire, blank=True, null=True, on_delete=models.CASCADE)
    remark = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.firer.number + '-' + str(self.date_created)
