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
        .pathbtn{position:relative;text-align:left;cursor:pointer;padding:clamp(1.4rem,2.4vw,2.2rem);border-radius:var(--r-lg);border:2px solid var(--glass-border);background:var(--glass);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);box-shadow:var(--s-sm);transition:transform .3s cubic-bezier(.22,1,.36,1),box-shadow .3s,border-color .3s;display:flex;flex-direction:column;justify-content:space-between;gap:clamp(1rem,2vh,1.6rem);font-family:inherit}
        .pathbtn:hover{transform:translateY(-5px);box-shadow:var(--s-md)}
        .pathbtn>div{display:flex;flex-direction:column;gap:.55rem}
        .pathbtn .vic{align-self:flex-start;flex:0 0 auto;width:clamp(48px,3.6vw,58px);height:clamp(48px,3.6vw,58px)}
        .pathbtn h3{font-size:clamp(1.2rem,1.6vw,1.5rem);color:var(--primary-dark)}
        .pathbtn p{font-size:clamp(.82rem,1vw,.96rem);color:var(--muted);line-height:1.45}
        .pathfeat{list-style:none;display:flex;flex-direction:column;gap:.5rem;margin-top:.3rem}
        .pathfeat li{display:flex;align-items:center;gap:.55rem;font-size:clamp(.84rem,1.02vw,.96rem);font-weight:600;color:var(--primary-dark)}
        .pathfeat li svg{width:16px;height:16px;stroke:var(--accent);stroke-width:2.6;fill:none;flex-shrink:0}
        .pathbtn .go{font-size:.82rem;font-weight:800;letter-spacing:.02em;color:var(--accent);display:inline-flex;align-items:center;gap:.4rem}
        .pathbtn .go::before{content:"\\2192 ";font-weight:800}
        body[data-chosen="gp"] .pathbtn[data-p="gp"],body[data-chosen="spec"] .pathbtn[data-p="spec"]{border-color:transparent;background:linear-gradient(var(--bg),var(--bg)) padding-box,linear-gradient(135deg,var(--primary),var(--accent)) border-box;box-shadow:var(--s-md)}
        body[data-chosen="gp"] .pathbtn[data-p="gp"] .go span,body[data-chosen="spec"] .pathbtn[data-p="spec"] .go span{display:none}
        .pathbtn .go::after{content:""}
        body[data-chosen="gp"] .pathbtn[data-p="gp"] .go::after,body[data-chosen="spec"] .pathbtn[data-p="spec"] .go::after{content:"Now viewing"}
        @media (max-width:760px){.pathpick{grid-template-columns:1fr}}
        @media (prefers-reduced-motion:reduce){.steps.anim .sic{animation:none}.slide.active .menu.pop .mi{animation:none;opacity:1}}
        /* split-view app panel: live app on the right, guide still on the left */
        body.split{--pw:min(46vw,660px)}
        .apppanel{position:fixed;top:0;right:0;bottom:0;width:min(46vw,660px);z-index:1200;background:#fff;box-shadow:-18px 0 50px -20px rgba(4,55,98,.45);transform:translateX(101%);transition:transform .42s cubic-bezier(.22,1,.36,1);display:flex;flex-direction:column}
        body.split .apppanel{transform:none}
        .apppanel-head{display:flex;align-items:center;justify-content:space-between;gap:1rem;padding:.7rem 1rem;border-bottom:1px solid var(--line);flex-shrink:0;background:var(--bg)}
        .apppanel-head .t{display:flex;align-items:center;gap:.5rem;font-weight:700;color:var(--primary-dark);font-size:.92rem}
        .apppanel-head .t .dotlive{width:8px;height:8px;border-radius:50%;background:#16a34a;box-shadow:0 0 0 0 rgba(22,163,74,.5);animation:pulse 2s infinite}
        .apppanel-close{border:none;background:rgba(4,55,98,.07);width:32px;height:32px;border-radius:50%;cursor:pointer;font-size:1.25rem;color:var(--muted);line-height:1;display:flex;align-items:center;justify-content:center;flex-shrink:0;transition:background .2s}
        .apppanel-close:hover{background:rgba(4,55,98,.14);color:var(--primary-dark)}
        .apppanel iframe{flex:1;width:100%;border:0;display:block;background:#fff}
        .apppanel-foot{padding:.5rem 1rem;font-size:.72rem;color:var(--muted);text-align:center;border-top:1px solid var(--line);flex-shrink:0}
        .apppanel-foot a{color:var(--accent);font-weight:700;text-decoration:none}
        body.split .deck{width:calc(100vw - var(--pw))}
        body.split .slide{flex:0 0 calc(100vw - var(--pw));width:calc(100vw - var(--pw));overflow-y:auto}
        body.split .nav{right:var(--pw)}
        body.split .progress{right:var(--pw);width:auto}
        body.split .counter{right:calc(var(--pw) + clamp(1rem,3vw,2.4rem))}
        @media (max-width:820px){
            .apppanel{width:100vw}
            body.split{--pw:100vw}
            body.split .deck,body.split .slide{width:100vw;flex-basis:100vw}
            body.split .nav,body.split .progress{right:0}
            body.split .counter{right:clamp(1rem,3vw,2.4rem)}
        }
        /* click a slide video to enlarge it (opens over the deck, clear of the panel) */
        .clip-frame{cursor:zoom-in;position:relative}
        .clip-frame::after{content:"\\2922";position:absolute;right:10px;bottom:8px;width:32px;height:32px;border-radius:9px;background:rgba(4,39,64,.5);color:#fff;font-size:18px;line-height:32px;text-align:center;opacity:0;transition:opacity .25s;pointer-events:none;z-index:3}
        .clip-frame:hover::after{opacity:1}
        .vlight{position:fixed;top:0;right:0;bottom:0;left:0;z-index:1150;display:none;align-items:center;justify-content:center;padding:clamp(16px,3vw,44px)}
        .vlight.on{display:flex}
        body.split .vlight{right:var(--pw)}
        .vlight-bd{position:absolute;inset:0;background:rgba(4,39,64,.74);backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px)}
        .vlight video{position:relative;z-index:1;width:auto;max-width:100%;max-height:84vh;border-radius:14px;box-shadow:var(--s-lg);background:#000;display:block}
        .vlight-x{position:absolute;top:clamp(12px,2vh,20px);right:clamp(12px,2vw,20px);z-index:2;width:40px;height:40px;border-radius:50%;border:none;background:rgba(255,255,255,.92);cursor:pointer;font-size:1.4rem;line-height:1;color:var(--primary-dark);display:flex;align-items:center;justify-content:center;box-shadow:var(--s-md)}
        .vlight-x:hover{background:#fff}
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
                        <div class="badge reveal"><span class="pulse"></span> Getting started</div>
                        <h1 class="reveal" data-delay="1">Welcome to Arvi.<br><span>Let's get you set up.</span></h1>
                        <p class="reveal" data-delay="2">This short guide walks you through getting started on Arvi, from creating your account to sending your first letter. Scroll, or use the arrow keys, to move through it. You can create your account whenever you are ready.</p>
                        <div class="tags reveal" data-delay="3"><span class="tag">For GPs &amp; specialists</span><span class="tag">Web &amp; mobile</span><span class="tag">Set up in minutes</span></div>
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
                    <div class="label reveal" style="justify-content:center"><svg viewBox="0 0 24 24"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg> Here's the Plan</div>
                    <div class="big reveal" data-delay="1">We'll Walk Through It Together</div>
                    <div class="menu reveal" data-delay="2">
                        <span class="mi"><b>01</b> Sign up</span>
                        <span class="mi"><b>02</b> Set up</span>
                        <span class="mi"><b>03</b> Your patients</span>
                        <span class="mi"><b>04</b> Your first note</span>
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
                    <h2 class="title reveal" data-delay="1">First, Create Your Account</h2>
                    <p class="subtitle reveal" data-delay="2">It only takes a minute. Here is all there is to it.</p>
                </div>
                <div class="steps anim">
                    <div class="step reveal" data-delay="2"><div class="sic"><svg viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg></div><div class="sn">STEP 01</div><h3>Open sign-up</h3><p>Tap the button below to start.</p></div>
                    <div class="step reveal" data-delay="3"><div class="sic"><svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg></div><div class="sn">STEP 02</div><h3>Enter your details</h3><p>Your name, email and practice. That is all.</p></div>
                    <div class="step reveal" data-delay="4"><div class="sic"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg></div><div class="sn">STEP 03</div><h3>You're in</h3><p>You will land on your dashboard, ready to go.</p></div>
                </div>
                <div style="text-align:center;margin-top:clamp(1rem,2.6vh,1.8rem)">
                    <a class="cta reveal" data-delay="5" href="''' + SIGNUP + '''&utm_content=signup-step" target="_blank" rel="noopener" onclick="return openApp(event,'signup-step')">Create your account <svg viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg></a>
                </div>
            </div>
        </section>
'''

SETUP_STEPS = '''        <!-- Initial setup (animated) -->
        <section class="slide" id="s-setup" data-sec="Set Up">
            <div class="inner">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg> Set Up</div>
                    <h2 class="title reveal" data-delay="1">Next, Make It Yours</h2>
                    <p class="subtitle reveal" data-delay="2">A couple of minutes now means every letter you send looks like it came from you.</p>
                </div>
                <div class="steps anim">
                    <div class="step reveal" data-delay="2"><div class="sic"><svg viewBox="0 0 24 24"><path d="M20 11.08V19a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h9"/><path d="M9 11l3 3L22 4"/></svg></div><div class="sn">STEP 01</div><h3>Add your signature</h3><p>So your letters come out signed and ready.</p></div>
                    <div class="step reveal" data-delay="3"><div class="sic"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg></div><div class="sn">STEP 02</div><h3>Add your logo</h3><p>It will show on everything you send.</p></div>
                    <div class="step reveal" data-delay="4"><div class="sic"><svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="8" y1="13" x2="16" y2="13"/></svg></div><div class="sn">STEP 03</div><h3>Choose a template</h3><p>Pick the letter layout you like.</p></div>
                    <div class="step reveal" data-delay="5"><div class="sic"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg></div><div class="sn">STEP 04</div><h3>All set</h3><p>Now let's see it in action.</p></div>
                </div>
            </div>
        </section>
'''

CHOICE = '''        <!-- GP / specialist fork -->
        <section class="slide" id="s-path" data-sec="Your Path">
            <div class="inner">
                <div class="slide-head" style="text-align:center">
                    <div class="label reveal" style="justify-content:center"><svg viewBox="0 0 24 24"><path d="M6 3v12"/><circle cx="18" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M18 9a9 9 0 0 1-9 9"/></svg> First, Tell Us Who You Are</div>
                    <h2 class="title reveal" data-delay="1">Are You a GP or a Specialist?</h2>
                    <p class="subtitle reveal" data-delay="2">Choose one to get started.</p>
                </div>
                <div class="pathpick">
                    <button class="pathbtn reveal" data-delay="3" data-p="gp" onclick="arviSetPath('gp')">
                        <div>
                            <div class="vic"><svg viewBox="0 0 24 24"><path d="M12 2a3 3 0 0 0-3 3v1a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3z"/><path d="M19 10a7 7 0 0 1-14 0"/><line x1="12" y1="17" x2="12" y2="22"/></svg></div>
                            <h3>General Practitioner</h3>
                            <p>Quick consults and referrals to specialists.</p>
                            <ul class="pathfeat">
                                <li><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> Consult notes</li>
                                <li><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> Referral letters</li>
                                <li><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> Quick record between patients</li>
                            </ul>
                        </div>
                        <span class="go"><span>Continue as a GP</span></span>
                    </button>
                    <button class="pathbtn reveal" data-delay="4" data-p="spec" onclick="arviSetPath('spec')">
                        <div>
                            <div class="vic"><svg viewBox="0 0 24 24"><path d="M8 2v4a4 4 0 0 0 8 0V2"/><path d="M6 6v5a6 6 0 0 0 12 0V6"/><path d="M12 17v0a5 5 0 0 0 5-5"/><circle cx="19" cy="10" r="2"/></svg></div>
                            <h3>Specialist</h3>
                            <p>Detailed consultations and letters back to the GP.</p>
                            <ul class="pathfeat">
                                <li><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> Consultation notes</li>
                                <li><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> Specialist letters</li>
                                <li><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> Patient summaries</li>
                            </ul>
                        </div>
                        <span class="go"><span>Continue as a specialist</span></span>
                    </button>
                </div>
            </div>
        </section>
'''

GP_DIV = '''        <!-- GP path divider -->
        <section class="slide" id="s-gp" data-path="gp" data-sec="For GPs">
            <div class="inner">
                <div class="divider">
                    <div class="label reveal" style="justify-content:center"><svg viewBox="0 0 24 24"><path d="M12 2a3 3 0 0 0-3 3v1a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3z"/><path d="M19 10a7 7 0 0 1-14 0"/><line x1="12" y1="17" x2="12" y2="22"/></svg> For GPs</div>
                    <div class="big reveal" data-delay="1">Now, Your First Note</div>
                    <p class="subtitle reveal" data-delay="2" style="text-align:center;max-width:700px;margin:0 auto">Let's walk through a real consult together, from seeing your patient to sending the referral.</p>
                </div>
            </div>
        </section>
'''

SPEC_DIV = '''        <!-- Specialist path divider -->
        <section class="slide" id="s-spec" data-path="spec" data-sec="For Specialists">
            <div class="inner">
                <div class="divider">
                    <div class="label reveal" style="justify-content:center"><svg viewBox="0 0 24 24"><path d="M8 2v4a4 4 0 0 0 8 0V2"/><path d="M6 6v5a6 6 0 0 0 12 0V6"/><circle cx="19" cy="10" r="2"/></svg> For Specialists</div>
                    <div class="big reveal" data-delay="1">Now, Your First Note</div>
                    <p class="subtitle reveal" data-delay="2" style="text-align:center;max-width:700px;margin:0 auto">Let's walk through a consult together, from seeing your patient to sending the letter back to their GP.</p>
                </div>
            </div>
        </section>
'''

MEETING = '''        <!-- Meeting minutes -->
        <section class="slide" id="s-meeting" data-sec="Beyond Consults">
            <div class="inner">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg> Beyond Consults</div>
                    <h2 class="title reveal" data-delay="1">It's Not Just for Patients</h2>
                    <p class="subtitle reveal" data-delay="2">In a meeting instead? Arvi can take the minutes too, the same way it writes your notes. Just hit record.</p>
                </div>
                <div class="cards c2" style="max-width:960px;margin:clamp(1rem,2.4vh,1.8rem) auto 0">
                    <div class="card glass reveal" data-delay="3" style="display:flex;flex-direction:column"><div class="vic"><svg viewBox="0 0 24 24"><path d="M3 3h18v14H8l-5 4V3z"/></svg></div><h3>Team meetings</h3><p>Get the discussion, decisions and actions written up for you.</p></div>
                    <div class="card glass reveal" data-delay="4" style="display:flex;flex-direction:column"><div class="vic"><svg viewBox="0 0 24 24"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg></div><h3>Case conferences</h3><p>Capture the whole discussion without anyone having to take notes.</p></div>
                </div>
            </div>
        </section>
'''

MOBILE_STEPS = '''        <!-- Mobile guided install (animated) -->
        <section class="slide" id="s-mobile" data-sec="On Mobile">
            <div class="inner fill">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><rect x="5" y="2" width="14" height="20" rx="2"/><line x1="12" y1="18" x2="12.01" y2="18"/></svg> On Mobile</div>
                    <h2 class="title reveal" data-delay="1">Get Arvi on Your Phone</h2>
                    <p class="subtitle reveal" data-delay="2">Same Arvi, in your pocket. Here is how to get it set up.</p>
                </div>
                <div class="steps anim">
                    <div class="step reveal" data-delay="2"><div class="sic"><svg viewBox="0 0 24 24"><path d="M3 7V5a2 2 0 0 1 2-2h2"/><path d="M17 3h2a2 2 0 0 1 2 2v2"/><path d="M21 17v2a2 2 0 0 1-2 2h-2"/><path d="M7 21H5a2 2 0 0 1-2-2v-2"/><line x1="7" y1="12" x2="17" y2="12"/></svg></div><div class="sn">STEP 01</div><h3>Scan the code</h3><p>Point your phone camera at the QR below.</p></div>
                    <div class="step reveal" data-delay="3"><div class="sic"><svg viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg></div><div class="sn">STEP 02</div><h3>Install the app</h3><p>From the App Store or Google Play.</p></div>
                    <div class="step reveal" data-delay="4"><div class="sic"><svg viewBox="0 0 24 24"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/></svg></div><div class="sn">STEP 03</div><h3>Sign in</h3><p>Use the account you just made.</p></div>
                    <div class="step reveal" data-delay="5"><div class="sic"><svg viewBox="0 0 24 24"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/></svg></div><div class="sn">STEP 04</div><h3>You're mobile</h3><p>Now you can record on the ward or anywhere.</p></div>
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
                    <h2 class="title reveal" data-delay="1" style="text-align:center">Soon, Letters Send Themselves</h2>
                    <p class="subtitle reveal" data-delay="2" style="text-align:center;max-width:760px;margin:0 auto">We are building a link into the practice software you already use, so your letters go straight there, with no copy and paste.</p>
                </div>
                <div class="cards c3">
                    <div class="card glass reveal" data-delay="3"><div class="vic"><svg viewBox="0 0 24 24"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg></div><h3>Straight to the record</h3><p>Letters land in the software you already run.</p></div>
                    <div class="card glass reveal" data-delay="4"><div class="vic"><svg viewBox="0 0 24 24"><path d="M22 2 11 13"/><path d="M22 2 15 22l-4-9-9-4 20-7z"/></svg></div><h3>Sent securely</h3><p>Over HealthLink, which clinics already trust.</p></div>
                    <div class="card glass reveal" data-delay="5"><div class="vic"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg></div><h3>No copy and paste</h3><p>The last bit of manual work, gone.</p></div>
                </div>
            </div>
        </section>
'''

FINALE = '''        <!-- Finale + sign up -->
        <section class="slide" id="s-signup" data-sec="Get Started">
            <div class="inner">
                <div class="divider">
                    <div class="label reveal" style="justify-content:center"><svg viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg> That's It</div>
                    <div class="big reveal" data-delay="1">You're Ready to Go</div>
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
                    <p class="subtitle reveal" data-delay="3" style="text-align:center;max-width:680px;margin:clamp(.6rem,1.4vh,1rem) auto 0">That's the whole thing. Create your account and your next consult can write itself up. It's $30 a month, and your first 30 days are free.</p>
                    <a class="cta reveal" data-delay="4" href="''' + SIGNUP + '''&utm_content=end-cta" target="_blank" rel="noopener" onclick="return openApp(event,'end-cta')">Create your account <svg viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg></a>
                </div>
            </div>
        </section>
'''

# ------------------------------------------------------ the workflow ----
BODY = (
    INTRO + CHOICE + OUTLINE + SIGNUP_STEPS + SETUP_STEPS
    + vid("Set up", "Set Up Your Letter Templates",
          "Do this once and your letters will always come out looking the way you like.",
          [("sliders", "Make your own", "Set up a template for any letter you send."),
           ("edit", "Lay it out your way", "Change the format so it feels like yours.")],
          "08-custom-template.mp4", "platform.arvihealth.com &middot; Templates")
    + vid("Your patients", "Add Your Patients",
          "Bring your patient list across so everyone is ready to go. For now that is a quick file upload. Automatic sync from your practice software is coming soon.",
          [("users", "Upload your list", "Bring all your patients in at once."),
           ("eye", "See everyone", "Your whole practice in one place.")],
          "02-admin-access.mp4", "platform.arvihealth.com &middot; Admin")
    + vid("Your patients", "Your Day at a Glance",
          "When you log in, you will see today's appointments. Tap any one to get started.",
          [("calendar", "Today's list", "Everyone you are seeing, in order."),
           ("users", "Their details", "Right there when you open a patient.")],
          "10-patient-management.mp4", "platform.arvihealth.com &middot; Patients")
    # -------- GP path --------
    + GP_DIV
    + vid("For GPs", "Start Your Consult",
          "Open the patient's appointment and tap record. Not booked in? Tap Quick Create and start straight away.",
          [("zap", "Not booked in?", "Use Quick Create and you are going."),
           ("mic", "Just tap record", "Then talk to your patient as you normally would.")],
          "03-quick-record.mp4", "Arvi &middot; Quick Record", path="gp")
    + vid("For GPs", "Your Note, Written for You",
          "While you talk with your patient, Arvi writes the note. When you are done, it is there waiting for you to check.",
          [("mic", "Just talk", "Arvi turns the conversation into a tidy note."),
           ("check", "Read, don't type", "You look it over instead of writing it."),
           ("file", "Need a summary?", "Turn the same consult into a patient summary in a tap.")],
          "01-letter-generation.mp4", "platform.arvihealth.com &middot; New note", path="gp")
    + vid("For GPs", "Write Your Referral",
          "From that same consult, Arvi drafts the referral for you. Read it over and change anything, all on one screen.",
          [("file", "Already drafted", "Your referral is written and ready."),
           ("edit", "A quick read", "Look it over before it goes.")],
          "07-edit-letter.mp4", "platform.arvihealth.com &middot; Referral", path="gp")
    + vid("For GPs", "Send It",
          "Send the referral straight to the specialist from Arvi. Need it again later? Send it again in a tap.",
          [("send", "Send from here", "No need to switch over to email."),
           ("mail", "Send again anytime", "One tap if it is ever needed twice.")],
          "09-approve-resend.mp4", "platform.arvihealth.com &middot; Send", path="gp")
    # -------- Specialist path --------
    + SPEC_DIV
    + vid("For specialists", "Start Your Consult",
          "Open your referred patient and tap record. Not booked in? Tap Quick Create and start straight away.",
          [("zap", "Not booked in?", "Use Quick Create and you are going."),
           ("mic", "Just tap record", "Then talk to your patient as you normally would.")],
          "03-quick-record.mp4", "Arvi &middot; Quick Record", path="spec")
    + vid("For specialists", "Your Note, Written for You",
          "While you consult with your patient, Arvi writes the note. When you are done, it is there waiting for you to check.",
          [("mic", "Just talk", "Arvi turns the conversation into a tidy note."),
           ("check", "Read, don't type", "You look it over instead of writing it."),
           ("file", "Need a summary?", "Turn the same consult into a patient summary in a tap.")],
          "01-letter-generation.mp4", "platform.arvihealth.com &middot; New note", path="spec")
    + vid("For specialists", "Your Letter Back to the GP",
          "From the same consult, Arvi drafts your letter to the referring GP. Read it over and change anything you like.",
          [("file", "Already drafted", "Your letter is written and ready."),
           ("edit", "A quick read", "Look it over before it goes.")],
          "07-edit-letter.mp4", "platform.arvihealth.com &middot; Specialist letter", path="spec")
    + vid("For specialists", "Send It Back",
          "Send your letter to the referring GP from Arvi, and send it again anytime it is needed. A patient summary is a tap away too.",
          [("send", "Close the loop", "Send it back to whoever referred them."),
           ("mail", "Send again anytime", "One tap if it is ever needed twice.")],
          "09-approve-resend.mp4", "platform.arvihealth.com &middot; Send", path="spec")
    # -------- shared, both paths converge --------
    + vid("Everyone", "Want to Change Something?",
          "Not happy with a line? Ask Arvi to rewrite any part until it reads the way you want.",
          [("refresh", "Rewrite a bit", "Redo a section, or the whole thing."),
           ("sliders", "It's your call", "The final words are always yours.")],
          "06-regeneration.mp4", "platform.arvihealth.com &middot; Regenerate")
    + vid("Everyone", "Already Have a Recording?",
          "Got audio from earlier? Upload it and Arvi writes the note, just the same.",
          [("upload", "Upload a file", "Any recording you already have works."),
           ("file", "Same result", "You still get a clean, finished note.")],
          "05-upload-recording.mp4", "platform.arvihealth.com &middot; Upload")
    + vid("Everyone", "Seeing Patients Remotely?",
          "Run your telehealth call inside Arvi and it writes the note, just like an in-person visit.",
          [("video", "Call from Arvi", "No separate video tool to open."),
           ("mic", "Written up for you", "Same as a face-to-face visit.")],
          "13-telehealth.mp4", "platform.arvihealth.com &middot; Telehealth")
    + vid("Everyone", "Keep Track of What's Left",
          "Anything still to do after a consult stays on your list until it is done.",
          [("tasks", "Your to-do list", "See what still needs doing."),
           ("check", "Tick it off", "Mark things done as you go.")],
          "11-task-management.mp4", "platform.arvihealth.com &middot; Tasks")
    + MEETING
    + vid("Your team", "Bring Your Team On",
          "Invite the rest of your practice to join you. Your admin seat is free.",
          [("userplus", "Send an invite", "They are in as soon as they accept."),
           ("user", "Free admin seat", "Oversight at no extra cost.")],
          "18-free-admin.mp4", "platform.arvihealth.com &middot; Admin")
    + MOBILE_STEPS
    + vid("On mobile", "Even in Theatre",
          "Record your operation note on your phone, even when the signal is weak. It catches up once you are back online.",
          [("phone", "Record right there", "Write the note in the moment."),
           ("wifi", "Works offline", "It syncs when you reconnect.")],
          "04-mobile-recording.mp4", "Arvi mobile &middot; Operating theatre")
    + HEALTHLINK
    + vid("The cost", "What It Costs",
          "It is $30 a month, and that includes 10 hours. Need more? Add 10-hour packs anytime. You start with 30 days free.",
          [("card", "$30 a month", "Ten hours included to get going."),
           ("check", "Top up as you go", "Add more only when you need it.")],
          "19-subscription.mp4", "platform.arvihealth.com &middot; Pricing")
    + FINALE
)

# ---- path-aware deck engine: IntersectionObserver activation + path filtering ----
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
  function refreshDot(){
    var idx=Math.round(deck.scrollLeft/deck.clientWidth);
    var dots=[].slice.call(dotsWrap.children);
    dots.forEach(function(d,k){ d.classList.toggle('active',k===idx); });
  }
  function applyPath(){
    all.forEach(function(s){ s.style.display=ok(s)?'':'none'; });
    buildDots(); totalEl.textContent=vis().length; refreshDot(); syncVideos();
  }
  window.arviSetPath=function(p){
    path=p; document.body.setAttribute('data-chosen',p); applyPath();
    if(window.arviFit) setTimeout(window.arviFit,120);
    // advance to the next slide (the onboarding steps begin), not the tailored section
    var choice=document.getElementById('s-path');
    var v=vis(); var ci=v.indexOf(choice); var next=v[ci+1];
    if(next){ setTimeout(function(){ next.scrollIntoView({behavior:'smooth',inline:'start'}); },90); }
  };

  // scroll-position based activation (robust; no IntersectionObserver needed)
  function tick(){
    var v=vis();
    var cw=deck.clientWidth||window.innerWidth||1;
    var idx=Math.round(deck.scrollLeft/cw);
    if(!(idx>=0))idx=0; if(idx>v.length-1)idx=v.length-1;
    var dots=[].slice.call(dotsWrap.children);
    dots.forEach(function(d,k){ d.classList.toggle('active',k===idx); });
    v.forEach(function(s,k){
      var vids=s.querySelectorAll('video');
      if(k===idx){
        s.classList.add('active');
        [].forEach.call(vids,function(vd){ if(vd.paused){ var p=vd.play(); if(p)p.catch(function(){}); } });
      } else {
        [].forEach.call(vids,function(vd){ if(!vd.paused){ try{vd.pause();}catch(_){} } });
      }
    });
    if(cur)cur.textContent=idx+1;
    if(secEl&&v[idx])secEl.textContent=v[idx].getAttribute('data-sec')||'';
    var max=deck.scrollWidth-deck.clientWidth;
    prog.style.setProperty('--p', max>0?(deck.scrollLeft/max).toFixed(4):'0');
  }
  function syncVideos(){ tick(); }

  // IntersectionObserver activation (matches the proven decks; fires on scroll in real browsers)
  try{
    var io=new IntersectionObserver(function(es){
      var hit=false;
      es.forEach(function(e){ if(e.isIntersecting&&e.intersectionRatio>=0.55){ e.target.classList.add('active'); hit=true; } });
      if(hit) tick();
    },{root:deck,threshold:[0,0.55,1]});
    all.forEach(function(s){ io.observe(s); });
  }catch(_){}

  var raf;
  deck.addEventListener('scroll',function(){ if(!raf){ raf=requestAnimationFrame(function(){ tick(); raf=null; }); } });
  addEventListener('resize',function(){ tick(); });
  addEventListener('keydown',function(ev){
    var v=vis(); var i=Math.round(deck.scrollLeft/(deck.clientWidth||1));
    if(ev.key==='ArrowRight'||ev.key==='PageDown'||ev.key===' '){ev.preventDefault(); if(i<v.length-1)v[i+1].scrollIntoView({behavior:'smooth',inline:'start'});}
    else if(ev.key==='ArrowLeft'||ev.key==='PageUp'){ev.preventDefault(); if(i>0)v[i-1].scrollIntoView({behavior:'smooth',inline:'start'});}
    else if(ev.key==='Home'){ev.preventDefault(); v[0].scrollIntoView({behavior:'smooth',inline:'start'});}
    else if(ev.key==='End'){ev.preventDefault(); v[v.length-1].scrollIntoView({behavior:'smooth',inline:'start'});}
  });

  document.body.setAttribute('data-chosen',path);
  applyPath();
  // run after layout is ready so clientWidth is correct
  requestAnimationFrame(function(){ requestAnimationFrame(function(){ tick(); }); });
  window.addEventListener('load',tick);
  setTimeout(tick,250);
})();
"""

HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="robots" content="noindex, nofollow, noarchive">
    <title>Arvi Health &middot; Getting Started</title>
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
        <div class="nav-tag">Arvi &middot; <b>Getting Started</b></div>
    </nav>

    <main class="deck" id="deck">
''' + BODY + '''    </main>

    <div class="counter"><span><b id="cur">1</b> / <span id="total">0</span></span><span class="sec" id="sec">Overview</span></div>

    <aside class="apppanel" id="apppanel" aria-label="Arvi sign-up">
        <div class="apppanel-head"><span class="t"><span class="dotlive"></span> Arvi &middot; Sign up</span><button class="apppanel-close" onclick="closeApp()" aria-label="Close">&times;</button></div>
        <iframe id="appframe" title="Sign up for Arvi" src="about:blank"></iframe>
        <div class="apppanel-foot">Keep moving through the guide on the left. <a href="''' + SIGNUP + '''&utm_content=panel-fallback" target="_blank" rel="noopener">Or open in a new tab</a></div>
    </aside>

    <div class="vlight" id="vlight" aria-hidden="true">
        <div class="vlight-bd" onclick="closeVideo()"></div>
        <button class="vlight-x" onclick="closeVideo()" aria-label="Close video">&times;</button>
        <video id="vlvideo" loop muted playsinline></video>
    </div>

    <script>''' + ENGINE + '''</script>
    <script>
    (function(){
        var BASE=''' + repr(SIGNUP) + ''';
        function visible(){ return [].slice.call(document.querySelectorAll('.slide')).filter(function(s){return getComputedStyle(s).display!=='none';}); }
        function current(){
            var deck=document.getElementById('deck'); var v=visible();
            var idx=Math.round(deck.scrollLeft/(deck.clientWidth||1));
            if(idx<0)idx=0; if(idx>v.length-1)idx=v.length-1;
            return v[idx];
        }
        function realign(el){ if(el) requestAnimationFrame(function(){ el.scrollIntoView({inline:'start'}); }); }
        // Scale each slide's content to fit the narrowed deck, so nothing is cut.
        // Measures the content, shrinks only if it overflows, with a readable floor.
        function fitSlides(){
            var split=document.body.classList.contains('split');
            [].slice.call(document.querySelectorAll('.slide')).forEach(function(s){
                var inner=s.querySelector('.inner'); if(!inner) return;
                inner.style.zoom='';
                if(!split || getComputedStyle(s).display==='none') return;
                var cs=getComputedStyle(s);
                var availW=s.clientWidth-(parseFloat(cs.paddingLeft)||0)-(parseFloat(cs.paddingRight)||0);
                var availH=s.clientHeight-(parseFloat(cs.paddingTop)||0)-(parseFloat(cs.paddingBottom)||0);
                var cw=inner.scrollWidth, ch=inner.scrollHeight;
                if(!cw||!ch||!availW||!availH) return;
                var z=Math.min(1, availW/cw, availH/ch);
                if(z<0.68) z=0.68;            // readability floor; overflow then scrolls
                if(z<0.995) inner.style.zoom=z.toFixed(3);
            });
        }
        window.arviFit=fitSlides;
        window.openApp=function(ev,src){
            if(ev&&ev.preventDefault)ev.preventDefault();
            var f=document.getElementById('appframe');
            if(f.getAttribute('data-loaded')!=='1'){ f.src=BASE+(src?('&utm_content='+src):''); f.setAttribute('data-loaded','1'); }
            var el=current();
            document.body.classList.add('split');
            void document.getElementById('deck').offsetWidth;   // flush the reflow first
            realign(el); fitSlides();
            setTimeout(fitSlides,180);                           // catch late reflow / scrollbar
            return false;
        };
        window.closeApp=function(){
            var el=current();
            document.body.classList.remove('split');
            void document.getElementById('deck').offsetWidth;
            realign(el); fitSlides();
            setTimeout(fitSlides,180);
        };
        // click any slide video to enlarge it (stays clear of the side panel)
        window.openVideo=function(src){
            if(!src) return;
            var v=document.getElementById('vlvideo');
            if(v.getAttribute('src')!==src){ v.setAttribute('src',src); }
            document.getElementById('vlight').classList.add('on');
            try{ var p=v.play(); if(p)p.catch(function(){}); }catch(e){}
        };
        window.closeVideo=function(){
            document.getElementById('vlight').classList.remove('on');
            try{ document.getElementById('vlvideo').pause(); }catch(e){}
        };
        [].slice.call(document.querySelectorAll('.clip-frame video')).forEach(function(v){
            v.addEventListener('click',function(){ openVideo(v.currentSrc||v.getAttribute('src')); });
        });

        document.addEventListener('keydown',function(e){
            if(e.key!=='Escape') return;
            if(document.getElementById('vlight').classList.contains('on')) closeVideo();
            else closeApp();
        });
        // realign and refit if the window (or panel) changes the space available
        var rt;
        addEventListener('resize',function(){ realign(current()); clearTimeout(rt); rt=setTimeout(fitSlides,120); });
    })();
    </script>
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
