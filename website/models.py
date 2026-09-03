from django.db import models


class SiteSettings(models.Model):
    """Global site info shown in topbar, header, footer, reservation section.
    Only one row is used (singleton) — edit it from the admin panel."""

    site_name = models.CharField(max_length=100, default="Grilli")
    tagline = models.CharField(max_length=200, default="Amazing & Delicious Food")

    logo = models.ImageField(upload_to="site/", blank=True, null=True)
    favicon = models.ImageField(upload_to="site/", blank=True, null=True)

    address = models.CharField(max_length=255, default="Restaurant St, Delicious City, London 9578, UK")
    open_hours = models.CharField(max_length=100, default="Daily : 8.00 am to 10.00 pm")
    phone = models.CharField(max_length=30, default="+1 123 456 7890")
    phone_link = models.CharField(max_length=30, default="+11234567890", help_text="Digits only, used for tel: link")
    email = models.EmailField(default="booking@restaurant.com")

    navbar_open_hours = models.CharField(max_length=100, default="Open: 9.30 am - 2.30pm")
    booking_phone = models.CharField(max_length=30, default="+88-123-123456")
    booking_phone_link = models.CharField(max_length=30, default="+88123123456")

    reservation_lunch_time = models.CharField(max_length=100, default="Monday to Sunday, 11.00 am - 2.30pm")
    reservation_dinner_time = models.CharField(max_length=100, default="Monday to Sunday, 05.00 pm - 10.00pm")

    footer_background = models.ImageField(upload_to="site/", blank=True, null=True)
    footer_open_hours = models.CharField(max_length=100, default="Open : 09:00 am - 01:00 pm")
    newsletter_offer_text = models.CharField(max_length=100, default="Subscribe us & Get 25% Off.")
    copyright_text = models.CharField(max_length=255, default="© 2026 Grilli. All Rights Reserved")

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        # keep this a singleton: always overwrite the first row
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class HeroSlide(models.Model):
    subtitle = models.CharField(max_length=100, help_text="Small text above the title, e.g. 'Traditional & Hygiene'")
    title_line_1 = models.CharField(max_length=100)
    title_line_2 = models.CharField(max_length=100, blank=True)
    text = models.CharField(max_length=255, default="Come with family & feel the joy of mouthwatering food")
    button_text = models.CharField(max_length=50, default="View Our Menu")
    image = models.ImageField(upload_to="hero/")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.order}. {self.title_line_1}"


class ServiceCard(models.Model):
    """The 3 cards in the 'We Offer Top Notch' section (Breakfast, Appetizers, Drinks)."""
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="service/")
    link_text = models.CharField(max_length=50, default="View Menu")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class ServiceSection(models.Model):
    """The heading/intro text above the service cards."""
    subtitle = models.CharField(max_length=100, default="Flavors For Royalty")
    title = models.CharField(max_length=150, default="We Offer Top Notch")
    text = models.TextField(default="Lorem Ipsum is simply dummy text of the printing and typesetting industry.")

    class Meta:
        verbose_name = "Service Section (heading)"
        verbose_name_plural = "Service Section (heading)"

    def __str__(self):
        return "Service section heading"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class AboutSection(models.Model):
    subtitle = models.CharField(max_length=100, default="Our Story")
    title = models.CharField(max_length=150, default="Every Flavor Tells a Story")
    text = models.TextField(default="Lorem Ipsum is simply dummy text of the printing and typesetting industry.")
    call_phone = models.CharField(max_length=30, default="+80 (400) 123 4567")
    call_phone_link = models.CharField(max_length=30, default="+804001234567")
    banner_image = models.ImageField(upload_to="about/", blank=True, null=True)
    small_image = models.ImageField(upload_to="about/", blank=True, null=True)

    class Meta:
        verbose_name = "About Section"
        verbose_name_plural = "About Section"

    def __str__(self):
        return "About section"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SpecialDish(models.Model):
    subtitle = models.CharField(max_length=100, default="Special Dish")
    title = models.CharField(max_length=150, default="Lobster Tortellini")
    text = models.TextField(default="Lorem Ipsum is simply dummy text of the printing and typesetting industry.")
    old_price = models.DecimalField(max_digits=6, decimal_places=2, default=40.00)
    new_price = models.DecimalField(max_digits=6, decimal_places=2, default=20.00)
    banner_image = models.ImageField(upload_to="special-dish/", blank=True, null=True)

    class Meta:
        verbose_name = "Special Dish"
        verbose_name_plural = "Special Dish"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class MenuItem(models.Model):
    BADGE_CHOICES = [
        ("", "No badge"),
        ("New", "New"),
        ("Seasonal", "Seasonal"),
        ("Hot", "Hot"),
    ]
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="menu/")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    badge = models.CharField(max_length=20, choices=BADGE_CHOICES, blank=True, default="")
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    text = models.TextField()
    customer_name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    background_image = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.customer_name


class Feature(models.Model):
    """'Why Choose Us' cards."""
    title = models.CharField(max_length=100)
    icon = models.ImageField(upload_to="features/")
    text = models.CharField(max_length=255, default="Lorem Ipsum is simply dummy printing and typesetting.")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=100, help_text="e.g. 'Food, Flavour'")
    image = models.ImageField(upload_to="events/")
    date = models.DateField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class SocialLink(models.Model):
    name = models.CharField(max_length=50, help_text="e.g. Facebook, Instagram")
    url = models.URLField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


class Reservation(models.Model):
    """Saved when a visitor submits the 'Online Reservation' form."""
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    persons = models.CharField(max_length=20)
    reservation_date = models.DateField()
    reservation_time = models.CharField(max_length=20)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.reservation_date}"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-subscribed_at"]

    def __str__(self):
        return self.email
