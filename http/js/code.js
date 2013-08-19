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
    },
    error: function(error) {
      console.log('Unable to connect to Wikipedia: ' + error)
    }
  }) 
}

getDataSuccess = function(data) {
  console.log(data)
  $('#submitBtn').attr('disabled', false)
  $('#submitBtn').removeClass('loading').html('<i class="icon-ok"></i> Done')  
  var query = "select count(*) from swdata;"
  scraperwiki.tool.sql(query, function(data, textStatus, jqXHR) {
    var info_span = data[0]['count(*)'] + ' infoboxes scraped'
    $('.help-inline').text(info_span)
  })  

  setTimeout(function() {
    $('#submitBtn').html('Get Data')
  }, 4000)
}

getData = function() {
  var category = scraperwiki.shellEscape($('#category').val())  
  var includeSubcat = $('#includeSubcat').is(':checked')
  if (includeSubcat) {
    includeSubcat = 't'
  } else {
    includeSubcat = 'f'
  }
  $(this).attr('disabled', true) 
  $(this).addClass('loading').html('Scraping&hellip;')  
  
  scraperwiki.exec('/home/tool/update_db.py ' + category)
  scraperwiki.exec('/home/tool/get_data.py ' + category + includeSubcat.substring(0, 1), getDataSuccess)
}

populateForm = function() {
  var query = "select * from swvariables;" 
  scraperwiki.tool.sql(query, function(data, textStatus, jqXHR) {
    $('#category').val(data[0]['value_blob']);
  })
}

$(function() {
  populateForm()
  $('#category').typeahead({
    source: typeaheadSource,
    items: 8,
    minLength: 1
  })

  $('#submitBtn').on('click', getData)
})
