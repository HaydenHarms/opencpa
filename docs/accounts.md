# Accounts (roadmap step 7)

Students can sign in with GitHub or an emailed link. Signing in moves the progress on that device into the account, so it follows the student to every device. Signing in is optional: a signed-out browser keeps its anonymous device id, as before.

## How it works

- **Code:** `apps/api/src/auth.ts` (routes under `/auth`, the merge, session lookup), migration `0006_accounts.sql`, `apps/web/src/pages/Account.tsx` (`/account`, `/signin/done`, `/signin/email`) and the token handling in `apps/web/src/api.ts`.
- **No cookies.** The web app (`pages.dev`) and the API (`workers.dev`) are different sites, so browsers would block the API's cookies. Signing in ends with the browser holding a random session token in `localStorage`, sent as `Authorization: Bearer <token>`. Only its SHA-256 hash is stored (`auth_sessions`). A session lasts 180 days from its last use.
- **An account is a `users` row** with `github_id` and/or `email` set (the columns existed since 0001). Anonymous device ids are `users` rows with neither. `/me/*` accepts a session token, or, signed out, `X-OpenCPA-User`. A device id that belongs to an account is refused, so an account is reachable only through a session.
- **Moving progress in (`mergeInto`).** When a device signs in, its attempts, practice sessions and Claude connector link move to the account, then the device row is deleted. Where both have a review card for the same item, the more recently reviewed one wins. Where both have an unfinished session in the same section (or Library topic), the older one is abandoned. Its answers still count. The account keeps its own connector link if it has one. After signing in or out, the browser starts a fresh device id.
- **GitHub:** `POST /auth/github/start` (from the web app, with the device id) stores a single-use `state` and returns GitHub's consent URL. GitHub redirects to `GET /auth/github/callback` on the API, which looks up or creates the account and sends the browser back to `<web origin>/signin/done#code=…`. The web app swaps that one-time code (valid for 2 minutes) for a session at `POST /auth/exchange`. The callback is on the API, not the web app, so a single GitHub OAuth app serves production, preview deployments and localhost (the return origin must be in `ALLOWED_ORIGINS`). The scope is `user:email`. If the student's primary verified GitHub email matches an email account, GitHub is linked to that account instead of creating a new one.
- **Email:** `POST /auth/email/start {email}` emails a link to `<web origin>/signin/email#token=…`, valid once for 15 minutes. The page asks for a click before it posts the token to `POST /auth/email/verify`, so mail scanners that open links can't use it up. The device that clicks is the one whose progress moves in. Limits: 3 links per address per 15 minutes and 90 a day site-wide (Resend's free tier is 100 a day).
- `GET /auth/status` reports which providers are set up and the signed-in account. `POST /auth/signout` deletes the session. The web app hides any provider that isn't set up.

## Setting it up (Hayden)

Until the secrets below exist, both buttons stay hidden and the site works exactly as before.

### GitHub sign-in

1. On github.com, click your profile photo (top right) → **Settings**.
2. At the bottom of the left sidebar, click **Developer settings** → **OAuth Apps** → **New OAuth App**.
3. Fill in:
   - **Application name:** `OpenCPA`
   - **Homepage URL:** `https://opencpa.pages.dev`
   - **Authorization callback URL:** `https://opencpa-api.haydenharms.workers.dev/auth/github/callback`
   - Leave **Enable Device Flow** unchecked. Click **Register application**.
4. On the app's page, copy the **Client ID**. Click **Generate a new client secret** and copy the secret; GitHub shows it only once.
5. In the Cloudflare dashboard: **Workers & Pages** → **opencpa-api** → **Settings** → **Variables and Secrets** → **+ Add**.
   - **Type:** `Secret`, **Variable name:** `GITHUB_CLIENT_ID`, **Value:** the Client ID.
   - Click **+ Add** again: **Type:** `Secret`, **Variable name:** `GITHUB_CLIENT_SECRET`, **Value:** the secret.
   - Click **Deploy**.
   - `wrangler.toml` sets `keep_vars = true`, so CI deploys keep dashboard variables too: the Client ID can be a plain **Variable** (it isn't secret; it appears in every sign-in URL), but the client secret must be a **Secret**.
6. Open https://opencpa.pages.dev/account. The **Continue with GitHub** button should appear.

### Email sign-in

Email needs a sending service, and every free one needs a domain you own: `pages.dev` and `workers.dev` belong to Cloudflare. So email sign-in waits for the custom domain (roadmap step 8). Once there is a domain:

1. Sign up at https://resend.com (free: 3,000 emails a month, 100 a day).
2. **Domains** → **Add Domain** → enter the domain → add the DNS records Resend shows. If the domain is on Cloudflare, Resend can add them for you. Wait until the domain shows **Verified**.
3. **API Keys** → **Create API Key** → name `opencpa`, permission **Sending access** → copy the key.
4. In Cloudflare (**opencpa-api** → **Settings** → **Variables and Secrets**), add two **Secrets**: `RESEND_API_KEY` (the key) and `EMAIL_FROM` (for example `OpenCPA <signin@yourdomain.com>`). Click **Deploy**.

Before then, Resend's test sender (`EMAIL_FROM` = `OpenCPA <onboarding@resend.dev>`) can deliver only to the address on your Resend account. That's enough to try the flow yourself, not to open it to students.

### Local development

Put the same variables in `apps/api/.dev.vars`, which is gitignored. For GitHub, register a second OAuth app with the callback `http://localhost:8787/auth/github/callback`.

## Not done yet

- Deleting an account (and its data) from the Account page.
- The Claude connector still uses its link token. Replacing it with OAuth tied to the account was noted as a later step in roadmap step 2.
- Rate limiting beyond the email limits: that's part of roadmap step 8.
