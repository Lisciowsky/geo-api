from django.db import models
from django.contrib.auth.models import User


class GEO(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="geos")
    address = models.CharField(max_length=300)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{str(self.user)} - {self.address}"

    @staticmethod
    def normilize_address(address):
        if address.startswith("http"):
            address = address.replace("https://", "")
            address = address.replace("http://", "")
        if address.startswith("www"):
            address = address.replace("www.", "")
        return address
