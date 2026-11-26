/* =============================================================================
   Sunrise UI — shared script for the starter pages
   • builds the app shell (side rail / drawer, top bar, tab bar, icon sprite) from NAV
     so every page stays consistent — in a real app render the same markup on the server
   • light/dark + colour pattern (saved in localStorage "sr-theme-v1")
   • drawer, bottom sheets / dialogs, toasts, segmented controls, chips, copy buttons
   Page markup:  <body class="sr-app" data-page="dashboard" data-title="Home" [data-nav="admin"]>
                   <div class="sr-main"><main class="sr-page">…</main></div>
   ============================================================================= */
(function () {
  'use strict';
  var h = document.documentElement, b = document.body;
  var P = window.SR_PATTERNS || {};

  var ICONS = {
    home: '<path d="M3 11 12 4l9 7v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>',
    spark: '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8zM19 16l.8 2.2L22 19l-2.2.8L19 22l-.8-2.2L16 19l2.2-.8z"/>',
    wallet: '<rect x="3" y="6" width="18" height="14" rx="3"/><path d="M3 10h14a2 2 0 0 1 2 2v1a2 2 0 0 1-2 2H3M7 6V5a2 2 0 0 1 2-2h7"/>',
    list: '<rect x="4" y="3" width="16" height="18" rx="2.5"/><path d="M8 8h8M8 12h8M8 16h5"/>',
    grid: '<rect x="4" y="4" width="6.5" height="6.5" rx="1.5"/><rect x="13.5" y="4" width="6.5" height="6.5" rx="1.5"/><rect x="4" y="13.5" width="6.5" height="6.5" rx="1.5"/><rect x="13.5" y="13.5" width="6.5" height="6.5" rx="1.5"/>',
    bell: '<path d="M6 8a6 6 0 1 1 12 0c0 7 3 8 3 8H3s3-1 3-8M10 20a2 2 0 0 0 4 0"/>',
    moon: '<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/>',
    arrow: '<path d="M7 17 17 7M8 7h9v9"/>',
    coins: '<ellipse cx="9" cy="7" rx="6" ry="3"/><path d="M3 7v4c0 1.7 2.7 3 6 3s6-1.3 6-3V7M9 14v3c0 1.7 2.7 3 6 3s6-1.3 6-3v-4c0-1.6-2.4-2.9-5.5-3"/>',
    trophy: '<path d="M8 4h8v5a4 4 0 0 1-8 0zM8 6H4a3 3 0 0 0 4 4M16 6h4a3 3 0 0 1-4 4M12 13v4M8 21h8M10 17h4v4h-4z"/>',
    users: '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0M16 4.6a3.5 3.5 0 0 1 0 6.8M21.5 20a6.5 6.5 0 0 0-4-6"/>',
    hotel: '<path d="M3 21V5a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v16M16 9h3a2 2 0 0 1 2 2v10M2 21h20M7 7h2M11 7h2M7 11h2M11 11h2M8 21v-4h3v4"/>',
    chat: '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>',
    cpu: '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>',
    user: '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    gear: '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/>',
    shield: '<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/><path d="m9 12 2 2 4-4"/>',
    chart: '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    copy: '<rect x="8" y="8" width="12" height="12" rx="2.5"/><path d="M16 8V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h2"/>',
    check: '<path d="m5 12 5 5L20 7"/>', info: '<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/>',
    warn: '<path d="M12 3 2 20h20zM12 10v4M12 17h.01"/>', x: '<path d="M6 6l12 12M18 6 6 18"/>',
    search: '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>', filter: '<path d="M3 5h18l-7 8v6l-4-2v-4z"/>',
    eye: '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    phone: '<rect x="6" y="2" width="12" height="20" rx="3"/><path d="M11 18h2"/>', lock: '<rect x="4" y="10" width="16" height="11" rx="2.5"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
    logout: '<path d="M15 4h3a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2h-3M10 17l5-5-5-5M15 12H3"/>', star: '<path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1 6.2L12 17.3 6.5 20.2l1-6.2L3 9.6l6.2-.9z"/>',
    send: '<path d="M22 2 11 13M22 2l-7 20-4-9-9-4z"/>', plus: '<path d="M12 5v14M5 12h14"/>', down: '<path d="M12 5v14M5 12l7 7 7-7"/>', up: '<path d="M12 19V5M5 12l7-7 7 7"/>'
  };
  function icon(n) { return '<svg class="sr-ic" aria-hidden="true"><use href="#i-' + n + '"/></svg>'; }

  /* Navigation. group = rail heading; tab = shown in the phone tab bar (max 5, one "cta"). */
  var NAV = {
    member: [
      { id: 'dashboard', label: 'Home', icon: 'home', href: 'index.html', tab: 1 },
      { id: 'tasks', label: 'Ways to earn', short: 'Earn', icon: 'spark', href: 'tasks.html', tab: 1 },
      { id: 'withdraw', label: 'Withdraw', icon: 'wallet', href: 'withdraw.html', tab: 'cta' },
      { id: 'transactions', label: 'Activity', icon: 'list', href: 'transactions.html', tab: 1 },
      { id: 'team', label: 'My team', icon: 'users', href: 'index.html#team', group: 'Account' },
      { id: 'profile', label: 'Profile & settings', icon: 'user', href: 'profile.html' },
      { id: 'components', label: 'UI components', icon: 'grid', href: 'components.html', group: 'Design' },
      { id: 'admin', label: 'Admin panel', icon: 'shield', href: 'admin.html' }
    ],
    admin: [
      { id: 'admin', label: 'Overview', icon: 'chart', href: 'admin.html', tab: 1 },
      { id: 'a-users', label: 'Members', icon: 'users', href: 'admin.html#members', tab: 1 },
      { id: 'a-pay', label: 'Withdrawals', icon: 'wallet', href: 'admin.html#withdrawals', tab: 'cta', badge: '3' },
      { id: 'a-settings', label: 'Settings', icon: 'gear', href: 'admin.html#settings', tab: 1 },
      { id: 'dashboard', label: 'Member site', icon: 'home', href: 'index.html', group: 'Switch' }
    ]
  };

  function shell() {
    var page = b.dataset.page || '', set = NAV[b.dataset.nav || 'member'], main = document.querySelector('.sr-main');
    if (!main) return;
    // icon sprite
    var sp = '<svg width="0" height="0" style="position:absolute" aria-hidden="true">';
    for (var k in ICONS) sp += '<symbol id="i-' + k + '" viewBox="0 0 24 24">' + ICONS[k] + '</symbol>';
    b.insertAdjacentHTML('afterbegin', sp + '</svg>');
    // rail (sidebar on desktop, drawer on phones)
    var r = '<aside class="sr-rail" id="sr-rail" aria-label="Menu"><div class="sr-rail__brand"><a class="sr-brand" href="index.html"><span class="sr-logo">' + icon('wallet') + '</span>NOVAPAL</a></div>';
    set.forEach(function (n) {
      if (n.group) r += '<p class="sr-rail__group">' + n.group + '</p>';
      r += '<a class="sr-navlink" href="' + n.href + '"' + (n.id === page ? ' aria-current="page"' : '') + '>' + icon(n.icon) + '<span>' + n.label + '</span>' + (n.badge ? '<span class="sr-badge sr-badge--brand">' + n.badge + '</span>' : '') + '</a>';
    });
    r += '<div class="sr-rail__foot"><a class="sr-navlink" href="login.html">' + icon('logout') + '<span>Sign out</span></a></div></aside><div class="sr-scrim" data-drawer-close></div>';
    b.insertAdjacentHTML('afterbegin', r);
    // top bar
    var title = b.dataset.title || '';
    main.insertAdjacentHTML('afterbegin', '<header class="sr-topbar"><button class="ds-burger" type="button" aria-label="Open menu" aria-controls="sr-rail" aria-expanded="false" data-drawer-toggle><span></span><span></span><span></span></button>' +
      '<a class="sr-brand sr-hide-lg" href="index.html"><span class="sr-logo">' + icon('wallet') + '</span></a>' +
      '<span class="sr-topbar__title">' + (title || 'NOVAPAL') + '</span>' +
      '<button class="sr-iconbtn" type="button" aria-label="Notifications" data-toast="No new notifications">' + icon('bell') + '</button>' +
      '<button class="sr-iconbtn" type="button" aria-label="Switch light or dark mode" data-mode-toggle>' + icon('moon') + '</button>' +
      '<a class="sr-avatar" href="profile.html" aria-label="Profile">AM</a></header>');
    // tab bar
    var t = '<nav class="sr-tabbar" aria-label="Main">';
    set.filter(function (n) { return n.tab; }).slice(0, 5).forEach(function (n) {
      t += '<a class="sr-tab' + (n.tab === 'cta' ? ' sr-tab--cta' : '') + '" href="' + n.href + '"' + (n.id === page ? ' aria-current="page"' : '') + '><span class="sr-tab__icon">' + icon(n.icon) + '</span>' + (n.short || n.label) + '</a>';
    });
    t += '<button class="sr-tab" type="button" data-drawer-toggle style="border:0;background:none"><span class="sr-tab__icon">' + icon('grid') + '</span>Menu</button></nav><div class="sr-toasts" aria-live="polite"></div>';
    b.insertAdjacentHTML('beforeend', t);
  }

  /* theme + pattern */
  function save() { try { localStorage.setItem('sr-theme-v1', JSON.stringify({ mode: h.classList.contains('dark') ? 'dark' : 'light', pattern: h.dataset.pattern })); } catch (e) {} }
  function setPattern(p) { if (!P[p]) return; h.dataset.pattern = p; h.dataset.kind = P[p][0]; h.dataset.ghost = P[p][1]; h.classList.toggle('dark', P[p][2] === 'dark'); save(); }

  /* toasts */
  function toast(msg) {
    var box = document.querySelector('.sr-toasts'); if (!box) return;
    var el = document.createElement('div'); el.className = 'sr-toast'; el.innerHTML = icon('check') + '<span></span>'; el.lastChild.textContent = msg;
    box.appendChild(el); setTimeout(function () { el.remove(); }, 2600);
  }

  /* drawer + sheets: focus moves in, Esc closes, focus returns */
  var lastFocus = null;
  function drawer(open) {
    b.classList.toggle('sr-drawer-open', open);
    document.querySelectorAll('[data-drawer-toggle][aria-controls]').forEach(function (x) { x.setAttribute('aria-expanded', open); });
    if (open) { lastFocus = document.activeElement; var f = document.querySelector('.sr-rail .sr-navlink'); f && f.focus(); } else if (lastFocus) lastFocus.focus();
  }
  function sheet(id, open) {
    var s = document.getElementById(id); if (!s) return;
    s.classList.toggle('is-open', open); s.setAttribute('aria-hidden', !open);
    if (open) { lastFocus = document.activeElement; var f = s.querySelector('button,input,select,a'); f && setTimeout(function () { f.focus(); }, 50); } else if (lastFocus) lastFocus.focus();
  }

  document.addEventListener('click', function (e) {
    var t = e.target.closest('[data-drawer-toggle],[data-drawer-close],[data-mode-toggle],[data-sheet-open],[data-sheet-close],[data-toast],[data-copy],.sr-seg button,.sr-chips .sr-chip,.sr-presets button,[data-pass-toggle]');
    if (!t) { var sh = e.target.classList && e.target.classList.contains('sr-sheet') ? e.target : null; if (sh) sheet(sh.id, false); return; }
    if (t.matches('[data-drawer-toggle]')) drawer(!b.classList.contains('sr-drawer-open'));
    else if (t.matches('[data-drawer-close]')) drawer(false);
    else if (t.matches('[data-mode-toggle]')) { h.classList.toggle('dark'); save(); }
    else if (t.matches('[data-sheet-open]')) sheet(t.dataset.sheetOpen, true);
    else if (t.matches('[data-sheet-close]')) sheet(t.closest('.sr-sheet').id, false);
    else if (t.matches('[data-copy]')) {
      var v = t.dataset.copy || (document.querySelector(t.dataset.copyFrom) || {}).textContent || '';
      (navigator.clipboard ? navigator.clipboard.writeText(v) : Promise.reject()).then(function () { toast('Copied'); }, function () { toast('Copied'); });
    }
    else if (t.matches('[data-pass-toggle]')) { var i = t.parentNode.querySelector('input'); i.type = i.type === 'password' ? 'text' : 'password'; t.setAttribute('aria-pressed', i.type === 'text'); }
    else if (t.matches('[data-toast]')) toast(t.dataset.toast);
    else { t.parentNode.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', x === t); });
      if (t.dataset.amount) { var a = document.getElementById(t.parentNode.dataset.target); if (a) { a.value = t.dataset.amount; a.dispatchEvent(new Event('input')); } } }
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (b.classList.contains('sr-drawer-open')) drawer(false);
    document.querySelectorAll('.sr-sheet.is-open').forEach(function (s) { sheet(s.id, false); });
  });
  document.addEventListener('change', function (e) { if (e.target.matches('[data-pattern-select]')) setPattern(e.target.value); });
  window.matchMedia('(min-width:1024px)').addEventListener('change', function () { drawer(false); });

  shell();
  document.querySelectorAll('[data-pattern-select]').forEach(function (s) { s.value = h.dataset.pattern; });
  window.SR = { toast: toast, sheet: sheet, drawer: drawer, setPattern: setPattern };
})();
