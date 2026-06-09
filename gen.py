# -*- coding: utf-8 -*-
import io

CSS = r"""
        :root{
            --primary-dark:#043762; --primary:#0455A3; --accent:#691A6A; --accent-2:#8a2b8b;
            --bg:#f4f9fe; --ink:#0c2740; --muted:#5b7189; --line:rgba(4,55,98,.10);
            --glass:rgba(255,255,255,.72); --glass-border:rgba(255,255,255,.65);
            --s-sm:0 4px 16px rgba(4,55,98,.06);
            --s-md:0 16px 44px -12px rgba(4,55,98,.20);
            --s-lg:0 34px 90px -28px rgba(4,55,98,.55), 0 10px 28px rgba(4,55,98,.14);
            --r-lg:clamp(16px,1.4vw,26px); --r-md:clamp(12px,1vw,18px); --r-sm:10px;
        }
        *{margin:0;padding:0;box-sizing:border-box}
        html,body{height:100%;overflow:hidden}
        body{font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;background:var(--bg);color:var(--ink);-webkit-font-smoothing:antialiased}

        /* layered modern background: soft mesh + faint grid */
        body::before{content:"";position:fixed;inset:0;z-index:0;pointer-events:none;
            background:
              radial-gradient(1100px 780px at 8% -12%, rgba(4,85,163,.12), transparent 58%),
              radial-gradient(960px 720px at 104% 112%, rgba(105,26,106,.12), transparent 54%),
              radial-gradient(700px 600px at 88% 4%, rgba(200,232,255,.5), transparent 60%);}
        body::after{content:"";position:fixed;inset:0;z-index:0;pointer-events:none;opacity:.5;
            background-image:linear-gradient(rgba(4,55,98,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(4,55,98,.035) 1px,transparent 1px);
            background-size:46px 46px;
            -webkit-mask:radial-gradient(circle at 50% 35%, #000, transparent 78%);
            mask:radial-gradient(circle at 50% 35%, #000, transparent 78%);}

        /* progress + nav */
        .progress{position:fixed;top:0;left:0;height:3px;width:100%;z-index:1100;background:transparent}
        .progress span{display:block;height:100%;width:calc(var(--p,0)*100%);background:linear-gradient(90deg,var(--primary),var(--accent));transition:width .2s ease}
        .nav{position:fixed;top:0;left:0;right:0;z-index:1000;display:flex;align-items:center;justify-content:space-between;
            padding:clamp(.7rem,1.5vh,1.05rem) clamp(1.1rem,4vw,3rem);
            background:rgba(244,249,254,.7);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border-bottom:1px solid var(--line)}
        .logo img{height:clamp(28px,4vh,40px);width:auto;display:block}
        .nav-tag{font-size:clamp(.6rem,1vw,.76rem);font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
        .nav-tag b{color:var(--primary)}
        .dots{display:flex;gap:5px;align-items:center}
        .dot{width:7px;height:7px;border-radius:50%;background:rgba(4,55,98,.22);cursor:pointer;border:none;padding:0;transition:all .35s cubic-bezier(.4,0,.2,1)}
        .dot:hover{background:rgba(4,85,163,.55);transform:scale(1.3)}
        .dot.active{background:linear-gradient(135deg,var(--primary),var(--accent));width:24px;border-radius:5px}

        /* deck */
        .deck{display:flex;height:100vh;height:100dvh;overflow-x:auto;overflow-y:hidden;scroll-snap-type:x mandatory;scroll-behavior:smooth;-webkit-overflow-scrolling:touch}
        .deck::-webkit-scrollbar{height:0}
        .slide{position:relative;z-index:1;flex:0 0 100vw;width:100vw;height:100vh;height:100dvh;scroll-snap-align:start;
            display:flex;flex-direction:column;justify-content:center;
            padding:clamp(4.4rem,9vh,6.4rem) clamp(1.25rem,5vw,4.6rem) clamp(2rem,5vh,3.4rem);overflow:hidden}
        .inner{width:100%;max-width:1660px;margin:0 auto}
        .inner.fill{display:flex;flex-direction:column;justify-content:center;height:100%;min-height:0}

        /* type */
        .kicker{display:inline-flex;align-items:center;gap:.65rem;margin-bottom:clamp(.7rem,1.6vh,1.1rem)}
        .kicker .n{font-variant-numeric:tabular-nums;font-weight:800;font-size:.78rem;letter-spacing:.03em;color:#fff;background:linear-gradient(135deg,var(--primary),var(--accent));padding:.32rem .58rem;border-radius:9px;box-shadow:0 6px 16px rgba(4,85,163,.28)}
        .kicker .s{font-size:.72rem;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:var(--muted)}
        .label{display:inline-flex;align-items:center;gap:.5rem;font-size:clamp(.66rem,1vw,.8rem);font-weight:700;text-transform:uppercase;letter-spacing:.16em;color:var(--accent);margin-bottom:clamp(.6rem,1.4vh,1rem)}
        .label svg{width:1em;height:1em;stroke:currentColor;stroke-width:2;fill:none}
        .label.imx{color:var(--primary)}
        .title{font-size:clamp(1.7rem,3.7vw,3.5rem);font-weight:800;line-height:1.06;letter-spacing:-.022em;
            background:linear-gradient(118deg,var(--primary-dark) 0%,var(--primary) 50%,var(--accent) 100%);
            -webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
        .subtitle{font-size:clamp(.95rem,1.35vw,1.28rem);color:var(--muted);line-height:1.55;margin-top:clamp(.6rem,1.4vh,1rem);max-width:60ch}
        .slide-head{margin-bottom:clamp(1rem,2.4vh,1.8rem)}
        .slide-head .subtitle{max-width:82ch}

        .glass{background:var(--glass);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border:1px solid var(--glass-border);border-radius:var(--r-lg);box-shadow:var(--s-sm)}

        /* feature layout */
        .feature{display:grid;grid-template-columns:minmax(0,.82fr) minmax(0,1.68fr);gap:clamp(1.5rem,4vw,4.2rem);align-items:center}
        .feature.reverse{grid-template-columns:minmax(0,1.68fr) minmax(0,.82fr)}
        .feature.reverse .feature-copy{order:2}
        .feature.reverse .clip{order:1}
        .points{list-style:none;display:flex;flex-direction:column;gap:clamp(.7rem,1.6vh,1.1rem);margin-top:clamp(1rem,2.4vh,1.7rem)}
        .points li{display:flex;gap:.85rem;align-items:flex-start}
        .ic{width:clamp(34px,2.5vw,40px);height:clamp(34px,2.5vw,40px);border-radius:var(--r-sm);flex-shrink:0;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,var(--primary),var(--primary-dark));box-shadow:0 7px 18px rgba(4,85,163,.26)}
        .ic svg{width:52%;height:52%;stroke:#fff;stroke-width:2;fill:none}
        .points h4{font-size:clamp(.95rem,1.2vw,1.12rem);color:var(--primary-dark);font-weight:700}
        .points p{font-size:clamp(.82rem,1vw,.97rem);color:var(--muted);line-height:1.45;margin-top:.1rem}
        .tags{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:clamp(1rem,2.2vh,1.5rem)}
        .tag{display:inline-flex;align-items:center;gap:.4rem;padding:.45rem .95rem;border-radius:30px;font-size:clamp(.72rem,.95vw,.85rem);font-weight:600;color:var(--primary-dark);background:linear-gradient(135deg,rgba(4,55,98,.07),rgba(105,26,106,.08))}

        /* video frame - premium */
        .clip{position:relative;min-width:0;display:flex;flex-direction:column;align-items:center}
        .clip-glow{position:absolute;inset:-9% -9% -16%;z-index:-1;background:radial-gradient(58% 58% at 50% 42%,rgba(105,26,106,.22),transparent 70%);filter:blur(14px);animation:glow 5s ease-in-out infinite}
        @keyframes glow{0%,100%{opacity:.5;transform:scale(1)}50%{opacity:1;transform:scale(1.05)}}
        .clip-frame{position:relative;width:100%;border-radius:var(--r-lg);overflow:hidden;background:#06182c;border:1px solid rgba(255,255,255,.12);box-shadow:var(--s-lg)}
        .chrome{display:flex;align-items:center;gap:.45rem;padding:.55rem .9rem;background:linear-gradient(135deg,#0a2744,#06457f)}
        .chrome i{width:10px;height:10px;border-radius:50%;background:rgba(255,255,255,.32)}
        .chrome .url{margin-left:.7rem;font-size:clamp(.62rem,.85vw,.74rem);color:rgba(255,255,255,.8);background:rgba(255,255,255,.13);padding:.22rem .85rem;border-radius:20px;max-width:72%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
        .clip-frame video{width:100%;height:auto;max-height:75dvh;display:block;background:#000;object-fit:contain}
        .clip-frame img{width:100%;height:auto;max-height:60dvh;display:block;background:#06182c;object-fit:contain}
        figcaption{font-size:clamp(.74rem,.95vw,.88rem);color:var(--muted);margin-top:.85rem;text-align:center}
        figcaption b{color:var(--primary-dark)}

        /* platform pillars */
        .apps{display:flex;gap:.8rem;flex-wrap:wrap;margin-top:clamp(.8rem,1.8vh,1.2rem)}
        .app{display:flex;align-items:center;gap:.7rem;padding:.7rem 1.1rem;border-radius:var(--r-md)}
        .app svg{width:24px;height:24px;stroke:var(--primary);stroke-width:1.8;fill:none;flex-shrink:0}
        .app strong{color:var(--primary-dark);font-size:.92rem;display:block}
        .app span{font-size:.76rem;color:var(--muted)}
        .pillars{display:grid;grid-template-columns:repeat(5,1fr);gap:clamp(.7rem,1.4vw,1.2rem);align-items:stretch;margin-top:clamp(.8rem,2vh,1.5rem)}
        .pillar{padding:clamp(1rem,1.6vw,1.5rem);display:flex;flex-direction:column;transition:transform .3s cubic-bezier(.22,1,.36,1),box-shadow .3s}
        .pillar:hover{transform:translateY(-4px);box-shadow:var(--s-md)}
        .pillar .num{font-size:clamp(.66rem,.9vw,.78rem);font-weight:800;color:var(--accent);letter-spacing:.12em}
        .pillar h3{font-size:clamp(.95rem,1.2vw,1.12rem);color:var(--primary-dark);margin:.4rem 0 .7rem;line-height:1.2}
        .pillar ul{list-style:none;display:flex;flex-direction:column;gap:.42rem}
        .pillar li{font-size:clamp(.78rem,.95vw,.92rem);color:#475569;display:flex;gap:.45rem;align-items:flex-start;line-height:1.3}
        .pillar li::before{content:"";width:6px;height:6px;border-radius:50%;background:linear-gradient(135deg,var(--primary),var(--accent));margin-top:.42rem;flex-shrink:0}

        /* infomedix */
        .imx-bar{display:flex;flex-wrap:wrap;gap:clamp(1.2rem,3vw,3rem);padding:clamp(1rem,2vh,1.5rem) clamp(1.3rem,2.5vw,2.2rem);margin:clamp(.8rem,2vh,1.3rem) 0}
        .imx-stat .v{font-size:clamp(1.5rem,2.7vw,2.3rem);font-weight:800;line-height:1;background:linear-gradient(118deg,var(--primary),var(--accent));-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
        .imx-stat .l{font-size:clamp(.72rem,.92vw,.85rem);color:var(--muted);margin-top:.35rem}
        .cards{display:grid;gap:clamp(.8rem,1.6vw,1.4rem)}
        .cards.c3{grid-template-columns:repeat(3,1fr)}
        .card{padding:clamp(1.1rem,1.8vw,1.7rem);transition:transform .3s cubic-bezier(.22,1,.36,1),box-shadow .3s}
        .card:hover{transform:translateY(-4px);box-shadow:var(--s-md)}
        .card .vic{width:clamp(40px,3vw,50px);height:clamp(40px,3vw,50px);border-radius:var(--r-md);display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,var(--primary),var(--accent));margin-bottom:clamp(.6rem,1.2vh,1rem)}
        .card .vic svg{width:50%;height:50%;stroke:#fff;stroke-width:2;fill:none}
        .card h3{font-size:clamp(.98rem,1.2vw,1.15rem);color:var(--primary-dark);margin-bottom:.4rem}
        .card p{font-size:clamp(.82rem,1vw,.96rem);color:var(--muted);line-height:1.5}

        .integ{display:grid;grid-template-columns:.95fr auto 1.3fr;gap:clamp(1rem,2.5vw,2rem);align-items:center;margin-top:clamp(1rem,2.4vh,2rem)}
        .integ-arvi{padding:clamp(1.2rem,2vw,1.9rem);border-radius:var(--r-lg);background:linear-gradient(150deg,var(--primary-dark),var(--primary));color:#fff;box-shadow:var(--s-md)}
        .integ-arvi .il{font-size:.7rem;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.72)}
        .integ-arvi h3{color:#fff;font-size:clamp(1.3rem,2.2vw,1.8rem);margin:.3rem 0 .5rem}
        .integ-arvi>p{font-size:clamp(.82rem,1vw,.95rem);color:rgba(255,255,255,.82);line-height:1.45}
        .integ-arvi ul{list-style:none;margin-top:1.1rem;display:flex;flex-direction:column;gap:.55rem}
        .integ-arvi li{font-size:clamp(.82rem,1vw,.95rem);color:#fff;display:flex;gap:.5rem;align-items:center}
        .integ-arvi li svg{width:16px;height:16px;stroke:#c8e8ff;stroke-width:2.4;fill:none;flex-shrink:0}
        .pipe{display:flex;flex-direction:column;align-items:center;gap:.55rem}
        .pipe .pl{font-size:clamp(.62rem,.85vw,.72rem);font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);text-align:center;line-height:1.3}
        .pipe .pl.sub{color:#94a3b8}
        .pipe svg{width:clamp(38px,4vw,54px);height:clamp(38px,4vw,54px);stroke:var(--accent);stroke-width:1.4;fill:none}
        .imx-prods{display:grid;grid-template-columns:1fr 1fr;gap:clamp(.6rem,1.2vw,.9rem)}
        .imx-prod{padding:clamp(.8rem,1.2vw,1.05rem);border-radius:var(--r-md);transition:transform .3s,box-shadow .3s}
        .imx-prod:hover{transform:translateY(-3px);box-shadow:var(--s-md)}
        .imx-prod h4{font-size:clamp(.84rem,1vw,.95rem);color:var(--primary-dark);margin-bottom:.2rem}
        .imx-prod p{font-size:clamp(.72rem,.9vw,.82rem);color:var(--muted);line-height:1.35}
        .imx-prod.span{grid-column:span 2}

        /* intro + close */
        .intro{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.3fr);gap:clamp(1.5rem,4vw,4.2rem);align-items:center}
        .intro h1{font-size:clamp(2rem,4.6vw,4.1rem);font-weight:800;line-height:1.04;letter-spacing:-.022em;color:var(--primary-dark)}
        .intro h1 span{background:linear-gradient(118deg,var(--primary),var(--accent));-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
        .intro p{font-size:clamp(1rem,1.4vw,1.3rem);color:var(--muted);line-height:1.6;margin-top:clamp(.8rem,1.8vh,1.2rem)}
        .badge{display:inline-flex;align-items:center;gap:.55rem;padding:.5rem 1.1rem;border-radius:50px;font-size:clamp(.72rem,1vw,.85rem);font-weight:700;color:var(--primary-dark);background:linear-gradient(135deg,rgba(4,55,98,.08),rgba(105,26,106,.08));margin-bottom:clamp(.8rem,1.8vh,1.2rem)}
        .pulse{width:9px;height:9px;border-radius:50%;background:var(--accent);box-shadow:0 0 0 0 rgba(105,26,106,.5);animation:pulse 2s infinite}
        @keyframes pulse{0%{box-shadow:0 0 0 0 rgba(105,26,106,.5)}70%{box-shadow:0 0 0 10px rgba(105,26,106,0)}100%{box-shadow:0 0 0 0 rgba(105,26,106,0)}}
        .intro .clip-frame video{max-height:78dvh;object-fit:cover}
        .close{display:flex;flex-direction:column;align-items:center;text-align:center;gap:clamp(1rem,2.4vh,1.6rem)}
        .close img{height:clamp(46px,6vh,70px)}
        .close .title,.close .subtitle{text-align:center}
        .close .subtitle{margin-left:auto;margin-right:auto}
        .cta{display:inline-flex;align-items:center;gap:.55rem;margin-top:.4rem;padding:.9rem 2rem;border-radius:50px;font-weight:700;text-decoration:none;color:#fff;background:linear-gradient(135deg,var(--accent),var(--accent-2));box-shadow:0 12px 34px rgba(105,26,106,.32);transition:transform .25s,box-shadow .25s}
        .cta:hover{transform:translateY(-3px);box-shadow:0 18px 46px rgba(105,26,106,.44)}
        .cta svg{width:18px;height:18px;stroke:#fff;stroke-width:2;fill:none}

        /* InfoMedix brand marks (white-bg logo blended via multiply) */
        .imx-logo{mix-blend-mode:multiply;width:auto;display:block}
        .imx-bar .imx-logo{height:clamp(28px,4vh,44px);align-self:center;padding-right:clamp(.7rem,1.6vw,1.3rem);border-right:1px solid var(--line)}
        .imx-side{display:flex;flex-direction:column;gap:clamp(.6rem,1.4vh,1rem);min-width:0}
        .imx-side-head{display:flex;align-items:center;gap:.6rem}
        .imx-side-head .imx-logo{height:clamp(20px,2.6vh,30px)}
        .imx-side-head span{font-size:clamp(.72rem,.9vw,.84rem);color:var(--muted);font-weight:600}
        .lockup{display:flex;align-items:center;justify-content:center;gap:clamp(1.1rem,3vw,2.4rem);flex-wrap:wrap}
        .lockup img{width:auto}
        .lockup .lk-arvi{height:clamp(40px,6vh,62px)}
        .lockup .lk-imx{height:clamp(30px,4.6vh,48px);mix-blend-mode:multiply}
        .lockup .x{font-size:clamp(1.3rem,2.6vw,1.9rem);color:#94a3b8;font-weight:300}

        /* --- added: agenda --- */
        .cards.c2{grid-template-columns:repeat(2,1fr)}
        .agenda{display:flex;flex-direction:column;gap:clamp(.6rem,1.4vh,1rem);margin-top:clamp(1rem,2.4vh,1.8rem);max-width:1000px}
        .agenda-item{display:flex;align-items:center;gap:1rem;padding:clamp(.8rem,1.4vw,1.2rem) clamp(1rem,1.6vw,1.5rem)}
        .agenda-item .an{font-variant-numeric:tabular-nums;font-weight:800;font-size:clamp(1rem,1.6vw,1.4rem);color:#fff;background:linear-gradient(135deg,var(--primary),var(--accent));width:clamp(36px,3vw,46px);height:clamp(36px,3vw,46px);border-radius:12px;display:flex;align-items:center;justify-content:center;flex-shrink:0}
        .agenda-item h3{font-size:clamp(1rem,1.4vw,1.3rem);color:var(--primary-dark);font-weight:700}
        .agenda-item p{font-size:clamp(.8rem,1vw,.95rem);color:var(--muted);margin-top:.1rem}
        .agenda-item .ad{margin-left:auto;font-size:clamp(.7rem,.9vw,.82rem);color:#94a3b8;font-weight:600;white-space:nowrap}
        /* --- how it works --- */
        .steps{display:grid;grid-template-columns:repeat(4,1fr);gap:clamp(.7rem,1.5vw,1.2rem);margin-top:clamp(1.2rem,3vh,2.2rem)}
        .step{padding:clamp(1.1rem,1.8vw,1.7rem);display:flex;flex-direction:column;gap:.6rem}
        .step .sic{width:clamp(42px,3.2vw,52px);height:clamp(42px,3.2vw,52px);border-radius:14px;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,var(--primary),var(--primary-dark));box-shadow:0 7px 18px rgba(4,85,163,.25)}
        .step .sic svg{width:50%;height:50%;stroke:#fff;stroke-width:2;fill:none}
        .step .sn{font-size:.7rem;font-weight:800;color:var(--accent);letter-spacing:.12em}
        .step h3{font-size:clamp(.95rem,1.2vw,1.15rem);color:var(--primary-dark)}
        .step p{font-size:clamp(.8rem,1vw,.95rem);color:var(--muted);line-height:1.45}
        /* --- demo divider --- */
        .divider{display:flex;flex-direction:column;align-items:center;text-align:center;gap:clamp(1rem,2.4vh,1.6rem)}
        .divider .big{font-size:clamp(2.2rem,5.2vw,4.4rem);font-weight:800;letter-spacing:-.022em;line-height:1.04;background:linear-gradient(118deg,var(--primary-dark),var(--primary) 55%,var(--accent));-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
        .menu{display:flex;flex-wrap:wrap;gap:.7rem;justify-content:center;max-width:920px}
        .menu .mi{display:inline-flex;align-items:center;gap:.5rem;padding:.6rem 1.2rem;border-radius:40px;font-weight:600;font-size:clamp(.8rem,1vw,.95rem);color:var(--primary-dark);background:var(--glass);border:1px solid var(--glass-border)}
        .menu .mi b{color:var(--accent)}
        /* --- comparison table --- */
        .cmp{margin-top:clamp(1rem,2.4vh,1.6rem);border-radius:var(--r-lg);overflow:hidden;border:1px solid var(--glass-border)}
        .cmp-row{display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr 1.1fr;font-size:clamp(.7rem,.92vw,.88rem)}
        .cmp-row>div{padding:clamp(.55rem,1vw,.85rem) clamp(.5rem,1vw,1rem);display:flex;align-items:center;justify-content:center;text-align:center;border-top:1px solid rgba(4,55,98,.07)}
        .cmp-row>div:first-child{justify-content:flex-start;text-align:left;font-weight:600;color:var(--primary-dark)}
        .cmp-head{background:var(--primary-dark);color:#fff;font-weight:700}
        .cmp-head>div{border-top:none}
        .cmp-head .arvi{background:linear-gradient(135deg,var(--accent),var(--accent-2));position:relative}
        .cmp .arvi{background:rgba(200,232,255,.34);font-weight:700;color:var(--primary-dark)}
        .cmp .tick svg{width:18px;height:18px;stroke:#22c55e;stroke-width:2.5;fill:none}
        .cmp-best{position:absolute;top:3px;right:5px;background:#ff3b30;color:#fff;font-size:.5rem;padding:1px 5px;border-radius:7px}
        /* --- market funnel --- */
        .funnel{display:flex;flex-direction:column;gap:clamp(.7rem,1.4vh,1.1rem)}
        .fbar{display:flex;justify-content:space-between;align-items:center;gap:1rem;padding:clamp(.8rem,1.4vw,1.2rem) clamp(1rem,1.6vw,1.5rem);border-radius:14px}
        .fbar .fl{font-size:.7rem;font-weight:800;letter-spacing:.1em;color:var(--accent)}
        .fbar .fd{font-size:clamp(.76rem,.95vw,.9rem);color:var(--muted);margin-top:.15rem}
        .fbar .fv{font-size:clamp(1.4rem,2.4vw,2rem);font-weight:800;color:var(--primary-dark)}
        .fbar.tam{background:rgba(240,248,255,.7);border:2px dashed rgba(4,55,98,.25)}
        .fbar.sam{background:rgba(200,232,255,.6);border:1px solid rgba(4,85,163,.25);margin:0 clamp(1rem,3vw,2.5rem)}
        .fbar.som{background:linear-gradient(135deg,var(--primary-dark),var(--primary));margin:0 clamp(2rem,6vw,5rem)}
        .fbar.som .fl{color:#c8e8ff}.fbar.som .fd{color:rgba(255,255,255,.8)}.fbar.som .fv{color:#fff}
        /* --- traction --- */
        .tr-live{display:flex;align-items:flex-start;gap:1rem;padding:clamp(1.1rem,1.8vw,1.6rem);border-radius:var(--r-lg);background:linear-gradient(140deg,var(--primary-dark),var(--primary));color:#fff;box-shadow:var(--s-md)}
        .tr-live strong{font-size:clamp(1rem,1.3vw,1.2rem)}
        .tr-live .badge2{display:inline-block;margin-top:.6rem;padding:.25rem .75rem;border-radius:20px;background:rgba(255,255,255,.18);font-size:.7rem;font-weight:700}
        .checklist{list-style:none;display:flex;flex-direction:column;gap:.55rem}
        .checklist li{display:flex;gap:.6rem;align-items:flex-start;font-size:clamp(.82rem,1vw,.96rem);color:#334155;line-height:1.4}
        .checklist li svg{width:18px;height:18px;stroke:#22c55e;stroke-width:2.4;fill:none;flex-shrink:0;margin-top:.12rem}
        /* --- team --- */
        .team{display:grid;grid-template-columns:1fr 1fr;gap:clamp(1rem,2.5vw,2rem);margin-top:clamp(1rem,2.4vh,1.8rem)}
        .tcard{padding:clamp(1.2rem,2vw,1.9rem);display:flex;flex-direction:column;align-items:center;text-align:center}
        .tcard img{width:clamp(84px,8vw,120px);height:clamp(84px,8vw,120px);border-radius:50%;object-fit:cover;border:3px solid var(--glass-border);box-shadow:var(--s-md)}
        .tcard h3{font-size:clamp(1.05rem,1.5vw,1.4rem);color:var(--primary-dark);margin-top:.8rem}
        .tcard .trole{font-size:.85rem;color:var(--accent);font-weight:700;margin-top:.15rem}
        .tchips{display:flex;flex-wrap:wrap;gap:.4rem;justify-content:center;margin:.7rem 0}
        .tchips span{font-size:.72rem;font-weight:600;color:var(--primary-dark);background:linear-gradient(135deg,rgba(4,55,98,.07),rgba(105,26,106,.08));padding:.3rem .7rem;border-radius:20px}
        .tcard ul{list-style:none;display:flex;flex-direction:column;gap:.45rem;text-align:left;margin-top:.4rem}
        .tcard li{font-size:clamp(.8rem,.98vw,.92rem);color:var(--muted);display:flex;gap:.5rem;align-items:flex-start;line-height:1.4}
        .tcard li svg{width:15px;height:15px;stroke:var(--primary);stroke-width:2.4;fill:none;flex-shrink:0;margin-top:.22rem}
        /* --- financials --- */
        .fin{display:grid;grid-template-columns:1.4fr 1fr;gap:clamp(1rem,2.5vw,2rem);margin-top:clamp(1rem,2vh,1.6rem);align-items:stretch}
        .bars{display:flex;align-items:flex-end;justify-content:space-around;gap:clamp(1rem,3vw,2.5rem);height:clamp(150px,24vh,240px);padding:1rem clamp(.5rem,2vw,1.5rem) 0}
        .bar{display:flex;flex-direction:column;align-items:center;gap:.5rem;flex:1;height:100%;justify-content:flex-end}
        .bar .bv{font-weight:800;color:var(--primary-dark);font-size:clamp(.85rem,1.1vw,1.05rem)}
        .bar .bcol{width:clamp(48px,6vw,92px);height:0;border-radius:8px 8px 0 0;background:linear-gradient(180deg,var(--primary),var(--primary-dark));transition:height .9s cubic-bezier(.22,1,.36,1)}
        .bar:last-child .bcol{background:linear-gradient(180deg,var(--accent),var(--accent-2))}
        .bar .bl{font-size:clamp(.72rem,.9vw,.85rem);color:var(--muted)}
        .fin-cards{display:flex;flex-direction:column;gap:clamp(.6rem,1.2vh,1rem);justify-content:center}
        .fin-card{padding:clamp(.9rem,1.4vw,1.2rem) clamp(1rem,1.6vw,1.3rem);border-left:4px solid var(--primary)}
        .fin-card .fcl{font-size:.72rem;font-weight:600;color:var(--muted)}
        .fin-card .fcv{font-size:clamp(1.2rem,1.8vw,1.6rem);font-weight:800;color:var(--primary-dark)}
        .fin-card .fcs{font-size:.72rem;color:var(--accent)}
        /* --- ask --- */
        .ask-amt{font-size:clamp(2.6rem,6vw,5rem);font-weight:800;letter-spacing:-.022em;line-height:1;background:linear-gradient(118deg,var(--primary),var(--accent));-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
        .ask-eq{font-size:clamp(1rem,1.6vw,1.4rem);font-weight:600;color:var(--primary-dark);margin-top:.3rem}
        .fundbar{display:flex;height:clamp(22px,2.6vh,30px);border-radius:8px;overflow:hidden;margin-top:.5rem}
        .fundbar span{display:flex;align-items:center;justify-content:center;font-size:.7rem;color:#fff;font-weight:700;white-space:nowrap}
        /* --- roadmap (showpiece) --- */
        .rm-wrap{margin-top:clamp(1rem,2.2vh,1.6rem)}
        .rmline{display:flex;justify-content:space-between;position:relative;margin:0 7% clamp(1.4rem,3vh,2.2rem)}
        .rmline::before{content:"";position:absolute;left:10px;right:10px;top:9px;height:3px;border-radius:3px;background:linear-gradient(90deg,var(--primary),var(--accent))}
        .rmpt{position:relative;z-index:1;display:flex;flex-direction:column;align-items:center;gap:.3rem;text-align:center}
        .rmpt .d{width:20px;height:20px;border-radius:50%;background:#fff;border:3px solid var(--primary);box-shadow:0 0 0 4px rgba(4,85,163,.12)}
        .rmpt:first-child .d{background:var(--primary)}
        .rmpt:last-child .d{border-color:var(--accent);background:var(--accent);box-shadow:0 0 0 4px rgba(105,26,106,.16)}
        .rmpt .l{font-size:clamp(.72rem,.95vw,.86rem);font-weight:700;color:var(--primary-dark)}
        .rmpt .v{font-size:clamp(.64rem,.82vw,.74rem);color:var(--muted)}
        .rm{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(.9rem,1.8vw,1.6rem);align-items:stretch}
        .rmcard{position:relative;padding:clamp(1.2rem,1.9vw,1.7rem);border-radius:var(--r-lg);display:flex;flex-direction:column;overflow:hidden;transition:transform .45s cubic-bezier(.22,1,.36,1),box-shadow .45s}
        .rmcard:hover{transform:translateY(-6px)}
        .rmcard .ph{display:flex;align-items:center;gap:.65rem;margin-bottom:.7rem}
        .rmcard .pn{width:clamp(34px,2.6vw,42px);height:clamp(34px,2.6vw,42px);border-radius:12px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:clamp(.95rem,1.2vw,1.15rem);flex-shrink:0}
        .rmcard .pn svg{width:54%;height:54%;stroke:currentColor;fill:none;stroke-width:2}
        .rmcard .pt{font-size:.68rem;font-weight:700;letter-spacing:.05em;text-transform:uppercase;padding:.26rem .62rem;border-radius:20px}
        .rmcard h3{font-size:clamp(1.05rem,1.4vw,1.35rem);line-height:1.15;margin-bottom:.65rem}
        .rmcard ul{list-style:none;display:flex;flex-direction:column;gap:.42rem;flex:1}
        .rmcard li{font-size:clamp(.8rem,.98vw,.94rem);display:flex;gap:.5rem;align-items:flex-start;line-height:1.38}
        .rmcard li::before{content:"";width:6px;height:6px;border-radius:50%;margin-top:.46rem;flex-shrink:0}
        .rmcard .tgt{margin-top:.9rem;padding-top:.8rem;border-top:1px solid var(--line);display:flex;align-items:baseline;gap:.45rem}
        .rmcard .tgt b{font-size:clamp(1.3rem,1.9vw,1.7rem);font-weight:800}
        .rmcard .tgt span{font-size:.72rem}
        .rmcard.lite{background:var(--glass);border:1px solid var(--glass-border);box-shadow:var(--s-sm)}
        .rmcard.lite .pn{background:linear-gradient(135deg,var(--primary),var(--primary-dark));color:#fff;box-shadow:0 6px 16px rgba(4,85,163,.25)}
        .rmcard.lite .pt{background:rgba(4,85,163,.1);color:var(--primary)}
        .rmcard.lite h3{color:var(--primary-dark)}
        .rmcard.lite li{color:var(--muted)}
        .rmcard.lite li::before{background:linear-gradient(135deg,var(--primary),var(--accent))}
        .rmcard.lite .tgt b{color:var(--primary-dark)}.rmcard.lite .tgt span{color:var(--muted)}
        .rmcard.climax{background:linear-gradient(150deg,var(--primary-dark),var(--primary) 58%,var(--accent));color:#fff;border:1px solid rgba(255,255,255,.14);box-shadow:0 30px 72px -22px rgba(105,26,106,.62),0 12px 30px rgba(4,55,98,.22)}
        .rmcard.climax::after{content:"";position:absolute;top:-45%;right:-35%;width:75%;height:75%;background:radial-gradient(circle,rgba(255,255,255,.2),transparent 70%);pointer-events:none}
        .rmcard.climax>*{position:relative;z-index:1}
        .rmcard.climax .pn{background:rgba(255,255,255,.2);color:#fff}
        .rmcard.climax .pt{background:rgba(255,255,255,.16);color:#fff}
        .rmcard.climax h3{color:#fff}
        .rmcard.climax li{color:rgba(255,255,255,.92)}
        .rmcard.climax li::before{background:#c8e8ff}
        .rmcard.climax .tgt{border-top-color:rgba(255,255,255,.22)}
        .rmcard.climax .tgt b{color:#fff}.rmcard.climax .tgt span{color:rgba(255,255,255,.78)}
        .rmcard .flag{position:absolute;top:clamp(.9rem,1.4vw,1.3rem);right:clamp(.9rem,1.4vw,1.3rem);display:inline-flex;align-items:center;gap:.34rem;font-size:.58rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#fff;background:rgba(255,255,255,.16);padding:.28rem .6rem;border-radius:20px;z-index:2}
        .rmcard .flag svg{width:11px;height:11px;stroke:#c8e8ff;fill:none;stroke-width:2}
        .rm-live{display:inline-flex;align-items:center;gap:.38rem;font-size:.6rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#16a34a;margin-left:auto}
        .rm-live .dot{width:7px;height:7px;border-radius:50%;background:#16a34a;box-shadow:0 0 0 0 rgba(22,163,74,.5);animation:pulse 2s infinite}
        .rm-cap{text-align:center;color:var(--muted);margin-top:clamp(.9rem,2vh,1.4rem);font-size:clamp(.82rem,1vw,.96rem)}
        .rm-cap b{color:var(--primary-dark)}
        /* --- A/B review flag (temporary marker for Dr Suhirdan to choose) --- */
        .reviewflag{position:absolute;top:clamp(4.2rem,8.5vh,5.6rem);left:50%;transform:translateX(-50%);z-index:6;background:#b45309;color:#fff;font-size:.6rem;font-weight:800;letter-spacing:.09em;text-transform:uppercase;padding:.32rem .85rem;border-radius:20px;box-shadow:0 6px 16px rgba(180,83,9,.32);white-space:nowrap}
        /* --- app download QR --- */
        .dl{display:flex;justify-content:center;gap:clamp(1rem,2.6vw,2rem);flex-wrap:wrap;margin-top:clamp(1rem,2.2vh,1.5rem)}
        .dlcard{display:flex;align-items:center;gap:.85rem;padding:clamp(.7rem,1.2vw,1rem) clamp(.9rem,1.4vw,1.2rem)}
        .dlcard img{width:clamp(60px,6.5vw,84px);height:auto;border-radius:8px;display:block}
        .dlcard .dt{font-size:.64rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
        .dlcard .dn{font-size:clamp(.92rem,1.2vw,1.08rem);font-weight:700;color:var(--primary-dark)}
        .dlcard .ds{font-size:.74rem;color:var(--muted)}
        /* --- interactive ROI calculator --- */
        .calc{display:grid;grid-template-columns:0.9fr 1.1fr;gap:clamp(1.2rem,3vw,2.5rem);margin-top:clamp(1rem,2.4vh,1.8rem);align-items:stretch}
        .calc-inputs{padding:clamp(1.2rem,2vw,1.8rem);display:flex;flex-direction:column;gap:clamp(1rem,2vh,1.5rem);justify-content:center}
        .calc-field label{display:flex;justify-content:space-between;align-items:baseline;font-size:clamp(.82rem,1vw,.96rem);font-weight:600;color:var(--primary-dark);margin-bottom:.55rem}
        .calc-field label span{color:var(--accent);font-weight:800;font-size:1.05em}
        .calc-field input[type=range]{width:100%;accent-color:var(--primary);height:6px;cursor:pointer}
        .calc-note{font-size:.74rem;color:var(--muted);line-height:1.45}
        .calc-outputs{display:grid;grid-template-columns:1fr 1fr;gap:clamp(.8rem,1.6vw,1.3rem)}
        .calc-out{padding:clamp(1.1rem,1.9vw,1.7rem);text-align:center;display:flex;flex-direction:column;justify-content:center}
        .calc-out .co-v{font-size:clamp(1.7rem,3.2vw,2.6rem);font-weight:800;line-height:1;background:linear-gradient(118deg,var(--primary),var(--accent));-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
        .calc-out .co-l{font-size:.78rem;color:var(--muted);margin-top:.45rem;line-height:1.3}
        @media (max-width:900px){.calc{grid-template-columns:1fr}}
        /* --- unit economics --- */
        .econ{display:grid;grid-template-columns:1fr auto 1fr auto 1fr;gap:clamp(.5rem,1.4vw,1.1rem);align-items:stretch;margin-top:clamp(1rem,2.4vh,1.8rem)}
        .econ-step{padding:clamp(1.1rem,1.9vw,1.7rem);text-align:center;display:flex;flex-direction:column;align-items:center;gap:.5rem;justify-content:center}
        .econ-step .ev{font-size:clamp(1.9rem,3.8vw,3.1rem);font-weight:800;line-height:1;background:linear-gradient(118deg,var(--primary),var(--accent));-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
        .econ-step .el{font-size:clamp(.82rem,1.05vw,1rem);font-weight:700;color:var(--primary-dark)}
        .econ-step .ed{font-size:clamp(.76rem,.92vw,.86rem);color:var(--muted);line-height:1.4}
        .econ-arrow{display:flex;align-items:center;justify-content:center}
        .econ-arrow svg{width:clamp(22px,2.8vw,38px);height:auto;stroke:var(--accent);stroke-width:1.6;fill:none}
        .econ-bar{display:flex;height:13px;border-radius:7px;overflow:hidden;width:100%;margin:.2rem 0}
        .econ-bar .cost{background:rgba(4,55,98,.16)}
        .econ-bar .marg{background:linear-gradient(90deg,var(--primary),var(--accent))}
        .econ-foot{display:flex;gap:clamp(.8rem,2vw,1.5rem);flex-wrap:wrap;margin-top:clamp(1rem,2.4vh,1.6rem)}
        .econ-foot .ef{flex:1;min-width:220px;padding:clamp(1rem,1.5vw,1.3rem);font-size:clamp(.82rem,1vw,.94rem);color:var(--muted);line-height:1.45}
        .econ-foot .ef b{color:var(--primary-dark)}
        .econ-foot .ef .efv{font-size:clamp(1.3rem,2vw,1.7rem);font-weight:800;line-height:1;background:linear-gradient(118deg,var(--primary),var(--accent));-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;display:block;margin-bottom:.3rem}
        @media (max-width:900px){.econ{grid-template-columns:1fr}.econ-arrow svg{transform:rotate(90deg)}.econ-foot .ef{min-width:0}}
        /* --- vision (today -> tomorrow) --- */
        .vis{display:grid;grid-template-columns:1fr auto 1fr;gap:clamp(1rem,2.5vw,2rem);align-items:stretch;margin-top:clamp(1rem,2.4vh,1.9rem)}
        .vis-card{padding:clamp(1.3rem,2.2vw,2rem);border-radius:var(--r-lg);display:flex;flex-direction:column;gap:.6rem;position:relative;overflow:hidden}
        .vis-card.now{background:var(--glass);border:1px solid var(--glass-border);box-shadow:var(--s-sm)}
        .vis-card.future{background:linear-gradient(150deg,var(--primary-dark),var(--primary) 58%,var(--accent));color:#fff;box-shadow:var(--s-lg)}
        .vis-card.future::after{content:"";position:absolute;top:-45%;right:-35%;width:75%;height:75%;background:radial-gradient(circle,rgba(255,255,255,.18),transparent 70%);pointer-events:none}
        .vis-card>*{position:relative;z-index:1}
        .vis-tag{font-size:.7rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase}
        .vis-card.now .vis-tag{color:var(--accent)}
        .vis-card.future .vis-tag{color:#c8e8ff}
        .vis-card h3{font-size:clamp(1.1rem,1.7vw,1.55rem);line-height:1.15;color:var(--primary-dark)}
        .vis-card.future h3{color:#fff}
        .vis-card p{font-size:clamp(.86rem,1.05vw,1rem);line-height:1.5;color:var(--muted)}
        .vis-card.future p{color:rgba(255,255,255,.9)}
        .vis-pill{margin-top:auto;align-self:flex-start;font-size:.74rem;font-weight:700;padding:.35rem .85rem;border-radius:20px}
        .vis-card.now .vis-pill{background:linear-gradient(135deg,rgba(4,55,98,.08),rgba(105,26,106,.08));color:var(--primary-dark)}
        .vis-card.future .vis-pill{background:rgba(255,255,255,.16);color:#fff}
        .vis-arrow{display:flex;align-items:center;justify-content:center}
        .vis-arrow svg{width:clamp(28px,3.5vw,48px);height:auto;stroke:var(--accent);stroke-width:1.5;fill:none}
        @media (max-width:900px){.vis{grid-template-columns:1fr}.vis-arrow svg{transform:rotate(90deg)}}
        @media (max-width:1024px){.steps{grid-template-columns:repeat(2,1fr)}.fin{grid-template-columns:1fr}.rm{grid-template-columns:1fr}.rmcard:hover{transform:none}}
        @media (max-width:640px){.steps,.team,.cards.c2{grid-template-columns:1fr}.agenda-item .ad{display:none}.cmp-row{font-size:.56rem}.fbar.sam,.fbar.som{margin:0}.rmline{display:none}}

        .counter{position:fixed;bottom:clamp(.8rem,2vh,1.5rem);right:clamp(1rem,3vw,2.4rem);font-size:clamp(.72rem,.95vw,.84rem);color:var(--muted);z-index:100;display:flex;gap:.6rem;align-items:center}
        .counter b{color:var(--primary);font-weight:700}
        .counter .sec{padding-left:.6rem;border-left:1px solid var(--line);text-transform:uppercase;letter-spacing:.1em;font-size:.72em;font-weight:700;color:#94a3b8}

        /* reveal - springy, staggered */
        .reveal{opacity:0;transform:translateY(24px);transition:opacity .6s cubic-bezier(.22,1,.36,1),transform .7s cubic-bezier(.34,1.4,.5,1)}
        .slide.active .reveal{opacity:1;transform:none}
        .slide.active .reveal[data-delay="1"]{transition-delay:.07s}
        .slide.active .reveal[data-delay="2"]{transition-delay:.14s}
        .slide.active .reveal[data-delay="3"]{transition-delay:.22s}
        .slide.active .reveal[data-delay="4"]{transition-delay:.30s}
        .slide.active .reveal[data-delay="5"]{transition-delay:.38s}
        .slide.active .reveal[data-delay="6"]{transition-delay:.46s}

        @media (max-width:1024px){
            .feature,.feature.reverse,.intro{grid-template-columns:1fr;gap:clamp(1rem,3vh,2rem);align-content:center}
            .feature.reverse .feature-copy,.feature.reverse .clip{order:0}
            .clip-frame video,.intro .clip-frame video{max-height:46dvh}
            .pillars{grid-template-columns:repeat(3,1fr);grid-auto-rows:1fr}
            .integ{grid-template-columns:1fr}
            .pipe{flex-direction:row;gap:1rem}.pipe svg{transform:rotate(90deg)}
        }
        @media (max-width:640px){
            .slide{justify-content:flex-start;overflow-y:auto;padding:clamp(4rem,11vh,5rem) 1.1rem 2rem}
            .inner.fill{height:auto}
            .cards.c3,.imx-prods{grid-template-columns:1fr}
            .pillars{grid-template-columns:1fr 1fr}
            .clip-frame video{max-height:none}
            .nav-tag,.dots{display:none}
            .subtitle{max-width:none}
        }
        @media (prefers-reduced-motion:reduce){
            .reveal{transition:none;opacity:1;transform:none}
            .clip-glow,.pulse{animation:none}.deck{scroll-behavior:auto}
        }
"""

ICONS = {
 "mic":'<path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/>',
 "check":'<polyline points="20 6 9 17 4 12"/>',
 "users":'<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/>',
 "eye":'<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>',
 "zap":'<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
 "wifi":'<path d="M5 12.55a11 11 0 0 1 14.08 0"/><path d="M1.42 9a16 16 0 0 1 21.16 0"/><path d="M8.53 16.11a6 6 0 0 1 6.95 0"/><line x1="12" y1="20" x2="12.01" y2="20"/>',
 "phone":'<rect x="5" y="2" width="14" height="20" rx="2"/><line x1="9" y1="6" x2="15" y2="6"/>',
 "clock":'<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
 "upload":'<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/>',
 "refresh":'<polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>',
 "file":'<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/>',
 "sliders":'<line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><line x1="1" y1="14" x2="7" y2="14"/><line x1="9" y1="8" x2="15" y2="8"/><line x1="17" y1="16" x2="23" y2="16"/>',
 "edit":'<path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.12 2.12 0 0 1 3 3L12 15l-4 1 1-4z"/>',
 "send":'<line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/>',
 "mail":'<path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/>',
 "calendar":'<rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>',
 "tasks":'<polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
 "video":'<polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2"/>',
 "bell":'<path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/>',
 "switch":'<polyline points="17 1 21 5 17 9"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><polyline points="7 23 3 19 7 15"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/>',
 "shield":'<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
 "lock":'<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
 "userplus":'<path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/><line x1="20" y1="8" x2="20" y2="14"/><line x1="23" y1="11" x2="17" y2="11"/>',
 "user":'<circle cx="12" cy="8" r="5"/><path d="M20 21a8 8 0 0 0-16 0"/>',
 "card":'<rect x="1" y="4" width="22" height="16" rx="2"/><line x1="1" y1="10" x2="23" y2="10"/>',
 "smartphone":'<rect x="5" y="2" width="14" height="20" rx="2"/><line x1="12" y1="18" x2="12.01" y2="18"/>',
 "gift":'<polyline points="20 12 20 22 4 22 4 12"/><rect x="2" y="7" width="20" height="5"/><line x1="12" y1="22" x2="12" y2="7"/><path d="M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7z"/><path d="M12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z"/>',
}

def svg(key):
    return '<svg viewBox="0 0 24 24">%s</svg>' % ICONS[key]

# feature slides: (section, title, subtitle, [ (icon,h4,p), ... ], clipfile, urllabel)
FEATURES = [
 ("Core Documentation","Individual Notes",
  "A clinician records a single consultation and Arvi generates a structured clinical note, formatted, accurate and ready to review in seconds.",
  [("mic","Record &amp; structure","Ambient capture becomes a clean, sectioned note, no typing."),
   ("check","Review, don't author","The clinician edits a draft instead of writing from scratch.")],
  "01-letter-generation.mp4","platform.arvihealth.com &middot; New note"),

 ("Core Documentation","Organisation &amp; Team Notes",
  "Documentation under a clinic or team account, with multiple clinicians working together and admin oversight across everyone's work.",
  [("users","Shared team workspace","Clinicians document under one organisation, not siloed accounts."),
   ("eye","Admin visibility","Administrators can access and manage notes across the team.")],
  "02-admin-access.mp4","platform.arvihealth.com &middot; Organisation"),

 ("Core Documentation","Quick Record for Emergencies",
  "A fast-capture mode for urgent situations, minimal steps between hitting record and having a usable note. Built for the pace of an emergency department.",
  [("zap","One tap to capture","No setup overhead when seconds matter."),
   ("check","Structured after the fact","The note is generated once the moment has passed.")],
  "03-quick-record.mp4","Arvi &middot; Quick Record"),

 ("Core Documentation","Operating Theatre on Mobile",
  "The clinician uses the mobile app right in theatre, capturing the operation note even when connectivity is low, then syncing when back online.",
  [("phone","In-theatre capture","The note is created at the point of care, not reconstructed later."),
   ("wifi","Low-connectivity ready","Works where hospital Wi-Fi is weak; syncs when reconnected.")],
  "04-mobile-recording.mp4","Arvi mobile &middot; Operating theatre"),

 ("Core Documentation","Upload an Existing Recording",
  "No live capture required, the user uploads an existing audio file and Arvi generates the structured note from it.",
  [("upload","Bring your own audio","Drop in a file recorded anywhere; Arvi does the rest."),
   ("file","Same structured output","Uploaded audio produces the same clean clinical note.")],
  "05-upload-recording.mp4","platform.arvihealth.com &middot; Upload"),

 ("Core Documentation","AI Regeneration",
  "Any note or letter can be regenerated or refined with AI, tune the tone, length or detail until it's exactly right.",
  [("refresh","Refine on demand","Regenerate sections or the whole document in a click."),
   ("sliders","Clinician in control","The AI assists; the clinician decides the final wording.")],
  "06-regeneration.mp4","platform.arvihealth.com &middot; Regenerate"),

 ("Letters &amp; Templates","Letter Generation &amp; Preview",
  "Arvi produces the GP or referral letter from the recording, then lets you review, edit and format it on a dedicated preview page before it goes out.",
  [("file","Letter from a recording","A ready-to-send GP or referral letter, generated automatically."),
   ("edit","Preview &amp; formatting","The final review page, edit and format before sending.")],
  "07-edit-letter.mp4","platform.arvihealth.com &middot; Preview &amp; formatting"),

 ("Letters &amp; Templates","Custom Letter Templates",
  "Users create their own templates and adjust the formatting to suit their practice, so every letter matches their house style.",
  [("sliders","Build your own","Create reusable templates for any letter type."),
   ("edit","Tune the formatting","Adjust layout and styling to match your practice.")],
  "08-custom-template.mp4","platform.arvihealth.com &middot; Templates"),

 ("Letters &amp; Templates","Approve, Send &amp; Resend",
  "Email the finished letter to the recipient directly from Arvi, with the option to resend whenever needed.",
  [("send","Send from Arvi","Deliver the letter to the recipient without leaving the app."),
   ("mail","Resend any time","Re-issue a letter in one click if it's needed again.")],
  "09-approve-resend.mp4","platform.arvihealth.com &middot; Send"),

 ("Patient &amp; Workflow","Patient Management &amp; Scheduling",
  "Manage patients, appointments and the calendar in one place, the day's schedule sits alongside the documentation.",
  [("calendar","Appointments &amp; calendar","See the day's schedule and book in patients."),
   ("users","Patient records","Keep patient details organised next to their notes.")],
  "10-patient-management.mp4","platform.arvihealth.com &middot; Patients"),

 ("Patient &amp; Workflow","Task Management",
  "Track outstanding work to completion, nothing slips between the consult and the follow-up.",
  [("tasks","Track outstanding work","A clear list of what still needs doing."),
   ("check","Close the loop","Mark tasks complete as the work gets done.")],
  "11-task-management.mp4","platform.arvihealth.com &middot; Tasks"),

 ("Patient &amp; Workflow","Telehealth Consultations",
  "Run remote consultations inside Arvi, and document them with the same AI workflow as in-person visits.",
  [("video","Remote consults in-app","Conduct telehealth sessions without a separate tool."),
   ("mic","Documented automatically","The same capture-to-note flow applies to remote visits.")],
  "13-telehealth.mp4","platform.arvihealth.com &middot; Telehealth"),

 ("Patient &amp; Workflow","Notifications",
  "Stay on top of what matters with in-app alerts and push notifications on mobile.",
  [("bell","In-app &amp; push alerts","Get notified across web and mobile."),
   ("phone","Never miss an action","Time-sensitive items reach the clinician promptly.")],
  "14-notifications.mp4","Arvi mobile &middot; Notifications"),

 ("Organisation &amp; Users","Organisation Switcher",
  "One user can belong to several organisations and switch between them instantly, ideal for clinicians working across sites.",
  [("switch","Belong to many orgs","Hold membership in multiple organisations at once."),
   ("check","Switch in one tap","Move between organisations without logging out.")],
  "15-org-switcher.mp4","platform.arvihealth.com &middot; Switch organisation"),

 ("Organisation &amp; Users","Roles &amp; Permissions",
  "Role-based access and restrictions govern who can see and do what, the access model hospitals require.",
  [("shield","Role-based access","Assign roles that match real responsibilities."),
   ("lock","Granular restrictions","Control permissions down to the action.")],
  "16-permission-update.mp4","platform.arvihealth.com &middot; Permissions"),

 ("Organisation &amp; Users","User Invites",
  "Bring new clinicians into an organisation quickly with a simple invite flow.",
  [("userplus","Invite in seconds","Add new users to the organisation with an invite."),
   ("users","Onboard the team","Grow the organisation without admin friction.")],
  "17-user-invite.mp4","platform.arvihealth.com &middot; Invite users"),

 ("Organisation &amp; Users","Free Admin User",
  "Every organisation includes an admin seat at no cost, oversight without an extra licence.",
  [("user","Admin at no cost","A free administrator seat comes with the organisation."),
   ("eye","Oversight built in","Manage the team without paying for the privilege.")],
  "18-free-admin.mp4","platform.arvihealth.com &middot; Admin"),

 ("Billing","Stripe Subscriptions (Web)",
  "Arvi bills customers today via Stripe, subscriptions and payments on the web app, in production now.",
  [("card","Subscriptions &amp; payments","Recurring billing handled through Stripe on web."),
   ("check","Live in production","The commercial engine is running, not on a roadmap.")],
  "19-subscription.mp4","platform.arvihealth.com &middot; Billing"),

 ("Billing","iOS In-App Purchase",
  "On iOS, Arvi bills natively through Apple's in-app purchase, a frictionless path for mobile users.",
  [("smartphone","Native Apple billing","Purchase and subscribe directly inside the iOS app."),
   ("check","Platform-appropriate","Meets Apple's requirements for mobile monetisation.")],
  "20-ios-billing.mp4","Arvi mobile &middot; iOS billing"),
]

def feat_slide(idx, sid, section, title, subtitle, points, clip, url, reverse):
    pts = "\n".join(
        '                            <li class="reveal" data-delay="%d"><span class="ic">%s</span><div><h4>%s</h4><p>%s</p></div></li>'
        % (3+j, svg(ic), h4, p) for j,(ic,h4,p) in enumerate(points))
    src = "Videos/" + clip.replace(" ", "%20")
    rev = " reverse" if reverse else ""
    return '''        <!-- {sid} -->
        <section class="slide" id="{sid}" data-sec="{section_plain}">
            <div class="inner">
                <div class="feature{rev}">
                    <div class="feature-copy">
                        <div class="kicker reveal"><span class="n">{idx:02d}</span><span class="s">{section}</span></div>
                        <h2 class="title reveal" data-delay="1">{title}</h2>
                        <p class="subtitle reveal" data-delay="2">{subtitle}</p>
                        <ul class="points">
{pts}
                        </ul>
                    </div>
                    <figure class="clip reveal" data-delay="2">
                        <div class="clip-glow"></div>
                        <div class="clip-frame"><div class="chrome"><i></i><i></i><i></i><span class="url">{url}</span></div><video src="{src}" loop muted playsinline preload="metadata"></video></div>
                    </figure>
                </div>
            </div>
        </section>
'''.format(sid=sid, section=section, section_plain=section.replace("&amp;","&"), rev=rev, idx=idx,
           title=title, subtitle=subtitle, pts=pts, url=url, src=src)

# ---- build feature slides ----
feat_html = []
for i,(section,title,subtitle,points,clip,url) in enumerate(FEATURES):
    sid = "f%d" % (i+1)
    feat_html.append(feat_slide(i+1, sid, section, title, subtitle, points, clip, url, reverse=(i%2==1)))
FEAT = "\n".join(feat_html)

INTRO = '''        <!-- Intro -->
        <section class="slide" id="s-intro" data-sec="Overview">
            <div class="inner">
                <div class="intro">
                    <div class="feature-copy">
                        <div class="badge reveal"><span class="pulse"></span> AI Clinical Documentation</div>
                        <h1 class="reveal" data-delay="1">Capture the consult.<br><span>Arvi does the rest.</span></h1>
                        <p class="reveal" data-delay="2">From clinic, emergency, ward or theatre to a structured clinical note and ready-to-send letter, the capture &amp; authoring layer that plugs into the systems hospitals already run.</p>
                        <div class="tags reveal" data-delay="3"><span class="tag">Web &amp; mobile apps</span><span class="tag">20 production features</span><span class="tag">HL7 / FHIR-ready</span></div>
                    </div>
                    <figure class="clip reveal" data-delay="2">
                        <div class="clip-glow"></div>
                        <div class="clip-frame"><video src="arvi-demo.mp4" autoplay loop muted playsinline preload="metadata"></video></div>
                    </figure>
                </div>
            </div>
        </section>
'''

PROBLEM = '''        <!-- Problem -->
        <section class="slide" id="s-problem" data-sec="Overview">
            <div class="inner">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg> The Problem</div>
                    <h2 class="title reveal" data-delay="1">Documentation Is the Tax on Every Clinical Minute</h2>
                    <p class="subtitle reveal" data-delay="2">Across hospitals, clinics and theatres, clinicians lose hours to notes and letters instead of patients, and that content still reaches the chart late, inconsistent and incomplete.</p>
                </div>
                <div class="cards c3">
                    <div class="card glass reveal" data-delay="2"><div class="vic"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg></div><h3>Time poverty</h3><p>Clinicians spend up to half their day documenting, much of it after hours.</p></div>
                    <div class="card glass reveal" data-delay="3"><div class="vic"><svg viewBox="0 0 24 24"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg></div><h3>Late, inconsistent records</h3><p>Notes typed from memory hours later, quality and timeliness both suffer.</p></div>
                    <div class="card glass reveal" data-delay="4"><div class="vic"><svg viewBox="0 0 24 24"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg></div><h3>Costly downstream</h3><p>Poor source documentation slows coding, referrals and discharge, the exact workflows hospitals depend on.</p></div>
                </div>
            </div>
        </section>
'''

PLATFORM = '''        <!-- Platform -->
        <section class="slide" id="s-platform" data-sec="Overview">
            <div class="inner fill">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg> The Platform</div>
                    <h2 class="title reveal" data-delay="1">One Platform. Two Apps. Twenty Production Features.</h2>
                    <div class="apps reveal" data-delay="2">
                        <div class="app glass"><svg viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg><div><strong>Web app</strong><span>Full clinic &amp; organisation workspace</span></div></div>
                        <div class="app glass"><svg viewBox="0 0 24 24"><rect x="5" y="2" width="14" height="20" rx="2"/><line x1="12" y1="18" x2="12.01" y2="18"/></svg><div><strong>iOS &amp; Android</strong><span>Capture anywhere, ward, ED, theatre</span></div></div>
                    </div>
                </div>
                <div class="pillars">
                    <div class="pillar glass reveal" data-delay="2"><div class="num">01</div><h3>Core Documentation</h3><ul><li>Individual notes</li><li>Org / team notes</li><li>Quick Record</li><li>Theatre recording</li><li>Upload audio</li><li>AI regeneration</li></ul></div>
                    <div class="pillar glass reveal" data-delay="3"><div class="num">02</div><h3>Letters &amp; Templates</h3><ul><li>Letter generation</li><li>Custom templates</li><li>Preview &amp; formatting</li><li>Send &amp; resend</li></ul></div>
                    <div class="pillar glass reveal" data-delay="4"><div class="num">03</div><h3>Patient &amp; Workflow</h3><ul><li>Patient management</li><li>Scheduling</li><li>Task management</li><li>Telehealth</li><li>Notifications</li></ul></div>
                    <div class="pillar glass reveal" data-delay="5"><div class="num">04</div><h3>Organisation &amp; Users</h3><ul><li>Org switcher</li><li>Roles &amp; permissions</li><li>User invites</li><li>Free admin user</li></ul></div>
                    <div class="pillar glass reveal" data-delay="6"><div class="num">05</div><h3>Billing</h3><ul><li>Stripe (web)</li><li>iOS in-app purchase</li></ul></div>
                </div>
            </div>
        </section>
'''

IMX_WORLD = '''        <!-- InfoMedix world -->
        <section class="slide" id="s-imx1" data-sec="InfoMedix">
            <div class="inner">
                <div class="slide-head">
                    <div class="label imx reveal"><svg viewBox="0 0 24 24"><path d="M3 21h18"/><path d="M5 21V7l8-4v18"/><path d="M19 21V11l-6-4"/></svg> The Opportunity &middot; InfoMedix</div>
                    <h2 class="title reveal" data-delay="1">Built for the World InfoMedix Serves</h2>
                    <p class="subtitle reveal" data-delay="2">InfoMedix runs the digital record for Australia's busiest hospitals, acute, emergency and surgical settings. Arvi's capture features were designed for exactly those environments.</p>
                </div>
                <div class="imx-bar glass reveal" data-delay="2">
                    <img src="InfoMedix-logo-png.webp" alt="InfoMedix" class="imx-logo">
                    <div class="imx-stat"><div class="v">250+</div><div class="l">hospitals on InfoMedix</div></div>
                    <div class="imx-stat"><div class="v">46k+</div><div class="l">daily active users</div></div>
                    <div class="imx-stat"><div class="v">2B+</div><div class="l">clinical documents managed</div></div>
                    <div class="imx-stat"><div class="v">30+</div><div class="l">systems integrated</div></div>
                </div>
                <div class="cards c3">
                    <div class="card glass reveal" data-delay="3"><div class="vic"><svg viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg></div><h3>Emergency departments</h3><p>Quick Record matches the tempo of ED, exactly where their hospitals operate.</p></div>
                    <div class="card glass reveal" data-delay="4"><div class="vic"><svg viewBox="0 0 24 24"><rect x="5" y="2" width="14" height="20" rx="2"/><line x1="9" y1="6" x2="15" y2="6"/></svg></div><h3>Operating theatres</h3><p>Mobile, low-connectivity theatre capture fits surgical workflows out of the box.</p></div>
                    <div class="card glass reveal" data-delay="5"><div class="vic"><svg viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg></div><h3>Teams &amp; departments</h3><p>Org/team accounts, roles and admin oversight mirror hospital structures.</p></div>
                </div>
            </div>
        </section>
'''

IMX_INTEG = '''        <!-- Integration -->
        <section class="slide" id="s-imx2" data-sec="InfoMedix">
            <span class="reviewflag">Framing A &middot; integration-led &middot; for review</span>
            <div class="inner">
                <div class="slide-head">
                    <div class="label imx reveal"><svg viewBox="0 0 24 24"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg> A Possible Pathway</div>
                    <h2 class="title reveal" data-delay="1">How Arvi Could Fit with InfoMedix</h2>
                    <p class="subtitle reveal" data-delay="2">One pathway we see: Arvi as the AI capture &amp; authoring front end to the InfoMedix record, workflow and coding backbone. Structured output could flow in over HL7 / FHIR, the interoperability layer InfoMedix already runs.</p>
                    <div class="tags reveal" data-delay="2"><span class="tag">Proposed integration &middot; for discussion</span></div>
                </div>
                <div class="integ">
                    <div class="integ-arvi reveal" data-delay="2">
                        <div class="il">Capture &amp; authoring</div>
                        <h3>Arvi</h3>
                        <p>Voice &rarr; structured note, letter &amp; referral</p>
                        <ul>
                            <li><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> Clinical notes</li>
                            <li><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> GP &amp; referral letters</li>
                            <li><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> Theatre &amp; discharge notes</li>
                        </ul>
                    </div>
                    <div class="pipe reveal" data-delay="3">
                        <div class="pl">HL7 / FHIR<br>secure messaging</div>
                        <svg viewBox="0 0 24 24"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
                        <div class="pl sub">structured documents</div>
                    </div>
                    <div class="imx-side">
                        <div class="imx-side-head reveal" data-delay="2"><img src="InfoMedix-logo-png.webp" alt="InfoMedix" class="imx-logo"><span>the InfoMedix suite</span></div>
                        <div class="imx-prods">
                            <div class="imx-prod glass reveal" data-delay="3"><h4>Digital Patient Chart</h4><p>Arvi notes could file into the chart, complete and on time.</p></div>
                            <div class="imx-prod glass reveal" data-delay="4"><h4>Referrals Manager</h4><p>Auto-generated referral letters could feed the HL7 referral pipeline.</p></div>
                            <div class="imx-prod glass reveal" data-delay="4"><h4>Discharge Manager</h4><p>Discharge summaries authored from the recording instead of retyped.</p></div>
                            <div class="imx-prod glass reveal" data-delay="5"><h4>Coding Manager</h4><p>Richer structured notes could lift coding accuracy &amp; speed.</p></div>
                            <div class="imx-prod glass span reveal" data-delay="5"><h4>Clinivid</h4><p>Arvi notes &amp; letters could be shared through InfoMedix's clinician collaboration layer.</p></div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
'''

IMX_VALUE = '''        <!-- Value -->
        <section class="slide" id="s-imx3" data-sec="InfoMedix">
            <div class="inner fill">
                <div class="slide-head">
                    <div class="label imx reveal"><svg viewBox="0 0 24 24"><line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="16"/></svg> Potential Value</div>
                    <h2 class="title reveal" data-delay="1">Where Arvi Could Add Value</h2>
                    <p class="subtitle reveal" data-delay="2">A complementary capability, not a competing one. Here is where Arvi could make the existing suite more valuable and stickier.</p>
                </div>
                <div class="cards c3">
                    <div class="card glass reveal" data-delay="2"><div class="vic"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg></div><h3>Fills the AI gap</h3><p>Would add ambient AI documentation, the one capability the suite doesn't have today, in the hottest category in health IT.</p></div>
                    <div class="card glass reveal" data-delay="3"><div class="vic"><svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg></div><h3>More, better documents</h3><p>Could feed the chart with complete, structured, on-time notes created at the point of care.</p></div>
                    <div class="card glass reveal" data-delay="4"><div class="vic"><svg viewBox="0 0 24 24"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg></div><h3>Lifts coding outcomes</h3><p>Richer source documentation could improve Coding Manager accuracy, speed and revenue capture.</p></div>
                    <div class="card glass reveal" data-delay="3"><div class="vic"><svg viewBox="0 0 24 24"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg></div><h3>Automates referrals &amp; discharge</h3><p>Letters and summaries could be generated, not retyped, accelerating the workflows InfoMedix sells.</p></div>
                    <div class="card glass reveal" data-delay="4"><div class="vic"><svg viewBox="0 0 24 24"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg></div><h3>Deeper stickiness</h3><p>Capture, chart, code and send in one loop could raise switching costs across the whole suite.</p></div>
                    <div class="card glass reveal" data-delay="5"><div class="vic"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg></div><h3>Ready distribution</h3><p>InfoMedix's 250+ hospitals and 46k daily users would be a natural channel for Arvi.</p></div>
                </div>
            </div>
        </section>
'''

CLOSE = '''        <!-- Close -->
        <section class="slide" id="s-close" data-sec="InfoMedix">
            <div class="inner">
                <div class="close">
                    <div class="lockup reveal"><img class="lk-arvi" src="arvi logo.avif" alt="Arvi Health"><span class="x">&times;</span><img class="lk-imx" src="InfoMedix-logo-png.webp" alt="InfoMedix"></div>
                    <h2 class="title reveal" data-delay="1">A Documentation Layer for InfoMedix's Hospitals</h2>
                    <p class="subtitle reveal" data-delay="2">Arvi captures and authors at the point of care; InfoMedix records, routes and codes. Together, that is a pathway to complete clinical documentation, end to end, with Arvi live today on web and mobile.</p>
                    <div class="tags reveal" data-delay="3" style="justify-content:center"><span class="tag">20 features in production</span><span class="tag">HL7 / FHIR-ready</span><span class="tag">Built for acute care</span></div>
                    <a class="cta reveal" data-delay="4" href="https://arvihealth.com" target="_blank" rel="noopener">Visit arvihealth.com <svg viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg></a>
                    <div class="dl reveal" data-delay="5">
                        <a class="dlcard glass" href="https://apps.apple.com/au/app/arvi-health/id6761469752" target="_blank" rel="noopener"><img src="qr-ios.png" alt="Download Arvi on the App Store"><div><div class="dt">Scan to download</div><div class="dn">Arvi for iOS</div><div class="ds">App Store</div></div></a>
                        <a class="dlcard glass" href="https://play.google.com/store/apps/details?id=com.healthai.mobile" target="_blank" rel="noopener"><img src="qr-android.png" alt="Download Arvi on Google Play"><div><div class="dt">Scan to download</div><div class="dn">Arvi for Android</div><div class="ds">Google Play</div></div></a>
                    </div>
                </div>
            </div>
        </section>
'''

AGENDA = '''        <!-- Agenda -->
        <section class="slide" id="s-agenda" data-sec="Overview">
            <div class="inner">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg> Agenda</div>
                    <h2 class="title reveal" data-delay="1">How We'll Spend the Time</h2>
                </div>
                <div class="agenda">
                    <div class="agenda-item glass reveal" data-delay="2"><div class="an">1</div><div><h3>The problem &amp; the product</h3><p>What Arvi is, and how it turns a consult into a clinical document.</p></div><div class="ad">~5 min</div></div>
                    <div class="agenda-item glass reveal" data-delay="3"><div class="an">2</div><div><h3>Why it wins</h3><p>Differentiation, market and the traction that proves it's real.</p></div><div class="ad">~8 min</div></div>
                    <div class="agenda-item glass reveal" data-delay="4"><div class="an">3</div><div><h3>Where Arvi fits with InfoMedix</h3><p>A proposed integration pathway, the value it adds, and our roadmap.</p></div><div class="ad">~10 min</div></div>
                    <div class="agenda-item glass reveal" data-delay="5"><div class="an">4</div><div><h3>The opportunity</h3><p>The team behind Arvi, and the raise.</p></div><div class="ad">~7 min</div></div>
                </div>
                <p class="rm-cap reveal" data-delay="6" style="text-align:left;margin-top:clamp(.8rem,1.6vh,1.2rem)">A full product walkthrough, all nineteen features in action, is in the <b>appendix</b>.</p>
            </div>
        </section>
'''

HOWITWORKS = '''        <!-- How it works -->
        <section class="slide" id="s-how" data-sec="Overview">
            <div class="inner">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg> How Arvi Works</div>
                    <h2 class="title reveal" data-delay="1">Voice In, Clinical Document Out</h2>
                    <p class="subtitle reveal" data-delay="2">The same four steps power every workflow you're about to see, on web and mobile.</p>
                </div>
                <div class="steps">
                    <div class="step glass reveal" data-delay="2"><div class="sic"><svg viewBox="0 0 24 24"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/></svg></div><div class="sn">STEP 01</div><h3>Capture</h3><p>Record the consult, or upload existing audio, anywhere.</p></div>
                    <div class="step glass reveal" data-delay="3"><div class="sic"><svg viewBox="0 0 24 24"><line x1="3" y1="12" x2="3" y2="12"/><line x1="7" y1="8" x2="7" y2="16"/><line x1="11" y1="4" x2="11" y2="20"/><line x1="15" y1="7" x2="15" y2="17"/><line x1="19" y1="10" x2="19" y2="14"/></svg></div><div class="sn">STEP 02</div><h3>Transcribe</h3><p>Speech becomes an accurate, medical-aware transcript.</p></div>
                    <div class="step glass reveal" data-delay="4"><div class="sic"><svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="8" y1="13" x2="16" y2="13"/><line x1="8" y1="17" x2="13" y2="17"/></svg></div><div class="sn">STEP 03</div><h3>Structure</h3><p>AI drafts a structured note or letter from the transcript.</p></div>
                    <div class="step glass reveal" data-delay="5"><div class="sic"><svg viewBox="0 0 24 24"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg></div><div class="sn">STEP 04</div><h3>Review &amp; send</h3><p>The clinician edits, formats and sends, in control throughout.</p></div>
                </div>
            </div>
        </section>
'''

WALK = '''        <!-- Demo cue: live demo starts now -->
        <section class="slide" id="s-walk" data-sec="Live Demo">
            <div class="inner">
                <div class="divider">
                    <div class="label reveal" style="justify-content:center"><svg viewBox="0 0 24 24"><polygon points="5 3 19 12 5 21 5 3"/></svg> Live Demo</div>
                    <div class="big reveal" data-delay="1">Let's See Arvi in Action</div>
                    <p class="subtitle reveal" data-delay="2" style="text-align:center;max-width:720px;margin:0 auto">We'll switch to a live demo now, from voice to a sent letter, across the five areas below. Recorded walkthroughs of every feature are in the appendix.</p>
                    <div class="menu reveal" data-delay="3">
                        <span class="mi"><b>01</b> Core Documentation</span>
                        <span class="mi"><b>02</b> Letters &amp; Templates</span>
                        <span class="mi"><b>03</b> Patient &amp; Workflow</span>
                        <span class="mi"><b>04</b> Organisation &amp; Users</span>
                        <span class="mi"><b>05</b> Billing</span>
                    </div>
                </div>
            </div>
        </section>
'''

COMPETITIVE = '''        <!-- Competitive -->
        <section class="slide" id="s-comp" data-sec="Differentiation">
            <div class="inner">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><path d="M18 20V10"/><path d="M12 20V4"/><path d="M6 20v-6"/></svg> Competitive Landscape</div>
                    <h2 class="title reveal" data-delay="1">Superior Quality, Accessible Pricing</h2>
                    <p class="subtitle reveal" data-delay="2">Specialist-led validation and a price built for adoption, against the generalist incumbents.</p>
                </div>
                <div class="cmp glass reveal" data-delay="2">
                    <div class="cmp-row cmp-head"><div>Feature</div><div>Nuance DAX</div><div>Lyrebird</div><div>Heidi</div><div class="arvi">Arvi<span class="cmp-best">BEST</span></div></div>
                    <div class="cmp-row"><div>Pricing</div><div>$300+/mo</div><div>$300+/mo</div><div>$1,320/yr</div><div class="arvi">From $30 + tokens</div></div>
                    <div class="cmp-row"><div>Target market</div><div>Large hospitals</div><div>GPs only</div><div>Practices</div><div class="arvi">GPs + specialists</div></div>
                    <div class="cmp-row"><div>Clinical validation</div><div>Standard</div><div>Standard</div><div>Standard</div><div class="arvi">Specialist-led</div></div>
                    <div class="cmp-row"><div>Care settings</div><div>Hospitals</div><div>GP</div><div>Practices</div><div class="arvi">All settings</div></div>
                    <div class="cmp-row"><div>Free admin seat</div><div>No</div><div>No</div><div>Limited</div><div class="arvi tick"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg></div></div>
                    <div class="cmp-row"><div>Entry barrier</div><div>Very high</div><div>Moderate</div><div>Med-high</div><div class="arvi">Lowest</div></div>
                </div>
                <div class="reveal" data-delay="3" style="display:flex;gap:clamp(.9rem,2.2vw,1.8rem);flex-wrap:wrap;margin-top:clamp(.9rem,1.8vh,1.3rem)">
                    <div style="flex:1;min-width:210px"><b style="color:var(--primary-dark);font-size:clamp(.9rem,1.05vw,1rem)">Clinician-led &amp; specialist-verified</b><span style="display:block;font-size:.82rem;color:var(--muted);line-height:1.4;margin-top:.2rem">Trained and corrected in live practice, not crowdsourced, unverified templates.</span></div>
                    <div style="flex:1;min-width:210px"><b style="color:var(--primary-dark);font-size:clamp(.9rem,1.05vw,1rem)">Adoption-friendly model</b><span style="display:block;font-size:.82rem;color:var(--muted);line-height:1.4;margin-top:.2rem">Entry from $30 + usage tokens, against ~$1,300/yr flat, so clinicians actually switch.</span></div>
                    <div style="flex:1;min-width:210px"><b style="color:var(--primary-dark);font-size:clamp(.9rem,1.05vw,1rem)">Early-partner upside</b><span style="display:block;font-size:.82rem;color:var(--muted);line-height:1.4;margin-top:.2rem">Come in at a fairer valuation than late-stage incumbents, and help shape the roadmap.</span></div>
                </div>
            </div>
        </section>
'''

MARKET = '''        <!-- Market -->
        <section class="slide" id="s-market" data-sec="Opportunity">
            <div class="inner">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg> Market Opportunity</div>
                    <h2 class="title reveal" data-delay="1">Bottom-Up Australian Market Sizing</h2>
                </div>
                <div class="cards" style="grid-template-columns:1.1fr 1fr;align-items:center;gap:clamp(1.2rem,3vw,2.5rem)">
                    <div class="funnel">
                        <div class="fbar tam reveal" data-delay="2"><div><div class="fl">TAM</div><div class="fd">Total addressable &middot; 70k clinicians</div></div><div class="fv">$63.8M</div></div>
                        <div class="fbar sam reveal" data-delay="3"><div><div class="fl">SAM</div><div class="fd">Metro GPs + specialists</div></div><div class="fv">$36.5M</div></div>
                        <div class="fbar som reveal" data-delay="4"><div><div class="fl">YEAR 3 TARGET</div><div class="fd">Serviceable obtainable &middot; 18k users</div></div><div class="fv">$16.9M</div></div>
                    </div>
                    <div style="display:flex;flex-direction:column;gap:clamp(.7rem,1.4vh,1rem)">
                        <div class="card glass reveal" data-delay="3"><h3>The specialist upside</h3><p>30,000+ specialists generate higher revenue per consult and are underserved by GP-focused tools.</p></div>
                        <div class="card glass reveal" data-delay="4"><h3>Usage revenue layer</h3><p>A $30 base removes friction; usage top-ups drive blended ARPU to ~$76 as adoption scales.</p></div>
                    </div>
                </div>
            </div>
        </section>
'''

TRACTION = '''        <!-- Traction -->
        <section class="slide" id="s-traction" data-sec="Traction">
            <div class="inner">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg> Traction &amp; Validation</div>
                    <h2 class="title reveal" data-delay="1">Proven in Production, Giving Clinicians Their Time Back</h2>
                </div>
                <div class="cards" style="grid-template-columns:0.92fr 1.08fr;gap:clamp(1.2rem,3vw,2.2rem);align-items:stretch">
                    <div style="display:flex;flex-direction:column;gap:clamp(.7rem,1.5vh,1.1rem)">
                        <div class="tr-live reveal" data-delay="2"><div class="ic" style="background:rgba(255,255,255,.18)"><svg viewBox="0 0 24 24"><path d="M3 21h18"/><path d="M5 21V7l8-4v18"/><path d="M19 21V11l-6-4"/></svg></div><div><strong>Live &middot; Sydney Gut Clinic</strong><p style="font-size:.85rem;color:rgba(255,255,255,.85);margin-top:.3rem;line-height:1.5">In production daily, validated by specialists in complex gastroenterology. The clinic owned by co-founder Dr Suhirdan.</p><span class="badge2">Production ready</span></div></div>
                        <div class="card glass reveal" data-delay="3" style="display:flex;flex-direction:column;gap:.55rem">
                            <div style="display:flex;align-items:baseline;gap:.65rem"><div style="font-size:clamp(2.2rem,4.2vw,3.1rem);font-weight:800;line-height:1;background:linear-gradient(118deg,var(--primary),var(--accent));-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent">80%</div><div style="font-size:clamp(.92rem,1.2vw,1.12rem);font-weight:700;color:var(--primary-dark)">less time on documentation</div></div>
                            <p style="font-size:.84rem;color:var(--muted);line-height:1.45">Dr Suhirdan: Arvi now does in about <b style="color:var(--primary-dark)">a fifth of the time</b> what his documentation used to take.</p>
                            <ul style="list-style:none;display:flex;flex-direction:column;gap:.5rem;margin-top:.2rem">
                                <li style="display:flex;gap:.55rem;align-items:flex-start;font-size:.84rem;color:#475569;line-height:1.4"><svg viewBox="0 0 24 24" style="width:17px;height:17px;stroke:var(--primary);stroke-width:2;fill:none;flex-shrink:0;margin-top:.12rem"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg><span><b style="color:var(--primary-dark)">Time back:</b> ~80% of admin time returned to patient care.</span></li>
                                <li style="display:flex;gap:.55rem;align-items:flex-start;font-size:.84rem;color:#475569;line-height:1.4"><svg viewBox="0 0 24 24" style="width:17px;height:17px;stroke:var(--primary);stroke-width:2;fill:none;flex-shrink:0;margin-top:.12rem"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg><span><b style="color:var(--primary-dark)">Cost saved:</b> scribe-level output without the $35-50k/yr scribe.</span></li>
                                <li style="display:flex;gap:.55rem;align-items:flex-start;font-size:.84rem;color:#475569;line-height:1.4"><svg viewBox="0 0 24 24" style="width:17px;height:17px;stroke:var(--primary);stroke-width:2;fill:none;flex-shrink:0;margin-top:.12rem"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg><span><b style="color:var(--primary-dark)">Revenue unlocked:</b> reclaimed hours become capacity for more consults &amp; billings.</span></li>
                            </ul>
                        </div>
                    </div>
                    <figure class="clip reveal" data-delay="3" style="align-self:center;min-width:0;width:100%">
                        <div class="card glass" style="width:100%;padding:clamp(1.1rem,1.8vw,1.6rem)">
                            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:clamp(.8rem,1.6vh,1.1rem)"><div style="font-size:clamp(.92rem,1.2vw,1.1rem);font-weight:700;color:var(--primary-dark)">Live usage &middot; Sydney Gut Clinic</div><span style="font-size:.6rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#16a34a;display:inline-flex;align-items:center;gap:.35rem"><span style="width:7px;height:7px;border-radius:50%;background:#16a34a"></span>Live</span></div>
                            <div style="display:flex;gap:clamp(1rem,2.6vw,2.2rem);flex-wrap:wrap;margin-bottom:clamp(.9rem,1.8vh,1.2rem)">
                                <div><div style="font-size:clamp(1.6rem,2.8vw,2.3rem);font-weight:800;line-height:1;background:linear-gradient(118deg,var(--primary),var(--accent));-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent">4,600+</div><div style="font-size:.74rem;color:var(--muted);margin-top:.3rem">clinical letters generated</div></div>
                                <div><div style="font-size:clamp(1.6rem,2.8vw,2.3rem);font-weight:800;line-height:1;background:linear-gradient(118deg,var(--primary),var(--accent));-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent">98%</div><div style="font-size:.74rem;color:var(--muted);margin-top:.3rem">approved, last 30 days*</div></div>
                                <div><div style="font-size:clamp(1.6rem,2.8vw,2.3rem);font-weight:800;line-height:1;background:linear-gradient(118deg,var(--primary),var(--accent));-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent">9</div><div style="font-size:.74rem;color:var(--muted);margin-top:.3rem">letter types in daily use</div></div>
                            </div>
                            <div style="font-size:.68rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-bottom:.6rem">Letters by type</div>
                            <div style="display:flex;flex-direction:column;gap:.5rem">
                                <div style="display:flex;align-items:center;gap:.6rem"><div style="font-size:.76rem;color:#475569;width:46%;flex-shrink:0">Dictation</div><div style="flex:1;height:7px;border-radius:4px;background:rgba(4,55,98,.08)"><div style="width:27%;height:100%;border-radius:4px;background:linear-gradient(90deg,var(--primary),var(--accent))"></div></div><div style="font-size:.72rem;color:var(--primary-dark);font-weight:700;width:32px;text-align:right">27%</div></div>
                                <div style="display:flex;align-items:center;gap:.6rem"><div style="font-size:.76rem;color:#475569;width:46%;flex-shrink:0">Follow-up</div><div style="flex:1;height:7px;border-radius:4px;background:rgba(4,55,98,.08)"><div style="width:22%;height:100%;border-radius:4px;background:linear-gradient(90deg,var(--primary),var(--accent))"></div></div><div style="font-size:.72rem;color:var(--primary-dark);font-weight:700;width:32px;text-align:right">22%</div></div>
                                <div style="display:flex;align-items:center;gap:.6rem"><div style="font-size:.76rem;color:#475569;width:46%;flex-shrink:0">Procedure report</div><div style="flex:1;height:7px;border-radius:4px;background:rgba(4,55,98,.08)"><div style="width:17%;height:100%;border-radius:4px;background:linear-gradient(90deg,var(--primary),var(--accent))"></div></div><div style="font-size:.72rem;color:var(--primary-dark);font-weight:700;width:32px;text-align:right">17%</div></div>
                                <div style="display:flex;align-items:center;gap:.6rem"><div style="font-size:.76rem;color:#475569;width:46%;flex-shrink:0">Initial consultation</div><div style="flex:1;height:7px;border-radius:4px;background:rgba(4,55,98,.08)"><div style="width:15%;height:100%;border-radius:4px;background:linear-gradient(90deg,var(--primary),var(--accent))"></div></div><div style="font-size:.72rem;color:var(--primary-dark);font-weight:700;width:32px;text-align:right">15%</div></div>
                                <div style="display:flex;align-items:center;gap:.6rem"><div style="font-size:.76rem;color:#475569;width:46%;flex-shrink:0">Consultation report</div><div style="flex:1;height:7px;border-radius:4px;background:rgba(4,55,98,.08)"><div style="width:11%;height:100%;border-radius:4px;background:linear-gradient(90deg,var(--primary),var(--accent))"></div></div><div style="font-size:.72rem;color:var(--primary-dark);font-weight:700;width:32px;text-align:right">11%</div></div>
                                <div style="display:flex;align-items:center;gap:.6rem"><div style="font-size:.76rem;color:#475569;width:46%;flex-shrink:0">Specialist-to-GP</div><div style="flex:1;height:7px;border-radius:4px;background:rgba(4,55,98,.08)"><div style="width:6%;height:100%;border-radius:4px;background:linear-gradient(90deg,var(--primary),var(--accent))"></div></div><div style="font-size:.72rem;color:var(--primary-dark);font-weight:700;width:32px;text-align:right">6%</div></div>
                            </div>
                            <p style="font-size:.66rem;color:#94a3b8;margin-top:.8rem">*Recent letters, excluding initial test &amp; draft data.</p>
                        </div>
                        <figcaption><b>Real production usage</b> across the practice, straight from the live Arvi dashboard.</figcaption>
                    </figure>
                </div>
            </div>
        </section>
'''

TEAM = '''        <!-- Team -->
        <section class="slide" id="s-team" data-sec="Team">
            <div class="inner">
                <div class="slide-head" style="text-align:center">
                    <div class="label reveal" style="justify-content:center"><svg viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg> The Team</div>
                    <h2 class="title reveal" data-delay="1">Clinical Authority Meets Proven SaaS Scaling</h2>
                </div>
                <div class="team">
                    <div class="tcard glass reveal" data-delay="2"><img src="ari%20latest%20photo.png" alt="Ari Vivekanandarajah" style="object-position:center 22%"><h3>Ari Vivekanandarajah</h3><div class="trole">Co-Founder</div><div class="tchips"><span>Successful SaaS exit</span><span>Agency owner</span></div><ul><li><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>20+ years in B2B &amp; SaaS marketing and growth</li><li><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>Specialist in healthcare &amp; SaaS go-to-market</li><li><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>Leads strategy, sales and operations</li></ul></div>
                    <div class="tcard glass reveal" data-delay="3"><img src="dr%20suhirdan.jpg" alt="Dr Suhirdan Vivekanandarajah"><h3>Dr Suhirdan Vivekanandarajah</h3><div class="trole">Co-Founder</div><div class="tchips"><span>Gastroenterologist</span><span>Clinic owner</span></div><ul><li><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>Practising gastroenterologist &amp; clinic owner</li><li><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>Deep clinical workflow validation</li><li><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>Leads product vision &amp; medical partnerships</li></ul></div>
                </div>
                <div class="dl reveal" data-delay="4" style="margin-top:clamp(1rem,2.4vh,1.6rem)">
                    <a class="dlcard glass" href="https://apps.apple.com/au/app/arvi-health/id6761469752" target="_blank" rel="noopener"><img src="qr-ios.png" alt="Download Arvi on the App Store"><div><div class="dt">Scan to try Arvi</div><div class="dn">Arvi for iOS</div><div class="ds">App Store</div></div></a>
                    <a class="dlcard glass" href="https://play.google.com/store/apps/details?id=com.healthai.mobile" target="_blank" rel="noopener"><img src="qr-android.png" alt="Download Arvi on Google Play"><div><div class="dt">Scan to try Arvi</div><div class="dn">Arvi for Android</div><div class="ds">Google Play</div></div></a>
                </div>
            </div>
        </section>
'''

SECURITY = '''        <!-- Security & interoperability -->
        <section class="slide" id="s-security" data-sec="Trust">
            <div class="inner fill">
                <div class="slide-head">
                    <div class="label imx reveal"><svg viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg> Security &amp; Interoperability</div>
                    <h2 class="title reveal" data-delay="1">Built to Sit Inside a Hospital's Stack</h2>
                    <p class="subtitle reveal" data-delay="2">The questions a CTO and CMO ask first, answered up front.</p>
                </div>
                <div class="cards c3">
                    <div class="card glass reveal" data-delay="2"><div class="vic"><svg viewBox="0 0 24 24"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg></div><h3>Australian data residency</h3><p>Patient data handled under Australian privacy compliance, certified.</p></div>
                    <div class="card glass reveal" data-delay="3"><div class="vic"><svg viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></div><h3>Encrypted &amp; access-controlled</h3><p>Role-based permissions and organisation-level isolation across the platform.</p></div>
                    <div class="card glass reveal" data-delay="4"><div class="vic"><svg viewBox="0 0 24 24"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg></div><h3>HL7 / FHIR-ready</h3><p>Designed to exchange structured documents over standard interfaces.</p></div>
                    <div class="card glass reveal" data-delay="3"><div class="vic"><svg viewBox="0 0 24 24"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><polyline points="17 11 19 13 23 9"/></svg></div><h3>Clinician in the loop</h3><p>AI drafts; the clinician reviews and approves every note and letter.</p></div>
                    <div class="card glass reveal" data-delay="4"><div class="vic"><svg viewBox="0 0 24 24"><path d="M4.8 2.3A.3.3 0 1 0 5 2H4a2 2 0 0 0-2 2v5a6 6 0 0 0 6 6v0a6 6 0 0 0 6-6V4a2 2 0 0 0-2-2h-1a.2.2 0 1 0 .3.3"/><path d="M8 15v1a6 6 0 0 0 6 6v0a6 6 0 0 0 6-6v-4"/><circle cx="20" cy="10" r="2"/></svg></div><h3>Specialist-validated</h3><p>Accuracy proven daily in a live specialist practice, not just GP visits.</p></div>
                    <div class="card glass reveal" data-delay="5"><div class="vic"><svg viewBox="0 0 24 24"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg></div><h3>Complements, not replaces</h3><p>Arvi feeds your system of record, it does not try to be it.</p></div>
                </div>
            </div>
        </section>
'''

FINANCIALS = '''        <!-- Financials -->
        <section class="slide" id="s-fin" data-sec="The Raise">
            <div class="inner">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg> Financial Projections</div>
                    <h2 class="title reveal" data-delay="1">Path to $12.8M ARR</h2>
                </div>
                <div class="fin">
                    <div class="card glass reveal" data-delay="2">
                        <h3 style="text-align:center;color:var(--muted);font-weight:600;font-size:.9rem">Projected ARR</h3>
                        <div class="bars">
                            <div class="bar"><div class="bv">$2.3M</div><div class="bcol" data-h="34%"></div><div class="bl">Year 1</div></div>
                            <div class="bar"><div class="bv">$5.5M</div><div class="bcol" data-h="62%"></div><div class="bl">Year 2</div></div>
                            <div class="bar"><div class="bv">$12.8M</div><div class="bcol" data-h="100%"></div><div class="bl">Year 3</div></div>
                        </div>
                    </div>
                    <div class="fin-cards">
                        <div class="fin-card glass reveal" data-delay="3"><div class="fcl">Blended ARPU</div><div class="fcv">~$76</div><div class="fcs">$30 base + $46 usage</div></div>
                        <div class="fin-card glass reveal" data-delay="4"><div class="fcl">LTV : CAC target</div><div class="fcv">5.1 : 1</div><div class="fcs">Efficient growth</div></div>
                        <div class="fin-card glass reveal" data-delay="5"><div class="fcl">Series A</div><div class="fcv">Q1 Year 2</div><div class="fcs">at $5M+ ARR</div></div>
                    </div>
                </div>
            </div>
        </section>
'''

ASK = '''        <!-- Ask -->
        <section class="slide" id="s-ask" data-sec="The Raise">
            <div class="inner">
                <div class="slide-head" style="text-align:center">
                    <div class="label reveal" style="justify-content:center"><svg viewBox="0 0 24 24"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg> The Ask</div>
                    <h2 class="title reveal" data-delay="1" style="text-align:center">Seed Round</h2>
                </div>
                <div style="text-align:center">
                    <div class="ask-amt reveal" data-delay="2">$2M</div>
                    <div class="ask-eq reveal" data-delay="2">for 10% equity</div>
                </div>
                <div style="max-width:780px;margin:clamp(1rem,2.4vh,1.8rem) auto 0">
                    <div class="reveal" data-delay="3" style="font-size:.8rem;font-weight:700;color:var(--primary-dark);margin-bottom:.4rem">Use of funds</div>
                    <div class="fundbar reveal" data-delay="3">
                        <span style="width:50%;background:var(--primary-dark)">S&amp;M 50%</span>
                        <span style="width:25%;background:var(--primary)">Product 25%</span>
                        <span style="width:20%;background:var(--accent)">Ops 20%</span>
                        <span style="width:5%;background:var(--accent-2)">5%</span>
                    </div>
                </div>
                <div class="cards c2" style="max-width:920px;margin:clamp(1rem,2.4vh,1.6rem) auto 0">
                    <div class="card glass reveal" data-delay="4"><h3>2,500+ active users</h3><p>Market leadership across Australia within 12 months.</p></div>
                    <div class="card glass reveal" data-delay="4"><h3>$2.3M ARR run-rate</h3><p>Revenue growth to a Series A-ready position.</p></div>
                    <div class="card glass reveal" data-delay="5"><h3>Enterprise ready</h3><p>Healthlink &amp; enterprise integrations delivered.</p></div>
                    <div class="card glass reveal" data-delay="5"><h3>Series A at $5.5M ARR</h3><p>Positioned for the next round in Year 2.</p></div>
                </div>
            </div>
        </section>
'''

ROADMAP = '''        <!-- Roadmap -->
        <section class="slide" id="s-roadmap" data-sec="Roadmap">
            <div class="inner fill">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg> Growth Roadmap</div>
                    <h2 class="title reveal" data-delay="1">From Specialist Clinics to the Hospital Ecosystem</h2>
                    <p class="subtitle reveal" data-delay="2">Arvi's path runs from individual clinicians today toward enterprise and hospital-wide documentation, where notes, coding and interoperability converge.</p>
                </div>
                <div class="rm-wrap">
                    <div class="rmline reveal" data-delay="2">
                        <div class="rmpt"><span class="d"></span><span class="l">Launch</span><span class="v">Mar 2026</span></div>
                        <div class="rmpt"><span class="d"></span><span class="l">100 practices</span><span class="v">Month 6</span></div>
                        <div class="rmpt"><span class="d"></span><span class="l">500 practices</span><span class="v">Month 12</span></div>
                        <div class="rmpt"><span class="d"></span><span class="l">$12.8M ARR</span><span class="v">Year 3</span></div>
                    </div>
                    <div class="rm">
                        <div class="rmcard lite reveal" data-delay="3">
                            <div class="ph"><div class="pn">1</div><div class="pt">Months 1-6</div><span class="rm-live"><span class="dot"></span>Live</span></div>
                            <h3>Launch &amp; Adoption</h3>
                            <ul><li>Sydney Gut Clinic as reference site</li><li>Metro GP &amp; specialist practices</li><li>Direct sales + 30-day free trial</li></ul>
                            <div class="tgt"><b>100</b><span>practices</span></div>
                        </div>
                        <div class="rmcard lite reveal" data-delay="4">
                            <div class="ph"><div class="pn">2</div><div class="pt">Months 7-12</div></div>
                            <h3>Market Expansion</h3>
                            <ul><li>National rollout across capital cities</li><li>Healthlink &amp; practice-system integrations</li><li>Specialist vertical expansion</li></ul>
                            <div class="tgt"><b>500</b><span>practices</span></div>
                        </div>
                        <div class="rmcard climax reveal" data-delay="5">
                            <span class="flag"><svg viewBox="0 0 24 24"><path d="M12 2l2.4 7.4H22l-6 4.6 2.3 7.4L12 17l-6.3 4.4L8 14 2 9.4h7.6z"/></svg>Where it converges</span>
                            <div class="ph"><div class="pn">3</div><div class="pt">Year 2+</div></div>
                            <h3>Enterprise &amp; Hospital</h3>
                            <ul><li>Hospital network pilots</li><li>Discharge summaries &amp; coding support</li><li>Deep EMR / system integrations</li><li>Enterprise-wide licensing</li></ul>
                            <div class="tgt"><b>$12.8M</b><span>ARR</span></div>
                        </div>
                    </div>
                    <p class="rm-cap reveal" data-delay="6">Phase 3 is where ambient documentation meets the systems that run hospitals, <b>discharge, coding and the patient record</b>.</p>
                </div>
            </div>
        </section>
'''

IMX_INTEG_ALT = '''        <!-- Integration (our-path framing) -->
        <section class="slide" id="s-imx2b" data-sec="InfoMedix">
            <div class="inner">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg> Our Path</div>
                    <h2 class="title reveal" data-delay="1">An Interoperable Documentation Layer</h2>
                    <p class="subtitle reveal" data-delay="2">Arvi is built to hand structured notes, letters and summaries to whatever records, workflow and coding systems sit downstream, over HL7 / FHIR. Where that lines up with your roadmap, there is a natural fit, and we would shape it together.</p>
                </div>
                <div class="integ">
                    <div class="integ-arvi reveal" data-delay="2">
                        <div class="il">Capture &amp; authoring</div>
                        <h3>Arvi</h3>
                        <p>Voice &rarr; structured note, letter &amp; referral</p>
                        <ul>
                            <li><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> Clinical notes</li>
                            <li><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> GP &amp; referral letters</li>
                            <li><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> Theatre &amp; discharge notes</li>
                        </ul>
                    </div>
                    <div class="pipe reveal" data-delay="3">
                        <div class="pl">HL7 / FHIR<br>secure messaging</div>
                        <svg viewBox="0 0 24 24"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
                        <div class="pl sub">structured documents</div>
                    </div>
                    <div class="imx-prods">
                        <div class="imx-prod glass reveal" data-delay="3"><h4>The patient record</h4><p>Complete, on-time notes filed where they belong.</p></div>
                        <div class="imx-prod glass reveal" data-delay="4"><h4>Referral workflows</h4><p>Auto-generated letters into the referral pipeline.</p></div>
                        <div class="imx-prod glass reveal" data-delay="4"><h4>Discharge</h4><p>Summaries authored from the recording, ready to file.</p></div>
                        <div class="imx-prod glass reveal" data-delay="5"><h4>Coding</h4><p>Richer source notes lift coding accuracy &amp; speed.</p></div>
                        <div class="imx-prod glass span reveal" data-delay="5"><h4>Clinician collaboration</h4><p>Notes &amp; letters shared across the care team.</p></div>
                    </div>
                </div>
                <p class="rm-cap reveal" data-delay="6" style="margin-top:clamp(.7rem,1.6vh,1.1rem)">This is our path. If you are thinking differently, we are happy to adapt.</p>
            </div>
        </section>
'''

PRODUCT_ROADMAP = '''        <!-- Product roadmap -->
        <section class="slide" id="s-proadmap" data-sec="Roadmap">
            <div class="inner fill">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg> Product Roadmap</div>
                    <h2 class="title reveal" data-delay="1">What We're Building Next</h2>
                    <p class="subtitle reveal" data-delay="2">Beyond today's twenty production features, the capabilities on Arvi's near and long-term horizon.</p>
                </div>
                <div class="rm-wrap">
                    <div class="rm">
                        <div class="rmcard lite reveal" data-delay="3">
                            <div class="ph"><div class="pn"><svg viewBox="0 0 24 24"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg></div><div class="pt">Now &rarr; 6 months</div></div>
                            <h3>Connected &amp; live</h3>
                            <ul><li>Inbound pathology &amp; results ingestion</li><li>Deeper patient-management system integrations</li><li>Real-time transcription &amp; live note preview</li><li>ISO 27001 / SOC 2 certification</li></ul>
                        </div>
                        <div class="rmcard lite reveal" data-delay="4">
                            <div class="ph"><div class="pn"><svg viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="14" x2="23" y2="14"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="14" x2="4" y2="14"/></svg></div><div class="pt">6 &rarr; 18 months</div></div>
                            <h3>Hospital-grade intelligence</h3>
                            <ul><li>Hospital EMR integration over HL7 / FHIR</li><li>Coding-ready structured output (SNOMED / ICD-aligned)</li><li>Evidence: guideline-backed answers at the point of care</li><li>Specialty-tuned models across disciplines</li><li>Organisation analytics &amp; insights</li></ul>
                        </div>
                        <div class="rmcard climax reveal" data-delay="5">
                            <span class="flag"><svg viewBox="0 0 24 24"><path d="M12 2l2.4 7.4H22l-6 4.6 2.3 7.4L12 17l-6.3 4.4L8 14 2 9.4h7.6z"/></svg>On the horizon</span>
                            <div class="ph"><div class="pn"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="6"/><polyline points="12 10 12 12 13 13"/><path d="M16.5 17.4l-.34 3.8a2 2 0 0 1-2 1.8H9.84a2 2 0 0 1-2-1.8l-.34-3.8m0-10.8l.34-3.8A2 2 0 0 1 9.84 1h4.32a2 2 0 0 1 2 1.8l.34 3.8"/></svg></div><div class="pt">The horizon</div></div>
                            <h3>Agentic &amp; autonomous</h3>
                            <ul><li>Ambient, continuous listening across the practice</li><li>Autonomous care coordination: book, refer, request, draft, you approve</li><li>Practice brain: reason over years of conversations, not just notes</li><li>Predictive patient insights (risk &amp; adherence)</li><li>Hardware beyond the phone: Arvi Badge &amp; Room</li></ul>
                        </div>
                    </div>
                    <p class="rm-cap reveal" data-delay="6">The long-term moat is not transcription. It is a longitudinal memory across every conversation, referral and result that agents can act on, an autonomous healthcare operating system.</p>
                </div>
            </div>
        </section>
'''

# Main narrative first; the 19 feature demos live in an Appendix at the end.
CALCULATOR = '''        <!-- Interactive ROI calculator (SGC-based) -->
        <section class="slide" id="s-calc" data-sec="ROI">
            <div class="inner">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><rect x="4" y="2" width="16" height="20" rx="2"/><line x1="8" y1="6" x2="16" y2="6"/><line x1="8" y1="10" x2="10" y2="10"/><line x1="12" y1="10" x2="14" y2="10"/><line x1="8" y1="14" x2="10" y2="14"/><line x1="12" y1="14" x2="14" y2="14"/><line x1="8" y1="18" x2="10" y2="18"/></svg> ROI Calculator</div>
                    <h2 class="title reveal" data-delay="1">What Arvi Gives a Practice Back</h2>
                    <p class="subtitle reveal" data-delay="2">Modelled on Sydney Gut Clinic's real usage. Drag the inputs to fit any practice.</p>
                </div>
                <div class="calc">
                    <div class="calc-inputs glass reveal" data-delay="2">
                        <div class="calc-field"><label>Clinicians <span id="ci-clin-v">6</span></label><input type="range" id="ci-clin" min="1" max="100" value="6"></div>
                        <div class="calc-field"><label>Documentation hrs / clinician / week <span id="ci-hrs-v">10</span></label><input type="range" id="ci-hrs" min="2" max="30" value="10"></div>
                        <div class="calc-field"><label>Value of a clinician hour <span id="ci-rate-v">$200</span></label><input type="range" id="ci-rate" min="50" max="600" step="10" value="200"></div>
                        <p class="calc-note">Default = Sydney Gut Clinic (6 clinicians). Arvi cuts documentation time by ~80%, so a fifth of the time gets the same job done.</p>
                    </div>
                    <div class="calc-outputs">
                        <div class="calc-out glass reveal" data-delay="3"><div class="co-v" id="co-hours">0</div><div class="co-l">clinician-hours saved / year</div></div>
                        <div class="calc-out glass reveal" data-delay="3"><div class="co-v" id="co-value">0</div><div class="co-l">value of time returned / year</div></div>
                        <div class="calc-out glass reveal" data-delay="4"><div class="co-v" id="co-week">0</div><div class="co-l">hours back per clinician / week</div></div>
                        <div class="calc-out glass reveal" data-delay="4"><div class="co-v">5&times;</div><div class="co-l">faster documentation</div></div>
                    </div>
                </div>
                <p class="rm-cap reveal" data-delay="5">Illustrative. The ~80% saving is drawn from live SGC use; cost &amp; revenue scale with every clinician added.</p>
            </div>
        </section>
'''

VISION = '''        <!-- Vision (today -> tomorrow) -->
        <section class="slide" id="s-vision" data-sec="Vision">
            <div class="inner">
                <div class="slide-head" style="text-align:center">
                    <div class="label reveal" style="justify-content:center"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg> Our Vision</div>
                    <h2 class="title reveal" data-delay="1">From the Documentation Crisis to the Autonomous Clinic</h2>
                    <p class="subtitle reveal" data-delay="2" style="margin-left:auto;margin-right:auto;text-align:center">Solve clinicians' biggest daily burden now, and build the intelligence to run the practice itself.</p>
                </div>
                <div class="vis">
                    <div class="vis-card now reveal" data-delay="2">
                        <div class="vis-tag">Today</div>
                        <h3>Free clinicians from the paperwork</h3>
                        <p>Clinicians lose up to half their day to notes, letters and admin. Arvi captures every consultation, in any setting, and hands the time straight back, with a clean, structured record every time.</p>
                        <span class="vis-pill">The problem, solved</span>
                    </div>
                    <div class="vis-arrow reveal" data-delay="3"><svg viewBox="0 0 24 24"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></div>
                    <div class="vis-card future reveal" data-delay="3">
                        <div class="vis-tag">Where we're heading</div>
                        <h3>An autonomous clinical operating system</h3>
                        <p>Arvi listens across the whole practice, remembers every conversation and result, and acts on it: booking, referring, coding-ready, coordinating care. The clinician approves; the clinic increasingly runs itself.</p>
                        <span class="vis-pill">Listen &middot; Reason &middot; Act</span>
                    </div>
                </div>
            </div>
        </section>
'''

APPENDIX = '''        <!-- Appendix divider -->
        <section class="slide" id="s-appendix" data-sec="Appendix">
            <div class="inner">
                <div class="divider">
                    <div class="label reveal" style="justify-content:center"><svg viewBox="0 0 24 24"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg> Appendix</div>
                    <div class="big reveal" data-delay="1">Feature Walkthrough</div>
                    <p class="subtitle reveal" data-delay="2" style="text-align:center;max-width:720px;margin:0 auto">Recorded demos of all twenty features, across the five areas, for reference. Jump to any feature on request.</p>
                    <div class="menu reveal" data-delay="3">
                        <span class="mi"><b>01</b> Core Documentation</span>
                        <span class="mi"><b>02</b> Letters &amp; Templates</span>
                        <span class="mi"><b>03</b> Patient &amp; Workflow</span>
                        <span class="mi"><b>04</b> Organisation &amp; Users</span>
                        <span class="mi"><b>05</b> Billing</span>
                    </div>
                </div>
            </div>
        </section>
'''

UNITECON = '''        <!-- Unit economics -->
        <section class="slide" id="s-unit" data-sec="The Raise">
            <div class="inner">
                <div class="slide-head">
                    <div class="label reveal"><svg viewBox="0 0 24 24"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg> Unit Economics</div>
                    <h2 class="title reveal" data-delay="1">The $30 Model, and Why It Profits</h2>
                    <p class="subtitle reveal" data-delay="2">A low entry point wins adoption. Margin comes from the base plan, then stacks with usage.</p>
                </div>
                <div class="econ">
                    <div class="econ-step glass reveal" data-delay="2"><div class="ev">$30</div><div class="el">per user / month</div><div class="ed">Low entry point, easy for any clinician to adopt.</div></div>
                    <div class="econ-arrow reveal" data-delay="3"><svg viewBox="0 0 24 24"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></div>
                    <div class="econ-step glass reveal" data-delay="3"><div class="ev">$10</div><div class="el">gross margin kept</div><div class="econ-bar"><div class="cost" style="width:67%"></div><div class="marg" style="width:33%"></div></div><div class="ed">About a third of the base plan, before any token use.</div></div>
                    <div class="econ-arrow reveal" data-delay="4"><svg viewBox="0 0 24 24"><line x1="12" y1="5" x2="12" y2="19"/><polyline points="5 12 12 5 19 12"/></svg></div>
                    <div class="econ-step glass reveal" data-delay="4"><div class="ev">+ tokens</div><div class="el">premium on usage</div><div class="ed">Heavy users buy tokens for extra usage, premium margin stacked on top.</div></div>
                </div>
                <div class="econ-foot">
                    <div class="ef glass reveal" data-delay="5"><span class="efv">~$76 / user / mo</span> blended revenue, base plus usage, lifting margin well above the $10 base.</div>
                    <div class="ef glass reveal" data-delay="5"><span class="efv">$120k / yr</span> base margin for every 1,000 users, before token revenue, and it compounds as the base grows.</div>
                </div>
            </div>
        </section>
'''

BODY = (INTRO + TEAM + AGENDA + PROBLEM + VISION + WALK
        + PLATFORM + TRACTION + CALCULATOR + COMPETITIVE + MARKET + SECURITY
        + IMX_WORLD + IMX_INTEG_ALT + IMX_VALUE + PRODUCT_ROADMAP + ROADMAP + UNITECON + FINANCIALS + ASK + CLOSE
        + APPENDIX + FEAT)

SCRIPT = r"""
        (function(){
            var deck=document.getElementById('deck');
            var slides=[].slice.call(document.querySelectorAll('.slide'));
            var dotsWrap=document.getElementById('dots');
            var cur=document.getElementById('cur');
            var secEl=document.getElementById('sec');
            var prog=document.getElementById('prog');
            document.getElementById('total').textContent=slides.length;

            slides.forEach(function(s,i){
                var b=document.createElement('button');
                b.className='dot'+(i===0?' active':'');
                b.setAttribute('aria-label','Go to slide '+(i+1));
                b.addEventListener('click',function(){s.scrollIntoView({behavior:'smooth',inline:'start'});});
                dotsWrap.appendChild(b);
            });
            var dots=[].slice.call(dotsWrap.children);

            var io=new IntersectionObserver(function(entries){
                entries.forEach(function(e){
                    var i=slides.indexOf(e.target);
                    var vids=e.target.querySelectorAll('video');
                    if(e.isIntersecting){
                        e.target.querySelectorAll('.bcol').forEach(function(b){b.style.height=b.dataset.h;});
                    }
                    if(e.isIntersecting&&e.intersectionRatio>=0.55){
                        e.target.classList.add('active');
                        dots.forEach(function(d,k){d.classList.toggle('active',k===i);});
                        cur.textContent=i+1;
                        if(secEl)secEl.textContent=e.target.dataset.sec||'';
                        [].forEach.call(vids,function(v){try{var p=v.play();if(p)p.catch(function(){});}catch(_){}});
                    }else if(!e.isIntersecting){
                        [].forEach.call(vids,function(v){try{v.pause();}catch(_){}});
                        e.target.querySelectorAll('.bcol').forEach(function(b){b.style.height='0';});
                    }
                });
            },{root:deck,threshold:[0,0.55,1]});
            slides.forEach(function(s){io.observe(s);});

            document.querySelectorAll('.slide:not(#s-intro) video').forEach(function(v){try{v.pause();}catch(_){}});

            // Deterministic playback: always play the slide currently in view, pause the rest.
            function syncVideos(){
                var idx=Math.round(deck.scrollLeft/innerWidth);
                slides.forEach(function(s,k){
                    var vs=s.querySelectorAll('video');
                    [].forEach.call(vs,function(v){
                        if(k===idx){ if(v.paused){ var p=v.play(); if(p)p.catch(function(){}); } }
                        else if(!v.paused){ try{v.pause();}catch(_){} }
                    });
                });
            }
            var vsync;
            deck.addEventListener('scroll',function(){clearTimeout(vsync);vsync=setTimeout(syncVideos,120);});
            window.addEventListener('load',syncVideos);
            syncVideos();

            function updateProgress(){
                var max=deck.scrollWidth-deck.clientWidth;
                var p=max>0?deck.scrollLeft/max:0;
                prog.style.setProperty('--p',p.toFixed(4));
            }
            var ticking=false;
            deck.addEventListener('scroll',function(){if(!ticking){ticking=true;requestAnimationFrame(function(){updateProgress();ticking=false;});}});
            updateProgress();

            addEventListener('keydown',function(ev){
                var i=Math.round(deck.scrollLeft/innerWidth);
                if(ev.key==='ArrowRight'||ev.key==='PageDown'||ev.key===' '){ev.preventDefault();if(i<slides.length-1)slides[i+1].scrollIntoView({behavior:'smooth',inline:'start'});}
                else if(ev.key==='ArrowLeft'||ev.key==='PageUp'){ev.preventDefault();if(i>0)slides[i-1].scrollIntoView({behavior:'smooth',inline:'start'});}
                else if(ev.key==='Home'){ev.preventDefault();slides[0].scrollIntoView({behavior:'smooth',inline:'start'});}
                else if(ev.key==='End'){ev.preventDefault();slides[slides.length-1].scrollIntoView({behavior:'smooth',inline:'start'});}
            });
            slides[0].classList.add('active');

            // Interactive ROI calculator (SGC-based)
            (function(){
                var clin=document.getElementById('ci-clin'), hrs=document.getElementById('ci-hrs'), rate=document.getElementById('ci-rate');
                if(!clin) return;
                var WEEKS=46, SAVE=0.8, FTE=1800;
                function money(n){ if(n>=1e6) return '$'+(n/1e6).toFixed(1)+'M'; if(n>=1e3) return '$'+Math.round(n/1e3)+'k'; return '$'+Math.round(n); }
                function calc(){
                    var c=+clin.value, h=+hrs.value, r=+rate.value;
                    document.getElementById('ci-clin-v').textContent=c;
                    document.getElementById('ci-hrs-v').textContent=h;
                    document.getElementById('ci-rate-v').textContent='$'+r;
                    var hoursYear=Math.round(c*h*SAVE*WEEKS);
                    document.getElementById('co-hours').textContent=hoursYear.toLocaleString('en-AU');
                    document.getElementById('co-value').textContent=money(hoursYear*r);
                    document.getElementById('co-week').textContent=Math.round(h*SAVE);
                }
                [clin,hrs,rate].forEach(function(el){ el.addEventListener('input',calc); });
                calc();
            })();

            // Deep-link: jump to #slide-id on load (e.g. .../arvi-features.html#s-roadmap)
            if(location.hash){
                var target=document.getElementById(location.hash.slice(1));
                if(target){ target.scrollIntoView({inline:'start'}); setTimeout(function(){target.scrollIntoView({inline:'start'});syncVideos();},250); }
            }
        })();
"""

HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Arvi Health &middot; Feature &amp; Integration Overview</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>''' + CSS + '''    </style>
</head>
<body>
    <div class="progress" id="prog"><span></span></div>
    <nav class="nav">
        <a href="https://arvihealth.com" target="_blank" rel="noopener" class="logo"><img src="arvi logo.avif" alt="Arvi Health"></a>
        <div class="dots" id="dots"></div>
        <div class="nav-tag">Prepared for <b>InfoMedix</b></div>
    </nav>

    <main class="deck" id="deck">
''' + BODY + '''    </main>

    <div class="counter"><span><b id="cur">1</b> / <span id="total">0</span></span><span class="sec" id="sec">Overview</span></div>

    <script>''' + SCRIPT + '''</script>
</body>
</html>
'''

with io.open('arvi-features.html','w',encoding='utf-8') as f:
    f.write(HTML)
# count slides
print("slides:", HTML.count('<section class="slide"'))
print("videos:", HTML.count('<video'))
print("WROTE arvi-features.html")
