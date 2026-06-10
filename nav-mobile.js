(function () {
    // Keep dropdowns open on touch — CSS :hover vanishes when finger lifts
    var style = document.createElement('style');
    style.textContent =
        '@media (max-width: 1024px) {' +
        '  .menu-item.dropdown.open > .dropdown-menu { display: block !important; }' +
        '}';
    document.head.appendChild(style);

    function isMobile() { return window.innerWidth <= 1024; }

    document.addEventListener('DOMContentLoaded', function () {

        // Tap on dropdown trigger: first tap opens, second tap follows the link
        document.querySelectorAll('.menu-item.dropdown > .menu-link').forEach(function (link) {
            link.addEventListener('click', function (e) {
                if (!isMobile()) return;
                var item = this.closest('.menu-item');
                if (!item.classList.contains('open')) {
                    e.preventDefault();
                    // Close any other open dropdowns
                    document.querySelectorAll('.menu-item.dropdown.open').forEach(function (other) {
                        other.classList.remove('open');
                    });
                    item.classList.add('open');
                }
                // Already open → allow normal navigation (don't preventDefault)
            });
        });

        // Close dropdowns when main menu is closed via checkbox
        var toggle = document.getElementById('menu-toggle');
        if (toggle) {
            toggle.addEventListener('change', function () {
                if (!this.checked) {
                    document.querySelectorAll('.menu-item.dropdown.open').forEach(function (item) {
                        item.classList.remove('open');
                    });
                }
            });
        }

        // Close dropdowns when tapping outside the menu
        document.addEventListener('click', function (e) {
            if (!isMobile()) return;
            if (!e.target.closest('.menu-item.dropdown')) {
                document.querySelectorAll('.menu-item.dropdown.open').forEach(function (item) {
                    item.classList.remove('open');
                });
            }
        });
    });
})();
