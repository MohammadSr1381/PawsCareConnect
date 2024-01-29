$('#filterInput').on('input', function() {
    var filterValue = $(this).val().toLowerCase();
    $('.filter-checkbox').each(function() {
        var textContent = $(this).next('.form-check-label').text().toLowerCase();
        $(this).closest('.form-check').toggle(textContent.includes(filterValue));
    });
  });