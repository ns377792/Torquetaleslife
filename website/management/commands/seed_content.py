import shutil
from pathlib import Path
from django.core.files import File
from django.core.management.base import BaseCommand
from django.conf import settings

from website.models import (
    SiteSettings, HeroSlide, ServiceCard, ServiceSection, AboutSection,
    SpecialDish, MenuItem, Testimonial, Feature, Event, SocialLink,
)

IMG_DIR = Path(settings.BASE_DIR) / "website" / "static" / "website" / "assets" / "images"


def img_file(name):
    path = IMG_DIR / name
    return File(open(path, "rb"), name=name) if path.exists() else None


class Command(BaseCommand):
    help = "Seed the database with the original site content so the admin panel and homepage aren't empty."

    def handle(self, *args, **options):
        # SiteSettings
        site = SiteSettings.load()
        if not site.logo:
            f = img_file("logo.svg")
            if f:
                site.logo.save("logo.svg", f, save=False)
        if not site.favicon:
            fav_path = Path(settings.BASE_DIR) / "website" / "static" / "website" / "favicon.svg"
            if fav_path.exists():
                site.favicon.save("favicon.svg", File(open(fav_path, "rb"), name="favicon.svg"), save=False)
        if not site.footer_background:
            f = img_file("footer-bg.jpg")
            if f:
                site.footer_background.save("footer-bg.jpg", f, save=False)
        site.save()
        self.stdout.write(self.style.SUCCESS("SiteSettings ready"))

        # HeroSlides
        if not HeroSlide.objects.exists():
            slides = [
                dict(subtitle="Tradational & Hygine", title_line_1="For the love of", title_line_2="delicious food",
                     image="hero-slider-1.jpg", order=1),
                dict(subtitle="delightful experience", title_line_1="Flavors Inspired by", title_line_2="the Seasons",
                     image="hero-slider-2.jpg", order=2),
                dict(subtitle="amazing & delicious", title_line_1="Where every flavor", title_line_2="tells a story",
                     image="hero-slider-3.jpg", order=3),
            ]
            for s in slides:
                f = img_file(s.pop("image"))
                slide = HeroSlide(**s)
                if f:
                    slide.image.save(f.name, f, save=False)
                slide.save()
        self.stdout.write(self.style.SUCCESS("HeroSlides ready"))

        # ServiceSection + ServiceCards
        ServiceSection.load()
        if not ServiceCard.objects.exists():
            cards = [
                dict(title="Breakfast", image="service-1.jpg", order=1),
                dict(title="Appetizers", image="service-2.jpg", order=2),
                dict(title="Drinks", image="service-3.jpg", order=3),
            ]
            for c in cards:
                f = img_file(c.pop("image"))
                card = ServiceCard(**c)
                if f:
                    card.image.save(f.name, f, save=False)
                card.save()
        self.stdout.write(self.style.SUCCESS("ServiceCards ready"))

        # About
        about = AboutSection.load()
        if not about.banner_image:
            f = img_file("about-banner.jpg")
            if f:
                about.banner_image.save("about-banner.jpg", f, save=False)
        if not about.small_image:
            f = img_file("about-abs-image.jpg")
            if f:
                about.small_image.save("about-abs-image.jpg", f, save=False)
        about.save()
        self.stdout.write(self.style.SUCCESS("AboutSection ready"))

        # Special dish
        dish = SpecialDish.load()
        if not dish.banner_image:
            f = img_file("special-dish-banner.jpg")
            if f:
                dish.banner_image.save("special-dish-banner.jpg", f, save=False)
        dish.save()
        self.stdout.write(self.style.SUCCESS("SpecialDish ready"))

        # Menu items
        if not MenuItem.objects.exists():
            items = [
                dict(title="Greek Salad", image="menu-1.png", price=25.50, badge="Seasonal",
                     description="Tomatoes, green bell pepper, sliced cucumber onion, olives, and feta cheese.", order=1),
                dict(title="Lasagne", image="menu-2.png", price=40.00, badge="",
                     description="Vegetables, cheeses, ground meats, tomato sauce, seasonings and spices", order=2),
                dict(title="Butternut Pumpkin", image="menu-3.png", price=10.00, badge="",
                     description="Typesetting industry lorem Lorem Ipsum is simply dummy text of the priand.", order=3),
                dict(title="Tokusen Wagyu", image="menu-4.png", price=39.00, badge="New",
                     description="Vegetables, cheeses, ground meats, tomato sauce, seasonings and spices.", order=4),
                dict(title="Olivas Rellenas", image="menu-5.png", price=25.00, badge="",
                     description="Avocados with crab meat, red onion, crab salad stuffed red bell pepper and green bell pepper.", order=5),
                dict(title="Opu Fish", image="menu-6.png", price=49.00, badge="",
                     description="Vegetables, cheeses, ground meats, tomato sauce, seasonings and spices", order=6),
            ]
            for it in items:
                f = img_file(it.pop("image"))
                item = MenuItem(**it)
                if f:
                    item.image.save(f.name, f, save=False)
                item.save()
        self.stdout.write(self.style.SUCCESS("MenuItems ready"))

        # Testimonial
        if not Testimonial.objects.exists():
            t = Testimonial(
                text="I wanted to thank you for inviting me down for that amazing dinner the other night. "
                     "The food was extraordinary.",
                customer_name="Sam Jhonson",
                order=1,
            )
            f = img_file("testi-avatar.jpg")
            if f:
                t.avatar.save("testi-avatar.jpg", f, save=False)
            bg = img_file("testimonial-bg.jpg")
            if bg:
                t.background_image.save("testimonial-bg.jpg", bg, save=False)
            t.save()
        self.stdout.write(self.style.SUCCESS("Testimonial ready"))

        # Features
        if not Feature.objects.exists():
            feats = [
                dict(title="Hygienic Food", icon="features-icon-1.png", order=1),
                dict(title="Fresh Environment", icon="features-icon-2.png", order=2),
                dict(title="Skilled Chefs", icon="features-icon-3.png", order=3),
                dict(title="Event & Party", icon="features-icon-4.png", order=4),
            ]
            for feat in feats:
                f = img_file(feat.pop("icon"))
                feature = Feature(**feat)
                if f:
                    feature.icon.save(f.name, f, save=False)
                feature.save()
        self.stdout.write(self.style.SUCCESS("Features ready"))

        # Events
        if not Event.objects.exists():
            events = [
                dict(title="Flavour so good you'll try to eat with your eyes.", subtitle="Food, Flavour",
                     image="event-1.jpg", date="2026-09-15", order=1),
                dict(title="Flavour so good you'll try to eat with your eyes.", subtitle="Healthy Food",
                     image="event-2.jpg", date="2026-09-08", order=2),
                dict(title="Flavour so good you'll try to eat with your eyes.", subtitle="Recipie",
                     image="event-3.jpg", date="2026-09-03", order=3),
            ]
            for ev in events:
                f = img_file(ev.pop("image"))
                event = Event(**ev)
                if f:
                    event.image.save(f.name, f, save=False)
                event.save()
        self.stdout.write(self.style.SUCCESS("Events ready"))

        # Social links
        if not SocialLink.objects.exists():
            socials = [
                ("Facebook", "https://facebook.com", 1),
                ("Instagram", "https://instagram.com", 2),
                ("Twitter", "https://twitter.com", 3),
                ("Youtube", "https://youtube.com", 4),
                ("Google Map", "https://maps.google.com", 5),
            ]
            for name, url, order in socials:
                SocialLink.objects.create(name=name, url=url, order=order)
        self.stdout.write(self.style.SUCCESS("SocialLinks ready"))

        self.stdout.write(self.style.SUCCESS("\nAll done! Your homepage content is now in the database."))
