# Engine pricing notes (internal, not for the calculator page)

Working figures as of 4 September 2026. Cost $0.001 per token (one audio second), list price $0.005, margin floor 60%, observed usage 15 audio hours per clinician per month.

## Recommendations

1. **Never price below the floor.** Cost / (1 - 0.60) = $0.0025 per token = $9.00 per audio hour. That is the number to protect in negotiation; it keeps 60% gross margin at any volume.
2. **Charge a platform fee plus a minimum monthly token commitment.** Per-token revenue ramps with the partner's rollout; a fixed cost to serve does not. The fee should at least equal the cost to serve so month one is profitable regardless of onboarding speed. This is the structural difference from the direct-to-user plan, which loses about $8 a month on any user who only uses the hours in the subscription.
3. **Lead with $0.005 for pilots.** $18.00 per audio hour, $270 per clinician a month at 15 hrs. Above six of the nine scribe seats in the comparison even at their highest reported price, and inside the enterprise band (Abridge $200 to $600, DAX Copilot $300 to $600, Suki $199 to $399, DeepScribe $300 to $500, all third-party reported). Right for a partner buying an engine for its own platform; too high for a partner reselling to individual clinicians.
4. **Offer a volume curve, not a discount.** Tiers at 100 / 80 / 60 / 50% of list, stopping at the floor: $0.005, $0.004, $0.003, $0.0025. At the Scale tier a clinician costs the partner $162 a month, which leaves room to resell inside a self-serve seat price ($79 to $160) with margin while Arvi keeps 67%.
5. **Sell the document, not the seconds.** Transcript-only medical speech APIs cost $0.26 to $4.50 per audio hour (Deepgram Nova-3 Medical, AssemblyAI Medical Mode, Corti, Amazon Transcribe Medical). A partner who benchmarks on raw transcription will call Arvi expensive. The comparison to lead with is a scribe seat converted to hours.
6. **Bill per token, quote per consult.** A 15-minute consult is $4.50 at list and $2.25 at the floor. Print both beside the per-token price with the conversion table (1 token = 1 s, 60 = 1 min, 3,600 = 1 hr).

## Token definition (recommended wording)

Token. Arvi's unit of metered usage for the Engine service. One token equals one second of audio accepted into a transcription job, rounded up to the next whole second per job, with a minimum of 15 tokens per job. Tokens are counted only for jobs that complete successfully. The token price is fixed for the term of the agreement and is inclusive of the compute, storage and cache resources Arvi consumes to transcribe the audio and generate the clinical document; those resources are not metered or invoiced separately.

## Source notes

Vendor pricing pages read on 4 September 2026: AWS (Transcribe Medical $0.075/min via the printed 15-minute example), Corti ($0.0065/min), AssemblyAI ($0.21/hr + $0.15/hr Medical Mode), Deepgram (Nova-3 Medical from $0.0043/min, launch post), Freed ($79 Core), Sunoh ($149 intro, $199 list), Lyrebird ($160 Pro, annual, AU).

No price published (pricing pages checked, no figures shown or page missing): Heidi, Nabla, Suki, DeepScribe, Abridge, DAX Copilot. Third-party figures disagree, so the page shows the range and links each source with the figure it states: Keragon, VoiceboxMD, Commure (pricing guide April 2026 and Heidi review), Freed cost guide (July 2026).

## Measured Azure AI cost per audio hour (app, direct-to-user)

| Month | Azure AI services bill | Hours used | Cost per hour |
|---|---|---|---|
| June 2026 | | | AUD 2.33 |
| July 2026 | $257.30 | 92.65 | about $2.70 |
| August 2026 | $185.26 | 57.69 | about $3.20 |

Planning assumption: **AUD 3.30 per hour**, chosen above the observed range to be safe. Per audio second that is AUD 0.00092, so the engine's $0.001 per token cost assumption holds with little headroom.

Reconciles the cost-per-user summary (cost_per_user_analysis copy 2.md): the AUD 39.60 Azure line at 17 hours is June's actual 2.33/hr (2.33 x 17 = 39.61); the AUD 3.33 x visible hrs row is the safe planning rate. At 3.30/hr the 17-hour user costs AUD 56.10 + 15.40 add-ons = about AUD 71.50 before the shared AUD 2,000 floor.

## Cost per user by user band (from cost_per_user_analysis, June 2026 average of 17 visible hrs/user, AUD)

| | 1–50 | 50–100 | 100–500 | 500–1,000 |
|---|---|---|---|---|
| Fixed floor (shared, per month) | 2,000 | 2,000 | 2,000 | 2,000 |
| Pusher plan upgrade | none | none | +77/month at 143 users | +385/month at 572 users |
| Azure per user | 3.33 x visible hrs (planning); June actual 2.33/hr | same | same | same |
| Redis per user | 15.40 | 15.40 | 15.40 | 15.40 |
| GCP resources per user added within band | 0 | 0 | 0.23 | 0.69 |
| Pusher amortised per user | 0 | 0 | 0.19 | 0.77 |
| Fixed add-ons per user | 15.40 | 15.40 | 15.82 | 16.86 |
| Total per user at 17 hrs (June actual rate, floor excluded) | 55.00 | 55.00 | 55.42 | 56.46 |

Clarified 4 September 2026:
- Azure per-hour rate comes from the Azure AI services bills only (variable). June 2.33 actual; 3.30 is the planning rate.
- Redis 15.40 per user stays as modelled for now; Isuru will say if it should move off the per-user band.
- GCP and Pusher "per user within a band" are resource step costs needed to serve that scale, not true per-user charges; they are amortised across the band.
- The 2,000 floor is a fixed monthly amount shared across users: per user it is 2,000 / users, and per user-hour it is 2,000 / (users x 17). So 117.65 per hour for a single user, 1.18 per hour at 100 users, 0.12 per hour at 1,000 users. The per-user share falls as users are added.

## Calculator moved to the per-hour cost structure (4 September 2026)

Application inputs are now: Azure AI cost per audio hour (3.30 planning), fixed add-ons per user (15.40, auto-stepping to 15.82 at 100 users and 16.86 at 500), shared floor 2,000 spread over active users, average usage 17 hrs, top-ups derived in whole 10-hour packs. All-in cost per user-hour = total per user / hours.

Result at defaults (100 users, 17 hrs): revenue 69.98, Azure 56.10, add-ons 15.82, contribution -1.94 before the floor; all-in 91.92 per user (5.41 per hour) including the 20.00 floor share. Top-up hour margin is only 0.70 (4.00 - 3.30). At June's actual 2.33/hr the same user contributes +14.55, so the planning rate is what decides whether the app breaks even.
