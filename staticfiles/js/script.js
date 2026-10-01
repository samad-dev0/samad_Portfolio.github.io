document.addEventListener("DOMContentLoaded", function () {
    const links = document.querySelectorAll('.nav_link');
    const hamburger = document.querySelector('.hamburger');
    const menuUl = document.querySelector('.menu_ul');
    const counters = document.querySelectorAll('[data-counter]');

    links.forEach(function (link) {
        link.addEventListener('click', function () {
            links.forEach(function (link) {
                link.classList.remove('active');
            });
            link.classList.add('active');

            if (menuUl && hamburger) {
                menuUl.classList.remove('active');
                hamburger.setAttribute('aria-expanded', 'false');
                document.body.classList.remove('menu-open');
            }
        });
    });

    if (hamburger && menuUl) {
        hamburger.addEventListener('click', function () {
            const isOpen = menuUl.classList.toggle('active');
            hamburger.setAttribute('aria-expanded', String(isOpen));
            document.body.classList.toggle('menu-open', isOpen);
        });
    }

    function animateCounter(counter) {
        const finalValue = counter.dataset.counter || counter.textContent.trim();
        const numberMatch = finalValue.match(/-?\d[\d\s.,]*/);
        if (!numberMatch) return;

        const target = Number(numberMatch[0].replace(/[\s.,]/g, ''));
        if (!Number.isFinite(target)) return;

        const prefix = finalValue.slice(0, numberMatch.index);
        const suffix = finalValue.slice(numberMatch.index + numberMatch[0].length);
        const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

        if (reducedMotion) {
            counter.textContent = finalValue;
            return;
        }

        const startTime = performance.now();
        const duration = 1600;

        function updateCounter(currentTime) {
            const progress = Math.min((currentTime - startTime) / duration, 1);
            const easedProgress = 1 - Math.pow(1 - progress, 3);
            const currentValue = Math.round(target * easedProgress).toLocaleString('fr-FR');
            counter.textContent = `${prefix}${currentValue}${progress === 1 ? suffix : ''}`;

            if (progress < 1) {
                window.requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = finalValue;
            }
        }

        counter.textContent = `${prefix}0`;
        window.requestAnimationFrame(updateCounter);
    }

    if ('IntersectionObserver' in window) {
        const counterObserver = new IntersectionObserver(function (entries, observer) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    observer.unobserve(entry.target);
                    animateCounter(entry.target);
                }
            });
        }, { threshold: 0.5 });

        counters.forEach(function (counter) {
            counterObserver.observe(counter);
        });
    } else {
        counters.forEach(animateCounter);
    }
});
function aos_init() {
    AOS.init({
        duration: 800,
        easing: 'slide',
        once: true,
        mirror: false
    });
}

window.addEventListener('load', () => {
    aos_init();
});
