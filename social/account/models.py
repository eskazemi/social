from django.db import models
from django.contrib.auth.models import User


class RelationShip(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='followers')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='following')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.from_user}-following-{self.to_user}"
