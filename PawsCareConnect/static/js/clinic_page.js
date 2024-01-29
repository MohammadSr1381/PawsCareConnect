$(document).ready(function(){

    var ratedIndex = -1;

    $('.rating span').click(function(){
        var starId = $(this).attr('id');
        
        ratedIndex = parseInt(starId.replace('star', ''));
        
        // Remove the 'active' class from all <span> elements inside elements with class 'rating'
        $('.rating span').removeClass('active');
        
        // Add the 'active' class to the clicked star and all stars before it
        $('#' + starId).nextAll('span').addBack().addClass('active');

        // Update the text content of the element with id 'ratingValue' to show the selected rating
        $('#ratingValue').text(ratedIndex + 1);

        // Set the rating value in the hidden form field
        $('#ratingInput').val(ratedIndex + 1);
    });

    $('.rating span').each(function(index) {
        var modifiedIndex = 4 - index;
        $(this).attr('id', 'star' + modifiedIndex);
    });

    // Handle the click event for the "ثبت" button
    $('.btn-primary').click(function(){
        // Submit the form
        $('#ratingForm').submit();
    });
});
