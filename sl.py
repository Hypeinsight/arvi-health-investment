# -*- coding: utf-8 -*-
# Concise, Sri Lanka localised cut of the Arvi pitch: mobile app + roadmap +
# the feature-glossary appendix. Reuses gen.py CSS, JS engine, the 19 feature
# demos and the appendix divider. No em dashes; AU English spelling.
import io
import gen

INTRO = '''        <!-- Intro (mobile, SL) -->
        <section class="slide" id="s-intro" data-sec="Overview">
            <div class="inner">
                <div class="intro">
                    <div class="feature-copy">
                        <div class="badge reveal"><span class="pulse"></span> Ayubowan &middot; AI Clinical Documentation</div>
                        <h1 class="reveal" data-delay="1">Capture every <span class="rotw" id="slrot">consult</span>.<br><span>Arvi does the rest.</span></h1>
                        <p class="reveal" data-delay="2">AI documentation that turns every encounter across your hospital into structured, connected clinical data. It integrates with the systems you already run, and scales up or down by department and use case. Engineered by a team here in Sri Lanka.</p>
                        <div class="tags reveal" data-delay="3"><span class="tag">Works with your systems</span><span class="tag">Modular &amp; scalable</span><span class="tag">Built in Sri Lanka</span></div>
                    </div>
                    <figure class="clip reveal" data-delay="2">
                        <div class="clip-glow"></div>
                        <div class="clip-frame"><video src="arvi-demo.mp4" autoplay loop muted playsinline preload="metadata"></video></div>
                    </figure>
                </div>
            </div>
        </section>
'''

APP = '''        <!-- The mobile app -->
        <section class="slide" id="s-app" data-sec="The App">
            <div class="inner fill">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><rect x="5" y="2" width="14" height="20" rx="2"/><line x1="12" y1="18" x2="12.01" y2="18"/></svg> The App</div>
                    <h2 class="title reveal" data-delay="1">One App, Every Setting a Clinician Works In</h2>
                    <p class="subtitle reveal" data-delay="2">No new hardware, no desktop at every bedside. Arvi lives on the phone the clinician already carries, and turns the moments of care into clean documentation.</p>
                </div>
                <div class="cards c4">
                    <div class="card glass reveal" data-delay="2"><div class="vic"><svg viewBox="0 0 24 24"><path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/></svg></div><h3>Ward round</h3><p>Capture at the bedside and move on, the note is written before the next patient.</p></div>
                    <div class="card glass reveal" data-delay="3"><div class="vic"><svg viewBox="0 0 24 24"><path d="M12 2v6"/><path d="M9 5h6"/><circle cx="12" cy="14" r="7"/></svg></div><h3>Emergency</h3><p>One tap to record when seconds matter, a usable note without setup.</p></div>
                    <div class="card glass reveal" data-delay="4"><div class="vic"><svg viewBox="0 0 24 24"><rect x="5" y="2" width="14" height="20" rx="2"/><line x1="9" y1="6" x2="15" y2="6"/></svg></div><h3>Operating theatre</h3><p>The operation note is created at the point of care, not reconstructed later.</p></div>
                    <div class="card glass reveal" data-delay="5"><div class="vic"><svg viewBox="0 0 24 24"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/></svg></div><h3>Clinic &amp; telehealth</h3><p>In person or remote, the same capture-to-note flow, ready to send.</p></div>
                </div>
                <div class="dl compact reveal" data-delay="6">
                    <a class="dlcard" href="https://apps.apple.com/au/app/arvi-health/id6761469752" target="_blank" rel="noopener"><img src="qr-ios.png" alt="Download Arvi on the App Store"><div><div class="dt"><svg viewBox="0 0 24 24"><path d="M3 7V5a2 2 0 0 1 2-2h2"/><path d="M17 3h2a2 2 0 0 1 2 2v2"/><path d="M21 17v2a2 2 0 0 1-2 2h-2"/><path d="M7 21H5a2 2 0 0 1-2-2v-2"/><line x1="7" y1="12" x2="17" y2="12"/></svg>Scan to try Arvi</div><div class="dn">Arvi for iOS</div><div class="ds">App Store</div></div></a>
                    <a class="dlcard" href="https://play.google.com/store/apps/details?id=com.healthai.mobile" target="_blank" rel="noopener"><img src="qr-android.png" alt="Download Arvi on Google Play"><div><div class="dt"><svg viewBox="0 0 24 24"><path d="M3 7V5a2 2 0 0 1 2-2h2"/><path d="M17 3h2a2 2 0 0 1 2 2v2"/><path d="M21 17v2a2 2 0 0 1-2 2h-2"/><path d="M7 21H5a2 2 0 0 1-2-2v-2"/><line x1="7" y1="12" x2="17" y2="12"/></svg>Scan to try Arvi</div><div class="dn">Arvi for Android</div><div class="ds">Google Play</div></div></a>
                </div>
            </div>
        </section>
'''

HOWITWORKS = '''        <!-- How it works -->
        <section class="slide" id="s-how" data-sec="How It Works">
            <div class="inner">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg> How It Works</div>
                    <h2 class="title reveal" data-delay="1">Speak. Everything Else Is Automatic.</h2>
                    <p class="subtitle reveal" data-delay="2">Four steps, and only the first one asks anything of the clinician.</p>
                </div>
                <div class="steps">
                    <div class="step reveal" data-delay="2"><div class="sic"><svg viewBox="0 0 24 24"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/></svg></div><div class="sn">STEP 01</div><h3>Speak</h3><p>Record the consult on the phone, or upload existing audio.</p></div>
                    <div class="step reveal" data-delay="3"><div class="sic"><svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="8" y1="13" x2="16" y2="13"/></svg></div><div class="sn">STEP 02</div><h3>Structure</h3><p>Arvi writes a clean, sectioned clinical note in seconds.</p></div>
                    <div class="step reveal" data-delay="4"><div class="sic"><svg viewBox="0 0 24 24"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg></div><div class="sn">STEP 03</div><h3>Letter</h3><p>Referral, discharge and clinic letters drafted from the same recording.</p></div>
                    <div class="step reveal" data-delay="5"><div class="sic"><svg viewBox="0 0 24 24"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg></div><div class="sn">STEP 04</div><h3>Share</h3><p>Into the patient record, over the standard interfaces hospitals run.</p></div>
                </div>
                <p class="rm-cap reveal" data-delay="6" style="text-align:center;margin-top:clamp(.9rem,2vh,1.4rem)">The clinician keeps their attention on the patient. Arvi handles the writing.</p>
            </div>
        </section>
'''

PROBLEM = '''        <!-- The gap: fragmentation, no history at the consult -->
        <section class="slide" id="s-gap" data-sec="The Gap">
            <div class="inner">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg> The Gap</div>
                    <h2 class="title reveal" data-delay="1">The Hospital Has the Data. The Consult Does Not.</h2>
                    <p class="subtitle reveal" data-delay="2">A patient's history is scattered across wards, clinics, laboratories, paper and disconnected systems. At the moment that matters most, the consultation, the clinician rarely has the full, accurate picture in front of them.</p>
                </div>
                <div class="cards c3">
                    <div class="card glass reveal" data-delay="2"><div class="vic"><svg viewBox="0 0 24 24"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14a9 3 0 0 0 18 0V5"/><path d="M3 12a9 3 0 0 0 18 0"/></svg></div><h3>No single source of truth</h3><p>Records live in silos across departments, systems and paper. Nothing holds the whole patient in one place.</p></div>
                    <div class="card glass reveal" data-delay="3"><div class="vic"><svg viewBox="0 0 24 24"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg></div><h3>Blind at the bedside</h3><p>The clinician consults without a reliable, complete history, rebuilding the story from memory and fragments.</p></div>
                    <div class="card glass reveal" data-delay="4"><div class="vic"><svg viewBox="0 0 24 24"><path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg></div><h3>The cost</h3><p>Repeated tests, missed context, slower decisions and avoidable risk to the patient.</p></div>
                </div>
            </div>
        </section>
'''

BRAIN = '''        <!-- Arvi as the brain of the hospital -->
        <section class="slide" id="s-brain" data-sec="Our Role">
            <div class="inner fill">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M12 2a4 4 0 0 0-4 4 4 4 0 0 0-2 7 4 4 0 0 0 2 7 4 4 0 0 0 8 0 4 4 0 0 0 2-7 4 4 0 0 0-2-7 4 4 0 0 0-4-4z"/></svg> Our Role</div>
                    <h2 class="title reveal" data-delay="1">Arvi Becomes the Brain of the Hospital</h2>
                    <p class="subtitle reveal" data-delay="2">Because Arvi captures and structures every consultation, it can hold what the hospital never centralised. One connected clinical memory, with the accurate history surfaced back to the clinician at the point of care.</p>
                </div>
                <div class="cards c4">
                    <div class="card glass reveal" data-delay="2"><div class="vic"><svg viewBox="0 0 24 24"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/></svg></div><h3>Captures every encounter</h3><p>Each consult, ward round and procedure, captured on the phone and structured.</p></div>
                    <div class="card glass reveal" data-delay="3"><div class="vic"><svg viewBox="0 0 24 24"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg></div><h3>Builds one record</h3><p>Fragments become a single, longitudinal patient story the hospital can trust.</p></div>
                    <div class="card glass reveal" data-delay="4"><div class="vic"><svg viewBox="0 0 24 24"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg></div><h3>Surfaces history at the consult</h3><p>The relevant, accurate history is in front of the clinician exactly when they need it.</p></div>
                    <div class="card glass reveal" data-delay="5"><div class="vic"><svg viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="14" x2="23" y2="14"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="14" x2="4" y2="14"/></svg></div><h3>Reasons across it all</h3><p>The foundation of the practice brain: intelligence that acts on years of care, not a single note.</p></div>
                </div>
                <p class="rm-cap reveal" data-delay="6" style="text-align:center;margin-top:clamp(.9rem,2vh,1.4rem)">This is the centre of our vision and roadmap: from a scribe on the phone to the intelligence layer for the whole hospital.</p>
            </div>
        </section>
'''

INTEGRATION = '''        <!-- Integration & modularity -->
        <section class="slide" id="s-integrate" data-sec="Fits Your Stack">
            <div class="inner fill">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg> Fits Your Stack</div>
                    <h2 class="title reveal" data-delay="1">Integrates With What You Run. Modular by Design.</h2>
                    <p class="subtitle reveal" data-delay="2">Arvi is not a rip and replace. It connects to the systems your hospital already depends on, and switches features on or off by department and use case, so it scales up or down fast.</p>
                </div>
                <div class="cards c4">
                    <div class="card glass reveal" data-delay="2"><div class="vic"><svg viewBox="0 0 24 24"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg></div><h3>Standards-based</h3><p>HL7 and FHIR-ready interfaces, so structured notes and letters flow into the record and onward to other systems.</p></div>
                    <div class="card glass reveal" data-delay="3"><div class="vic"><svg viewBox="0 0 24 24"><rect x="2" y="2" width="20" height="8" rx="2"/><rect x="2" y="14" width="20" height="8" rx="2"/><line x1="6" y1="6" x2="6.01" y2="6"/><line x1="6" y1="18" x2="6.01" y2="18"/></svg></div><h3>Sits alongside your EMR</h3><p>It augments the record, patient administration and laboratory systems you run today, rather than replacing them.</p></div>
                    <div class="card glass reveal" data-delay="4"><div class="vic"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg></div><h3>Feature modules</h3><p>Capture, letters, coding, pathology, analytics. Switch on only what a department actually needs.</p></div>
                    <div class="card glass reveal" data-delay="5"><div class="vic"><svg viewBox="0 0 24 24"><polyline points="17 11 21 7 17 3"/><line x1="21" y1="7" x2="9" y2="7"/><polyline points="7 21 3 17 7 13"/><line x1="3" y1="17" x2="15" y2="17"/></svg></div><h3>Scale up or down, fast</h3><p>Start with one ward, expand hospital-wide, or dial back. Configured in days, not months.</p></div>
                </div>
                <p class="rm-cap reveal" data-delay="6" style="text-align:center;margin-top:clamp(.9rem,2vh,1.4rem)">Pay for what is used, deploy where it helps, and grow at your pace.</p>
            </div>
        </section>
'''

SL_ROLE = '''        <!-- Arvi in Sri Lanka -->
        <section class="slide" id="s-slrole" data-sec="In Sri Lanka">
            <div class="inner">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><path d="M21 10c0 7-9 12-9 12s-9-5-9-12a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg> In Sri Lanka</div>
                    <h2 class="title reveal" data-delay="1">What Arvi Can Do for a Sri Lankan Hospital</h2>
                    <p class="subtitle reveal" data-delay="2">Our clinicians carry some of the heaviest patient loads in the region, and much of their day is lost to writing. Arvi is built for exactly that pressure, and it is built here.</p>
                </div>
                <div class="cards c3">
                    <div class="card glass reveal" data-delay="2"><div class="vic"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg></div><h3>Give clinicians time back</h3><p>Under high patient volume, every minute saved on notes is a minute returned to care, and more patients seen.</p></div>
                    <div class="card glass reveal" data-delay="3"><div class="vic"><svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="8" y1="13" x2="16" y2="13"/><line x1="8" y1="17" x2="13" y2="17"/></svg></div><h3>Structured English records</h3><p>Sri Lankan clinical records are already in English. Arvi turns them into clean, consistent documents.</p></div>
                    <div class="card glass reveal" data-delay="4"><div class="vic"><svg viewBox="0 0 24 24"><rect x="5" y="2" width="14" height="20" rx="2"/><line x1="12" y1="18" x2="12.01" y2="18"/></svg></div><h3>Mobile-first, ward-ready</h3><p>It runs on the phone in the clinician's pocket, so it works where a desktop at every bed does not.</p></div>
                    <div class="card glass reveal" data-delay="4"><div class="vic"><svg viewBox="0 0 24 24"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg></div><h3>Affordable at scale</h3><p>Pay for what is used. A model that suits a public and private system watching every rupee.</p></div>
                    <div class="card glass reveal" data-delay="5"><div class="vic"><svg viewBox="0 0 24 24"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg></div><h3>Reach beyond the city</h3><p>Support telemedicine and connect district care to specialists whose time is scarce.</p></div>
                    <div class="card glass reveal" data-delay="5"><div class="vic"><svg viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg></div><h3>Built locally</h3><p>Engineered by a Sri Lankan team, so support, training and iteration stay close to you.</p></div>
                </div>
            </div>
        </section>
'''

SL_VISION = '''        <!-- Vision: SL and beyond -->
        <section class="slide" id="s-slvision" data-sec="Our Vision">
            <div class="inner">
                <div class="divider">
                    <div class="label reveal" style="justify-content:center"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg> Our Vision</div>
                    <p class="vision-statement reveal" data-delay="1">To become the autonomous operating system for healthcare, proven in Sri Lanka and built for the world.</p>
                    <div class="menu reveal" data-delay="2">
                        <span class="mi"><b>Here</b> Sri Lankan hospitals</span>
                        <span class="mi"><b>Then</b> The region</span>
                        <span class="mi"><b>Onward</b> The world</span>
                    </div>
                    <p class="subtitle reveal" data-delay="3" style="text-align:center;max-width:760px;margin:clamp(.6rem,1.4vh,1rem) auto 0">We want Sri Lanka to be where this is proven first: a home base and a launch pad, not an afterthought. What works under our pressure will work anywhere.</p>
                </div>
            </div>
        </section>
'''

ROADMAP_SL = '''        <!-- Product roadmap (SL tailored) -->
        <section class="slide" id="s-proadmap" data-sec="Roadmap">
            <div class="inner fill">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg> Product Roadmap</div>
                    <h2 class="title reveal" data-delay="1">Where Arvi Is Going</h2>
                    <p class="subtitle reveal" data-delay="2">Beyond today's twenty production features, from a scribe on the phone toward the intelligence layer for a whole hospital.</p>
                </div>
                <div class="rm-wrap">
                    <div class="rm">
                        <div class="rmcard lite reveal" data-delay="3">
                            <div class="ph"><div class="pn"><svg viewBox="0 0 24 24"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg></div><div class="pt">Now &rarr; 6 months</div></div>
                            <h3>Connected &amp; live</h3>
                            <ul><li>Real-time transcription &amp; live note preview</li><li>Pathology &amp; results ingestion</li><li>Hospital system &amp; EMR integration</li><li>Security certification</li></ul>
                        </div>
                        <div class="rmcard lite reveal" data-delay="4">
                            <div class="ph"><div class="pn"><svg viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="14" x2="23" y2="14"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="14" x2="4" y2="14"/></svg></div><div class="pt">6 &rarr; 18 months</div></div>
                            <h3>Hospital-grade intelligence</h3>
                            <ul><li>Coding-ready structured output</li><li>Evidence: guideline-backed answers at the point of care</li><li>Specialty-tuned models across disciplines</li><li>Organisation analytics &amp; insights</li></ul>
                        </div>
                        <div class="rmcard climax reveal" data-delay="5">
                            <span class="flag"><svg viewBox="0 0 24 24"><path d="M12 2l2.4 7.4H22l-6 4.6 2.3 7.4L12 17l-6.3 4.4L8 14 2 9.4h7.6z"/></svg>On the horizon</span>
                            <div class="ph"><div class="pn"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="6"/><polyline points="12 10 12 12 13 13"/><path d="M16.5 17.4l-.34 3.8a2 2 0 0 1-2 1.8H9.84a2 2 0 0 1-2-1.8l-.34-3.8m0-10.8l.34-3.8A2 2 0 0 1 9.84 1h4.32a2 2 0 0 1 2 1.8l.34 3.8"/></svg></div><div class="pt">The horizon</div></div>
                            <h3>Agentic &amp; autonomous</h3>
                            <ul><li>Ambient, continuous listening across the ward</li><li>Autonomous care coordination: book, refer, request, draft, you approve</li><li>Practice brain: reason over years of care, not just notes</li><li>Hardware beyond the phone: Arvi Badge &amp; Room</li></ul>
                        </div>
                    </div>
                    <p class="rm-cap reveal" data-delay="6">The long-term goal is not transcription. It is a longitudinal memory across every conversation, referral and result that agents can act on, an autonomous healthcare operating system.</p>
                </div>
            </div>
        </section>
'''

BODY = (INTRO + PROBLEM + APP + HOWITWORKS + BRAIN + INTEGRATION + SL_ROLE + SL_VISION + ROADMAP_SL
        + gen.APPENDIX + gen.FEAT)

HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="robots" content="noindex, nofollow, noarchive">
    <title>Arvi Health &middot; Mobile, Roadmap &amp; Features</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>''' + gen.CSS + '''    </style>
</head>
<body>
    <div class="progress" id="prog"><span></span></div>
    <nav class="nav">
        <a href="https://arvihealth.com" target="_blank" rel="noopener" class="logo"><img src="arvi logo.avif" alt="Arvi Health"></a>
        <div class="dots" id="dots"></div>
        <div class="nav-tag">Prepared for <b>Hospital Leadership</b> &middot; Sri Lanka</div>
    </nav>

    <main class="deck" id="deck">
''' + BODY + '''    </main>

    <div class="counter"><span><b id="cur">1</b> / <span id="total">0</span></span><span class="sec" id="sec">Overview</span></div>

    <script>''' + gen.SCRIPT + '''</script>
    <script>
    (function(){
        var el=document.getElementById('slrot'); if(!el) return;
        var words=['consult','ward round','procedure','discharge','clinic','emergency'];
        var i=0;
        setInterval(function(){
            el.classList.add('swap');
            setTimeout(function(){ i=(i+1)%words.length; el.textContent=words[i]; el.classList.remove('swap'); },340);
        },2200);
    })();
    </script>
</body>
</html>
'''

OUT = 'arvi-sri-lanka.html'

if __name__ == "__main__":
    with io.open(OUT, 'w', encoding='utf-8') as f:
        f.write(HTML)
    print("slides:", HTML.count('<section class="slide"'))
    print("videos:", HTML.count('<video'))
    print("WROTE", OUT)
