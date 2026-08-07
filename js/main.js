// MegaProz Consult — shared nav behaviour for every page.
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('year') && (document.getElementById('year').textContent = new Date().getFullYear());

  // Desktop dropdowns open on hover/focus via CSS (:hover / :focus-within).
  // The nav label itself is a real link to the page, so clicking it always
  // navigates — no JS needed for that. This click handler is only a
  // fallback for touch-capable laptops that can't hover: tapping a
  // dropdown parent the first time reveals the menu instead of navigating.
  const items = document.querySelectorAll('.navlinks > li.has-dropdown');
  items.forEach((li) => {
    const trigger = li.querySelector('.navtop');
    if (!trigger) return;
    trigger.addEventListener('click', (e) => {
      if (window.matchMedia('(hover: hover)').matches) return; // real hover devices: let the link navigate
      if (!li.classList.contains('open')) {
        e.preventDefault();
        items.forEach((other) => other.classList.remove('open'));
        li.classList.add('open');
      }
    });
  });
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.has-dropdown')) items.forEach((li) => li.classList.remove('open'));
  });

  // Mobile menu toggle.
  const burger = document.querySelector('.navburger');
  const mobilenav = document.querySelector('.mobilenav');
  if (burger && mobilenav) {
    burger.addEventListener('click', () => mobilenav.classList.toggle('open'));
    document.addEventListener('click', (e) => {
      if (mobilenav.classList.contains('open') && !mobilenav.contains(e.target) && !burger.contains(e.target)) {
        mobilenav.classList.remove('open');
      }
    });
  }

  // Projects page category filter (only present on projects.html).
  const filterBtns = document.querySelectorAll('.proj-filter button');
  const projectCards = document.querySelectorAll('[data-category]');
  if (filterBtns.length && projectCards.length) {
    filterBtns.forEach((btn) => {
      btn.addEventListener('click', () => {
        filterBtns.forEach((b) => b.classList.remove('active'));
        btn.classList.add('active');
        const cat = btn.dataset.filter;
        projectCards.forEach((card) => {
          card.style.display = (cat === 'all' || card.dataset.category === cat) ? '' : 'none';
        });
      });
    });
  }

  // Scroll-reveal: sections marked with class="reveal" ease in as they
  // enter the viewport instead of appearing instantly on load.
  const revealEls = document.querySelectorAll('.reveal');
  if (revealEls.length) {
    if ('IntersectionObserver' in window) {
      const io = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('in-view');
            io.unobserve(entry.target);
          }
        });
      }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
      revealEls.forEach((el) => io.observe(el));
    } else {
      revealEls.forEach((el) => el.classList.add('in-view'));
    }
  }

  // Contact form: submit via fetch instead of a normal browser POST so the
  // visitor never leaves megaprozconsult.com or sees formspree.io at all.
  const contactForm = document.getElementById('contactForm');
  const formStatus = document.getElementById('formStatus');
  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const submitBtn = contactForm.querySelector('button[type="submit"]');
      const originalLabel = submitBtn ? submitBtn.textContent : '';
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = 'Sending...';
      }
      if (formStatus) {
        formStatus.textContent = '';
        formStatus.classList.remove('is-error', 'is-success');
      }

      fetch(contactForm.action, {
        method: 'POST',
        body: new FormData(contactForm),
        headers: { Accept: 'application/json' },
      })
        .then((response) => {
          if (response.ok) {
            contactForm.reset();
            if (formStatus) {
              formStatus.textContent = "Thank you — your request has been sent. We'll be in touch shortly.";
              formStatus.classList.add('is-success');
            }
          } else {
            throw new Error('Submission failed');
          }
        })
        .catch(() => {
          if (formStatus) {
            formStatus.textContent = 'Sorry, something went wrong sending your request. Please call or WhatsApp us directly instead.';
            formStatus.classList.add('is-error');
          }
        })
        .finally(() => {
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.textContent = originalLabel;
          }
        });
    });
  }
});
