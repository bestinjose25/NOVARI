from django.db import models


class QuoteRequest(models.Model):

    SERVICE_CHOICES = [
        ('residential_move', 'Residential move'),
        ('business_move', 'Business move'),
        ('furniture_transport', 'Furniture transport'),
        ('furniture_assembly', 'Furniture assembly / disassembly'),
        ('household_clearance', 'Household clearance'),
        ('carrying_assistance', 'Carrying assistance'),
        ('handyman', 'Small job / handyman'),
        ('not_sure', 'Not sure yet'),
    ]

    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('quoted', 'Quote sent'),
        ('closed', 'Closed'),
    ]

    # ----------------------------
    # Personal information
    # ----------------------------

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    email = models.EmailField()

    phone = models.CharField(max_length=50)

    service = models.CharField(
        max_length=50,
        choices=SERVICE_CHOICES
    )


    # ----------------------------
    # Pickup information
    # ----------------------------

    pickup_address = models.CharField(
        max_length=255,
        blank=True
    )

    pickup_city = models.CharField(
        max_length=100,
        blank=True
    )

    pickup_postal_code = models.CharField(
        max_length=20,
        blank=True
    )

    pickup_floor = models.CharField(
        max_length=30,
        blank=True
    )

    pickup_elevator = models.BooleanField(
        default=False
    )


    # ----------------------------
    # Destination
    # ----------------------------

    destination_address = models.CharField(
        max_length=255,
        blank=True
    )

    destination_city = models.CharField(
        max_length=100,
        blank=True
    )

    destination_postal_code = models.CharField(
        max_length=20,
        blank=True
    )

    destination_floor = models.CharField(
        max_length=30,
        blank=True
    )

    destination_elevator = models.BooleanField(
        default=False
    )


    # ----------------------------
    # Moving details
    # ----------------------------

    preferred_date = models.DateField(
        null=True,
        blank=True
    )

    items = models.CharField(
        max_length=500,
        blank=True
    )

    notes = models.TextField(
        blank=True
    )


    # ----------------------------
    # Consent / administration
    # ----------------------------

    consent_accepted = models.BooleanField(
        default=False
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
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
        return (
            f"{self.first_name} "
            f"{self.last_name} - "
            f"{self.get_service_display()}"
        )


class QuoteAttachment(models.Model):

    quote = models.ForeignKey(
        QuoteRequest,
        on_delete=models.CASCADE,
        related_name='attachments'
    )

    file = models.FileField(
        upload_to='quote_uploads/%Y/%m/'
    )

    original_name = models.CharField(
        max_length=255
    )

    content_type = models.CharField(
        max_length=100,
        blank=True
    )

    file_size = models.PositiveBigIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.original_name