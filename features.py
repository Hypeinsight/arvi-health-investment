# -*- coding: utf-8 -*-
# Standalone feature-walkthrough deck: just the feature clips (the glossary),
# with a sign-up call to action on every slide and a closing sign-up slide, all
# linking to the Arvi platform with UTM tags. Reuses gen.py CSS + JS engine and
# feat_slide. No em dashes; AU English spelling.
import io
import gen

SIGNUP = "https://platform.arvihealth.com/signup?utm_source=feature-deck&utm_medium=deck&utm_campaign=signup"

EXTRA_CSS = '''
        .signup-fab{position:fixed;left:clamp(12px,2vw,26px);bottom:clamp(12px,2.2vh,22px);z-index:70;display:inline-flex;align-items:center;gap:.5rem;padding:.6rem 1.15rem;border-radius:40px;background:linear-gradient(135deg,var(--primary),var(--accent));color:#fff;font-weight:700;font-size:clamp(.74rem,1vw,.88rem);text-decoration:none;box-shadow:0 12px 28px -6px rgba(105,26,106,.55);transition:transform .3s cubic-bezier(.22,1,.36,1),box-shadow .3s}
        .signup-fab:hover{transform:translateY(-2px);box-shadow:0 18px 36px -8px rgba(105,26,106,.6)}
        .signup-fab svg{width:15px;height:15px;stroke:#fff;stroke-width:2.4;fill:none}
'''

# Feature list: reuse gen's list but drop the two "Billing" mechanics slides
# (Stripe web + iOS in-app) and replace them with a single price slide.
PRICING = ("Pricing", "Simple, Transparent Pricing",
    "From $30 a month with 10 hours of documentation included, and 10-hour top-up packs when a clinician needs more. Start with a 30 day free trial.",
    [("card", "From $30 / month", "Ten hours of transcription included in the base plan."),
     ("check", "Pay as you grow", "Add 10-hour packs only when they are needed, no lock-in.")],
    "19-subscription.mp4", "platform.arvihealth.com &middot; Pricing")

FEATURES = list(gen.FEATURES[:17]) + [PRICING]

feat_html = []
for i, (section, title, subtitle, points, clip, url) in enumerate(FEATURES):
    sid = "f%d" % (i + 1)
    feat_html.append(gen.feat_slide(i + 1, sid, section, title, subtitle, points, clip, url, reverse=(i % 2 == 1)))
FEAT = "\n".join(feat_html)

INTRO = '''        <!-- Intro divider -->
        <section class="slide" id="s-intro" data-sec="Feature Walkthrough">
            <div class="inner">
                <div class="divider">
                    <div class="label reveal" style="justify-content:center"><svg viewBox="0 0 24 24"><polygon points="5 3 19 12 5 21 5 3"/></svg> Feature Walkthrough</div>
                    <div class="big reveal" data-delay="1">Everything Arvi Does</div>
                    <p class="subtitle reveal" data-delay="2" style="text-align:center;max-width:760px;margin:0 auto">A short clip of each production feature, across documentation, letters, patient workflow, organisation and pricing. Live today on web and mobile.</p>
                    <div class="menu reveal" data-delay="3">
                        <span class="mi"><b>01</b> Core Documentation</span>
                        <span class="mi"><b>02</b> Letters &amp; Templates</span>
                        <span class="mi"><b>03</b> Patient &amp; Workflow</span>
                        <span class="mi"><b>04</b> Organisation &amp; Users</span>
                        <span class="mi"><b>05</b> Pricing</span>
                    </div>
                    <a class="cta reveal" data-delay="4" href="''' + SIGNUP + '''&utm_content=intro-cta" target="_blank" rel="noopener">Sign up free <svg viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg></a>
                </div>
            </div>
        </section>
'''

CTA = '''        <!-- Sign-up close -->
        <section class="slide" id="s-signup" data-sec="Get Started">
            <div class="inner">
                <div class="divider">
                    <div class="label reveal" style="justify-content:center"><svg viewBox="0 0 24 24"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><line x1="19" y1="8" x2="19" y2="14"/><line x1="22" y1="11" x2="16" y2="11"/></svg> Get Started</div>
                    <div class="big reveal" data-delay="1">Start Using Arvi Today</div>
                    <p class="subtitle reveal" data-delay="2" style="text-align:center;max-width:720px;margin:0 auto">Create your account and turn your next consultation into a finished note and letter. Set up in minutes, on web and mobile. From $30 a month, with a 30 day free trial.</p>
                    <a class="cta reveal" data-delay="3" href="''' + SIGNUP + '''&utm_content=end-cta" target="_blank" rel="noopener">Sign up on the Arvi platform <svg viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg></a>
                    <div class="tags reveal" data-delay="4" style="justify-content:center"><span class="tag">Web &amp; mobile</span><span class="tag">20 production features</span><span class="tag">30 day free trial</span></div>
                </div>
            </div>
        </section>
'''

BODY = INTRO + FEAT + CTA

HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="robots" content="noindex, nofollow, noarchive">
    <title>Arvi Health &middot; Feature Walkthrough</title>
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
        <div class="nav-tag">Arvi &middot; <b>Feature Walkthrough</b></div>
    </nav>

    <main class="deck" id="deck">
''' + BODY + '''    </main>

    <div class="counter"><span><b id="cur">1</b> / <span id="total">0</span></span><span class="sec" id="sec">Overview</span></div>
    <a class="signup-fab" href="''' + SIGNUP + '''&utm_content=footer" target="_blank" rel="noopener"><svg viewBox="0 0 24 24"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><line x1="19" y1="8" x2="19" y2="14"/><line x1="22" y1="11" x2="16" y2="11"/></svg> Sign up free</a>

    <script>''' + gen.SCRIPT + '''</script>
</body>
</html>
'''

OUT = 'arvi-features-walkthrough.html'

if __name__ == "__main__":
    with io.open(OUT, 'w', encoding='utf-8') as f:
        f.write(HTML)
    print("slides:", HTML.count('<section class="slide"'))
    print("videos:", HTML.count('<video'))
    print("signup links:", HTML.count('platform.arvihealth.com/signup'))
    print("WROTE", OUT)
