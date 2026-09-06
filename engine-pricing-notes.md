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
| June 2026 | $396.00 | 169.89 | AUD 2.33 |
| July 2026 | $257.30 | 92.65 | about $2.70 |
| August 2026 | $185.26 | 57.69 | about $3.20 |

Planning assumption: **AUD 3.33 per hour**, chosen above the observed range to be safe. Per audio second that is AUD 0.00093, so the engine's $0.001 per token cost assumption holds with little headroom.

Reconciles the cost-per-user summary (cost_per_user_analysis copy 2.md): the AUD 39.60 Azure line at 17 hours is June's actual 2.33/hr (2.33 x 17 = 39.61); the AUD 3.33 x visible hrs row is the safe planning rate. At 3.33/hr the 17-hour user costs AUD 56.61 + 15.40 add-ons = about AUD 72.01 before the shared AUD 2,000 floor.

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
- Azure per-hour rate comes from the Azure AI services bills only (variable). June 2.33 actual; 3.33 is the planning rate.
- Redis 15.40 per user stays as modelled for now; Isuru will say if it should move off the per-user band.
- GCP and Pusher "per user within a band" are resource step costs needed to serve that scale, not true per-user charges; they are amortised across the band.
- The 2,000 floor is a fixed monthly amount shared across users: per user it is 2,000 / users, and per user-hour it is 2,000 / (users x 17). So 117.65 per hour for a single user, 1.18 per hour at 100 users, 0.12 per hour at 1,000 users. The per-user share falls as users are added.

## Calculator moved to the per-hour cost structure (4 September 2026)

Application inputs are now: Azure AI cost per audio hour (3.33 planning), fixed add-ons per user (15.40, auto-stepping to 15.82 at 100 users and 16.86 at 500), shared floor 2,000 spread over active users, average usage 17 hrs, top-ups derived in whole 10-hour packs. All-in cost per user-hour = total per user / hours.

Result at defaults (100 users, 17 hrs): revenue 69.98, Azure 56.61, add-ons 15.82, contribution -2.45 before the floor; all-in 92.43 per user (5.44 per hour) including the 20.00 floor share. Top-up hour margin is only 0.67 (4.00 - 3.33). Top-ups per user are now a direct input (default 1). At June's actual 2.33/hr the same user contributes +14.55, so the planning rate is what decides whether the app breaks even.

## Azure AI cost curve (fitted 4 September 2026)

Three months of Azure AI services bills at different volumes:

| Month | Hours | Bill (AUD) | Per hour |
|---|---|---|---|
| June 2026 | 169.89 | 396.00 | 2.33 |
| July 2026 | 92.65 | 257.30 | 2.78 |
| August 2026 | 57.69 | 185.26 | 3.21 |

Linear fit: **bill = 80.48 + 1.8646 x hours** (R^2 = 0.999; all three months within AUD 4). So about AUD 80/month behaves as fixed and the marginal cost is about **AUD 1.86 per audio hour** (AUD 0.00052 per second). The falling per-hour rate is the fixed part being spread over more hours, not a volume discount.

Forecast cost per hour by monthly volume (linear model): 100 h 2.67; 170 h 2.34; 500 h 2.03; 1,000 h 1.95; 1,700 h (100 users x 17) 1.91; 17,000 h (1,000 users) 1.87. A power-law fit extrapolates lower (0.59/h at 17,000 h) but has no mechanism behind it; treat 1.86 as the floor unless Azure commitment tiers are bought.

Caveats: three points, all under 170 h/month; service mix may differ by month. Planning rate 3.33 is roughly 1.75x the expected rate at 100 users.

## Cross-check against Azure public pricing (4 September 2026)

Azure Speech to Text list prices (USD, pay-as-you-go): real-time standard $1.00 per audio hour; fast transcription $0.36; batch $0.18. Commitment tiers: 2,000 hrs/month for $1,600 ($0.80/hr, same overage); 50,000 hrs/month at $0.50/hr. Commitment tiers cover real-time, fast and batch. Azure OpenAI token prices equal OpenAI's: gpt-4o-mini $0.15 / $0.60 per 1M tokens, gpt-4.1-mini $0.40 / $1.60, gpt-4o $2.50 / $10.00.

Bottom-up per audio hour: an hour of consult is roughly 12k to 15k input tokens plus 1k to 2k output per document. With gpt-4o and a few passes that is about US$0.10 to $0.15 per hour; with mini models it is cents. So the speech service dominates. Real-time STT + LLM is about US$1.10 to $1.15 per hour, which at AUD 1 = US$0.65 is about AUD 1.70 to 1.80. The fitted marginal cost of AUD 1.86 matches that within about 5%, which says the app is being billed at the real-time rate. Batch ($0.18) or fast ($0.36) would put the marginal cost near AUD 0.45 to 0.75.

The AUD 80/month fixed component is not a published Speech or OpenAI fee; it is either baseline usage (testing, health checks) or another AI resource on the same bill. Worth identifying on the invoice.

Levers visible in public pricing: (1) fast or batch transcription for recorded consults, roughly 3x to 5x cheaper per hour than real-time; (2) the 2,000-hour commitment tier once monthly volume passes about 1,600 hours (about 95 users at 17 hrs), 20% off; (3) commitment tiers at 50,000 hours halve the rate.

Sources: Azure Speech pricing page (prices render per region, verified structure and free tier), Microsoft Q&A on commitment tiers covering all modes, third-party summaries of the $1 / $0.36 / $0.18 rates and the $1,600 for 2,000 hours tier, CloudZero and Finout for Azure OpenAI token prices.
