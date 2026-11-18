# -*- coding: utf-8 -*-
import os, json, html, urllib.parse, sys
sys.path.insert(0, os.path.dirname(__file__))
from textos import ES, EN, PLANS, WHO, ROW_A, ROW_B

OUT = sys.argv[1] if len(sys.argv) > 1 else '/mnt/user-data/outputs/site'
SPOTS = 3
SITE = 'https://overtonelab.com'
WA = '573024451526'
IG = 'https://www.instagram.com/andres.overtone/'
GSC = '<meta name="google-site-verification" content="HlJrtvQfvIT3nS2rB-KH9VZTEIDbUcyKHV5RAdV2ObU">'
MAPS = 'https://www.google.com/maps/place/Overtone+Lab/@6.2664378,-75.7505852,11z/data=!3m1!4b1!4m6!3m5!1s0xfb44d8c8b2bc5c3:0x8e6599276e11b8a0!8m2!3d6.2664635!4d-75.5857785!16s%2Fg%2F11ynym54fd'
TT = 'https://www.tiktok.com/@andres.overtone'

def e(s): return html.escape(s, quote=True)

PATHS = {  # url pública por idioma y página
 'es': {'home': '/', 'book': '/agendar.html', 'thanks': '/gracias.html', 'priv': '/privacidad.html'},
 'en': {'home': '/en/', 'book': '/en/book.html', 'thanks': '/en/thanks.html', 'priv': '/en/privacy.html'},
}
FILES = {  # archivo de salida
 'es': {'home': 'index.html', 'book': 'agendar.html', 'thanks': 'gracias.html', 'priv': 'privacidad.html'},
 'en': {'home': 'en/index.html', 'book': 'en/book.html', 'thanks': 'en/thanks.html', 'priv': 'en/privacy.html'},
}
OTHER = {'es': 'en', 'en': 'es'}

def pre(L): return '' if L == 'es' else '../'
def asset(L, p): return pre(L) + 'assets/embudo/' + p
def img(L, p): return asset(L, 'img/' + p)
def link(L, page):  # enlace relativo dentro del mismo idioma
    return os.path.basename(FILES[L][page])
def alt_link(L, page):  # enlace relativo a la misma página en el otro idioma
    o = OTHER[L]
    return (FILES[o][page] if L == 'es' else '../' + FILES[o][page])

def wa_url(msg=None):
    u = 'https://api.whatsapp.com/send?phone=' + WA
    if msg: u += '&text=' + urllib.parse.quote(msg, safe='')
    return u
WA_INFO = wa_url('Hola! Quiero más información de sus planes mensuales de marketing de contenido')

def head(L, T, page, title, desc, robots=None, extra=''):
    o = OTHER[L]
    can = SITE + PATHS[L][page]
    h = ['<!doctype html>', '<html lang="%s">' % L, '<head>', '<meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width,initial-scale=1">',
         '<title>%s</title>' % e(title),
         '<meta name="description" content="%s">' % e(desc)]
    if robots: h.append('<meta name="robots" content="%s">' % robots)
    else: h.append('<meta name="robots" content="index,follow,max-image-preview:large">')
    h.append('<link rel="canonical" href="%s">' % can)
    if not robots:
        h.append('<link rel="alternate" hreflang="%s" href="%s">' % (L, can))
        h.append('<link rel="alternate" hreflang="%s" href="%s">' % (o, SITE + PATHS[o][page]))
        h.append('<link rel="alternate" hreflang="x-default" href="%s">' % (SITE + PATHS['es'][page]))
    h += ['<meta property="og:type" content="website">', '<meta property="og:title" content="%s">' % e(title),
          '<meta property="og:description" content="%s">' % e(desc), '<meta property="og:url" content="%s">' % can,
          '<meta property="og:locale" content="%s">' % T['ogLocale'], '<meta property="og:site_name" content="Overtone Lab">',
          '<meta property="og:image" content="%s/assets/embudo/img/og.png">' % SITE,
          '<meta property="og:image:alt" content="Overtone Lab">',
          '<meta name="twitter:card" content="summary_large_image">',
          '<meta name="theme-color" content="#2A2659">',
          '<link rel="icon" href="/favicon.ico" sizes="any">',
          '<link rel="icon" type="image/png" sizes="32x32" href="%s">' % img(L, 'favicon-32.png'),
          '<link rel="apple-touch-icon" href="%s">' % img(L, 'apple-touch-icon.png'),
          '<link rel="preconnect" href="https://fonts.googleapis.com">',
          '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
          '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">',
          '<link rel="stylesheet" href="%s">' % asset(L, 'embudo.css'), extra, '</head>', '<body>']
    return '\n'.join(h)

def header(L, T, page):
    o = OTHER[L]
    on, off = 'on', 'off'
    es_cls, en_cls = (on, off) if L == 'es' else (off, on)
    es_href = '#' if L == 'es' else alt_link(L, page)
    en_href = '#' if L == 'en' else alt_link(L, page)
    return '''<header style="background:#2A2659;color:#fff">
<div class="wrap" style="display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;padding-top:14px;padding-bottom:14px">
<a href="%s" aria-label="Overtone Lab" style="display:flex;align-items:center;min-height:44px"><img src="%s" alt="Overtone Lab" width="167" height="30" style="height:30px;width:auto;display:block"></a>
<div class="lang" style="display:flex;gap:4px;background:#151029;border-radius:999px;padding:4px">
<a class="%s" href="%s" hreflang="es" lang="es" %s>ES</a><a class="%s" href="%s" hreflang="en" lang="en" %s>EN</a>
</div></div></header>''' % (link(L, 'home'), asset(L, 'overtone-wordmark.png'),
        es_cls, es_href, 'aria-current="page"' if L == 'es' else '', en_cls, en_href, 'aria-current="page"' if L == 'en' else '')

def footer(L, T):
    return '''<footer style="background:#151029;color:#fff;padding:40px 0">
<div class="wrap" style="display:flex;flex-direction:column;gap:14px">
<p style="margin:0;font-weight:800;font-size:22px">%s</p>
<div style="display:flex;flex-direction:column;gap:8px;font-weight:600;font-size:16px">
<a href="%s" target="_blank" rel="noopener" style="text-decoration:none">+57 302 445 1526</a>
<a href="mailto:contacto@overtonelab.com" style="text-decoration:none">contacto@overtonelab.com</a>
<a href="%s" style="text-decoration:none;color:#CDC5FD;font-size:14px;margin-top:8px">%s</a>
</div></div></footer>''' % (e(T['ask']), WA_INFO, link(L, 'priv'), e(T['consentLink']))

def foot_scripts(L, extra_i18n=None):
    s = '<script src="%s"></script>\n' % asset(L, 'config.js')
    if extra_i18n is not None:
        s += '<script>window.OT_I18N=%s;</script>\n' % json.dumps(extra_i18n, ensure_ascii=False)
    s += '<script src="%s" defer></script>\n</body>\n</html>\n' % asset(L, 'embudo.js')
    return s

def cta_btn(L, T, cls='btn-n'):
    return '<a class="btn %s" href="%s">%s</a>' % (cls, link(L, 'book'), e(T['cta']))

def profile_card(L, T, key, bg='#0C1014'):
    p = T['profiles'][key]
    ver = '<svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true" style="flex:none"><circle cx="12" cy="12" r="11" fill="#0095F6"></circle><path d="M7 12.5l3.2 3.2L17 9" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"></path></svg>' if p['verified'] else ''
    return '''<div style="display:flex;align-items:center;gap:16px;background:#0C1014;color:#F5F5F5;border-radius:18px;padding:18px 20px">
<img src="%s" alt="" width="84" height="84" loading="lazy" style="width:84px;height:84px;border-radius:50%%;flex:none;object-fit:cover;border:3px solid #2A2F36">
<div style="min-width:0"><div style="display:flex;align-items:center;gap:8px"><span style="font-weight:800;font-size:21px;overflow-wrap:anywhere">%s</span>%s</div>
<div style="font-size:14px;margin-top:2px">%s</div>
<div style="display:flex;flex-wrap:wrap;gap:4px 14px;margin-top:10px;font-size:13px"><span><b>%s</b> %s</span><span><b>%s</b> %s</span><span><b>%s</b> %s</span></div></div></div>''' % (
        img(L, p['av']), e(p['handle']), ver, e(p['bio']), p['posts'], T['lPosts'], p['followers'], T['lFollowers'], p['following'], T['lFollowing'])

PLAY = '<svg class="play" width="56" height="56" viewBox="0 0 56 56" aria-hidden="true"><circle cx="28" cy="28" r="27" fill="#fff"></circle><path d="M23 18 L39 28 L23 38 Z" fill="#2A2659"></path></svg>'

def faq_html(T):
    out = []
    for i, q in enumerate(T['faq']):
        body = ''.join(('<b>%s</b>' % e(t)) if b else e(t) for t, b in q['seg'])
        out.append('''<div class="faq-item" style="background:#fff;border-radius:20px;overflow:hidden">
<button type="button" class="faq-btn" aria-expanded="false" aria-controls="faq%d"><span>%s</span><span class="faq-icon" aria-hidden="true">+</span></button>
<div class="faq-wrap" id="faq%d"><div class="faq-inner"><p class="faq-txt">%s</p></div></div></div>''' % (i, e(q['q']), i, body))
    return '\n'.join(out)

def plans_html(L, T):
    out = []
    for p in PLANS:
        best = p['best']
        price = p['cop'] if L == 'es' else p['usd']
        box = 'position:relative;display:flex;flex-direction:column;border-radius:28px;padding:32px 28px;' + ('background:#fff;color:#2A2659;z-index:1;box-shadow:0 0 0 4px #DDD9FD,0 24px 70px rgba(255,255,255,.45)' if best else 'background:#2A2659;color:#fff')
        chk = 'flex:none;font-weight:900;color:' + ('#5546D9' if best else '#CDC5FD')
        badge = '<span style="position:absolute;top:-16px;left:28px;background:#2A2659;color:#fff;font-weight:900;font-size:13px;letter-spacing:.1em;text-transform:uppercase;padding:8px 16px;border-radius:999px">%s</span>' % e(T['best']) if best else ''
        flist = [T['filmDays2'] if (p.get('days', 1) == 2 and i == 3) else f for i, f in enumerate(T['feat'][:8])]
        feats = ''.join('<div style="display:flex;gap:10px"><span aria-hidden="true" style="%s">–</span><span>%s</span></div>' % (chk, e(f)) for f in flist)
        feats += '<div style="display:flex;gap:10px"><span aria-hidden="true" style="%s">★</span><span style="font-weight:900">%s</span></div>' % (chk, e(T['feat'][8]))
        out.append('''<div class="%s" style="%s">%s
<p style="margin:0;font-weight:900;font-size:15px;letter-spacing:.14em">%s</p>
<p style="margin:14px 0 0;font-weight:900;font-size:clamp(38px,4.4vw,50px);letter-spacing:-.03em;line-height:1">%s</p>
<p style="margin:6px 0 0;font-size:15px;font-weight:600">%s</p>
<div style="height:2px;background:currentColor;opacity:.15;margin:24px 0"></div>
<p style="margin:0;font-weight:900;font-size:28px;letter-spacing:-.01em">%d <span style="font-size:19px;font-weight:700">%s</span></p>
<p style="margin:6px 0 0;font-size:19px;font-weight:600">%d %s</p>
<div style="height:2px;background:currentColor;opacity:.15;margin:24px 0"></div>
<p style="margin:0 0 14px;font-weight:900;font-size:14px;letter-spacing:.12em;text-transform:uppercase">%s</p>
<div style="display:flex;flex-direction:column;gap:10px;margin-bottom:28px;font-size:16px;font-weight:600;line-height:1.35">%s</div>
<a class="btn %s" href="%s" style="width:100%%;margin-top:auto">%s</a></div>''' % (
            'plan-best' if best else '', box, badge, p['name'], price, e(T['perMonth']), p['shorts'], e(T['videos']), p['stories'], e(T['stories']),
            e(T['includes']), feats, 'btn-n' if best else 'btn-p', link(L, 'book'), e(T['cta'])))
    return '\n'.join(out)

def marquee_html(L, T):
    def row(idx, cls):
        items = [WHO[i] for i in idx]
        cards = []
        for rep in range(4):
            for name, f in items:
                alt = e(name) if rep == 0 else ''
                hid = '' if rep == 0 else ' aria-hidden="true"'
                cards.append('<div%s style="flex:none"><div style="position:relative;aspect-ratio:1/1;border-radius:20px;overflow:hidden;background:#151029"><img src="%s" alt="%s" loading="lazy" width="162" height="162" style="position:absolute;inset:0;width:100%%;height:100%%;object-fit:cover;display:block"><div style="position:absolute;left:0;right:0;bottom:0;padding:48px 14px 12px;background:linear-gradient(to top,rgba(21,16,41,.95) 0%%,rgba(21,16,41,.7) 55%%,rgba(21,16,41,0) 100%%)"><p style="margin:0;font-weight:800;line-height:1.2;color:#fff">%s</p></div></div></div>' % (hid, img(L, 'c_' + f), alt, e(name)))
        return '<div class="mq"><div class="mq-t %s">%s</div></div>' % (cls, ''.join(cards))
    return row(ROW_A, '') + '\n' + row(ROW_B, 'mq-t2')

def _num(s): return int(''.join(ch for ch in s if ch.isdigit()))

def _faq_text(item):
    s = ''.join(seg[0] for seg in item['seg'])
    out, bullets = [], []
    def flush():
        if bullets:
            out.append('; '.join(x.rstrip('.;') for x in bullets) + '.'); bullets.clear()
    for line in s.split('\n'):
        line = line.strip()
        if line.startswith('•'): bullets.append(line.lstrip('• ').strip())
        else:
            flush()
            if line: out.append(line)
    flush()
    return ' '.join(out)

def jsonld(L, T):
    home = SITE + PATHS[L]['home']
    cur = 'COP' if L == 'es' else 'USD'
    org_id, person_id = SITE + '/#empresa', SITE + '/#fundador'
    plan_word = 'Plan' if L == 'es' else 'Plan'
    offers = []
    for p in PLANS:
        price = _num(p['cop'] if L == 'es' else p['usd'])
        desc = ('%d videos cortos y %d historias al mes' % (p['shorts'], p['stories'])) if L == 'es' else ('%d short videos and %d stories per month' % (p['shorts'], p['stories']))
        offers.append({"@type": "Offer", "priceSpecification": {"@type": "UnitPriceSpecification", "price": price, "priceCurrency": cur, "unitCode": "MON", "unitText": "month", "valueAddedTaxIncluded": False},
                       "itemOffered": {"@type": "Service", "name": "%s %s" % (plan_word, p['name'].title()), "description": desc + '. ' + ', '.join([T['filmDays2'] if (p.get('days', 1) == 2 and i == 3) else f for i, f in enumerate(T['feat'][:8])]) + '.',
                                       "provider": {"@id": org_id}, "areaServed": "Medellín, Colombia"}})
    graph = [
        {"@type": "ProfessionalService", "@id": org_id, "name": "Overtone Lab", "alternateName": "Overtone Lab Medellín", "url": SITE + '/',
         "logo": SITE + "/assets/embudo/img/icon-192.png", "image": SITE + "/assets/embudo/img/og.png",
         "description": T['desc'], "email": "contacto@overtonelab.com", "telephone": "+573024451526",
         "address": {"@type": "PostalAddress", "addressLocality": "Medellín", "addressRegion": "Antioquia", "addressCountry": "CO"},
         "areaServed": [{"@type": "City", "name": "Medellín"}, {"@type": "Country", "name": "Colombia"}, {"@type": "Country", "name": "United States"}],
         "founder": {"@id": person_id}, "hasMap": MAPS, "sameAs": [IG, TT, MAPS],
         "knowsLanguage": ["es", "en"],
         "hasOfferCatalog": {"@type": "OfferCatalog", "name": T['planTitle'], "itemListElement": offers}},
        {"@type": "Person", "@id": person_id, "name": "Andrés Giraldo", "jobTitle": "Fundador y CEO" if L == 'es' else "Founder and CEO",
         "worksFor": {"@id": org_id}, "sameAs": [IG, TT]},
        {"@type": "WebSite", "@id": SITE + '/#sitio', "url": SITE + '/', "name": "Overtone Lab", "inLanguage": ["es", "en"], "publisher": {"@id": org_id}},
        {"@type": "WebPage", "@id": home + '#pagina', "url": home, "name": T['title'], "inLanguage": L, "isPartOf": {"@id": SITE + '/#sitio'}, "about": {"@id": org_id}},
        {"@type": "FAQPage", "@id": home + '#preguntas', "inLanguage": L,
         "mainEntity": [{"@type": "Question", "name": q['q'], "acceptedAnswer": {"@type": "Answer", "text": _faq_text(q)}} for q in T['faq']]},
    ]
    d = {"@context": "https://schema.org", "@graph": graph}
    return '<script type="application/ld+json">%s</script>' % json.dumps(d, ensure_ascii=False)

def build_home(L, T):
    spots = T['spots'].replace('{n}', str(SPOTS))
    def vcard(c):
        vid = c.get('vimeo')
        attrs = ' class="vplay" role="button" tabindex="0" data-vimeo="%s" data-ratio="%s" aria-label="%s" style="cursor:pointer;' % (vid, c['ratio'], e(T['playLabel'] + ' ' + c['h'])) if vid else ' style="'
        play = PLAY if vid else ''
        return '''<div class="vcard" style="background:#151029;border-radius:24px;padding:20px">
<div%sposition:relative;aspect-ratio:9/16;border-radius:16px;overflow:hidden;background:#7259F5"><img src="%s" alt="%s" loading="lazy" width="540" height="960" style="position:absolute;inset:0;width:100%%;height:100%%;object-fit:cover"><div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center">%s</div></div>
<p class="vh" style="margin:18px 0 4px;font-weight:700;font-size:16px;color:#CDC5FD">%s</p>
<p class="vb" style="margin:0;font-weight:900;font-size:34px;letter-spacing:-.02em;line-height:1.05">%s <span class="vu" style="font-size:20px;font-weight:700">%s</span></p>
<p class="vm" style="margin:6px 0 0;font-size:15px;color:#CDC5FD">%s</p></div>''' % (attrs, img(L, 'r_' + c['img']), e(c['alt']), play, e(c['h']), e(c['big']), e(c['unit']), e(c['meta']))
    cards = ''.join(vcard(c) for c in T['cards'])
    more = ''.join('''<div style="background:#DDD9FD;color:#2A2659;border-radius:24px;padding:24px"><div style="margin-bottom:20px">%s</div>
<div class="mr-row" style="display:flex;flex-wrap:wrap;gap:20px 8px;align-items:stretch">
<div style="flex:1 1 200px;text-align:center"><p style="margin:0;font-weight:900;font-size:clamp(22px,2.3vw,30px);letter-spacing:-.02em;line-height:1.05;color:#5546D9">%s</p><p style="margin:8px 0 0;font-size:14px;line-height:1.3;font-weight:700">%s</p></div>
<div class="mr-div" aria-hidden="true" style="flex:none;width:2px;margin:2px 0;border-radius:2px;background:rgba(85,70,217,.3)"></div>
<div style="flex:1 1 200px;text-align:center"><p style="margin:0;font-weight:900;font-size:clamp(22px,2.3vw,30px);letter-spacing:-.02em;line-height:1.05;color:#5546D9">%s</p><p style="margin:8px 0 0;font-size:14px;line-height:1.3;font-weight:700">%s</p></div></div></div>''' % (
        profile_card(L, T, m['h']), e(m['a']), e(T['followers']), e(m['b']), e(T['engagement'])) for m in T['more'])
    testi = ''.join('''<figure style="margin:0;background:#fff;border-radius:24px;padding:28px;display:flex;flex-direction:column;justify-content:space-between;gap:24px">
<div><div aria-hidden="true" style="color:#F5A623;font-size:22px;letter-spacing:.1em">★★★★★</div><blockquote style="margin:14px 0 0;font-weight:600;font-size:19px;line-height:1.45">%s</blockquote></div>
<figcaption><span style="display:block;font-weight:900;font-size:17px">%s</span><span style="display:block;margin-top:2px;font-size:14px;font-weight:600;color:#3D3868">%s</span></figcaption></figure>''' % (e(x['q']), e(x['name']), e(x['src'])) for x in T['testi'])
    steps = ''
    for i, s in enumerate(T['steps']):
        hi = i == 2
        steps += '''<div style="background:%s;color:%s;border-radius:24px;padding:24px 20px"><div style="width:44px;height:44px;border-radius:50%%;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:19px;background:%s;color:#fff">%d</div>
<h3 style="margin:16px 0 8px;font-weight:900;font-size:19px;letter-spacing:-.01em">%s</h3><p style="margin:0;font-size:16px;line-height:1.5;font-weight:500">%s</p></div>''' % (
            '#2A2659' if hi else '#DDD9FD', '#fff' if hi else '#2A2659', '#7259F5' if hi else '#2A2659', i + 1, e(s['t']), e(s['d']))
    body = '''%s
<main>
<section style="background:#7259F5;color:#fff;padding:80px 0 96px;text-align:center"><div class="wrap">
<h1 class="h1" style="max-width:1100px;margin:0 auto;font-size:clamp(34px,5.6vw,76px);text-wrap:balance">%s</h1>
<p style="margin:24px auto 36px;max-width:900px;text-wrap:balance;font-weight:700;font-size:15px;line-height:1.5;letter-spacing:.12em;text-transform:uppercase;color:#fff">%s</p>
%s<p style="margin:22px 0 0;font-weight:700;font-size:15px">%s</p></div></section>

<section style="background:#2A2659;color:#fff;padding:96px 0"><div class="wrap">
<h2 class="h2" style="text-align:center">%s</h2>
<p style="text-align:center;margin:14px 0 48px;font-size:19px;color:#CDC5FD">%s</p>
<div class="grid vgrid" style="grid-template-columns:repeat(auto-fit,minmax(230px,1fr))">%s</div>
<div style="margin-top:28px;background:#7259F5;border-radius:28px;padding:clamp(28px,5vw,56px);display:flex;flex-wrap:wrap;gap:32px;align-items:center;justify-content:space-between">
<div style="flex:1 1 280px"><p style="margin:0;font-weight:800;font-size:14px;letter-spacing:.14em;text-transform:uppercase">%s</p><div style="max-width:460px;margin-top:16px">%s</div>
<p style="margin:16px 0 0;font-size:18px;line-height:1.5;max-width:420px">%s</p></div>
<div style="display:flex;flex-wrap:wrap;gap:32px">
<div><p style="margin:0;font-weight:900;font-size:clamp(56px,8vw,96px);line-height:1;letter-spacing:-.03em">%s</p><p style="margin:6px 0 0;font-size:19px;font-weight:600">%s</p></div>
<div><p style="margin:0;font-weight:900;font-size:clamp(56px,8vw,96px);line-height:1;letter-spacing:-.03em">%s</p><p style="margin:6px 0 0;font-size:19px;font-weight:600">%s</p></div></div></div>
<h3 style="margin:64px 0 28px;text-align:center;font-weight:900;font-size:clamp(26px,3.4vw,38px);text-transform:uppercase;letter-spacing:-.01em">%s</h3>
<div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(300px,1fr))">%s</div>
<div style="text-align:center;margin-top:56px">%s</div></div></section>

<section style="background:#DDD9FD;color:#2A2659;padding:96px 0"><div class="wrap">
<h2 class="h2" style="text-align:center">%s</h2>
<div class="grid" style="margin-top:48px">%s</div>
<div style="text-align:center;margin-top:56px">%s</div></div></section>

<section style="background:#fff;color:#2A2659;padding:96px 0"><div class="wrap">
<h2 class="h2" style="text-align:center">%s</h2>
<p style="text-align:center;margin:14px 0 48px;font-size:19px;color:#3D3868">%s</p>
<div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:16px">%s</div>
<div style="text-align:center;margin-top:56px">%s</div></div></section>

<section style="background:#2A2659;color:#fff;padding:72px 0"><div class="wrap" style="text-align:center">
<h2 class="h2">%s</h2>
<div style="margin-top:28px;display:flex;flex-direction:column;gap:14px">%s</div></div></section>

<section style="background:#DDD9FD;color:#2A2659;padding:96px 0"><div class="wrap" style="max-width:860px">
<h2 class="h2" style="text-align:center">%s</h2>
<div style="margin-top:44px;display:flex;flex-direction:column;gap:12px">%s</div>
<div style="text-align:center;margin-top:48px">%s</div></div></section>

<section style="background:#7259F5;color:#fff;padding:96px 0"><div class="wrap">
<h2 class="h2" style="text-align:center">%s</h2>
<p style="text-align:center;margin:14px 0 52px;font-size:19px;font-weight:500">%s</p>
<div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(280px,1fr));align-items:stretch">%s</div>
<div style="margin-top:64px;background:#DDD9FD;color:#2A2659;border-radius:24px;padding:24px 28px;display:flex;flex-wrap:wrap;gap:16px 28px;align-items:center;justify-content:space-between">
<div style="flex:1 1 380px"><p style="margin:0;font-weight:900;font-size:20px">%s</p><p style="margin:4px 0 0;font-size:16px;line-height:1.5;font-weight:500">%s</p></div>
<a class="btn btn-n btn-s" href="%s">%s</a></div>
<p style="margin:32px 0 0;text-align:center;font-weight:700;font-size:16px">%s</p></div></section>

<section style="background:#2A2659;color:#fff;padding:96px 0;text-align:center"><div class="wrap">
<h2 class="h2" style="max-width:820px;margin:0 auto">%s</h2>
<p style="margin:20px 0 36px;font-size:20px;color:#CDC5FD">%s</p>%s</div></section>
</main>
%s''' % (
        header(L, T, 'home'), e(T['h1']), e(T['kicker']), cta_btn(L, T, 'btn-w'), e(spots),
        e(T['resTitle']), e(T['resSub']), cards,
        e(T['storyTag']), profile_card(L, T, '@ledesma_barber888'), e(T['storyTxt']), e(T['storyA']), e(T['storyAL']), e(T['storyB']), e(T['storyBL']),
        e(T['moreTitle']), more, cta_btn(L, T, 'btn-p'),
        e(T['testiTitle']), testi, cta_btn(L, T, 'btn-n'),
        e(T['procTitle']), e(T['procSub']), steps, cta_btn(L, T, 'btn-n'),
        e(T['whoTitle']), marquee_html(L, T),
        e(T['faqTitle']), faq_html(T), cta_btn(L, T, 'btn-n'),
        e(T['planTitle']), e(T['planSub']), plans_html(L, T), e(T['customTitle']), e(T['customTxt']), link(L, 'book'), e(T['customCta']), e(T['planNote']),
        e(T['endTitle']), e(T['endSub']), cta_btn(L, T, 'btn-p'),
        footer(L, T))
    return head(L, T, 'home', T['title'], T['desc'], extra=(GSC if L == 'es' else '') + jsonld(L, T)) + '\n' + body + '\n' + foot_scripts(L)

def i18n_for(T):
    keys = ['loading', 'noSlots', 'goals', 'budgets', 'missName', 'missSocial', 'missBiz', 'missGoal', 'missBudget', 'missPhone', 'missEmail', 'missConsent', 'errMissing', 'errServer', 'errTaken', 'sending', 'submit', 'thanksTitleN']
    d = {k: T[k] for k in keys}
    d['soons'] = T['soon']
    return d

def build_book(L, T):
    waurl = wa_url(T['waMsg'])
    body = '''%s
<main style="background:#DDD9FD;padding:56px 0 96px;min-height:900px"><div class="wrap" style="max-width:780px">
<div id="book" data-thanks="%s" style="background:#fff;border-radius:28px;padding:clamp(24px,5vw,48px)">
<h1 class="h2" style="font-size:clamp(30px,4.4vw,48px);color:#2A2659">%s</h1>
<p style="margin:12px 0 0;font-size:16px;font-weight:600;color:#3D3868">%s</p>
<p style="margin:4px 0 0;font-size:16px;font-weight:600;color:#5546D9">%s</p>
<div style="margin-top:20px;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:12px;background:#DDD9FD;border-radius:16px;padding:14px 18px">
<span style="font-weight:700;font-size:15px;line-height:1.4;color:#2A2659">%s</span>
<a class="btn btn-n btn-s" href="%s" target="_blank" rel="noopener">%s</a></div>
<p id="demoNote" hidden style="margin:16px 0 0;padding:10px 14px;border-radius:12px;background:#FFF3CD;color:#7A5B00;font-weight:700;font-size:14px">%s</p>

<div id="step1">
<p class="lb" style="margin-top:32px">%s</p>
<p id="slotStatus" style="margin:0;font-size:15px;color:#3D3868" hidden></p>
<div id="dates" style="display:flex;flex-wrap:wrap;gap:10px"></div>
<p class="lb" id="timeLabel" hidden>%s</p>
<div id="times" style="display:flex;flex-wrap:wrap;gap:10px" hidden></div>
<button type="button" id="next" class="btn btn-n btn-off" style="margin-top:28px">%s</button>
</div>

<div id="step2" hidden>
<div style="margin-top:24px;display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:space-between;background:#DDD9FD;border-radius:16px;padding:12px 16px">
<span id="summary" style="font-weight:800;color:#2A2659"></span><button type="button" id="backBtn" class="chip">%s</button></div>
<h2 style="margin:36px 0 0;font-weight:900;font-size:26px;color:#2A2659">%s</h2>
<label class="lb" for="f-name">%s <span class="req">*</span></label><input id="f-name" class="in" type="text" autocomplete="name">
<label class="lb" for="f-social">%s <span class="req">*</span></label><textarea id="f-social" class="in" rows="2"></textarea>
<label class="lb" for="f-biz">%s <span class="req">*</span></label><textarea id="f-biz" class="in" rows="3"></textarea>
<p class="lb">%s</p><div id="soonBox" style="display:flex;flex-wrap:wrap;gap:10px"></div>
<p class="lb">%s <span class="req">*</span></p><div id="goalBox" style="display:flex;flex-wrap:wrap;gap:10px"></div>
<p class="lb">%s <span class="req">*</span></p><div id="budgetBox" style="display:flex;flex-wrap:wrap;gap:10px"></div>
<p style="margin:8px 0 0;font-size:14px;color:#3D3868">%s</p>
<label class="lb" for="f-phone">%s <span class="req">*</span></label><input id="f-phone" class="in" type="tel" autocomplete="tel">
<label class="lb" for="f-email">%s <span class="req">*</span></label><input id="f-email" class="in" type="email" autocomplete="email">
<label class="lb" for="f-ref">%s</label><input id="f-ref" class="in" type="text">
<div class="hp" aria-hidden="true"><label for="f-website">Website</label><input id="f-website" type="text" tabindex="-1" autocomplete="off"></div>
<div style="display:flex;gap:12px;align-items:flex-start;margin-top:28px"><input id="f-consent" type="checkbox" style="width:24px;height:24px;margin:2px 0 0;flex:none;accent-color:#5546D9">
<label for="f-consent" style="font-size:15px;line-height:1.5;color:#3D3868">%s <a href="%s" target="_blank" rel="noopener" style="color:#5546D9">%s</a> <span class="req">*</span></label></div>
<p id="err" role="alert" hidden style="margin:20px 0 0;font-weight:700;font-size:15px;color:#B3261E"></p>
<button type="button" id="submit" class="btn btn-n" style="margin-top:28px;width:100%%">%s</button>
</div></div></div></main>
%s''' % (header(L, T, 'book'), link(L, 'thanks'), e(T['bookTitle']), e(T['bookMeta']), e(T['bookDays']), e(T['waLine']), waurl, e(T['waCta']), e(T['demoNote']),
         e(T['pickDate']), e(T['pickTime']), e(T['next']), e(T['back']), e(T['detailsTitle']),
         e(T['fName']), e(T['fSocial']), e(T['fBiz']), e(T['fSoon']), e(T['fGoal']), e(T['fBudget']), e(T['budgetNote']), e(T['fPhone']), e(T['fEmail']), e(T['fRef']),
         e(T['consent']), link(L, 'priv'), e(T['consentLink']), e(T['submit']), footer(L, T))
    return head(L, T, 'book', T['bookPageTitle'], T['desc'], robots='noindex,follow') + '\n' + body + '\n' + foot_scripts(L, i18n_for(T))

def icon_links():
    return '''<div style="display:flex;justify-content:center;gap:16px">
<a class="soc" href="%s" target="_blank" rel="noopener" aria-label="Instagram"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"></rect><circle cx="12" cy="12" r="4"></circle><circle cx="17.5" cy="6.5" r="1" fill="#fff" stroke="none"></circle></svg></a>
<a class="soc" href="%s" target="_blank" rel="noopener" aria-label="WhatsApp"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 21l1.65-4.9A9 9 0 1 1 8 19.4L3 21z"></path><path d="M9 8.5c0 3.5 3 6.5 6.5 6.5l1-1.5-2-1-1 .8c-1-.4-2-1.4-2.4-2.4l.8-1-1-2L9 8.5z"></path></svg></a>
<a class="soc" href="%s" target="_blank" rel="noopener" aria-label="TikTok"><svg width="24" height="24" viewBox="0 0 24 24" fill="#fff" aria-hidden="true"><path d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"></path></svg></a></div>''' % (IG, WA_INFO, TT)

def build_thanks(L, T):
    body = '''%s
<main id="thanks" style="background:#fff;color:#2A2659">
<section style="padding:64px 0 48px;text-align:center"><div class="wrap" style="max-width:920px">
<h1 id="thanksTitle" class="h1" style="font-size:clamp(34px,6vw,72px);color:#2A2659">%s</h1>
<p id="thanksSub" hidden style="margin:20px 0 0;font-size:20px;font-weight:600;color:#3D3868">%s</p>
<p id="thanksSummary" hidden style="display:inline-block;margin:20px 0 0;padding:10px 20px;border-radius:999px;background:#DDD9FD;font-size:16px;font-weight:800;color:#2A2659"></p>
</div></section>
<section style="background:#7259F5;color:#fff;padding:40px 0 72px;text-align:center"><div class="wrap" style="max-width:980px">
<div id="videoWrap" hidden style="margin-bottom:48px"><div id="video" style="position:relative;aspect-ratio:16/9;border-radius:24px;overflow:hidden;background:#151029"></div></div>
<h2 style="margin:0;font-weight:900;font-size:clamp(26px,3.6vw,40px);text-transform:uppercase;letter-spacing:-.01em;line-height:1.05">%s</h2>
<p style="margin:16px auto 0;max-width:860px;font-size:20px;line-height:1.5;font-weight:500">%s</p>
</div></section>
<section style="padding:56px 0 64px;text-align:center"><p style="margin:0 0 20px;font-weight:800;font-size:15px;letter-spacing:.12em;text-transform:uppercase;color:#3D3868">%s</p>%s</section>
</main>
%s''' % (header(L, T, 'thanks'), e(T['thanksTitle']), e(T['thanksSub']), e(T['thanksHead']), e(T['thanksTxt']), e(T['follow']), icon_links(), footer(L, T))
    return head(L, T, 'thanks', T['thanksPageTitle'], T['desc'], robots='noindex,nofollow') + '\n' + body + '\n' + foot_scripts(L, i18n_for(T))

def build_priv(L):
    from privacy import ES_PRIV, EN_PRIV
    T = ES if L == 'es' else EN
    P = ES_PRIV if L == 'es' else EN_PRIV
    body = '''%s
<main style="background:#fff;padding:64px 0 96px"><div class="wrap" style="max-width:820px">
<h1 class="h2" style="font-size:clamp(30px,4.4vw,48px);color:#2A2659">%s</h1>
<p style="margin:12px 0 24px;font-weight:600;color:#3D3868">%s</p>
<div class="prose">%s</div></div></main>
%s''' % (header(L, T, 'priv'), e(P['title']), e(P['updated']), P['html'], footer(L, T))
    return head(L, T, 'priv', T['privPageTitle'], P['desc']) + '\n' + body + '\n' + foot_scripts(L)

def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f: f.write(content)

if __name__ == '__main__':
    for L, T in (('es', ES), ('en', EN)):
        write(FILES[L]['home'], build_home(L, T))
        write(FILES[L]['book'], build_book(L, T))
        write(FILES[L]['thanks'], build_thanks(L, T))
        write(FILES[L]['priv'], build_priv(L))
    print('ok', OUT)
