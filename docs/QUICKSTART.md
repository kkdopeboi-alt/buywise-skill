# First comparison quickstart

## Install into your agent

With Node.js/npm available, use the upstream skills CLI:

```sh
npx skills add kkdopeboi-alt/buywise-skill --skill buywise
```

Select your host and installation scope when prompted. For a project-local Codex copy:

```sh
npx skills add kkdopeboi-alt/buywise-skill --skill buywise --agent codex --copy
```

No browser, merchant credentials or payment permission is added by installation. Restart/reload your host if necessary. CLI support for copying a folder is different from verifying the agent's live shopping performance. The third-party skills CLI may collect aggregate install telemetry; opt out using DISABLE_TELEMETRY=1 or DO_NOT_TRACK=1 as documented upstream. BuyWise itself has no telemetry.

Manual alternative: download the repository ZIP and copy the complete skills/buywise directory into your host's documented skill folder. Preserve references and scripts. Do not replace an existing customized copy without reviewing changes.

## Try research only

```text
Use BuyWise to compare new video-call headsets under USD 100 all-in.
Ship to US ZIP 10001. Windows laptop. No subscriptions or new memberships.
Use available browser/search tools. Ask any missing critical questions.
Research only; do not purchase.
```

Expected shape: one leading choice and at most two useful alternatives; exact variant/seller, cost status, delivery evidence, downside, source link and check time. It must not invent tax/shipping or claim an order was placed.

If the host has no browsing/search, provide public source material or run the offline demo instead. Do not describe offline data as current merchant information.

## No agent needed: offline demo

After downloading/cloning the repo, with Python 3.10+:

```sh
python scripts/demo.py
```

It shows missing fit/location questions, unknown shipping and a wrong-variant rejection using fictional data. No API key, account or payment is required. It demonstrates helper decisions, not a comparison against a measured baseline Bot.

## Send useful feedback

Use the [feedback form](https://github.com/kkdopeboi-alt/buywise-skill/issues/new?template=usage-feedback.md). Tell us your host, whether first use worked, and one redacted failure. Feedback is public; never include addresses or credentials. One real failure is more useful than an unsupported “works on every Bot” claim.

Upstream install documentation: https://github.com/vercel-labs/skills and https://skills.sh/docs.
