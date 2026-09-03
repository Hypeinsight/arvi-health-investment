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
