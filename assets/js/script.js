document.addEventListener("DOMContentLoaded", function () {
    const links = document.querySelectorAll('.nav_link');
    links.forEach(function (link) {
        link.addEventListener('click', function (event) {
            event.preventDefault();
            // Remove 'active' class from all links
            links.forEach(function (link) {
                link.classList.remove('active');
            });
            // Add 'active' class to the clicked link
            link.classList.add('active');
        });
    });
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
