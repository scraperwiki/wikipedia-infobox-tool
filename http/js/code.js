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
  console.log('Done!') 
  console.log(data)
}

getData = function() {
  var category = scraperwiki.shellEscape($('#category').val())  
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
