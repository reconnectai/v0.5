# Reconnect.ai (v0.5)

Welcome to **Reconnect.ai**, an open-source AI-powered app for creating and chatting with digital *Personae*—twins of real or imagined beings. Built to run locally (for now) with a WordPress frontend and a FastAPI backend, this is our scrappy v0.5 prototype. AGPL 3.0 all the way—share it, tweak it, join the ride!

## What’s This?
Reconnect.ai lets you:
- Craft *Personae* from text Artifacts (ASCII, Word, PDFs for now—more later).
- Chat with them via an LLM (Ollama locally, maybe cloud later).
- Manage it all with a WordPress UI (membership, subscriptions) on Hostinger.

Think digital companions, role-playing characters, or even a “diary” Persona—v0.5’s the first stab, rough but real.

## Stack
- **Frontend**: WordPress on Hostinger (MemberPress, WooCommerce, custom plugin).
- **Backend**: FastAPI server (local, Ngrok-tunneled), Postgres with `pgvector` for Vectors + Metadata.
- **LLM**: Ollama (local for now—your beefy PC’s the star).
- **Sync**: WP owns membership; FastAPI mirrors it via CRUD APIs.

## Getting Started
1. **Clone It**: `git clone https://github.com/reconnectai/v0.5.git`
2. **Ngrok**: Tunnel your local FastAPI—`ngrok http 5000` (free tier, ~$5/mo for static).
3. **FastAPI**: Spin it up—`cd server && uvicorn main:app --host 0.0.0.0 --port 5000`.
4. **WordPress**: Hostinger WP calls `https://your-ngrok-url` (plugin WIP).
5. **Play**: Upload a text file, make a Persona, chat away.

*Details in `/docs` soon—bear with us!*

## Roadmap
- **v0.5 (March-May 2025)**: Text-only Personae, local dev, WP prototype.
- **v0.9 (June-Aug 2025)**: HTML scraping (X profiles?), UI polish.
- **1.0+**: Full cloud, sharing Personae—sky’s the limit.

Check `docs/roadmap.md` (coming soon) for the gritty details.

## License
Reconnect.ai is AGPL 3.0—free as in freedom. See `LICENSE` for the full text. Fork it, hack it, share it—just keep it open.

## Contributing
Solo dev for now (grey-hair ‘80s OSS vet), but pull requests welcome once we’re rolling. Issues? File ‘em. Ideas? Yell.

## Shoutouts
- Grok (xAI) for the AI assist—my co-pilot’s a beast.
- You, for poking this repo—let’s reconnect the world!

---
*Last tweak: March 3, 2025*