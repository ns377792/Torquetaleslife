# Vercel Deploy Fix — kaise lagayein

Ye zip mein 4 files hain:
- `requirements.txt` (naya, repo root mein)
- `vercel.json` (naya, repo root mein)
- `mysite/wsgi.py` (existing file ka updated version)
- `mysite/settings.py` (existing file ka updated version — sirf ALLOWED_HOSTS line badli hai)

## Lagane ka tarika

1. Is zip ko extract karein.
2. Extract ki hui saari files/folders ko apne local git repo folder ke andar copy-paste karein (jahan `manage.py` hai) — jab pooche "replace existing files?" to **Yes/Replace** karein, kyunki `mysite/wsgi.py` aur `mysite/settings.py` already exist karti hain.
3. Terminal mein apne repo folder ke andar:

```bash
git add requirements.txt vercel.json mysite/wsgi.py mysite/settings.py
git commit -m "Add Vercel deployment config"
git push
```

4. Push karte hi Vercel automatically naya deployment start kar dega (agar auto-deploy on hai). Ya Vercel dashboard mein "Redeploy" dabayein.

## ⚠️ Zaroori baat — Admin panel se edit karna

Vercel serverless hai — iska matlab har request ke liye filesystem **fresh/temporary** hota hai. Isse:

- SQLite database (`db.sqlite3`) mein admin panel se kiya gaya koi bhi change (menu edit, reservation, naya subscriber) **permanently save nahi hoga** — deployment refresh hote hi wapas purani state pe chala jayega.
- Admin panel se upload ki gayi nayi images bhi **persist nahi hongi**.

Matlab: site dikhegi bilkul theek, lekin agar aap Vercel pe admin panel se live content edit karna chahte ho (jo aapki original requirement thi), to database ko ek **external hosted database** (jaise Neon, Supabase, ya Vercel Postgres — sab ke free tier available hain) se connect karna padega, aur images ke liye Cloudinary/S3 jaisi external storage.

Agar chahen to main ye external database + storage setup bhi kara sakta hoon — bata dijiye.
