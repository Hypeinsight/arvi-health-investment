# -*- coding: utf-8 -*-
# Internal strategy deck: Arvi <-> PMS integration research.
# Reuses the exact CSS + JS engine from gen.py so the look and feel match the
# investor/feature deck. No em dashes anywhere; AU English spelling.
import io
import gen

# Small supplemental styles layered on top of the shared CSS:
#  - 4-column comparison tables (the shared .cmp is hardwired to 5 columns)
#  - 4-across phase cards (the shared .rm grid is 3 columns)
EXTRA_CSS = '''
        .cmp.c4 .cmp-row{grid-template-columns:1.6fr 1fr 1fr 1.3fr}
        .rm.c4{grid-template-columns:repeat(4,1fr)}
        @media (max-width:1024px){.rm.c4{grid-template-columns:1fr 1fr}}
        @media (max-width:860px){.cmp.c4 .cmp-row{font-size:.56rem}}
'''

# ---------------------------------------------------------------- slides ----

INTRO = '''        <!-- Title -->
        <section class="slide" id="s-intro" data-sec="Overview">
            <div class="inner">
                <div class="divider">
                    <div class="badge reveal"><span class="pulse"></span> Internal Research &middot; 18 Jun 2026</div>
                    <div class="big reveal" data-delay="1">Connecting Arvi to the Systems<br>Clinics Already Run</div>
                    <p class="subtitle reveal" data-delay="2" style="text-align:center;max-width:820px;margin:0 auto">How Arvi becomes the AI layer on top of the practice management software clinics already use: patient data flows in, letters and notes flow back out.</p>
                    <div class="menu reveal" data-delay="3">
                        <span class="mi"><b>BP</b> Best Practice</span>
                        <span class="mi"><b>MD</b> Medical Director</span>
                        <span class="mi"><b>Z</b> Zedmed</span>
                        <span class="mi"><b>G</b> Genie / Gentu</span>
                    </div>
                    <p class="subtitle reveal" data-delay="4" style="text-align:center;font-size:clamp(.78rem,1vw,.9rem);opacity:.7">For Dr Suhirdan and the Arvi team</p>
                </div>
            </div>
        </section>
'''

PROBLEM = '''        <!-- Problem: two silos -->
        <section class="slide" id="s-problem" data-sec="The Problem">
            <div class="inner">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg> The Problem</div>
                    <h2 class="title reveal" data-delay="1">Today, Arvi and the PMS Are Two Separate Silos</h2>
                    <p class="subtitle reveal" data-delay="2">Australian practices already run Best Practice, Medical Director, Zedmed or Genie, and they will not replace them. Right now a doctor using Arvi alongside their PMS does everything twice.</p>
                </div>
                <div class="cards c3">
                    <div class="card glass reveal" data-delay="2"><div class="vic"><svg viewBox="0 0 24 24"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><line x1="19" y1="8" x2="19" y2="14"/><line x1="22" y1="11" x2="16" y2="11"/></svg></div><h3>Patients re-entered by hand</h3><p>Every patient already in the PMS has to be typed into Arvi again before a consult.</p></div>
                    <div class="card glass reveal" data-delay="3"><div class="vic"><svg viewBox="0 0 24 24"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg></div><h3>Letters copy-pasted back</h3><p>A letter written in Arvi has to be copied and pasted into the PMS patient file by hand.</p></div>
                    <div class="card glass reveal" data-delay="4"><div class="vic"><svg viewBox="0 0 24 24"><path d="M18 6 6 18"/><path d="M6 6l12 12"/></svg></div><h3>Nothing is shared</h3><p>No shared appointments, no shared history. The two systems never talk to each other.</p></div>
                </div>
            </div>
        </section>
'''

POSITION = '''        <!-- Positioning: Arvi as the hub -->
        <section class="slide" id="s-position" data-sec="The Goal">
            <div class="inner">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg> The Goal</div>
                    <h2 class="title reveal" data-delay="1">Arvi Is the AI Hub. The PMS Are Data Sources.</h2>
                    <p class="subtitle reveal" data-delay="2">We make Arvi the primary AI layer that connects to the PMS, so the doctor works in one place and the data moves on its own. That means solving two jobs.</p>
                </div>
                <div class="cards c2" style="max-width:960px;margin:clamp(1rem,2.4vh,1.8rem) auto 0">
                    <div class="card glass reveal" data-delay="3" style="display:flex;flex-direction:column"><div class="vic"><svg viewBox="0 0 24 24"><path d="M12 5v14"/><polyline points="19 12 12 19 5 12"/></svg></div><h3>Job 1: Patients come IN</h3><p>The patient list and history flow from the PMS into Arvi automatically. The doctor opens Arvi and their existing patients are already there, no re-typing.</p></div>
                    <div class="card glass reveal" data-delay="4" style="display:flex;flex-direction:column"><div class="vic"><svg viewBox="0 0 24 24"><path d="M12 19V5"/><polyline points="5 12 12 5 19 12"/></svg></div><h3>Job 2: Letters go OUT</h3><p>The finished note or letter flows from Arvi straight back into the PMS patient file, no copy-paste.</p></div>
                </div>
                <p class="rm-cap reveal" data-delay="5" style="text-align:center;margin-top:clamp(.9rem,2vh,1.4rem)">Solve both and the loop is closed: one conversation, captured once, filed everywhere it belongs.</p>
            </div>
        </section>
'''

METHODS = '''        <!-- Industry integration methods -->
        <section class="slide" id="s-methods" data-sec="How It Is Done">
            <div class="inner fill">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg> How the Industry Does It</div>
                    <h2 class="title reveal" data-delay="1">Four Proven Ways to Plug a Scribe Into a PMS</h2>
                    <p class="subtitle reveal" data-delay="2">These are the verified patterns used by Heidi and Nabla today. Each is a different trade-off between effort and how deep the integration feels.</p>
                </div>
                <div class="cards c4">
                    <div class="card glass reveal" data-delay="2" style="display:flex;flex-direction:column"><div class="vic"><svg viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="18" rx="2"/><line x1="14" y1="3" x2="14" y2="21"/></svg></div><h3>Widget sidebar</h3><p>Arvi sits as a panel inside the PMS browser. Doctor records, then clicks Push Note.</p><span class="sol-pill"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>Heidi in Zedmed</span></div>
                    <div class="card glass reveal" data-delay="3" style="display:flex;flex-direction:column"><div class="vic"><svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="14" rx="2"/><line x1="3" y1="10" x2="21" y2="10"/></svg></div><h3>Native button</h3><p>Arvi is built straight into the PMS toolbar. No popup, it is part of their own interface.</p><span class="sol-pill"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>Heidi in Medical Director</span></div>
                    <div class="card glass reveal" data-delay="4" style="display:flex;flex-direction:column"><div class="vic"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15 15 0 0 1 0 20 15 15 0 0 1 0-20z"/></svg></div><h3>Browser extension</h3><p>A Chrome add-on replaces Copy with Export to PMS, works on any web-based PMS, no partner needed.</p><span class="sol-pill"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>Nabla</span></div>
                    <div class="card glass reveal" data-delay="5" style="display:flex;flex-direction:column"><div class="vic"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2"/><rect x="7" y="7" width="10" height="10" rx="1"/></svg></div><h3>iFrame embed</h3><p>The PMS opens Arvi inside a panel via a session URL, with patient context passed in.</p><span class="sol-pill"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>Nabla Connect</span></div>
                </div>
            </div>
        </section>
'''

HALO = '''        <!-- Halo Connect: patients IN -->
        <section class="slide" id="s-halo" data-sec="Patients In">
            <div class="inner">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><path d="M12 5v14"/><polyline points="19 12 12 19 5 12"/></svg> Patients In</div>
                    <h2 class="title reveal" data-delay="1">Halo Connect: the FHIR Bridge Into BP and Zedmed</h2>
                    <p class="subtitle reveal" data-delay="2">An Australian platform that lets a cloud app like Arvi read patient data out of a clinic's local PMS database. This is the fastest win for patient sync.</p>
                </div>
                <div class="integ">
                    <div class="integ-arvi reveal" data-delay="2">
                        <div class="il">Cloud app</div>
                        <h3>Arvi</h3>
                        <p>Asks for a patient by name or appointment</p>
                        <ul>
                            <li><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> Patient list synced in</li>
                            <li><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> Demographics &amp; history</li>
                            <li><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> No manual re-entry</li>
                        </ul>
                    </div>
                    <div class="pipe reveal" data-delay="3">
                        <div class="pl">Halo Cloud<br>FHIR to SQL</div>
                        <svg viewBox="0 0 24 24"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
                        <div class="pl sub">Halo Link at the clinic</div>
                    </div>
                    <div class="imx-prods">
                        <div class="imx-prod glass reveal" data-delay="3"><h4>BP Premier</h4><p>Primary support, via the FHIR facade.</p></div>
                        <div class="imx-prod glass reveal" data-delay="4"><h4>Zedmed</h4><p>FHIR plus SQL passthrough.</p></div>
                        <div class="imx-prod glass reveal" data-delay="4"><h4>How it reads</h4><p>Halo Link runs the query on the local PMS database and hands data back as FHIR.</p></div>
                        <div class="imx-prod glass reveal" data-delay="5"><h4>The catch</h4><p>Read only. It pulls patients out, it cannot push letters back in.</p></div>
                    </div>
                </div>
                <p class="rm-cap reveal" data-delay="6" style="margin-top:clamp(.7rem,1.6vh,1.1rem)">Most critical first step: register at haloconnect.io and confirm pricing.</p>
            </div>
        </section>
'''

HL7 = '''        <!-- HL7: letters OUT, already built -->
        <section class="slide" id="s-hl7" data-sec="Letters Out">
            <div class="inner">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><path d="M12 19V5"/><polyline points="5 12 12 5 19 12"/></svg> Letters Out</div>
                    <h2 class="title reveal" data-delay="1">HL7 to the Inbox: the Half We Already Have</h2>
                    <p class="subtitle reveal" data-delay="2">Arvi already sends documents as HL7 messages through HealthLink in production. The same rail drops a finished letter straight into a PMS correspondence inbox.</p>
                </div>
                <div class="steps">
                    <div class="step reveal" data-delay="2"><div class="sic"><svg viewBox="0 0 24 24"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/></svg></div><div class="sn">STEP 01</div><h3>Arvi writes</h3><p>The consult becomes a structured letter or note.</p></div>
                    <div class="step reveal" data-delay="3"><div class="sic"><svg viewBox="0 0 24 24"><path d="M22 2 11 13"/><path d="M22 2 15 22l-4-9-9-4 20-7z"/></svg></div><div class="sn">STEP 02</div><h3>HL7 message sent</h3><p>The same secure format already used for HealthLink.</p></div>
                    <div class="step reveal" data-delay="4"><div class="sic"><svg viewBox="0 0 24 24"><path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/></svg></div><div class="sn">STEP 03</div><h3>Lands in the inbox</h3><p>BP, Medical Director or Genie correspondence inbox.</p></div>
                    <div class="step reveal" data-delay="5"><div class="sic"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg></div><div class="sn">STEP 04</div><h3>Waiting for the doctor</h3><p>They open the PMS and the letter is already there.</p></div>
                </div>
                <p class="rm-cap reveal" data-delay="6" style="text-align:center;margin-top:clamp(.9rem,2vh,1.4rem)">Halo Connect brings patients IN, HL7 sends letters OUT. Together that is the full circle for BP and Zedmed, the two biggest PMS in Australia.</p>
            </div>
        </section>
'''

MAGENTUS = '''        <!-- Magentus / Gentu: specialists -->
        <section class="slide" id="s-magentus" data-sec="Specialists">
            <div class="inner fill">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><path d="M20 7h-9"/><path d="M14 17H5"/><circle cx="17" cy="17" r="3"/><circle cx="7" cy="7" r="3"/></svg> Specialists</div>
                    <h2 class="title reveal" data-delay="1">Magentus / Gentu: Built for AI Scribes Like Arvi</h2>
                    <p class="subtitle reveal" data-delay="2">Gentu is Australia's number one cloud PMS for specialists, Arvi's core market. Magentus runs a partner program that does both halves in one API: patient data in and letters out.</p>
                </div>
                <div class="cards c3">
                    <div class="card glass reveal" data-delay="2"><div class="vic"><svg viewBox="0 0 24 24"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/></svg></div><h3>Patient API</h3><p>Read patient demographics and appointments, and write reports or attachments back to the file. Read and write.</p></div>
                    <div class="card glass reveal" data-delay="3"><div class="vic"><svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg></div><h3>Bookings API</h3><p>Create bookings, referrals and new patients, and read practitioner availability.</p></div>
                    <div class="card glass reveal" data-delay="4"><div class="vic"><svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="8" y1="13" x2="16" y2="13"/></svg></div><h3>Letters API</h3><p>Push outgoing correspondence from a transcription service straight into the Gentu letter workflow. This is Arvi's exact product.</p></div>
                </div>
                <div class="reveal" data-delay="5" style="display:flex;gap:clamp(.9rem,2.2vw,1.8rem);flex-wrap:wrap;margin-top:clamp(.9rem,1.8vh,1.3rem)">
                    <div style="flex:1;min-width:240px"><b style="color:var(--primary-dark);font-size:clamp(.9rem,1.05vw,1rem)">Full circle in one integration</b><span style="display:block;font-size:.82rem;color:var(--muted);line-height:1.4;margin-top:.2rem">Unlike Halo Connect, Gentu pushes letters back too, so it solves in and out together.</span></div>
                    <div style="flex:1;min-width:240px"><b style="color:var(--primary-dark);font-size:clamp(.9rem,1.05vw,1rem)">A partner track, not instant keys</b><span style="display:block;font-size:.82rem;color:var(--muted);line-height:1.4;margin-top:.2rem">Seven-step onboarding through a developer portal, sandbox, then a marketplace listing.</span></div>
                    <div style="flex:1;min-width:240px"><b style="color:var(--primary-dark);font-size:clamp(.9rem,1.05vw,1rem)">Does not cover BP</b><span style="display:block;font-size:.82rem;color:var(--muted);line-height:1.4;margin-top:.2rem">Magentus and BP are competitors. BP stays on Halo Connect plus HL7.</span></div>
                </div>
            </div>
        </section>
'''

TELSTRA = '''        <!-- Telstra Smart API+ : Medical Director -->
        <section class="slide" id="s-telstra" data-sec="Medical Director">
            <div class="inner">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><path d="M4 11a9 9 0 0 1 9 9"/><path d="M4 4a16 16 0 0 1 16 16"/><circle cx="5" cy="19" r="1"/></svg> Medical Director</div>
                    <h2 class="title reveal" data-delay="1">Telstra Smart API+ for Medical Director</h2>
                    <p class="subtitle reveal" data-delay="2">A FHIR-native gateway from Telstra Health, the path into Medical Director for getting patient data in. We apply, they approve.</p>
                </div>
                <div class="cards c4">
                    <div class="card glass reveal" data-delay="2" style="display:flex;flex-direction:column"><div class="vic"><svg viewBox="0 0 24 24"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg></div><h3>FHIR-native</h3><p>Modern standard interface for reading and writing patient data.</p></div>
                    <div class="card glass reveal" data-delay="3" style="display:flex;flex-direction:column"><div class="vic"><svg viewBox="0 0 24 24"><path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"/></svg></div><h3>Helix, cloud</h3><p>Available for partners integrating with Medical Director Helix.</p></div>
                    <div class="card glass reveal" data-delay="4" style="display:flex;flex-direction:column"><div class="vic"><svg viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg></div><h3>Clinical, desktop</h3><p>Case-by-case for the desktop version of Medical Director.</p></div>
                    <div class="card glass reveal" data-delay="5" style="display:flex;flex-direction:column"><div class="vic"><svg viewBox="0 0 24 24"><path d="M18 6 6 18"/><path d="M6 6l12 12"/></svg></div><h3>Scope</h3><p>Does not cover BP, Zedmed or Genie. Medical Director only.</p></div>
                </div>
                <p class="rm-cap reveal" data-delay="6" style="text-align:center;margin-top:clamp(.9rem,2vh,1.4rem)">Letters still go out to Medical Director over HL7, which Arvi already has. Smart API+ is for bringing patients in.</p>
            </div>
        </section>
'''

OWNERMAP = '''        <!-- PMS ownership map -->
        <section class="slide" id="s-owners" data-sec="The Landscape">
            <div class="inner">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/><line x1="8" y1="2" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="22"/></svg> The Landscape</div>
                    <h2 class="title reveal" data-delay="1">Who Owns What, and How Arvi Gets In</h2>
                    <p class="subtitle reveal" data-delay="2">The path differs by vendor because the ownership and the technology differ. There is no single key that opens every PMS.</p>
                </div>
                <div class="cmp c4 glass reveal" data-delay="2">
                    <div class="cmp-row cmp-head"><div>PMS</div><div>Owned by</div><div>Market</div><div class="arvi">Arvi path</div></div>
                    <div class="cmp-row"><div>Best Practice (BP)</div><div>Best Practice (independent)</div><div>GP, number 1</div><div class="arvi">Halo Connect in, HL7 out</div></div>
                    <div class="cmp-row"><div>Medical Director / Helix</div><div>Telstra Health</div><div>GP, number 2</div><div class="arvi">Smart API+ in, HL7 out</div></div>
                    <div class="cmp-row"><div>Genie / Gentu / Clinic to Cloud</div><div>Magentus</div><div>Specialist</div><div class="arvi">Magentus partner API, in and out</div></div>
                    <div class="cmp-row"><div>Zedmed</div><div>Zedmed (independent)</div><div>GP + specialist</div><div class="arvi">Halo Connect in, widget or HL7 out</div></div>
                </div>
            </div>
        </section>
'''

DESKTOP = '''        <!-- Critical discovery: BP is desktop -->
        <section class="slide" id="s-desktop" data-sec="Key Nuance">
            <div class="inner">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg> A Key Nuance</div>
                    <h2 class="title reveal" data-delay="1">BP Is a Desktop App, Not a Website</h2>
                    <p class="subtitle reveal" data-delay="2">This changes the Chrome extension plan. A browser add-on can only reach things inside a browser. BP Premier is a standalone Windows program, so the extension cannot touch it.</p>
                </div>
                <div class="cards c2" style="max-width:980px;margin:clamp(1rem,2.4vh,1.8rem) auto 0">
                    <div class="card glass reveal" data-delay="3" style="display:flex;flex-direction:column"><div class="vic"><svg viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg></div><h3>Web PMS, for example Zedmed</h3><p>Runs in the browser, so a Chrome extension can read and write to it. Export to PMS works here.</p><span class="sol-pill"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>Extension works</span></div>
                    <div class="card glass reveal" data-delay="4" style="display:flex;flex-direction:column"><div class="vic"><svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="14" rx="2"/><line x1="3" y1="20" x2="21" y2="20"/></svg></div><h3>Desktop PMS, BP Premier</h3><p>A Windows .exe outside the browser. The extension cannot reach it, so letters go in by HL7 to the BP correspondence inbox instead.</p><span class="sol-pill" style="background:rgba(105,26,106,.12);color:var(--accent)"><svg viewBox="0 0 24 24"><path d="M22 2 11 13"/><path d="M22 2 15 22l-4-9-9-4 20-7z"/></svg>Use HL7 instead</span></div>
                </div>
                <p class="rm-cap reveal" data-delay="5" style="text-align:center;margin-top:clamp(.9rem,2vh,1.4rem)">Good news: Arvi already has the HL7 path, so BP delivery is nearly done.</p>
            </div>
        </section>
'''

MATRIX = '''        <!-- Desktop vs web matrix -->
        <section class="slide" id="s-matrix" data-sec="The Landscape">
            <div class="inner">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg> The Landscape</div>
                    <h2 class="title reveal" data-delay="1">Each PMS, by Type and by Direction</h2>
                    <p class="subtitle reveal" data-delay="2">How patients come in and how letters go out, for the four systems that matter most.</p>
                </div>
                <div class="cmp c4 glass reveal" data-delay="2">
                    <div class="cmp-row cmp-head"><div>PMS</div><div>Type</div><div>Patients in</div><div class="arvi">Letters out</div></div>
                    <div class="cmp-row"><div>Best Practice</div><div>Desktop app</div><div>Halo Connect</div><div class="arvi">HL7 to BP inbox</div></div>
                    <div class="cmp-row"><div>Medical Director</div><div>Desktop app</div><div>Telstra Smart API+</div><div class="arvi">HL7 to MD inbox</div></div>
                    <div class="cmp-row"><div>Zedmed</div><div>Web app</div><div>Halo Connect</div><div class="arvi">Chrome ext or widget</div></div>
                    <div class="cmp-row"><div>Genie / Gentu</div><div>Cloud + desktop</div><div>Magentus partner API</div><div class="arvi">Gentu Letters API</div></div>
                </div>
            </div>
        </section>
'''

HEIDI = '''        <!-- Heidi vs Arvi readiness -->
        <section class="slide" id="s-heidi" data-sec="Versus Heidi">
            <div class="inner">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><path d="M18 20V10"/><path d="M12 20V4"/><path d="M6 20v-6"/></svg> Versus Heidi</div>
                    <h2 class="title reveal" data-delay="1">Where We Stand Against Heidi</h2>
                    <p class="subtitle reveal" data-delay="2">Heidi is the leading Australian scribe and has the integrations we are targeting. We already lead on HL7 delivery and Australian letters.</p>
                </div>
                <div class="cmp c4 glass reveal" data-delay="2">
                    <div class="cmp-row cmp-head"><div>Capability</div><div>Heidi today</div><div>Arvi today</div><div class="arvi">Arvi target</div></div>
                    <div class="cmp-row"><div>Zedmed native widget</div><div>Yes</div><div>No</div><div class="arvi">Phase 4</div></div>
                    <div class="cmp-row"><div>Medical Director button</div><div>Yes</div><div>No</div><div class="arvi">Phase 3 to 4</div></div>
                    <div class="cmp-row"><div>Chrome extension</div><div>Some PMS</div><div>No</div><div class="arvi">Phase 1</div></div>
                    <div class="cmp-row"><div>Patient sync (FHIR)</div><div>Unknown</div><div>No</div><div class="arvi">Phase 2, Halo</div></div>
                    <div class="cmp-row"><div>HealthLink HL7 delivery</div><div>Partial</div><div class="arvi tick"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg></div><div class="arvi">Done</div></div>
                    <div class="cmp-row"><div>Australian AI letters</div><div>Yes</div><div class="arvi tick"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg></div><div class="arvi">Done</div></div>
                </div>
                <p class="rm-cap reveal" data-delay="3" style="margin-top:clamp(.7rem,1.6vh,1rem)">Worth knowing: many healthcare integrations are really well-designed copy-paste. Heidi often just makes copying one click. A true two-way sync is a real edge.</p>
            </div>
        </section>
'''

STRATEGY = '''        <!-- Recommended 4-phase strategy -->
        <section class="slide" id="s-strategy" data-sec="The Plan">
            <div class="inner fill">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg> The Plan</div>
                    <h2 class="title reveal" data-delay="1">A Four-Phase Path, Quickest Wins First</h2>
                    <p class="subtitle reveal" data-delay="2">Start with what needs no permission, then layer on the official partnerships that make Arvi deeper and more trusted.</p>
                </div>
                <div class="rm-wrap">
                    <div class="rmline reveal" data-delay="2">
                        <div class="rmpt"><span class="d"></span><span class="l">Chrome extension</span><span class="v">0 to 3 mo</span></div>
                        <div class="rmpt"><span class="d"></span><span class="l">Halo Connect</span><span class="v">1 to 4 mo</span></div>
                        <div class="rmpt"><span class="d"></span><span class="l">Smart API+</span><span class="v">3 to 6 mo</span></div>
                        <div class="rmpt"><span class="d"></span><span class="l">Native widget</span><span class="v">6 to 12 mo</span></div>
                    </div>
                    <div class="rm c4">
                        <div class="rmcard lite reveal" data-delay="3"><div class="ph"><div class="pn">1</div><div class="pt">0 to 3 mo</div></div><h3>Chrome extension</h3><ul><li>No partnership needed</li><li>Export to PMS for web systems</li><li>Letters go out via the browser</li></ul><div class="tgt"><b>OUT</b><span>Arvi builds it</span></div></div>
                        <div class="rmcard lite reveal" data-delay="4"><div class="ph"><div class="pn">2</div><div class="pt">1 to 4 mo</div></div><h3>Halo Connect</h3><ul><li>FHIR patient sync</li><li>BP and Zedmed patients in</li><li>No manual re-entry</li></ul><div class="tgt"><b>IN</b><span>Arvi connects to Halo</span></div></div>
                        <div class="rmcard lite reveal" data-delay="5"><div class="ph"><div class="pn">3</div><div class="pt">3 to 6 mo</div></div><h3>Telstra Smart API+</h3><ul><li>Open partner program</li><li>Medical Director patient data</li><li>Read and write over FHIR</li></ul><div class="tgt"><b>MD</b><span>Arvi applies, Telstra approves</span></div></div>
                        <div class="rmcard climax reveal" data-delay="6"><span class="flag"><svg viewBox="0 0 24 24"><path d="M12 2l2.4 7.4H22l-6 4.6 2.3 7.4L12 17l-6.3 4.4L8 14 2 9.4h7.6z"/></svg>Deepest tie-in</span><div class="ph"><div class="pn">4</div><div class="pt">6 to 12 mo</div></div><h3>Native widget</h3><ul><li>Arvi built inside the PMS</li><li>Official marketplace listing</li><li>Vendor markets Arvi for us</li></ul><div class="tgt"><b>IN+OUT</b><span>PMS builds it with Arvi</span></div></div>
                    </div>
                </div>
            </div>
        </section>
'''

WHYFOUR = '''        <!-- Why all four: technical vs partnership -->
        <section class="slide" id="s-whyfour" data-sec="The Plan">
            <div class="inner">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg> Why All Four</div>
                    <h2 class="title reveal" data-delay="1">Technical First, Then Official</h2>
                    <p class="subtitle reveal" data-delay="2">Phases 1 and 2 are technical: Arvi connects quietly in the background. Phases 3 and 4 are partnerships: the PMS company officially supports Arvi.</p>
                </div>
                <div class="cards c2" style="max-width:980px;margin:clamp(1rem,2.4vh,1.8rem) auto 0">
                    <div class="card glass reveal" data-delay="3" style="display:flex;flex-direction:column"><div class="vic"><svg viewBox="0 0 24 24"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg></div><h3>Phases 1 &amp; 2: technical</h3><p>The doctor sets it up themselves. It works, but it can feel like a workaround, the PMS does not know Arvi exists, and an update could break it.</p></div>
                    <div class="card glass reveal" data-delay="4" style="display:flex;flex-direction:column"><div class="vic"><svg viewBox="0 0 24 24"><path d="M12 2l2.4 7.4H22l-6 4.6 2.3 7.4L12 17l-6.3 4.4L8 14 2 9.4h7.6z"/></svg></div><h3>Phases 3 &amp; 4: official</h3><p>Arvi is built in, with a trust badge and marketplace listing. When the PMS updates, they update Arvi too, and they market Arvi to their clinics.</p></div>
                </div>
                <p class="rm-cap reveal" data-delay="5" style="text-align:center;margin-top:clamp(.9rem,2vh,1.4rem)">The analogy: phases 1 and 2 are sneaking your own food into the cinema. Phases 3 and 4 are the cinema putting your food on the menu and selling it for you.</p>
            </div>
        </section>
'''

NEXT = '''        <!-- Next steps -->
        <section class="slide" id="s-next" data-sec="Next Steps">
            <div class="inner">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg> Next Steps</div>
                    <h2 class="title reveal" data-delay="1">What We Do Next</h2>
                    <p class="subtitle reveal" data-delay="2">A short list to turn this research into movement.</p>
                </div>
                <div class="cards c3">
                    <div class="card glass reveal" data-delay="2"><div class="vic"><svg viewBox="0 0 24 24"><path d="M12 8v8"/><path d="M8 12h8"/><circle cx="12" cy="12" r="10"/></svg></div><h3>Contact Halo Connect</h3><p>Register at haloconnect.io and get pricing. Most critical first step for BP and Zedmed patient sync.</p></div>
                    <div class="card glass reveal" data-delay="3"><div class="vic"><svg viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg></div><h3>Apply to Telstra Smart API+</h3><p>Get into the Medical Director partner program early, the queue is the slow part.</p></div>
                    <div class="card glass reveal" data-delay="4"><div class="vic"><svg viewBox="0 0 24 24"><path d="M20 7h-9"/><path d="M14 17H5"/><circle cx="17" cy="17" r="3"/><circle cx="7" cy="7" r="3"/></svg></div><h3>Register with Magentus / Gentu</h3><p>Start the developer-partner process for the specialist market and the Letters API.</p></div>
                    <div class="card glass reveal" data-delay="4"><div class="vic"><svg viewBox="0 0 24 24"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg></div><h3>Decide the build order</h3><p>Chrome extension first, or Halo Connect first. Scope both against current engineering load.</p></div>
                    <div class="card glass reveal" data-delay="5"><div class="vic"><svg viewBox="0 0 24 24"><path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/></svg></div><h3>Confirm BP HL7 inbox</h3><p>Verify BP accepts our HL7 letters into the correspondence inbox end to end.</p></div>
                    <div class="card glass reveal" data-delay="5"><div class="vic"><svg viewBox="0 0 24 24"><line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><line x1="1" y1="14" x2="7" y2="14"/><line x1="9" y1="8" x2="15" y2="8"/><line x1="17" y1="16" x2="23" y2="16"/></svg></div><h3>Define the data contract</h3><p>Pin down what Arvi needs from the PMS (demographics, appointments, history) and what it sends back (letters, notes).</p></div>
                </div>
            </div>
        </section>
'''

SOURCES = '''        <!-- Sources / appendix -->
        <section class="slide" id="s-sources" data-sec="Appendix">
            <div class="inner">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg> Appendix</div>
                    <h2 class="title reveal" data-delay="1">Key Sources</h2>
                    <p class="subtitle reveal" data-delay="2">All verified during the research on 18 to 19 June 2026.</p>
                </div>
                <div class="cmp c4 glass reveal" data-delay="2">
                    <div class="cmp-row cmp-head"><div>Topic</div><div>Source</div><div>Standard</div><div class="arvi">Use</div></div>
                    <div class="cmp-row"><div>Halo Connect FHIR</div><div>docs.haloconnect.io</div><div>FHIR facade</div><div class="arvi">Patients in (BP, Zedmed)</div></div>
                    <div class="cmp-row"><div>Telstra Smart API+</div><div>telstrahealth.com</div><div>FHIR</div><div class="arvi">Medical Director in</div></div>
                    <div class="cmp-row"><div>Magentus / Gentu</div><div>magentus.com developer-partners</div><div>REST, read+write</div><div class="arvi">Specialists, in and out</div></div>
                    <div class="cmp-row"><div>Heidi integrations</div><div>heidihealth.com integrations, developers</div><div>Widget SDK</div><div class="arvi">Benchmark</div></div>
                    <div class="cmp-row"><div>Nabla EHR integration</div><div>docs.nabla.com, nabla.com/connect</div><div>Extension, iFrame</div><div class="arvi">Method reference</div></div>
                </div>
            </div>
        </section>
'''

BODY = (INTRO + PROBLEM + POSITION + METHODS + HALO + HL7 + MAGENTUS + TELSTRA
        + OWNERMAP + DESKTOP + MATRIX + HEIDI + STRATEGY + WHYFOUR + NEXT + SOURCES)

HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="robots" content="noindex, nofollow, noarchive">
    <meta name="referrer" content="no-referrer">
    <title>Arvi Health &middot; PMS Integration Strategy</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>''' + gen.CSS + EXTRA_CSS + '''    </style>
</head>
<body>
    <div class="progress" id="prog"><span></span></div>
    <nav class="nav">
        <a href="https://arvihealth.com" target="_blank" rel="noopener" class="logo"><img src="arvi logo.avif" alt="Arvi Health"></a>
        <div class="dots" id="dots"></div>
        <div class="nav-tag">Internal &middot; <b>PMS Integration</b></div>
    </nav>

    <main class="deck" id="deck">
''' + BODY + '''    </main>

    <div class="counter"><span><b id="cur">1</b> / <span id="total">0</span></span><span class="sec" id="sec">Overview</span></div>

    <script>''' + gen.SCRIPT + '''</script>
</body>
</html>
'''

# Unguessable filename so the deck is reachable by direct link only, never by
# browsing the root domain. Combined with the noindex meta tag above, it stays
# off search engines too.
OUT = 'pms-integration-71d44f9533884ef8.html'

if __name__ == "__main__":
    with io.open(OUT, 'w', encoding='utf-8') as f:
        f.write(HTML)
    print("slides:", HTML.count('<section class="slide"'))
    print("WROTE", OUT)
