$(document).ready(function() {
    // Toggle menu visibility
    $('#hamburger-menu').on('click', function() {
        $('#menu').toggle();
    });

    // Show status message when form is submitted
    $('form').on('submit', function() {
        $('#status-message').show();
    });

    // About modal functionality
    var modal = $('#about-modal');
    var closeBtn = $('.close');
    var aboutLink = $('#about-link');

    aboutLink.on('click', function(e) {
        e.preventDefault();
        modal.show();
    });

    closeBtn.on('click', function() {
        modal.hide();
    });

    $(window).on('click', function(e) {
        if ($(e.target).is(modal)) {
            modal.hide();
        }
    });
});
