# First ten real users: a 14-day experiment

Start: 2026-10-17. This is a plan and a record of completed repository improvements, not scheduled autonomous outreach. Targets below are hypotheses, not forecasts.

## Positioning

Audience: people already using an agent with browsing/search who need physical-product comparisons. Start with exact-model electronics/accessories, rather than promising all-category automatic purchasing. Message: “Your agent should not compare the wrong variant, omit shipping, or guess a gift recipient's size.”

## Funnel and decision rules

| Stage | Measure | Decision |
|---|---|---|
| Discovery | GitHub unique visitors and referring sources | Low visits: improve channel/content, not add more features |
| Installation | Voluntary first-use reports; optional third-party directory install aggregate | Visits with install failures: fix setup before promotion |
| Activation | A real user's first completed research comparison | Installed but no useful result: examine tool prerequisites/output |
| Retention | User reports a second distinct task within 7 days | One-off curiosity without repeats: narrow the recurring use case |
| Quality | Wrong variant/cost/fit and missing critical-question reports | Fix critical failures before increasing reach |

Stars are a secondary signal. Clones can include CI/scanners; directory installs can include tests/reinstalls; neither equals an active user. No hidden shopping telemetry is introduced. Don't sum overlapping 14-day traffic windows. Keep owner-only traffic snapshots private.

## Execution

**Days 1–2:** install instructions, fictional runnable demo, feedback/bug forms, topics, release with honest limits. Run clean-directory installation with telemetry disabled; record network failures distinctly from skill failures.

**Days 3–5:** share one short demo in one community that explicitly permits self-promotion, after the account owner approves destination and text. Ask for a redacted failure, not a star. Use normal channel attribution in voluntary feedback; don't buy stars or spam issues/DMs.

**Days 6–7:** aim for 5 completed first-use reports. If 30 qualified visits produce no first use, watch/collect installation steps before adding functionality. These thresholds are experiment triggers, not statistical proof.

**Days 8–14:** aim for 10 distinct testers, 5 completed comparisons and 3 users returning for a second task. Prioritize the most common blocker; only then add one requested host integration. Publish a concise report distinguishing known results, unknowns and failed attempts.

## Channels

1. GitHub search: accurate topics, searchable description, installation/demo above the fold.
2. Skills CLI/directory: valid SKILL.md and easy install command. According to the upstream FAQ, organic installations can cause directory listing automatically. Do not repeatedly self-install to manufacture ranking; a listing is not guaranteed or claimed until verified.
3. Agent-host communities: only the host actually tested; check current self-promotion rules immediately before sharing.
4. Technical tutorial: one concrete failure and reproducible fix, with synthetic data clearly labeled.

External posts and invitations are drafts until the owner chooses a destination and authorizes sending. No advertising budget, cross-post campaign or recurring automation has been started.

## Sources checked 2026-10-17

- https://skills.sh/docs/faq — directory discovery and install signals.
- https://github.com/vercel-labs/skills — CLI installation and telemetry opt-out.
- https://docs.github.com/en/repositories/viewing-activity-and-data-for-your-repository/viewing-traffic-to-a-repository — traffic window and limits.
