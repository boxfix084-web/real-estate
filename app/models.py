from django.db import models
from django.contrib.auth.models import User


class Property(models.Model):

    PROPERTY_TYPES = [
        ('Apartment', 'Apartment'),
        ('Villa', 'Villa'),
        ('House', 'Independent House'),
        ('Plot', 'Plot'),
        ('Commercial', 'Commercial'),
    ]

    PURPOSE_CHOICES = [
        ('Sale', 'Sale'),
        ('Rent', 'Rent'),
    ]

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='properties'
    )

    title = models.CharField(max_length=200)

    property_type = models.CharField(
        max_length=30,
        choices=PROPERTY_TYPES
    )

    purpose = models.CharField(
        max_length=20,
        choices=PURPOSE_CHOICES
    )

    location = models.CharField(max_length=200)

    city = models.CharField(max_length=100)

    price = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    bedrooms = models.PositiveIntegerField(
        default=0
    )

    bathrooms = models.PositiveIntegerField(
        default=0
    )

    area = models.PositiveIntegerField(
        help_text="Area in square feet"
    )

    description = models.TextField()

    image = models.ImageField(
        upload_to='properties/',
        blank=True,
        null=True
    )

    is_featured = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class SavedProperty(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('user', 'property')

    def __str__(self):
        return f"{self.user.username} - {self.property.title}"