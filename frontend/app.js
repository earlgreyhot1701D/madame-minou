/**
 * Madame Minou — Café-Terrace App Logic
 * State machine: LANDING → INTAKE_NAME → INTAKE_DATE → REVEALING → READING → GO_DEEPER → REVEALING → READING
 *
 * Keys stay server-side. NEVER call the model from the browser.
 * Reading text set via textContent, NEVER innerHTML.
 */

(function () {
  'use strict';

  // ─── State ─────────────────────────────────────────────────────────────────
  const state = {
    catName: '',
    birthDate: '',
    birthTime: '',
    birthCity: '',
    isEstimated: false,
    currentScreen: 'landing',
    hasFirstReading: false,
  };

  // ─── API Config ────────────────────────────────────────────────────────────
  const API_URL = window.__MINOU_API_URL__ || '';
  const MOCK_MODE = !API_URL;

  // ─── DOM References ────────────────────────────────────────────────────────
  const screens = {
    landing: document.getElementById('screen-landing'),
    intake: document.getElementById('screen-intake'),
    reveal: document.getElementById('screen-reveal'),
    reading: document.getElementById('screen-reading'),
  };

  const els = {
    ctaConsult: document.getElementById('cta-consult'),
    formName: document.getElementById('form-name'),
    formDate: document.getElementById('form-date'),
    formDeeper: document.getElementById('form-deeper'),
    inputCatName: document.getElementById('input-cat-name'),
    inputBirthDate: document.getElementById('input-birth-date'),
    inputBirthTime: document.getElementById('input-birth-time'),
    inputBirthCity: document.getElementById('input-birth-city'),
    btnMystery: document.getElementById('btn-mystery'),
    stepName: document.getElementById('intake-step-name'),
    stepDate: document.getElementById('intake-step-date'),
    dateCatNameDisplay: document.getElementById('date-cat-name-display'),
    revealText: document.getElementById('reveal-text'),
    cardTitle: document.getElementById('card-title'),
    cardTier: document.getElementById('card-tier'),
    cardReading: document.getElementById('card-reading'),
    cardFacts: document.getElementById('card-facts'),
    readingCard: document.getElementById('reading-card'),
    goDeeper: document.getElementById('go-deeper'),
    deeperPrompt: document.getElementById('deeper-prompt'),
    btnShare: document.getElementById('btn-share'),
    btnDownload: document.getElementById('btn-download'),
  };

  // ─── Screen Management ─────────────────────────────────────────────────────
  function showScreen(name) {
    Object.values(screens).forEach(s => s.classList.add('hidden'));
    screens[name].classList.remove('hidden');
    state.currentScreen = name;
  }

  // ─── API Call ──────────────────────────────────────────────────────────────
  async function fetchReading(facts) {
    if (MOCK_MODE) {
      return getMockReading(facts);
    }

    const res = await fetch(API_URL + '/reading', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ facts: facts, reading_type: facts.behavior ? 'behavior' : 'natal' }),
    });

    if (!res.ok) throw new Error('HTTP ' + res.status);
    return res.json();
  }

  // ─── Mock Response (local dev without server) ──────────────────────────────
  function getMockReading(facts) {
    const tier = facts.chart_tier || 'date_only';
    const name = facts.cat_name || 'your magnificent feline';
    const sun = facts.sun || 'the Unknown';

    let readingText;

    if (tier === 'full') {
      readingText = 'Ah, ' + name + '! With the sun in ' + sun +
        (facts.moon ? ', the moon in ' + facts.moon : '') +
        (facts.rising ? ', and ' + facts.rising + ' rising' : '') +
        ', this cat is a creature of exquisite complexity. ' +
        'The cosmos has woven them from starlight and sardines in equal measure. ' +
        'Today, the transit of ' + (facts.notable_transit || 'Venus through the 7th house') +
        ' suggests a particularly demanding afternoon nap is in order. ' +
        'Trust the slow blink, cherie.';
    } else if (tier === 'date_only') {
      readingText = 'Mon cher ' + name + '! The sun placed them firmly in ' + sun +
        (facts.moon ? ', with the moon whispering through ' + facts.moon : '') + '. ' +
        'Without the birth time, Madame cannot see the rising sign\u2014but what she sees is magnifique. ' +
        'This is a cat who knows exactly what they want, even if what they want is to knock your coffee off the table. ' +
        'The stars say: let them.';
    } else if (tier === 'estimated') {
      readingText = 'Ah, sweet ' + name + '! The stars are a little shy today\u2014we work with starlight-guesswork, ' +
        'but even guesses from the cosmos carry truth. ' +
        'Sun in ' + sun + ' speaks of a soul who arrived in this world with opinions, ' +
        'and has only grown more certain since. Today is for watching birds and ignoring humans with grace.';
    } else {
      readingText = 'Ah, mysterious ' + name + '! A cat of unknown stars\u2014how fitting, ' +
        'for are cats not the universe\u2019s own mystery? Madame Minou reads the invisible chart: ' +
        'this cat chose YOU, and that is all the horoscope anyone needs. ' +
        'Today, the crystal ball says: extra treats. Non-negotiable.';
    }

    return new Promise(function (resolve) {
      // Simulate AI latency (1.5-3s) to test the reveal sequence
      var delay = 1500 + Math.random() * 1500;
      setTimeout(function () {
        resolve({
          facts: facts,
          reading_text: readingText,
        });
      }, delay);
    });
  }

  // ─── Build Facts Object ────────────────────────────────────────────────────
  function buildFacts() {
    var facts = {
      cat_name: state.catName,
      chart_tier: 'date_only',
      sun: null,
      moon: null,
      moon_cusp: false,
      rising: null,
      notable_transit: null,
      tz_assumption: 'noon UTC',
    };

    if (!state.birthDate && state.isEstimated) {
      facts.chart_tier = 'mystery';
    } else if (state.birthDate && state.birthTime && state.birthCity) {
      facts.chart_tier = 'full';
    } else if (state.birthDate && state.isEstimated) {
      facts.chart_tier = 'estimated';
    } else if (state.birthDate) {
      facts.chart_tier = 'date_only';
    }

    // In mock mode, derive a sun sign from the date for realism
    if (MOCK_MODE && state.birthDate) {
      facts.sun = getSunSignFromDate(state.birthDate);
      facts.moon = getMockMoon(state.birthDate);
      if (facts.chart_tier === 'full') {
        facts.rising = getMockRising();
        facts.notable_transit = 'Saturn trine natal Moon';
        facts.tz_assumption = null;
      }
    }

    return facts;
  }

  // ─── Mock Astrology Helpers ────────────────────────────────────────────────
  function getSunSignFromDate(dateStr) {
    var parts = dateStr.split('-');
    var month = parseInt(parts[1], 10);
    var day = parseInt(parts[2], 10);
    var signs = [
      [1, 20, 'Capricorn'], [2, 19, 'Aquarius'], [3, 20, 'Pisces'],
      [4, 20, 'Aries'], [5, 21, 'Taurus'], [6, 21, 'Gemini'],
      [7, 23, 'Cancer'], [8, 23, 'Leo'], [9, 23, 'Virgo'],
      [10, 23, 'Libra'], [11, 22, 'Scorpio'], [12, 22, 'Sagittarius'],
    ];
    for (var i = 0; i < signs.length; i++) {
      if (month === signs[i][0] && day <= signs[i][1]) {
        return i === 0 ? 'Capricorn' : signs[i - 1][2];
      }
    }
    return 'Sagittarius';
  }

  function getMockMoon(dateStr) {
    var moons = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'];
    var hash = 0;
    for (var i = 0; i < dateStr.length; i++) {
      hash = ((hash << 5) - hash) + dateStr.charCodeAt(i);
    }
    return moons[Math.abs(hash) % 12];
  }

  function getMockRising() {
    var risings = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                   'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'];
    return risings[Math.floor(Math.random() * 12)];
  }

  // ─── Render Reading Card ───────────────────────────────────────────────────
  function renderCard(data) {
    var facts = data.facts || {};
    var readingText = data.reading_text || '';

    // Title — use textContent (NEVER innerHTML)
    els.cardTitle.textContent = facts.cat_name ? facts.cat_name + '\u2019s Reading' : 'Your Reading';

    // Tier badge
    var tierLabels = {
      full: 'Full Chart',
      date_only: 'Estimated Chart',
      estimated: 'Starlight Guesswork',
      mystery: 'Mystery Cat',
    };
    var tierParts = [];
    if (facts.sun) tierParts.push('Sun in ' + facts.sun);
    if (facts.moon) tierParts.push('Moon in ' + facts.moon);
    if (facts.rising) tierParts.push(facts.rising + ' Rising');
    var tierText = tierParts.join(' \u2022 ');
    if (tierLabels[facts.chart_tier]) {
      tierText = (tierText ? tierText + ' \u2022 ' : '') + tierLabels[facts.chart_tier];
    }
    els.cardTier.textContent = tierText;

    // Reading text — textContent, NEVER innerHTML
    els.cardReading.textContent = readingText;

    // Facts summary pills
    els.cardFacts.innerHTML = '';
    var factItems = [];
    if (facts.sun) factItems.push('\u2609 ' + facts.sun);
    if (facts.moon) factItems.push('\u263D ' + facts.moon);
    if (facts.rising) factItems.push('\u2191 ' + facts.rising);
    if (facts.notable_transit) factItems.push('\u2721 ' + facts.notable_transit);
    if (facts.tz_assumption) factItems.push('\u23F0 ' + facts.tz_assumption);

    factItems.forEach(function (text) {
      var pill = document.createElement('span');
      pill.className = 'inline-block bg-surface-bright/40 border border-outline/20 rounded-full px-3 py-1';
      pill.textContent = text;
      els.cardFacts.appendChild(pill);
    });

    // Update go-deeper prompt
    var deeperText = '\u201CMadame Minou can see more\u2026 would you share ' +
      (facts.cat_name || 'your cat') + '\u2019s birth time and city?\u201D';
    els.deeperPrompt.textContent = deeperText;
  }

  // ─── Show Error State (in-voice) ──────────────────────────────────────────
  function showError() {
    els.cardTitle.textContent = 'Oh non\u2026';
    els.cardTier.textContent = '';
    els.cardReading.textContent =
      'Madame Minou\u2019s crystal ball is cloudy tonight. ' +
      'The stars are shy\u2014please try again in a moment, ch\u00E9rie.';
    els.cardFacts.innerHTML = '';
    showScreen('reading');
  }

  // ─── Reveal Sequence ──────────────────────────────────────────────────────
  async function doReveal(facts) {
    // Update anticipation text with cat name
    els.revealText.textContent = '\u201CHmm\u2026 the stars are aligning for ' +
      (facts.cat_name || 'your cat') + '\u2026 one moment, ch\u00E9rie\u2026\u201D';

    showScreen('reveal');

    // Minimum anticipation beat (for theater)
    var minWait = new Promise(function (r) { setTimeout(r, 1200); });

    try {
      var results = await Promise.all([fetchReading(facts), minWait]);
      var data = results[0];

      // Remove previous animation class, re-trigger
      els.readingCard.classList.remove('reveal-card');
      // Force reflow
      void els.readingCard.offsetWidth;

      // Check prefers-reduced-motion
      var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      if (!reducedMotion) {
        els.readingCard.classList.add('reveal-card');
      }

      renderCard(data);
      showScreen('reading');

      // Show go-deeper offer after first reading (not on deeper readings)
      if (!state.hasFirstReading) {
        state.hasFirstReading = true;
        setTimeout(function () {
          els.goDeeper.classList.remove('hidden');
        }, 800);
      }
    } catch (err) {
      console.error('Reading failed:', err);
      showError();
    }
  }

  // ─── Event Handlers ────────────────────────────────────────────────────────

  // CTA: Start consultation
  els.ctaConsult.addEventListener('click', function () {
    showScreen('intake');
    els.stepName.classList.remove('hidden');
    els.stepDate.classList.add('hidden');
    els.inputCatName.focus();
  });

  // Name form submit
  els.formName.addEventListener('submit', function (e) {
    e.preventDefault();
    var name = els.inputCatName.value.trim();
    if (!name) return;

    state.catName = name;
    els.dateCatNameDisplay.textContent = name;
    els.stepName.classList.add('hidden');
    els.stepDate.classList.remove('hidden');
    els.inputBirthDate.focus();
  });

  // Date form submit
  els.formDate.addEventListener('submit', function (e) {
    e.preventDefault();
    state.birthDate = els.inputBirthDate.value || '';
    state.isEstimated = !state.birthDate;

    var facts = buildFacts();
    doReveal(facts);
  });

  // Mystery button ("She's a mystery to me too")
  els.btnMystery.addEventListener('click', function () {
    state.birthDate = '';
    state.isEstimated = true;

    var facts = buildFacts();
    doReveal(facts);
  });

  // Go deeper form submit
  els.formDeeper.addEventListener('submit', function (e) {
    e.preventDefault();
    state.birthTime = els.inputBirthTime.value || '';
    state.birthCity = els.inputBirthCity.value.trim() || '';

    // Hide go-deeper, rebuild facts with additional data
    els.goDeeper.classList.add('hidden');
    var facts = buildFacts();
    doReveal(facts);
  });

  // Share button (Web Share API with fallback)
  els.btnShare.addEventListener('click', function () {
    var text = els.cardReading.textContent;
    var title = els.cardTitle.textContent;

    if (navigator.share) {
      navigator.share({
        title: title,
        text: text,
      }).catch(function () { /* user cancelled */ });
    } else {
      // Fallback: copy to clipboard
      navigator.clipboard.writeText(title + '\n\n' + text).then(function () {
        // TODO: show a toast notification
        alert('Reading copied to clipboard!');
      });
    }
  });

  // Download button (stub — full image rendering is Task 5.1)
  els.btnDownload.addEventListener('click', function () {
    // TODO: Task 5.1 — implement html-to-image card rendering
    var text = els.cardTitle.textContent + '\n\n' + els.cardReading.textContent;
    var blob = new Blob([text], { type: 'text/plain' });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = 'madame-minou-reading.txt';
    a.click();
    URL.revokeObjectURL(url);
  });

  // Nav: Consult link resets to landing
  document.getElementById('nav-consult').addEventListener('click', function (e) {
    e.preventDefault();
    showScreen('landing');
  });

})();
