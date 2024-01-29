$('.dashboard-section').not(':first').hide();
$('.nav-pills a').click(function(e) {
    e.preventDefault(); 

    $('.nav-pills a.active').removeClass('active');

        // Add active class to the clicked link
    $(this).addClass('active');

    // Get the target section id from the data-target attribute
    var targetSectionId = $(this).data('target');
    console.log("Target section id:", targetSectionId); // Debug statement

    // Hide all sections
    $('.dashboard-section').hide();

    // Show the target section
    $('#' + targetSectionId).show();
});