from __future__ import unicode_literals
from django.db import models
from ..login_registration.models import User

class ItemManager(models.Manager):
    def add_item(self, postData, user_id):
        errors = self.validate(postData)
        if not errors:
            added_by = User.objects.get(id=user_id)
            item = Item.objects.create(
                item=postData['item'],
                added_by=added_by
            )
            return item
        else:
            return errors

    def add_to_list(self, item_id, user_id, first_name, last_name):
        wisher = Wisher.objects.create(
            item=Item.objects.get(id=item_id),
            user=User.objects.get(id=user_id),
            first_name=first_name,
            last_name=last_name
        )
        return wisher

    def validate(self, postData):
        errors = []
        if len(postData['item']) == 0:
            errors.append("Item cannot be blank!")
        if len(postData['item']) < 4:
            errors.append("Item name must be more than 3 characters!")
        return errors

class Item(models.Model):
    item = models.CharField(max_length=255)
    added_by = models.ForeignKey(User, related_name='user')
    wishers = models.ManyToManyField(User, through='Wisher')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ItemManager()

    def __str__(self):
        return self.item

class Wisher(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    item = models.ForeignKey(Item)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
