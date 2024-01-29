$(document).ready(function(){
    // Initially, no stars are selected
    var ratedIndex = -1;

    $('.rating span').click(function(){
        // Get index of clicked star
        ratedIndex = 5 - $(this).index();
        console.log(ratedIndex);
        // Remove active class from all stars
        $('.rating span').removeClass('active');
        // Add active class to clicked star and all previous stars
        for (var i = 5; i <= ratedIndex-1; i--) {
            $('.rating span:eq('+i+')').addClass('active');
        }
        // Update rating value in the paragraph
        $('#ratingValue').text(ratedIndex);
    });
});