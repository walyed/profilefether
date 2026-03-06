# ig-proxy

Instagram profile picture proxy for instacontest. Deployed on Railway.

## Deploy to Railway

1. Push this repo to GitHub
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Select this repo
4. Add environment variable: `PROXY_SECRET` = `instacontest-proxy-2026`
5. Deploy — Railway gives you a URL like `https://ig-proxy-production-xxxx.up.railway.app`
6. In Vercel (instacontest): Settings → Environment Variables → `IG_PROXY_URL` = that Railway URL
7. Redeploy instacontest on Vercel

## Test

```
curl https://YOUR-RAILWAY-URL/health
curl -H "x-proxy-secret: instacontest-proxy-2026" "https://YOUR-RAILWAY-URL/api/instagram?username=leomessi"
```
