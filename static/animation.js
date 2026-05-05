/* ============================================================
   SmartTailor — animation.js
   Particle system · Mouse parallax · Scroll reveal
   ============================================================ */

(function () {
  if (window.__stAnimInit) return;
  window.__stAnimInit = true;

  /* ── Inject background elements into <body> ── */
  function injectBg() {
    if (document.getElementById('st-particle-canvas')) return;

    const canvas = document.createElement('canvas');
    canvas.id = 'st-particle-canvas';
    document.body.prepend(canvas);

    ['orb-1', 'orb-2', 'orb-3'].forEach(function (cls) {
      if (!document.querySelector('.st-orb.' + cls)) {
        const orb = document.createElement('div');
        orb.className = 'st-orb ' + cls;
        document.body.prepend(orb);
      }
    });
  }

  /* ── Particle system ── */
  function initParticles() {
    const canvas = document.getElementById('st-particle-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let W, H;

    function resize() {
      W = canvas.width = window.innerWidth;
      H = canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize);

    function rand(a, b) { return Math.random() * (b - a) + a; }

    const COLORS = [
      'rgba(167,139,250,',
      'rgba(96,165,250,',
      'rgba(52,211,153,'
    ];

    function Particle() { this.reset(); }
    Particle.prototype.reset = function () {
      this.x = rand(0, W);
      this.y = rand(0, H);
      this.r = rand(1, 2.5);
      this.vx = rand(-0.3, 0.3);
      this.vy = rand(-0.5, -0.1);
      this.alpha = rand(0.2, 0.7);
      this.color = COLORS[Math.floor(rand(0, COLORS.length))];
      this.life = rand(80, 200);
      this.age = 0;
    };
    Particle.prototype.update = function () {
      this.x += this.vx;
      this.y += this.vy;
      this.age++;
      if (this.age > this.life || this.y < -10) this.reset();
    };
    Particle.prototype.draw = function () {
      var fade = 1 - this.age / this.life;
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
      ctx.fillStyle = this.color + (this.alpha * fade) + ')';
      ctx.fill();
    };

    var particles = [];
    for (var i = 0; i < 120; i++) particles.push(new Particle());

    function animate() {
      ctx.clearRect(0, 0, W, H);
      particles.forEach(function (p) { p.update(); p.draw(); });

      for (var i = 0; i < particles.length; i++) {
        for (var j = i + 1; j < particles.length; j++) {
          var dx = particles[i].x - particles[j].x;
          var dy = particles[i].y - particles[j].y;
          var dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 100) {
            ctx.beginPath();
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.strokeStyle = 'rgba(167,139,250,' + (0.08 * (1 - dist / 100)) + ')';
            ctx.lineWidth = 0.6;
            ctx.stroke();
          }
        }
      }
      requestAnimationFrame(animate);
    }
    animate();
  }

  /* ── Mouse parallax on orbs ── */
  function initParallax() {
    document.addEventListener('mousemove', function (e) {
      var rx = (e.clientX / window.innerWidth - 0.5) * 30;
      var ry = (e.clientY / window.innerHeight - 0.5) * 30;
      document.querySelectorAll('.st-orb').forEach(function (o, i) {
        var factor = (i + 1) * 0.4;
        o.style.transform = 'translate(' + rx * factor + 'px,' + ry * factor + 'px)';
      });
    });
  }

  /* ── Scroll reveal ── */
  function initScrollReveal() {
    var els = document.querySelectorAll('.reveal');
    if (!els.length) return;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) e.target.classList.add('visible');
      });
    }, { threshold: 0.15 });
    els.forEach(function (el) { io.observe(el); });
  }

  /* ── Boot ── */
  function boot() {
    injectBg();
    initParticles();
    initParallax();
    initScrollReveal();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
