# Torque Tales — Django Admin Guide

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
| **Special Dish**        | Featured section (title, description, image/video)     |
| **Menu Items**          | Poora "Delicious Menu" (title, price, badge, image, description) |
| **Testimonials**        | Customer review + avatar + background                  |
| **Features**            | "Why Choose Us" 4 cards                                |
| **Events**              | "Upcoming Event" cards                                  |
| **Social Links**        | Footer ke social media links                            |
| **Reservations**        | Website ke "Online Reservation" form se aaye submissions yahin dikhte hain |
| **Newsletter Subscribers** | Footer ke email subscribe form se aaye emails yahin dikhte hain |

## Image ya Video kaise select karein

Image/Video option in sections mein diya gaya hai:

- Hero Slides
- Service Cards
- About Section ka main banner
- Special Dish banner
- Testimonials ka background
- Events

Admin panel mein section open karein:

1. **Media type** mein `Image` ya `Video` select karein.
2. Image select karne par sirf image upload field dikhegi.
3. Video select karne par sirf video upload field dikhegi.
4. File upload karke **Save** karein.
5. Selected media hi website par dikhega. Purana inactive upload record se clear ho jayega.

Video ke liye MP4 recommended hai. MP4, WebM aur OGG supported hain. Maximum file size 50 MB hai. Website videos muted, autoplay, loop aur mobile-friendly mode mein play hoti hain.

Logo, favicon, menu thumbnails, feature icons, about ki small image aur customer avatar image-only rakhe gaye hain.

Naye items add karne ke liye (jaise naya menu item, naya event, naya slide) — us section mein jaake "Add" button dabaiye. Order badalne ke liye "order" number set karein (chhota number pehle dikhega). "is_active" uncheck karke kisi item ko site se hide kar sakte hain bina delete kiye.

## Images

Saari images `media/` folder mein save hoti hain jab aap admin se upload karte hain. Production mein deploy karte waqt `MEDIA_ROOT`/`MEDIA_URL` ko apne server (ya S3 jaisi storage) ke hisaab se configure karna hoga — abhi ye Django ka development server hi serve karta hai.

Vercel par admin se upload ki gayi images/videos permanent store nahi hoti. Live admin uploads ke liye Cloudinary ya S3 jaisi external media storage zaroor configure karein.

## Production ke liye zaroori

Deploy karne se pehle:
1. `mysite/settings.py` mein `SECRET_KEY` badal dein aur environment variable se lein.
2. `DEBUG = False` karein aur `ALLOWED_HOSTS` set karein.
3. SQLite ki jagah PostgreSQL/MySQL use karna better hoga bade traffic ke liye.
4. Static/media files ko properly serve karne ke liye Nginx/WhiteNoise/S3 setup karein.
