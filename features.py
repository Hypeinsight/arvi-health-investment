# -*- coding: utf-8 -*-
# Self-guided onboarding walkthrough with an interactive GP / Specialist fork.
# The viewer picks a path and only that path's slides show. Steps that have no
# product video are illustrated with CSS animation. Reuses gen.py CSS + feat_slide,
# but ships its own path-aware engine. No em dashes; AU English spelling.
import io
import gen

SIGNUP = "https://platform.arvihealth.com/signup?utm_source=onboarding-deck&utm_medium=deck&utm_campaign=signup"

# ------------------------------------------------------------------ styles ----
EXTRA_CSS = '''
        /* animated step illustrations (slides with no video) */
        .steps.anim .sic{animation:sicPulse 3.6s ease-in-out infinite}
        .steps.anim .step:nth-child(1) .sic{animation-delay:0s}
        .steps.anim .step:nth-child(2) .sic{animation-delay:.45s}
        .steps.anim .step:nth-child(3) .sic{animation-delay:.9s}
        .steps.anim .step:nth-child(4) .sic{animation-delay:1.35s}
        @keyframes sicPulse{0%,72%,100%{transform:scale(1);box-shadow:0 7px 18px rgba(4,85,163,.25)}10%{transform:scale(1.13);box-shadow:0 12px 30px rgba(105,26,106,.5)}}
        /* finale capability chips pop in sequence */
        .slide.active .menu.pop .mi{opacity:0;animation:chipPop .5s cubic-bezier(.34,1.4,.5,1) forwards}
        .slide.active .menu.pop .mi:nth-child(1){animation-delay:.15s}
        .slide.active .menu.pop .mi:nth-child(2){animation-delay:.27s}
        .slide.active .menu.pop .mi:nth-child(3){animation-delay:.39s}
        .slide.active .menu.pop .mi:nth-child(4){animation-delay:.51s}
        .slide.active .menu.pop .mi:nth-child(5){animation-delay:.63s}
        .slide.active .menu.pop .mi:nth-child(6){animation-delay:.75s}
        .slide.active .menu.pop .mi:nth-child(7){animation-delay:.87s}
        .slide.active .menu.pop .mi:nth-child(8){animation-delay:.99s}
        .slide.active .menu.pop .mi:nth-child(9){animation-delay:1.11s}
        @keyframes chipPop{0%{opacity:0;transform:translateY(12px) scale(.9)}100%{opacity:1;transform:none}}
        /* GP / specialist path picker */
        .pathpick{display:grid;grid-template-columns:1fr 1fr;gap:clamp(1rem,2.5vw,2rem);max-width:900px;margin:clamp(1.1rem,2.8vh,2rem) auto 0}
        .pathbtn{position:relative;text-align:left;cursor:pointer;padding:clamp(1.3rem,2.3vw,2.1rem);border-radius:var(--r-lg);border:2px solid var(--glass-border);background:var(--glass);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);box-shadow:var(--s-sm);transition:transform .3s cubic-bezier(.22,1,.36,1),box-shadow .3s,border-color .3s;display:flex;flex-direction:column;gap:.55rem;font-family:inherit}
        .pathbtn:hover{transform:translateY(-5px);box-shadow:var(--s-md)}
        .pathbtn h3{font-size:clamp(1.1rem,1.5vw,1.4rem);color:var(--primary-dark)}
        .pathbtn p{font-size:clamp(.82rem,1vw,.95rem);color:var(--muted);line-height:1.45}
        .pathbtn .go{margin-top:.3rem;font-size:.8rem;font-weight:800;letter-spacing:.02em;color:var(--accent);display:inline-flex;align-items:center;gap:.35rem}
        body[data-chosen="gp"] .pathbtn[data-p="gp"],body[data-chosen="spec"] .pathbtn[data-p="spec"]{border-color:transparent;background:linear-gradient(var(--bg),var(--bg)) padding-box,linear-gradient(135deg,var(--primary),var(--accent)) border-box;box-shadow:var(--s-md)}
        body[data-chosen="gp"] .pathbtn[data-p="gp"] .go span,body[data-chosen="spec"] .pathbtn[data-p="spec"] .go span{display:none}
        .pathbtn .go::after{content:""}
        body[data-chosen="gp"] .pathbtn[data-p="gp"] .go::after,body[data-chosen="spec"] .pathbtn[data-p="spec"] .go::after{content:"Now viewing"}
        @media (max-width:760px){.pathpick{grid-template-columns:1fr}}
        @media (prefers-reduced-motion:reduce){.steps.anim .sic{animation:none}.slide.active .menu.pop .mi{animation:none;opacity:1}}
'''

# --------------------------------------------------- video-slide helper ----
_idx = [0]
def vid(section, title, subtitle, points, clip, url, path=None):
    _idx[0] += 1
    i = _idx[0]
    html = gen.feat_slide(i, "v%d" % i, section, title, subtitle, points, clip, url, reverse=(i % 2 == 0))
    if path:
        html = html.replace('id="v%d" data-sec=' % i, 'id="v%d" data-path="%s" data-sec=' % (i, path), 1)
    return html

# ----------------------------------------------------- framing slides ----

INTRO = '''        <!-- Punch intro -->
        <section class="slide" id="s-intro" data-sec="Welcome">
            <div class="inner">
                <div class="intro">
                    <div class="feature-copy">
                        <div class="badge reveal"><span class="pulse"></span> A guided walkthrough</div>
                        <h1 class="reveal" data-delay="1">Meet Arvi.<br><span>Let's take a look.</span></h1>
                        <p class="reveal" data-delay="2">A quick walk through how Arvi turns your consultations into finished notes and letters. Scroll, or use the arrow keys, to move through it. There is a sign-up link waiting at the end.</p>
                        <div class="tags reveal" data-delay="3"><span class="tag">For GPs &amp; specialists</span><span class="tag">Web &amp; mobile</span><span class="tag">Live today</span></div>
                    </div>
                    <figure class="clip reveal" data-delay="2">
                        <div class="clip-glow"></div>
                        <div class="clip-frame"><video src="arvi-demo.mp4" autoplay loop muted playsinline preload="metadata"></video></div>
                    </figure>
                </div>
            </div>
        </section>
'''

OUTLINE = '''        <!-- Outline -->
        <section class="slide" id="s-outline" data-sec="Overview">
            <div class="inner">
                <div class="divider">
                    <div class="label reveal" style="justify-content:center"><svg viewBox="0 0 24 24"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg> What You'll See</div>
                    <div class="big reveal" data-delay="1">From Sign-Up to Your First Note</div>
                    <div class="menu reveal" data-delay="2">
                        <span class="mi"><b>01</b> Sign up</span>
                        <span class="mi"><b>02</b> Set up</span>
                        <span class="mi"><b>03</b> Your patients</span>
                        <span class="mi"><b>04</b> Your workflow</span>
                        <span class="mi"><b>05</b> On mobile</span>
                        <span class="mi"><b>06</b> What's next</span>
                    </div>
                    <p class="subtitle reveal" data-delay="3" style="text-align:center;font-size:clamp(.76rem,.95vw,.88rem);opacity:.66;max-width:680px;margin:clamp(.6rem,1.4vh,1rem) auto 0">The screens shown are from our current interface. A refreshed look is on the way.</p>
                </div>
            </div>
        </section>
'''

SIGNUP_STEPS = '''        <!-- How simple sign-up is (animated) -->
        <section class="slide" id="s-signup-steps" data-sec="Sign Up">
            <div class="inner">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><line x1="19" y1="8" x2="19" y2="14"/><line x1="22" y1="11" x2="16" y2="11"/></svg> Sign Up</div>
                    <h2 class="title reveal" data-delay="1">Signing Up Takes About a Minute</h2>
                    <p class="subtitle reveal" data-delay="2">No sales call, no setup fee. You can be recording your first consultation today.</p>
                </div>
                <div class="steps anim">
                    <div class="step reveal" data-delay="2"><div class="sic"><svg viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg></div><div class="sn">STEP 01</div><h3>Open the sign-up page</h3><p>Head to the Arvi platform in any browser.</p></div>
                    <div class="step reveal" data-delay="3"><div class="sic"><svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg></div><div class="sn">STEP 02</div><h3>Enter your details</h3><p>Name, email and your practice. That is it.</p></div>
                    <div class="step reveal" data-delay="4"><div class="sic"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg></div><div class="sn">STEP 03</div><h3>You're in</h3><p>Straight to your dashboard, ready to set up.</p></div>
                </div>
            </div>
        </section>
'''

SETUP_STEPS = '''        <!-- Initial setup (animated) -->
        <section class="slide" id="s-setup" data-sec="Set Up">
            <div class="inner">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg> Set Up</div>
                    <h2 class="title reveal" data-delay="1">Set Up Your Practice, Once</h2>
                    <p class="subtitle reveal" data-delay="2">A few minutes now, and every letter you generate comes out looking like yours.</p>
                </div>
                <div class="steps anim">
                    <div class="step reveal" data-delay="2"><div class="sic"><svg viewBox="0 0 24 24"><path d="M20 11.08V19a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h9"/><path d="M9 11l3 3L22 4"/></svg></div><div class="sn">STEP 01</div><h3>Upload your signature</h3><p>Signed letters, without printing and scanning.</p></div>
                    <div class="step reveal" data-delay="3"><div class="sic"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg></div><div class="sn">STEP 02</div><h3>Add your logo</h3><p>Your practice branding on every document.</p></div>
                    <div class="step reveal" data-delay="4"><div class="sic"><svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="8" y1="13" x2="16" y2="13"/></svg></div><div class="sn">STEP 03</div><h3>Pick a template</h3><p>Choose the letter format that suits you.</p></div>
                    <div class="step reveal" data-delay="5"><div class="sic"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg></div><div class="sn">STEP 04</div><h3>You're ready</h3><p>Time to see it work.</p></div>
                </div>
            </div>
        </section>
'''

CHOICE = '''        <!-- GP / specialist fork -->
        <section class="slide" id="s-path" data-sec="Your Path">
            <div class="inner">
                <div class="slide-head" style="text-align:center">
                    <div class="label reveal" style="justify-content:center"><svg viewBox="0 0 24 24"><path d="M6 3v12"/><circle cx="18" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M18 9a9 9 0 0 1-9 9"/></svg> Your Path</div>
                    <h2 class="title reveal" data-delay="1">Are You a GP or a Specialist?</h2>
                    <p class="subtitle reveal" data-delay="2">Pick your path and the walkthrough follows your workflow. You can switch any time.</p>
                </div>
                <div class="pathpick">
                    <button class="pathbtn reveal" data-delay="3" data-p="gp" onclick="arviSetPath('gp')">
                        <div class="vic"><svg viewBox="0 0 24 24"><path d="M12 2a3 3 0 0 0-3 3v1a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3z"/><path d="M19 10a7 7 0 0 1-14 0"/><line x1="12" y1="17" x2="12" y2="22"/></svg></div>
                        <h3>General Practitioner</h3>
                        <p>Quick consults, referral letters to specialists, and fast records between patients.</p>
                        <span class="go"><span>See the GP workflow</span></span>
                    </button>
                    <button class="pathbtn reveal" data-delay="4" data-p="spec" onclick="arviSetPath('spec')">
                        <div class="vic"><svg viewBox="0 0 24 24"><path d="M8 2v4a4 4 0 0 0 8 0V2"/><path d="M6 6v5a6 6 0 0 0 12 0V6"/><path d="M12 17v0a5 5 0 0 0 5-5"/><circle cx="19" cy="10" r="2"/></svg></div>
                        <h3>Specialist</h3>
                        <p>Detailed consultations, specialist letters back to the referring GP, and patient summaries.</p>
                        <span class="go"><span>See the specialist workflow</span></span>
                    </button>
                </div>
            </div>
        </section>
'''

GP_DIV = '''        <!-- GP path divider -->
        <section class="slide" id="s-gp" data-path="gp" data-sec="GP Workflow">
            <div class="inner">
                <div class="divider">
                    <div class="label reveal" style="justify-content:center"><svg viewBox="0 0 24 24"><path d="M12 2a3 3 0 0 0-3 3v1a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3z"/><path d="M19 10a7 7 0 0 1-14 0"/><line x1="12" y1="17" x2="12" y2="22"/></svg> GP Workflow</div>
                    <div class="big reveal" data-delay="1">A Day in General Practice</div>
                    <p class="subtitle reveal" data-delay="2" style="text-align:center;max-width:700px;margin:0 auto">See a patient, capture the consult, write the referral, and move on. Here is how Arvi fits your day.</p>
                </div>
            </div>
        </section>
'''

SPEC_DIV = '''        <!-- Specialist path divider -->
        <section class="slide" id="s-spec" data-path="spec" data-sec="Specialist Workflow">
            <div class="inner">
                <div class="divider">
                    <div class="label reveal" style="justify-content:center"><svg viewBox="0 0 24 24"><path d="M8 2v4a4 4 0 0 0 8 0V2"/><path d="M6 6v5a6 6 0 0 0 12 0V6"/><circle cx="19" cy="10" r="2"/></svg> Specialist Workflow</div>
                    <div class="big reveal" data-delay="1">A Specialist Consultation</div>
                    <p class="subtitle reveal" data-delay="2" style="text-align:center;max-width:700px;margin:0 auto">Take the consultation, generate the note, and send your letter back to the referring GP. Here is how Arvi fits your practice.</p>
                </div>
            </div>
        </section>
'''

MEETING = '''        <!-- Meeting minutes -->
        <section class="slide" id="s-meeting" data-sec="Beyond Consults">
            <div class="inner">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg> Beyond Consults</div>
                    <h2 class="title reveal" data-delay="1">Not Every Recording Is a Patient</h2>
                    <p class="subtitle reveal" data-delay="2">Running a business meeting or a case conference? Arvi captures the minutes too, structured and ready to share, with the same record-and-review flow.</p>
                </div>
                <div class="cards c2" style="max-width:960px;margin:clamp(1rem,2.4vh,1.8rem) auto 0">
                    <div class="card glass reveal" data-delay="3" style="display:flex;flex-direction:column"><div class="vic"><svg viewBox="0 0 24 24"><path d="M3 3h18v14H8l-5 4V3z"/></svg></div><h3>Business meetings</h3><p>Turn the discussion into clean minutes with decisions and actions captured.</p></div>
                    <div class="card glass reveal" data-delay="4" style="display:flex;flex-direction:column"><div class="vic"><svg viewBox="0 0 24 24"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg></div><h3>Case conferences</h3><p>Document a multidisciplinary discussion without anyone playing scribe.</p></div>
                </div>
            </div>
        </section>
'''

MOBILE_STEPS = '''        <!-- Mobile guided install (animated) -->
        <section class="slide" id="s-mobile" data-sec="On Mobile">
            <div class="inner fill">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><rect x="5" y="2" width="14" height="20" rx="2"/><line x1="12" y1="18" x2="12.01" y2="18"/></svg> On Mobile</div>
                    <h2 class="title reveal" data-delay="1">Take Arvi to the Bedside</h2>
                    <p class="subtitle reveal" data-delay="2">The same Arvi, on the phone in your pocket. Set it up in four steps.</p>
                </div>
                <div class="steps anim">
                    <div class="step reveal" data-delay="2"><div class="sic"><svg viewBox="0 0 24 24"><path d="M3 7V5a2 2 0 0 1 2-2h2"/><path d="M17 3h2a2 2 0 0 1 2 2v2"/><path d="M21 17v2a2 2 0 0 1-2 2h-2"/><path d="M7 21H5a2 2 0 0 1-2-2v-2"/><line x1="7" y1="12" x2="17" y2="12"/></svg></div><div class="sn">STEP 01</div><h3>Scan the QR</h3><p>Point your camera at the code below.</p></div>
                    <div class="step reveal" data-delay="3"><div class="sic"><svg viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg></div><div class="sn">STEP 02</div><h3>Install the app</h3><p>From the App Store or Google Play.</p></div>
                    <div class="step reveal" data-delay="4"><div class="sic"><svg viewBox="0 0 24 24"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/></svg></div><div class="sn">STEP 03</div><h3>Sign in</h3><p>The same account you just created.</p></div>
                    <div class="step reveal" data-delay="5"><div class="sic"><svg viewBox="0 0 24 24"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/></svg></div><div class="sn">STEP 04</div><h3>Record anywhere</h3><p>Ward, clinic or theatre, note done.</p></div>
                </div>
                <div class="dl compact reveal" data-delay="6">
                    <a class="dlcard" href="https://apps.apple.com/au/app/arvi-health/id6761469752" target="_blank" rel="noopener"><img src="qr-ios.png" alt="Download Arvi on the App Store"><div><div class="dt"><svg viewBox="0 0 24 24"><path d="M3 7V5a2 2 0 0 1 2-2h2"/><path d="M17 3h2a2 2 0 0 1 2 2v2"/><path d="M21 17v2a2 2 0 0 1-2 2h-2"/><path d="M7 21H5a2 2 0 0 1-2-2v-2"/><line x1="7" y1="12" x2="17" y2="12"/></svg>Scan to install</div><div class="dn">Arvi for iOS</div><div class="ds">App Store</div></div></a>
                    <a class="dlcard" href="https://play.google.com/store/apps/details?id=com.healthai.mobile" target="_blank" rel="noopener"><img src="qr-android.png" alt="Download Arvi on Google Play"><div><div class="dt"><svg viewBox="0 0 24 24"><path d="M3 7V5a2 2 0 0 1 2-2h2"/><path d="M17 3h2a2 2 0 0 1 2 2v2"/><path d="M21 17v2a2 2 0 0 1-2 2h-2"/><path d="M7 21H5a2 2 0 0 1-2-2v-2"/><line x1="7" y1="12" x2="17" y2="12"/></svg>Scan to install</div><div class="dn">Arvi for Android</div><div class="ds">Google Play</div></div></a>
                </div>
            </div>
        </section>
'''

HEALTHLINK = '''        <!-- HealthLink coming soon -->
        <section class="slide" id="s-healthlink" data-sec="Coming Soon">
            <div class="inner">
                <div class="slide-head">
                    <div class="badge reveal" style="margin:0 auto clamp(.6rem,1.4vh,1rem)"><span class="pulse"></span> Coming soon</div>
                    <h2 class="title reveal" data-delay="1" style="text-align:center">HealthLink Integration, Arriving Soon</h2>
                    <p class="subtitle reveal" data-delay="2" style="text-align:center;max-width:760px;margin:0 auto">Soon Arvi will send letters straight into the practice software you already run, over HealthLink. Documents land where they belong, without copy and paste.</p>
                </div>
                <div class="cards c3">
                    <div class="card glass reveal" data-delay="3"><div class="vic"><svg viewBox="0 0 24 24"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg></div><h3>Straight to the record</h3><p>Letters delivered into your existing practice software.</p></div>
                    <div class="card glass reveal" data-delay="4"><div class="vic"><svg viewBox="0 0 24 24"><path d="M22 2 11 13"/><path d="M22 2 15 22l-4-9-9-4 20-7z"/></svg></div><h3>Secure messaging</h3><p>Over HealthLink, the standard rail clinics already trust.</p></div>
                    <div class="card glass reveal" data-delay="5"><div class="vic"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg></div><h3>No copy and paste</h3><p>The last manual step in documentation, gone.</p></div>
                </div>
            </div>
        </section>
'''

FINALE = '''        <!-- Finale + sign up -->
        <section class="slide" id="s-signup" data-sec="Get Started">
            <div class="inner">
                <div class="divider">
                    <div class="label reveal" style="justify-content:center"><svg viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg> That's Arvi</div>
                    <div class="big reveal" data-delay="1">Everything, in One Place</div>
                    <div class="menu pop" data-delay="2" style="max-width:840px">
                        <span class="mi">Consult notes</span>
                        <span class="mi">Referral letters</span>
                        <span class="mi">Specialist letters</span>
                        <span class="mi">Patient summaries</span>
                        <span class="mi">Meeting minutes</span>
                        <span class="mi">Quick record</span>
                        <span class="mi">Telehealth</span>
                        <span class="mi">Mobile capture</span>
                        <span class="mi">Your templates</span>
                    </div>
                    <p class="subtitle reveal" data-delay="3" style="text-align:center;max-width:680px;margin:clamp(.6rem,1.4vh,1rem) auto 0">You have seen how it works. Create your account and turn your next consultation into a finished note. From $30 a month, with a 30 day free trial.</p>
                    <a class="cta reveal" data-delay="4" href="''' + SIGNUP + '''&utm_content=end-cta" target="_blank" rel="noopener">Sign up for free <svg viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg></a>
                </div>
            </div>
        </section>
'''

# ------------------------------------------------------ the workflow ----
BODY = (
    INTRO + OUTLINE + SIGNUP_STEPS + SETUP_STEPS
    + vid("Set up", "Your Letters, Your Format",
          "Build templates that match your practice, GP referrals or specialist letters, so every document comes out in your house style.",
          [("sliders", "Build your own", "Reusable templates for any letter type."),
           ("edit", "Tune the formatting", "Adjust layout and styling to suit you.")],
          "08-custom-template.mp4", "platform.arvihealth.com &middot; Templates")
    + vid("Your patients", "Bring Your Patients In",
          "Add your patient list with a simple upload. Manual today by CSV, with automatic sync from your practice software on the way.",
          [("users", "Upload by CSV", "Import your patient list in one step."),
           ("eye", "Admin oversight", "Manage patients across the practice.")],
          "02-admin-access.mp4", "platform.arvihealth.com &middot; Admin")
    + vid("Your patients", "Your Day, on One Screen",
          "The home page opens on today's appointments, so every consultation starts a tap away from documentation.",
          [("calendar", "Appointments &amp; calendar", "See the day's schedule at a glance."),
           ("users", "Patient records", "Details sit right beside the notes.")],
          "10-patient-management.mp4", "platform.arvihealth.com &middot; Patients")
    + CHOICE
    # -------- GP path --------
    + GP_DIV
    + vid("GP workflow", "Start the Consult",
          "Open the appointment, or Quick Create if the patient is not booked in. One tap and you are recording.",
          [("zap", "Quick Create", "No appointment needed to get going."),
           ("mic", "One tap to record", "Minimal steps between you and a note.")],
          "03-quick-record.mp4", "Arvi &middot; Quick Record", path="gp")
    + vid("GP workflow", "Your Consultation Note",
          "Arvi writes the GP consult note while you focus on the patient, structured and ready to review in seconds.",
          [("mic", "Record &amp; structure", "Ambient capture becomes a clean note."),
           ("check", "Review, don't author", "Edit a draft, don't write from scratch.")],
          "01-letter-generation.mp4", "platform.arvihealth.com &middot; New note", path="gp")
    + vid("GP workflow", "Write the Referral",
          "Generate the referral letter to the specialist from the same recording, then preview and format it on one page.",
          [("file", "Referral, drafted for you", "A ready-to-send referral, automatically."),
           ("edit", "Preview &amp; formatting", "Final review before it goes out.")],
          "07-edit-letter.mp4", "platform.arvihealth.com &middot; Referral", path="gp")
    + vid("GP workflow", "Send It On",
          "Email the referral to the specialist from Arvi, and resend any time it is needed.",
          [("send", "Send from Arvi", "Deliver without leaving the app."),
           ("mail", "Resend any time", "Re-issue a letter in one click.")],
          "09-approve-resend.mp4", "platform.arvihealth.com &middot; Send", path="gp")
    # -------- Specialist path --------
    + SPEC_DIV
    + vid("Specialist workflow", "Take the Consultation",
          "Open the referred patient, or Quick Create if needed. One tap and Arvi is capturing the consultation.",
          [("zap", "Quick Create", "Start even without a booking."),
           ("mic", "One tap to record", "Minimal steps between you and a note.")],
          "03-quick-record.mp4", "Arvi &middot; Quick Record", path="spec")
    + vid("Specialist workflow", "Your Consultation Note",
          "Arvi writes the specialist consultation note as you talk, structured to your field and ready to review.",
          [("mic", "Record &amp; structure", "Ambient capture becomes a clean note."),
           ("check", "Review, don't author", "Edit a draft, don't write from scratch.")],
          "01-letter-generation.mp4", "platform.arvihealth.com &middot; New note", path="spec")
    + vid("Specialist workflow", "Your Specialist Letter",
          "Generate the specialist letter back to the referring GP from the same recording, then preview and format it.",
          [("file", "Letter to the GP", "A ready-to-send specialist letter."),
           ("edit", "Preview &amp; formatting", "Final review before it goes out.")],
          "07-edit-letter.mp4", "platform.arvihealth.com &middot; Specialist letter", path="spec")
    + vid("Specialist workflow", "Send Back to the GP",
          "Email the letter to the referring GP from Arvi, and resend any time. A patient summary is a click away too.",
          [("send", "Send from Arvi", "Close the loop with the referrer."),
           ("mail", "Resend any time", "Re-issue a letter in one click.")],
          "09-approve-resend.mp4", "platform.arvihealth.com &middot; Send", path="spec")
    # -------- shared, both paths converge --------
    + vid("Everyone", "Refine in a Click",
          "Regenerate or adjust any section until the wording is exactly right. The AI drafts, you decide.",
          [("refresh", "Regenerate on demand", "Redo a section or the whole document."),
           ("sliders", "You stay in control", "The final wording is always yours.")],
          "06-regeneration.mp4", "platform.arvihealth.com &middot; Regenerate")
    + vid("Everyone", "Already Have a Recording?",
          "Upload existing audio and Arvi produces the same structured note. No live capture required.",
          [("upload", "Bring your own audio", "Drop in a file recorded anywhere."),
           ("file", "Same structured output", "The same clean clinical note.")],
          "05-upload-recording.mp4", "platform.arvihealth.com &middot; Upload")
    + vid("Everyone", "Remote Consults, Same Flow",
          "Run telehealth inside Arvi and document it exactly as an in-person visit.",
          [("video", "Consults in-app", "No separate telehealth tool."),
           ("mic", "Documented automatically", "The same capture-to-note flow.")],
          "13-telehealth.mp4", "platform.arvihealth.com &middot; Telehealth")
    + vid("Everyone", "Nothing Slips",
          "Track outstanding work to completion, from the consult through to the follow up.",
          [("tasks", "Track outstanding work", "A clear list of what still needs doing."),
           ("check", "Close the loop", "Mark tasks done as the work gets done.")],
          "11-task-management.mp4", "platform.arvihealth.com &middot; Tasks")
    + MEETING
    + vid("Your team", "Add Your Team, Free Admin Included",
          "Invite clinicians into your organisation, with a free administrator seat for oversight at no cost.",
          [("userplus", "Invite in seconds", "Bring new users in with an invite."),
           ("user", "Free admin seat", "Oversight without an extra licence.")],
          "18-free-admin.mp4", "platform.arvihealth.com &middot; Admin")
    + MOBILE_STEPS
    + vid("On mobile", "Even in Theatre",
          "Capture the operation note on your phone, even on low connectivity, syncing when you are back online.",
          [("phone", "In-theatre capture", "Created at the point of care."),
           ("wifi", "Low-connectivity ready", "Syncs when you reconnect.")],
          "04-mobile-recording.mp4", "Arvi mobile &middot; Operating theatre")
    + HEALTHLINK
    + vid("Pricing", "Simple, Transparent Pricing",
          "From $30 a month with 10 hours of documentation included, and 10-hour top-up packs when you need more. Start with a 30 day free trial.",
          [("card", "From $30 / month", "Ten hours included in the base plan."),
           ("check", "Pay as you grow", "Add 10-hour packs only when needed, no lock-in.")],
          "19-subscription.mp4", "platform.arvihealth.com &middot; Pricing")
    + FINALE
)

# ---- path-aware deck engine (self-contained; not gen.SCRIPT) ----
ENGINE = r"""
(function(){
  var deck=document.getElementById('deck');
  var dotsWrap=document.getElementById('dots');
  var cur=document.getElementById('cur');
  var totalEl=document.getElementById('total');
  var secEl=document.getElementById('sec');
  var prog=document.getElementById('prog');
  var all=[].slice.call(document.querySelectorAll('.slide'));
  var path='gp';

  function ok(s){var p=s.getAttribute('data-path');return !p||p==='all'||p===path;}
  function vis(){return all.filter(ok);}

  function buildDots(){
    dotsWrap.innerHTML='';
    vis().forEach(function(s,i){
      var b=document.createElement('button');
      b.className='dot'; b.setAttribute('aria-label','Slide '+(i+1));
      b.addEventListener('click',function(){s.scrollIntoView({behavior:'smooth',inline:'start'});});
      dotsWrap.appendChild(b);
    });
  }
  function apply(){
    all.forEach(function(s){ s.style.display=ok(s)?'':'none'; });
    buildDots(); totalEl.textContent=vis().length; update(); syncVideos();
  }
  window.arviSetPath=function(p){
    path=p; document.body.setAttribute('data-chosen',p); apply();
    var first=all.filter(function(s){return s.getAttribute('data-path')===p;})[0];
    if(first){ setTimeout(function(){ first.scrollIntoView({behavior:'smooth',inline:'start'}); },90); }
  };

  var raf;
  function update(){
    var v=vis();
    var idx=Math.round(deck.scrollLeft/deck.clientWidth);
    if(idx<0)idx=0; if(idx>v.length-1)idx=v.length-1;
    var dots=[].slice.call(dotsWrap.children);
    dots.forEach(function(d,k){ d.classList.toggle('active',k===idx); });
    if(v[idx])v[idx].classList.add('active');
    if(cur)cur.textContent=idx+1;
    if(secEl&&v[idx])secEl.textContent=v[idx].getAttribute('data-sec')||'';
    var max=deck.scrollWidth-deck.clientWidth;
    prog.style.setProperty('--p', max>0?(deck.scrollLeft/max).toFixed(4):'0');
  }
  function syncVideos(){
    var v=vis(); var idx=Math.round(deck.scrollLeft/deck.clientWidth);
    v.forEach(function(s,k){
      [].forEach.call(s.querySelectorAll('video'),function(vd){
        if(k===idx){ if(vd.paused){ var p=vd.play(); if(p)p.catch(function(){}); } }
        else if(!vd.paused){ try{vd.pause();}catch(e){} }
      });
    });
  }
  var t;
  deck.addEventListener('scroll',function(){
    if(!raf){ raf=requestAnimationFrame(function(){ update(); raf=null; }); }
    clearTimeout(t); t=setTimeout(syncVideos,120);
  });
  addEventListener('keydown',function(ev){
    var v=vis(); var i=Math.round(deck.scrollLeft/deck.clientWidth);
    if(ev.key==='ArrowRight'||ev.key==='PageDown'||ev.key===' '){ev.preventDefault(); if(i<v.length-1)v[i+1].scrollIntoView({behavior:'smooth',inline:'start'});}
    else if(ev.key==='ArrowLeft'||ev.key==='PageUp'){ev.preventDefault(); if(i>0)v[i-1].scrollIntoView({behavior:'smooth',inline:'start'});}
    else if(ev.key==='Home'){ev.preventDefault(); v[0].scrollIntoView({behavior:'smooth',inline:'start'});}
    else if(ev.key==='End'){ev.preventDefault(); v[v.length-1].scrollIntoView({behavior:'smooth',inline:'start'});}
  });
  document.body.setAttribute('data-chosen',path);
  apply();
  window.addEventListener('load',syncVideos);
})();
"""

HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="robots" content="noindex, nofollow, noarchive">
    <title>Arvi Health &middot; Guided Walkthrough</title>
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
        <div class="nav-tag">Arvi &middot; <b>Guided Walkthrough</b></div>
    </nav>

    <main class="deck" id="deck">
''' + BODY + '''    </main>

    <div class="counter"><span><b id="cur">1</b> / <span id="total">0</span></span><span class="sec" id="sec">Overview</span></div>

    <script>''' + ENGINE + '''</script>
</body>
</html>
'''

OUT = 'arvi-features-walkthrough.html'

if __name__ == "__main__":
    with io.open(OUT, 'w', encoding='utf-8') as f:
        f.write(HTML)
    print("slides total:", HTML.count('<section class="slide"'))
    print("gp slides:", HTML.count('data-path="gp"'))
    print("spec slides:", HTML.count('data-path="spec"'))
    print("videos:", HTML.count('<video'))
    print("WROTE", OUT)
