# Grilli — Django Admin Guide

## Chalane ke liye

```bash
unzip mysite_django.zip
cd mysite
pip install django Pillow
python manage.py runserver
```

Browser mein kholiye: http://127.0.0.1:8000/

## Admin Panel

URL: http://127.0.0.1:8000/admin/

Default login (isse turant badal lein):
- Username: `admin`
- Password: `admin12345`

Password change karne ke liye:
```bash
python manage.py changepassword admin
```

Ya naya superuser banane ke liye:
```bash
python manage.py createsuperuser
```

## Admin se kya-kya edit ho sakta hai

Har section database se aata hai, isliye admin panel se change karte hi website pe turant reflect hoga (refresh karne par):

| Admin Section          | Website pe kahan dikhta hai                          |
|-------------------------|-------------------------------------------------------|
| **Site Settings**       | Logo, favicon, address, phone, email, footer info (singleton — ek hi entry) |
| **Hero Slides**         | Homepage ka top slider (images, titles, text, button) |
| **Service Section**     | "We Offer Top Notch" heading text                     |
| **Service Cards**       | Breakfast / Appetizers / Drinks cards                  |
| **About Section**       | "Our Story" section (text, images, phone)              |
| **Special Dish**        | Lobster Tortellini section (title, price, image)       |
| **Menu Items**          | Poora "Delicious Menu" (title, price, badge, image, description) |
| **Testimonials**        | Customer review + avatar + background                  |
| **Features**            | "Why Choose Us" 4 cards                                |
| **Events**              | "Upcoming Event" cards                                  |
| **Social Links**        | Footer ke social media links                            |
| **Reservations**        | Website ke "Online Reservation" form se aaye submissions yahin dikhte hain |
| **Newsletter Subscribers** | Footer ke email subscribe form se aaye emails yahin dikhte hain |

Naye items add karne ke liye (jaise naya menu item, naya event, naya slide) — us section mein jaake "Add" button dabaiye. Order badalne ke liye "order" number set karein (chhota number pehle dikhega). "is_active" uncheck karke kisi item ko site se hide kar sakte hain bina delete kiye.

## Images

Saari images `media/` folder mein save hoti hain jab aap admin se upload karte hain. Production mein deploy karte waqt `MEDIA_ROOT`/`MEDIA_URL` ko apne server (ya S3 jaisi storage) ke hisaab se configure karna hoga — abhi ye Django ka development server hi serve karta hai.

## Production ke liye zaroori

Deploy karne se pehle:
1. `mysite/settings.py` mein `SECRET_KEY` badal dein aur environment variable se lein.
2. `DEBUG = False` karein aur `ALLOWED_HOSTS` set karein.
3. SQLite ki jagah PostgreSQL/MySQL use karna better hoga bade traffic ke liye.
4. Static/media files ko properly serve karne ke liye Nginx/WhiteNoise/S3 setup karein.
