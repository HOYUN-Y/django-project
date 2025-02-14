from django.db import models

# Create your models here.
class Item(models.Model):

    TYPE_CHOICES = [
        ('dessert','dessert'),
        ('md','md'),
        ('seasonal','seasonal'),
        ('stock','stock'),
        ('syrup','syrup'),
        ('etc','etc')
    ]
    PLACE_CHOICES = [
        ('창고','창고'),
        ('냉장고','냉장고'),
        ('냉동고','냉동고'),
        ('뒷문','뒷문'),
        ('쇼케이스','쇼케이스'),
        ('캐비닛','캐비닛'),
        ('전시대','전시대'),
        ('앞문','앞문'),
        ('etc','etc'),
    ]

    itemCode = models.IntegerField(unique=True, null=True, blank=True, verbose_name='Code')
    typeOfItem = models.CharField(max_length=30, choices=TYPE_CHOICES ,verbose_name='Type')
    name = models.CharField(max_length=30,verbose_name='Name')
    units = models.IntegerField(default=0, verbose_name='Units')
    place = models.CharField(max_length=30, choices=PLACE_CHOICES ,verbose_name='Place')
    #pricePerUnits = models.CharField(max_length=30)
    amountOfBulk = models.FloatField(default=0.0,verbose_name='Amount Of Bulk')
    amountOfEach = models.FloatField(default=0.0, verbose_name='Amount of Each')
    lastTimeSaved = models.DateTimeField(null=True, auto_now=True, verbose_name='Last Savetime')
    #forSale = models.BooleanField()
    def save(self, *args, **kwargs):
        self.place = self.place.lower()
        if self.itemCode is None:
            last_item = Item.objects.order_by('-itemCode').first()
            self.itemCode = last_item.itemCode + 1 if last_item else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.itemCode} | {self.typeOfItem} | {self.name} | {self.units} | {self.place} | {self.amountOfBulk} | {self.amountOfEach} | {self.lastTimeSaved}"