document.addEventListener("DOMContentLoaded", function () {
    const links = document.querySelectorAll('.nav_link');
    const hamburger = document.querySelector('.hamburger');
    const menuUl = document.querySelector('.menu_ul');
    const themeToggle = document.querySelector('[data-theme-toggle]');
    const counters = Array.from(document.querySelectorAll('[data-counter]')).filter(function (counter) {
        return !counter.closest('[data-metric-slide]');
    });
    const counterAnimationFrames = new WeakMap();

    if (themeToggle) {
        const themeIcon = themeToggle.querySelector('i');
        const themeLabel = themeToggle.querySelector('[data-theme-label]');
        let currentTheme = 'light';

        function applyTheme(theme) {
            currentTheme = theme;
            document.body.dataset.theme = currentTheme;
            themeToggle.setAttribute('aria-pressed', String(currentTheme === 'light'));
            themeToggle.setAttribute(
                'aria-label',
                currentTheme === 'light' ? 'Activer le thème sombre' : 'Activer le thème clair'
            );
            themeToggle.title = currentTheme === 'light' ? 'Activer le thème sombre' : 'Activer le thème clair';

            if (themeIcon) {
                themeIcon.classList.toggle('fa-sun', currentTheme === 'dark');
                themeIcon.classList.toggle('fa-moon', currentTheme === 'light');
            }
            if (themeLabel) {
                themeLabel.textContent = currentTheme === 'light' ? 'Mode sombre' : 'Mode clair';
            }
        }

        applyTheme(currentTheme);
        themeToggle.addEventListener('click', function () {
            const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
            applyTheme(nextTheme);
        });
    }

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

    const skillTabList = document.querySelector('[data-skill-tabs]');
    if (skillTabList) {
        const skillTabs = Array.from(skillTabList.querySelectorAll('[data-skill-tab]'));
        const skillPanels = Array.from(document.querySelectorAll('[data-skill-panel]'));

        function selectSkillTab(tab, moveFocus) {
            const category = tab.dataset.skillTab;
            skillTabs.forEach(function (skillTab) {
                const isSelected = skillTab === tab;
                skillTab.classList.toggle('is-active', isSelected);
                skillTab.setAttribute('aria-selected', String(isSelected));
                skillTab.tabIndex = isSelected ? 0 : -1;
            });
            skillPanels.forEach(function (panel) {
                panel.hidden = panel.dataset.skillPanel !== category;
            });
            if (moveFocus) tab.focus();
        }

        skillTabs.forEach(function (tab, index) {
            tab.addEventListener('click', function () {
                selectSkillTab(tab, false);
            });
            tab.addEventListener('keydown', function (event) {
                let nextIndex;
                if (event.key === 'ArrowRight') {
                    nextIndex = (index + 1) % skillTabs.length;
                } else if (event.key === 'ArrowLeft') {
                    nextIndex = (index - 1 + skillTabs.length) % skillTabs.length;
                } else if (event.key === 'Home') {
                    nextIndex = 0;
                } else if (event.key === 'End') {
                    nextIndex = skillTabs.length - 1;
                } else {
                    return;
                }
                event.preventDefault();
                selectSkillTab(skillTabs[nextIndex], true);
            });
        });
    }

    function animateCounter(counter) {
        const previousFrame = counterAnimationFrames.get(counter);
        if (previousFrame) window.cancelAnimationFrame(previousFrame);

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
            counterAnimationFrames.delete(counter);
            return;
        }

        const startTime = performance.now();
        const duration = 1600;
        let frameId;

        function updateCounter(currentTime) {
            const progress = Math.min((currentTime - startTime) / duration, 1);
            const easedProgress = 1 - Math.pow(1 - progress, 3);
            const currentValue = Math.round(target * easedProgress).toLocaleString('fr-FR');
            counter.textContent = `${prefix}${currentValue}${progress === 1 ? suffix : ''}`;

            if (progress < 1) {
                frameId = window.requestAnimationFrame(updateCounter);
                counterAnimationFrames.set(counter, frameId);
            } else {
                counter.textContent = finalValue;
                counterAnimationFrames.delete(counter);
            }
        }

        counter.textContent = `${prefix}0`;
        frameId = window.requestAnimationFrame(updateCounter);
        counterAnimationFrames.set(counter, frameId);
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

    const servicesCarousel = document.querySelector('[data-services-carousel]');
    if (servicesCarousel) {
        const servicesTrack = servicesCarousel.querySelector('[data-services-track]');
        const serviceSlides = Array.from(servicesCarousel.querySelectorAll('[data-service-slide]'));
        const serviceDots = Array.from(document.querySelectorAll('[data-service-dot]'));
        const serviceStatus = document.querySelector('[data-service-status]');
        const serviceViewport = servicesCarousel.querySelector('[data-service-viewport]');
        const previousServiceButton = servicesCarousel.querySelector('[data-service-prev]');
        const nextServiceButton = servicesCarousel.querySelector('[data-service-next]');
        const serviceCloneCount = Math.min(3, serviceSlides.length);
        const serviceReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        let activeServiceIndex = 0;
        let servicePosition = serviceCloneCount;
        let serviceTouchStartX = null;

        if (servicesTrack && serviceSlides.length > 0 && previousServiceButton && nextServiceButton) {
            function visibleServiceCount() {
                if (window.matchMedia('(max-width: 768px)').matches) return 1;
                if (window.matchMedia('(max-width: 1024px)').matches) return 2;
                return 3;
            }

            function serviceStep() {
                const firstSlide = servicesTrack.querySelector('[data-service-slide]');
                const gap = parseFloat(window.getComputedStyle(servicesTrack).gap) || 0;
                return firstSlide ? firstSlide.getBoundingClientRect().width + gap : 0;
            }

            function moveServicesTrack(position, animate) {
                servicePosition = position;
                if (!animate) servicesTrack.style.transition = 'none';
                servicesTrack.style.transform = `translate3d(-${servicePosition * serviceStep()}px, 0, 0)`;
                if (!animate) {
                    void servicesTrack.offsetWidth;
                    servicesTrack.style.removeProperty('transition');
                }
            }

            function updateServiceAvailability() {
                const visibleCount = Math.min(visibleServiceCount(), serviceSlides.length);
                serviceSlides.forEach(function (slide, slideIndex) {
                    const distance = (slideIndex - activeServiceIndex + serviceSlides.length) % serviceSlides.length;
                    slide.setAttribute('aria-hidden', String(distance >= visibleCount));
                });
                serviceDots.forEach(function (dot, dotIndex) {
                    const isActive = dotIndex === activeServiceIndex;
                    dot.classList.toggle('is-active', isActive);
                    dot.setAttribute('aria-current', String(isActive));
                });

                if (serviceStatus) {
                    const visibleTitles = Array.from({ length: visibleCount }, function (_, offset) {
                        const slideIndex = (activeServiceIndex + offset) % serviceSlides.length;
                        const title = serviceSlides[slideIndex].querySelector('.service_title');
                        return title ? title.textContent.trim() : '';
                    }).filter(Boolean);
                    const lastVisibleIndex = (activeServiceIndex + visibleCount - 1) % serviceSlides.length;
                    serviceStatus.textContent =
                        `${activeServiceIndex + 1} à ${lastVisibleIndex + 1} sur ${serviceSlides.length} services : ${visibleTitles.join(', ')}`;
                }
            }

            function showService(index, direction, animate) {
                const nextIndex = (index + serviceSlides.length) % serviceSlides.length;
                const movement = direction || (
                    nextIndex === 0 && activeServiceIndex === serviceSlides.length - 1 ? 1 :
                    nextIndex === serviceSlides.length - 1 && activeServiceIndex === 0 ? -1 :
                    Math.sign(nextIndex - activeServiceIndex)
                );
                let nextPosition = serviceCloneCount + nextIndex;

                if (animate && movement === 1 && activeServiceIndex === serviceSlides.length - 1 && nextIndex === 0) {
                    nextPosition = serviceCloneCount + serviceSlides.length;
                } else if (animate && movement === -1 && activeServiceIndex === 0 && nextIndex === serviceSlides.length - 1) {
                    nextPosition = serviceCloneCount - 1;
                }

                activeServiceIndex = nextIndex;
                moveServicesTrack(nextPosition, animate && !serviceReducedMotion);
                updateServiceAvailability();

                if (serviceReducedMotion && (nextPosition < serviceCloneCount || nextPosition >= serviceCloneCount + serviceSlides.length)) {
                    moveServicesTrack(serviceCloneCount + activeServiceIndex, false);
                }
            }

            for (let offset = serviceCloneCount; offset > 0; offset -= 1) {
                const clone = serviceSlides[serviceSlides.length - offset].cloneNode(true);
                clone.removeAttribute('data-service-slide');
                clone.removeAttribute('data-aos');
                clone.removeAttribute('data-aos-delay');
                clone.setAttribute('aria-hidden', 'true');
                clone.setAttribute('inert', '');
                clone.classList.add('is-clone');
                servicesTrack.insertBefore(clone, servicesTrack.firstChild);
            }

            for (let offset = 0; offset < serviceCloneCount; offset += 1) {
                const clone = serviceSlides[offset].cloneNode(true);
                clone.removeAttribute('data-service-slide');
                clone.removeAttribute('data-aos');
                clone.removeAttribute('data-aos-delay');
                clone.setAttribute('aria-hidden', 'true');
                clone.setAttribute('inert', '');
                clone.classList.add('is-clone');
                servicesTrack.appendChild(clone);
            }

            servicesTrack.addEventListener('transitionend', function (event) {
                if (event.target !== servicesTrack || serviceReducedMotion) return;
                if (servicePosition < serviceCloneCount || servicePosition >= serviceCloneCount + serviceSlides.length) {
                    moveServicesTrack(serviceCloneCount + activeServiceIndex, false);
                }
            });

            previousServiceButton.addEventListener('click', function () {
                showService(activeServiceIndex - 1, -1, true);
            });
            nextServiceButton.addEventListener('click', function () {
                showService(activeServiceIndex + 1, 1, true);
            });
            serviceDots.forEach(function (dot) {
                dot.addEventListener('click', function () {
                    showService(Number(dot.dataset.serviceDot), 0, true);
                });
            });

            servicesCarousel.addEventListener('keydown', function (event) {
                if (event.target.closest('button')) return;
                if (event.key === 'ArrowLeft') {
                    event.preventDefault();
                    showService(activeServiceIndex - 1, -1, true);
                } else if (event.key === 'ArrowRight') {
                    event.preventDefault();
                    showService(activeServiceIndex + 1, 1, true);
                } else if (event.key === 'Home') {
                    event.preventDefault();
                    showService(0, 0, true);
                } else if (event.key === 'End') {
                    event.preventDefault();
                    showService(serviceSlides.length - 1, 0, true);
                }
            });

            if (serviceViewport) {
                serviceViewport.addEventListener('touchstart', function (event) {
                    serviceTouchStartX = event.changedTouches[0].clientX;
                }, { passive: true });
                serviceViewport.addEventListener('touchend', function (event) {
                    if (serviceTouchStartX === null) return;
                    const swipeDistance = event.changedTouches[0].clientX - serviceTouchStartX;
                    serviceTouchStartX = null;
                    if (Math.abs(swipeDistance) < 50) return;
                    const direction = swipeDistance < 0 ? 1 : -1;
                    showService(activeServiceIndex + direction, direction, true);
                }, { passive: true });
            }

            let serviceResizeFrame = 0;
            window.addEventListener('resize', function () {
                window.cancelAnimationFrame(serviceResizeFrame);
                serviceResizeFrame = window.requestAnimationFrame(function () {
                    moveServicesTrack(serviceCloneCount + activeServiceIndex, false);
                    updateServiceAvailability();
                });
            });

            servicesCarousel.dataset.carouselReady = 'true';
            moveServicesTrack(servicePosition, false);
            updateServiceAvailability();
        }
    }

    const carousel = document.querySelector('[data-metrics-carousel]');
    if (!carousel) return;

    const track = carousel.querySelector('[data-carousel-track]');
    const slides = Array.from(carousel.querySelectorAll('[data-metric-slide]'));
    const dots = Array.from(document.querySelectorAll('[data-carousel-dot]'));
    const status = document.querySelector('[data-carousel-status]');
    const previousButton = carousel.querySelector('[data-carousel-prev]');
    const nextButton = carousel.querySelector('[data-carousel-next]');
    const viewport = carousel.querySelector('[data-carousel-viewport]');
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    let activeIndex = 0;
    let carouselPosition = slides.length;
    let visibleCount = 1;
    let touchStartX = null;

    if (!track || !viewport || slides.length === 0 || !previousButton || !nextButton) return;
    carousel.dataset.carouselReady = 'true';

    function cloneMetricSlide(slide) {
        const clone = slide.cloneNode(true);
        clone.removeAttribute('data-metric-slide');
        clone.setAttribute('aria-hidden', 'true');
        clone.setAttribute('inert', '');
        clone.classList.remove('is-active');
        clone.classList.add('is-clone');
        const counter = clone.querySelector('[data-counter]');
        if (counter) counter.removeAttribute('data-counter');
        return clone;
    }

    for (let index = slides.length - 1; index >= 0; index -= 1) {
        track.insertBefore(cloneMetricSlide(slides[index]), track.firstChild);
    }
    slides.forEach(function (slide) {
        track.appendChild(cloneMetricSlide(slide));
    });

    function getVisibleCount() {
        if (window.matchMedia('(max-width: 640px)').matches) return 1;
        if (window.matchMedia('(max-width: 1024px)').matches) return Math.min(2, slides.length);
        return Math.min(4, slides.length);
    }

    function updateMetricLayout() {
        visibleCount = getVisibleCount();
        carousel.dataset.visibleSlides = String(visibleCount);
        const gap = parseFloat(window.getComputedStyle(track).gap) || 0;
        const slideWidth = (viewport.clientWidth - gap * (visibleCount - 1)) / visibleCount;
        track.style.setProperty('--metric-slide-width', `${slideWidth}px`);
    }

    function metricStep() {
        const firstSlide = track.firstElementChild;
        const gap = parseFloat(window.getComputedStyle(track).gap) || 0;
        return firstSlide ? firstSlide.getBoundingClientRect().width + gap : 0;
    }

    function moveMetricTrack(position, animate) {
        carouselPosition = position;
        if (!animate) track.style.transition = 'none';
        track.style.transform = `translate3d(-${carouselPosition * metricStep()}px, 0, 0)`;
        if (!animate) {
            void track.offsetWidth;
            if (reducedMotion) {
                track.style.transition = 'none';
            } else {
                track.style.removeProperty('transition');
            }
        }
    }

    function updateMetricVisibility() {
        slides.forEach(function (slide, slideIndex) {
            const distance = (slideIndex - activeIndex + slides.length) % slides.length;
            const isVisible = distance < visibleCount;
            slide.classList.toggle('is-active', isVisible);
            slide.setAttribute('aria-hidden', String(!isVisible));
        });

        dots.forEach(function (dot, dotIndex) {
            const isActive = dotIndex === activeIndex;
            dot.classList.toggle('is-active', isActive);
            dot.setAttribute('aria-current', String(isActive));
        });

        if (status) {
            const lastVisibleIndex = (activeIndex + visibleCount - 1) % slides.length;
            const visibleTitles = Array.from({ length: visibleCount }, function (_, offset) {
                const slideIndex = (activeIndex + offset) % slides.length;
                const title = slides[slideIndex].querySelector('h3');
                return title ? title.textContent.trim() : '';
            }).filter(Boolean);
            status.textContent =
                `${activeIndex + 1} à ${lastVisibleIndex + 1} sur ${slides.length} : ${visibleTitles.join(', ')}`;
        }
    }

    function animateVisibleMetricCounters(direction) {
        if (direction === 1 || direction === -1) {
            const enteringIndex = direction === 1 ?
                (activeIndex + visibleCount - 1) % slides.length :
                activeIndex;
            const counter = slides[enteringIndex].querySelector('[data-counter]');
            if (counter) animateCounter(counter);
            return;
        }

        for (let offset = 0; offset < visibleCount; offset += 1) {
            const slideIndex = (activeIndex + offset) % slides.length;
            const counter = slides[slideIndex].querySelector('[data-counter]');
            if (counter) animateCounter(counter);
        }
    }

    function showSlide(index, direction, animate) {
        const nextIndex = (index + slides.length) % slides.length;
        const movement = direction || (
            nextIndex === 0 && activeIndex === slides.length - 1 ? 1 :
            nextIndex === slides.length - 1 && activeIndex === 0 ? -1 :
            Math.sign(nextIndex - activeIndex)
        );
        let nextPosition = slides.length + nextIndex;

        if (animate && !reducedMotion && movement === 1 &&
            activeIndex === slides.length - 1 && nextIndex === 0) {
            nextPosition = slides.length * 2;
        } else if (animate && !reducedMotion && movement === -1 &&
            activeIndex === 0 && nextIndex === slides.length - 1) {
            nextPosition = slides.length - 1;
        }

        activeIndex = nextIndex;
        moveMetricTrack(nextPosition, animate && !reducedMotion);
        updateMetricVisibility();
        animateVisibleMetricCounters(direction);
    }

    track.addEventListener('transitionend', function (event) {
        if (event.target !== track || reducedMotion) return;

        if (carouselPosition < slides.length ||
            carouselPosition >= slides.length * 2) {
            moveMetricTrack(slides.length + activeIndex, false);
        }
    });

    previousButton.addEventListener('click', function () {
        showSlide(activeIndex - 1, -1, true);
    });

    nextButton.addEventListener('click', function () {
        showSlide(activeIndex + 1, 1, true);
    });

    dots.forEach(function (dot) {
        dot.addEventListener('click', function () {
            showSlide(Number(dot.dataset.carouselDot), 0, true);
        });
    });

    carousel.addEventListener('keydown', function (event) {
        if (event.target.closest('button')) return;

        if (event.key === 'ArrowLeft') {
            event.preventDefault();
            showSlide(activeIndex - 1, -1, true);
        } else if (event.key === 'ArrowRight') {
            event.preventDefault();
            showSlide(activeIndex + 1, 1, true);
        } else if (event.key === 'Home') {
            event.preventDefault();
            showSlide(0, 0, true);
        } else if (event.key === 'End') {
            event.preventDefault();
            showSlide(slides.length - 1, 0, true);
        }
    });

    if (viewport) {
        viewport.addEventListener('touchstart', function (event) {
            touchStartX = event.changedTouches[0].clientX;
        }, { passive: true });

        viewport.addEventListener('touchend', function (event) {
            if (touchStartX === null) return;

            const swipeDistance = event.changedTouches[0].clientX - touchStartX;
            touchStartX = null;
            if (Math.abs(swipeDistance) < 50) return;

            const direction = swipeDistance < 0 ? 1 : -1;
            showSlide(activeIndex + direction, direction, true);
        }, { passive: true });
    }

    let metricResizeFrame = 0;
    window.addEventListener('resize', function () {
        window.cancelAnimationFrame(metricResizeFrame);
        metricResizeFrame = window.requestAnimationFrame(function () {
            updateMetricLayout();
            moveMetricTrack(slides.length + activeIndex, false);
            updateMetricVisibility();
        });
    });

    updateMetricLayout();
    moveMetricTrack(carouselPosition, false);
    updateMetricVisibility();
    animateVisibleMetricCounters(0);
});
function aos_init() {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        document.querySelectorAll('[data-aos]').forEach(function (element) {
            element.classList.add('aos-animate');
        });
        return;
    }

    AOS.init({
        duration: 750,
        easing: 'ease-out-cubic',
        once: true,
        mirror: false,
        offset: 70
    });
}

window.addEventListener('load', () => {
    aos_init();
});
