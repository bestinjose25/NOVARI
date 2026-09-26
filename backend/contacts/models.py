from django.db import models


class ContactRequest(models.Model):

    name = models.CharField(
        max_length=150
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=50,
        blank=True
    )

    message = models.TextField()

    consent_accepted = models.BooleanField(
        default=False
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    class Meta:
        ordering = ['-created_at']


    def __str__(self):
        return f"{self.name} - {self.email}"
