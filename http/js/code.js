typeaheadSource = function(query, process) {
  var url = 'https://en.wikipedia.org/w/api.php'
  var data = {
    action: 'opensearch',
    limit: 100,
    namespace: 14,
    format: 'json',
    search: query
  }

  $.ajax({
    dataType: 'jsonp',
    url: url,
    data: data,
    success: function(data) {
      var suggestions = []
      $.each(data[1], function(key, value) {
        suggestions.push(value.replace(/^Category:/, ''))
      })
      process(suggestions)
    }
  }) 
}

getDataSuccess = function(data) {
  console.log(data)
  $('#submitBtn').attr('disabled', false)
  $('#submitBtn').removeClass('loading').html('<i class="icon-ok"></i> Done')  
  setTimeout(function() {
    $('#submitBtn').html('Get Data')
  }, 2000)
}

getData = function() {
  var category = scraperwiki.shellEscape($('#category').val())  
  $(this).attr('disabled', true) 
  $(this).addClass('loading').html('Scraping&hellip;')  
  scraperwiki.exec('/home/tool/get_data.py ' + category, getDataSuccess)
}

$(function() {
  $('#category').typeahead({
    source: typeaheadSource,
    items: 8,
    minLength: 1
  })

  $('#submitBtn').on('click', getData)
})
