var tg = window.Telegram ? window.Telegram.WebApp : null;
var API = '';
var currentUser = null;
var currentCase = null;
var rollAnimation = null;

function getInitData() {
  if (tg && tg.initData) return tg.initData;
  return '';
}

function api(url, options) {
  options = options || {};
  options.headers = options.headers || {};
  options.headers['X-Init-Data'] = getInitData();
  if (options.body && typeof options.body === 'object') {
    options.headers['Content-Type'] = 'application/json';
    options.body = JSON.stringify(options.body);
  }
  return fetch(API + url, options).then(function(r) {
    if (!r.ok) return r.text().then(function(t){ throw new Error(t); });
    return r.json();
  });
}

function showToast(text, isError) {
  var t = document.getElementById('toast');
  if (!t) return;
  t.textContent = text;
  t.className = 'toast show' + (isError ? ' error' : '');
  clearTimeout(t._timer);
  t._timer = setTimeout(function(){ t.classList.remove('show'); }, 2500);
}

function updateBalance(stars, crystals) {
  var s = document.getElementById('stars-balance');
  var c = document.getElementById('crystals-balance');
  if (s && stars !== undefined) s.textContent = stars;
  if (c && crystals !== undefined) c.textContent = crystals;
}

function closeModal() {
  var m = document.getElementById('modal');
  if (m) m.classList.remove('show');
}

function initPage(page) {
  if (tg) {
    tg.ready();
    tg.expand();
    try { tg.setHeaderColor('#0a0e14'); } catch(e){}
  }
  if (page === 'index') loadIndex();
  else if (page === 'case') loadCase();
  else if (page === 'profile') loadProfile();
}

// ========== INDEX ==========
function loadIndex() {
  api('/api/me').then(function(me){
    currentUser = me;
    updateBalance(me.stars, me.crystals);
  }).catch(function(e){
    showToast('Ошибка авторизации', true);
    console.error(e);
  });

  api('/api/cases').then(function(cases){
    var grid = document.getElementById('cases-grid');
    if (!grid) return;
    var html = '';
    cases.forEach(function(c){
      var priceText = c.price === 0 ? 'Бесплатно' : '⭐ ' + c.price;
      var priceClass = c.price === 0 ? 'free' : '';
      html += '<div class="case-card" style="--case-color:' + c.color + '" onclick="location.href=\'/case?id=' + c.id + '\'">' +
        '<div class="case-card-emoji">' + c.emoji + '</div>' +
        '<div class="case-card-name">' + c.name + '</div>' +
        '<div class="case-card-price ' + priceClass + '">' + priceText + '</div>' +
      '</div>';
    });
    grid.innerHTML = html;
  }).catch(function(e){
    document.getElementById('cases-grid').innerHTML = '<div class="loading">Ошибка загрузки</div>';
  });

  var liveItems = ['🧸','⭐','🎀','🪔','🖊️','🎭','👑','💍','💎','🐻','😇','🦁','🐼','🕹️','🎮','🥽','✨','💿','🎒','🦋','🚀','👼','☁️','💀','🧪','🏴‍☠️','🧞','⌚','🫙','🌈','🧞‍♂️','❄️','📦','🥊','🧪'];
  var liveEl = document.getElementById('live-items');
  if (liveEl) {
    var doubled = liveItems.concat(liveItems);
    var html2 = '';
    doubled.forEach(function(e){ html2 += '<div class="live-item">' + e + '</div>'; });
    liveEl.innerHTML = html2;
  }
}

// ========== CASE ==========
function loadCase() {
  var params = new URLSearchParams(location.search);
  var caseId = params.get('id') || 'free';

  api('/api/me').then(function(me){
    currentUser = me;
    updateBalance(me.stars, me.crystals);
  });

  api('/api/case/' + caseId).then(function(c){
    currentCase = c;
    var title = document.getElementById('case-title');
    var price = document.getElementById('case-price');
    if (title) title.textContent = c.emoji + ' ' + c.name;
    if (price) price.textContent = c.price === 0 ? 'Бесплатно' : '⭐ ' + c.price;

    var itemsGrid = document.getElementById('items-grid');
    if (itemsGrid) {
      var html = '';
      c.items.forEach(function(it){
        var color = rarityColor(it.rarity);
        html += '<div class="item-card" style="border-color:' + color + '40">' +
          '<span class="it-emoji">' + it.emoji + '</span>' +
          '<div class="it-name">' + it.name + '</div>' +
          '<div class="it-value" style="color:' + color + '">' + it.value + ' ⭐</div>' +
        '</div>';
      });
      itemsGrid.innerHTML = html;
    }

    var btn = document.getElementById('open-btn');
    if (btn) {
      btn.textContent = c.price === 0 ? 'Крутить бесплатно' : 'Крутить за ⭐ ' + c.price;
    }

    fillRoulettePlaceholder(c);
  });
}

function rarityColor(r) {
  return {
    common: '#8b95a5',
    rare: '#3b82f6',
    epic: '#a371f7',
    legendary: '#ffcc00',
    mythic: '#ef4444'
  }[r] || '#888';
}

function fillRoulettePlaceholder(c) {
  var track = document.getElementById('roulette-track');
  if (!track) return;
  var html = '';
  for (var i = 0; i < 30; i++) {
    var it = c.items[i % c.items.length];
    html += '<div class="roulette-item rarity-' + it.rarity + '">' +
      '<span class="it-emoji">' + it.emoji + '</span>' +
      '<span class="it-name">' + it.name + '</span>' +
    '</div>';
  }
  track.innerHTML = html;
  track.style.transform = 'translateX(0)';
}

function doOpen() {
  if (!currentCase) return;
  var btn = document.getElementById('open-btn');
  btn.disabled = true;
  btn.textContent = 'Крутим...';

  api('/api/open', {
    method: 'POST',
    body: { case_id: currentCase.id }
  }).then(function(res) {
    playRoll(res.item, res.roll, currentCase);
    updateBalance(res.newBalance, currentUser ? currentUser.crystals : 0);
  }).catch(function(e) {
    btn.disabled = false;
    btn.textContent = currentCase.price === 0 ? 'Крутить бесплатно' : 'Крутить за ⭐ ' + currentCase.price;
    var msg = 'Ошибка';
    try { msg = JSON.parse(e.message).detail || msg; } catch(err){}
    if (e.message.indexOf('not enough') >= 0) msg = 'Недостаточно звёзд';
    showToast(msg, true);
  });
}

function playRoll(winItem, rollData, c) {
  var track = document.getElementById('roulette-track');
  if (!track) return;

  var items = rollData.items;
  var winIndex = rollData.win_index || 35;

  var html = '';
  items.forEach(function(it, i) {
    var isWin = (i === winIndex);
    var itFinal = isWin ? winItem : it;
    html += '<div class="roulette-item rarity-' + itFinal.rarity + '">' +
      '<span class="it-emoji">' + itFinal.emoji + '</span>' +
      '<span class="it-name">' + itFinal.name + '</span>' +
    '</div>';
  });
  track.innerHTML = html;

  var itemWidth = 100;
  var wrapWidth = track.parentElement.offsetWidth;
  var winOffset = winIndex * itemWidth;
  var centerOffset = winOffset - (wrapWidth / 2) + (itemWidth / 2);
  var jitter = Math.random() * 30 - 15;
  centerOffset += jitter;

  track.style.transition = 'none';
  track.style.transform = 'translateX(0)';
  track.offsetHeight;

  track.style.transition = 'transform 4s cubic-bezier(0.15, 0.9, 0.3, 1)';
  track.style.transform = 'translateX(-' + centerOffset + 'px)';

  setTimeout(function() {
    showWinModal(winItem);
    var btn = document.getElementById('open-btn');
    btn.disabled = false;
    btn.textContent = c.price === 0 ? 'Крутить бесплатно' : 'Крутить за ⭐ ' + c.price;

    api('/api/me').then(function(me){
      currentUser = me;
      updateBalance(me.stars, me.crystals);
    });
  }, 4200);
}

function showWinModal(item) {
  var m = document.getElementById('modal');
  var mc = document.getElementById('modal-content');
  if (!m || !mc) return;

  var color = rarityColor(item.rarity);

  mc.innerHTML =
    '<div class="modal-emoji" style="color:' + color + '">' + item.emoji + '</div>' +
    '<div class="modal-title">' + item.name + '</div>' +
    '<div class="modal-rarity" style="color:' + color + '">' + rarityName(item.rarity) + '</div>' +
    '<div class="modal-value">' + item.value + ' ⭐</div>' +
    '<button class="modal-btn" onclick="closeModal()">Забрать</button>';

  m.classList.add('show');
  if (tg && tg.HapticFeedback) {
    try {
      if (item.rarity === 'mythic' || item.rarity === 'legendary') {
        tg.HapticFeedback.notificationOccurred('success');
      } else {
        tg.HapticFeedback.impactOccurred('light');
      }
    } catch(e){}
  }
  spawnConfetti(color);
}

function rarityName(r) {
  return {
    common: 'Обычный',
    rare: 'Редкий',
    epic: 'Эпический',
    legendary: 'Легендарный',
    mythic: 'Мифический'
  }[r] || r;
}

function spawnConfetti(color) {
  var count = 30;
  for (var i = 0; i < count; i++) {
    var c = document.createElement('div');
    c.className = 'confetti';
    c.style.position = 'fixed';
    c.style.left = (Math.random() * 100) + '%';
    c.style.top = '-20px';
    c.style.width = '8px';
    c.style.height = '8px';
    c.style.background = color;
    c.style.borderRadius = Math.random() > 0.5 ? '50%' : '0';
    c.style.opacity = '0.9';
    c.style.pointerEvents = 'none';
    c.style.zIndex = '999';
    c.style.transition = 'transform 2s ease-out, opacity 2s';
    document.body.appendChild(c);
    (function(el, delay) {
      setTimeout(function() {
        var x = (Math.random() - 0.5) * 400;
        var y = window.innerHeight + 100;
        el.style.transform = 'translate(' + x + 'px,' + y + 'px) rotate(' + (Math.random()*720) + 'deg)';
        el.style.opacity = '0';
      }, delay);
      setTimeout(function() { el.remove(); }, 2500 + delay);
    })(c, i * 15);
  }
}

// ========== PROFILE ==========
function loadProfile() {
  api('/api/me').then(function(me){
    currentUser = me;
    updateBalance(me.stars, me.crystals);
    var name = document.getElementById('profile-name');
    if (name) name.textContent = me.first_name || me.username || 'Игрок';
    document.getElementById('stat-opened').textContent = me.total_opened;
    document.getElementById('stat-spent').textContent = me.total_spent + ' ⭐';
    document.getElementById('stat-won').textContent = me.total_won + ' ⭐';
  });

  api('/api/inventory').then(function(inv){
    var grid = document.getElementById('inventory-grid');
    if (!grid) return;
    if (!inv.length) {
      grid.innerHTML = '<div class="loading">Инвентарь пуст</div>';
      return;
    }
    var html = '';
    inv.forEach(function(it){
      var color = rarityColor(it.item_rarity);
      html += '<div class="inv-card" style="--rarity-color:' + color + '">' +
        '<span class="it-emoji">' + it.item_emoji + '</span>' +
        '<div class="it-name">' + it.item_name + '</div>' +
        '<div class="it-rarity">' + rarityName(it.item_rarity) + '</div>' +
        '<div class="it-value">' + it.item_value + ' ⭐</div>' +
        '<button class="sell-btn" onclick="sellItem(' + it.id + ', ' + Math.floor(it.item_value * 0.7) + ')">Продать за ' + Math.floor(it.item_value * 0.7) + '</button>' +
      '</div>';
    });
    grid.innerHTML = html;
  });
}

function sellItem(itemId, price) {
  if (!confirm('Продать за ' + price + ' ⭐?')) return;
  api('/api/sell', {
    method: 'POST',
    body: { item_id: itemId }
  }).then(function(res){
    showToast('Продано за ' + res.sold_for + ' ⭐');
    loadProfile();
  }).catch(function(e){
    showToast('Ошибка продажи', true);
  });
}

// ========== TOP / PROFILE OPEN ==========
function openProfile() {
  location.href = '/profile';
}

function openTop() {
  api('/api/top').then(function(rows){
    var m = document.getElementById('modal');
    var mc = document.getElementById('modal-content');
    if (!m || !mc) return;
    var html = '<div class="modal-title" style="margin-bottom:16px">🏆 Топ игроков</div>';
    if (!rows.length) {
      html += '<div style="color:var(--text-dim)">Пока пусто</div>';
    } else {
      rows.forEach(function(r, i) {
        var medal = i === 0 ? '🥇' : (i === 1 ? '🥈' : (i === 2 ? '🥉' : (i+1) + '.'));
        var name = r.first_name || r.username || 'Игрок';
        html += '<div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--border);font-size:13px;">' +
          '<span>' + medal + ' <b>' + name + '</b></span>' +
          '<span style="color:var(--accent);font-weight:800">' + r.total_won + ' ⭐</span>' +
        '</div>';
      });
    }
    html += '<button class="modal-btn" style="margin-top:16px" onclick="closeModal()">Закрыть</button>';
    mc.innerHTML = html;
    m.classList.add('show');
  });
}

document.addEventListener('click', function(e) {
  if (e.target.classList && e.target.classList.contains('modal')) {
    closeModal();
  }
});

window.initPage = initPage;
window.doOpen = doOpen;
window.closeModal = closeModal;
window.openProfile = openProfile;
window.openTop = openTop;
window.sellItem = sellItem;
