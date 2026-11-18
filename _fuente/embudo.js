/* Overtone Lab — comportamiento del embudo (FAQ, agendar, gracias) */
(function () {
  'use strict';
  var CFG = window.OT_CONFIG || {};
  var I = window.OT_I18N || {};
  var lang = document.documentElement.lang === 'en' ? 'en' : 'es';
  var loc = lang === 'en' ? 'en-US' : 'es-CO';

  function $(s, r) { return (r || document).querySelector(s); }
  function el(tag, cls, txt) { var e = document.createElement(tag); if (cls) e.className = cls; if (txt != null) e.textContent = txt; return e; }

  /* ---------- FAQ ---------- */
  document.addEventListener('click', function (e) {
    var b = e.target.closest ? e.target.closest('.faq-btn') : null;
    if (!b) return;
    var item = b.parentNode;
    var open = item.classList.toggle('open');
    b.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  /* ---------- Agendar ---------- */
  var book = $('#book');
  if (book) initBook();

  function timeLabel(hh) {
    if (lang === 'es') return hh;
    var h = parseInt(hh.slice(0, 2), 10);
    return ((h % 12) || 12) + ':' + hh.slice(3) + (h < 12 ? ' AM' : ' PM');
  }
  function dateLabel(iso) {
    var p = iso.split('-');
    var d = new Date(+p[0], +p[1] - 1, +p[2], 12, 0, 0);
    return d.toLocaleDateString(loc, { weekday: 'short', day: 'numeric', month: 'short' });
  }
  function demoSlots() {
    var out = [], d = new Date(), times = ['08:00', '09:00', '10:00', '11:00', '13:00', '14:00', '15:00', '16:00', '17:00'];
    d.setHours(12, 0, 0, 0);
    while (out.length < 6) {
      d.setDate(d.getDate() + 1);
      if (d.getDay() !== 3) continue;
      var iso = d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
      out.push({ date: iso, times: times.slice() });
    }
    return out;
  }

  function initBook() {
    var S = { slots: [], date: '', time: '', f: { soon: '', goal: '', budget: '' }, busy: false };
    var step1 = $('#step1'), step2 = $('#step2');
    var dateBox = $('#dates'), timeBox = $('#times'), timeLbl = $('#timeLabel'), next = $('#next');
    var summary = $('#summary'), err = $('#err'), submit = $('#submit'), demo = $('#demoNote');

    function setStep(n) {
      step1.hidden = n !== 1; step2.hidden = n !== 2;
      window.scrollTo(0, 0);
    }
    function chipGroup(box, items, getOn, onPick) {
      box.innerHTML = '';
      items.forEach(function (it) {
        var b = el('button', 'chip' + (getOn(it) ? ' chip-on' : ''), it.label);
        b.type = 'button';
        b.setAttribute('aria-pressed', getOn(it) ? 'true' : 'false');
        b.addEventListener('click', function () { onPick(it); });
        box.appendChild(b);
      });
    }
    function renderDates() {
      chipGroup(dateBox, S.slots.map(function (s) { return { v: s.date, label: dateLabel(s.date) }; }),
        function (it) { return S.date === it.v; },
        function (it) { S.date = it.v; S.time = ''; renderDates(); renderTimes(); updateNext(); });
    }
    function renderTimes() {
      var day = S.slots.filter(function (s) { return s.date === S.date; })[0];
      timeLbl.hidden = timeBox.hidden = !day;
      if (!day) return;
      chipGroup(timeBox, day.times.map(function (t) { return { v: t, label: timeLabel(t) }; }),
        function (it) { return S.time === it.v; },
        function (it) { S.time = it.v; renderTimes(); updateNext(); });
    }
    function updateNext() { next.classList.toggle('btn-off', !(S.date && S.time)); }
    function loadSlots() {
      var status = $('#slotStatus');
      status.textContent = I.loading; status.hidden = false;
      var done = function (slots) {
        S.slots = slots || [];
        status.hidden = true;
        if (!S.slots.length) { status.textContent = I.noSlots; status.hidden = false; }
        if (S.date && !S.slots.some(function (s) { return s.date === S.date; })) { S.date = ''; S.time = ''; }
        renderDates(); renderTimes(); updateNext();
      };
      if (!CFG.apiBase) { demo.hidden = false; done(demoSlots()); return; }
      fetch(CFG.apiBase + '/availability').then(function (r) { return r.json(); })
        .then(function (j) { done(j.slots); })
        .catch(function () { status.textContent = I.noSlots; status.hidden = false; });
    }

    next.addEventListener('click', function () {
      if (!(S.date && S.time)) return;
      summary.textContent = dateLabel(S.date) + ' · ' + timeLabel(S.time);
      setStep(2);
    });
    $('#backBtn').addEventListener('click', function () { setStep(1); });

    [['soon', '#soonBox'], ['goal', '#goalBox'], ['budget', '#budgetBox']].forEach(function (pair) {
      var key = pair[0], box = $(pair[1]), items = I[key + 's'];
      (function render() {
        chipGroup(box, items.map(function (x) { return { v: x, label: x }; }),
          function (it) { return S.f[key] === it.v; },
          function (it) { S.f[key] = (key === 'soon' && S.f[key] === it.v) ? '' : it.v; render(); });
      })();
    });

    function val(id) { return ($('#' + id).value || '').trim(); }
    submit.addEventListener('click', function () {
      if (S.busy) return;
      var f = { name: val('f-name'), social: val('f-social'), biz: val('f-biz'), phone: val('f-phone'), email: val('f-email'), ref: val('f-ref'), consent: $('#f-consent').checked };
      var miss = [];
      if (!f.name) miss.push(I.missName);
      if (!f.social) miss.push(I.missSocial);
      if (!f.biz) miss.push(I.missBiz);
      if (!S.f.goal) miss.push(I.missGoal);
      if (!S.f.budget) miss.push(I.missBudget);
      if (!f.phone) miss.push(I.missPhone);
      if (f.email.indexOf('@') < 1) miss.push(I.missEmail);
      if (!f.consent) miss.push(I.missConsent);
      if (miss.length) { err.textContent = I.errMissing + miss.join(', '); err.hidden = false; return; }
      err.hidden = true;
      if ($('#f-website').value) return; // trampa para spam
      var payload = { date: S.date, time: S.time, name: f.name, social: f.social, biz: f.biz, soon: S.f.soon, goal: S.f.goal, budget: S.f.budget, phone: f.phone, email: f.email, ref: f.ref, lang: lang };
      var finish = function () {
        try { sessionStorage.setItem('ot_booking', JSON.stringify({ name: f.name.split(' ')[0], label: dateLabel(S.date) + ' · ' + timeLabel(S.time) })); } catch (e) {}
        window.location.href = book.getAttribute('data-thanks');
      };
      if (!CFG.apiBase) { finish(); return; }
      S.busy = true; submit.textContent = I.sending; submit.classList.add('btn-off');
      fetch(CFG.apiBase + '/book', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
        .then(function (r) { return r.json().then(function (j) { return { s: r.status, j: j }; }); })
        .then(function (res) {
          if (res.s === 200 || res.s === 201) { finish(); return; }
          S.busy = false; submit.textContent = I.submit; submit.classList.remove('btn-off');
          if (res.s === 409) { err.textContent = I.errTaken; err.hidden = false; S.time = ''; setStep(1); loadSlots(); return; }
          err.textContent = I.errServer; err.hidden = false;
        })
        .catch(function () { S.busy = false; submit.textContent = I.submit; submit.classList.remove('btn-off'); err.textContent = I.errServer; err.hidden = false; });
    });

    loadSlots();
  }

  /* ---------- Gracias ---------- */
  var th = $('#thanks');
  if (th) {
    var data = null;
    try { data = JSON.parse(sessionStorage.getItem('ot_booking') || 'null'); } catch (e) {}
    var title = $('#thanksTitle'), sum = $('#thanksSummary');
    if (data && data.name) title.textContent = (I.thanksTitleN || '').replace('{n}', data.name);
    if (data && data.label) { sum.textContent = data.label; sum.hidden = false; }
    var yt = CFG.youtubeId;
    var vw = $('#videoWrap'), sub = $('#thanksSub');
    if (yt) {
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(yt) + '?rel=0&modestbranding=1';
      f.title = 'Overtone Lab';
      f.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
      f.allowFullscreen = true;
      f.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;border:0';
      $('#video').appendChild(f);
      vw.hidden = false; sub.hidden = false;
    }
  }

  /* ---------- Videos de resultados (se reproducen dentro de la tarjeta) ---------- */
  var plays = document.querySelectorAll('.vplay'), current = null;
  var restore = function () {
    if (!current) return;
    current.el.innerHTML = current.html;
    current.el.setAttribute('role', 'button'); current.el.setAttribute('tabindex', '0');
    current.el.style.cursor = 'pointer'; current.el.style.background = '#7259F5';
    current = null;
  };
  var playIn = function (el) {
    if (current && current.el === el) return;
    restore();
    current = { el: el, html: el.innerHTML };
    var f = document.createElement('iframe');
    f.src = 'https://player.vimeo.com/video/' + encodeURIComponent(el.getAttribute('data-vimeo')) + '?autoplay=1&title=0&byline=0&portrait=0&dnt=1';
    f.allow = 'autoplay; fullscreen; picture-in-picture; encrypted-media';
    f.setAttribute('allowfullscreen', ''); f.title = el.getAttribute('aria-label') || 'Video';
    f.referrerPolicy = 'strict-origin-when-cross-origin';
    f.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;border:0';
    el.innerHTML = ''; el.appendChild(f);
    el.removeAttribute('role'); el.removeAttribute('tabindex');
    el.style.cursor = 'auto'; el.style.background = '#000';
  };
  Array.prototype.forEach.call(plays, function (el) {
    el.addEventListener('click', function () { playIn(el); });
    el.addEventListener('keydown', function (ev) { if ((ev.key === 'Enter' || ev.key === ' ') && ev.target === el) { ev.preventDefault(); playIn(el); } });
  });
})();
