class SeasonPlanner
  constructor: () -> 
    @start_date = null; 
    @end_date = null; 
    @default_time_values = ["20:00","21:00","22:00"]

  dateChanged: (date, position) =>
    
    @start_date = date if position is 'start'
    @end_date = date if position is 'end'
      
    [@start_date, @end_date] = [@end_date,@start_date] if @end_date < @start_date and @start_date and @end_date
    @triggerRender() if @start_date and @end_date

  renderDate: (date) ->
    elements = []
    elements.push $('<span>').text date.toLocaleDateString()
    
    for id in [0,1,2]
      elements.push $('<input type="time" class="input-small time-selector" >').
        attr('name',date.toJSON()+"@"+id).
        attr('data-column',id).
        val(@default_time_values[id])
      elements.push $('<input type="checkbox" checked="checked" class="time-activator">').
        attr('name',date.toJSON()+"@"+id+"@valid").
        attr('data-column',id)
    elements
    

  wrap: ($elements)->
    $wrapper = $('<tr>')
    $wrapper.append($('<td>').append($element)) for $element in $elements
    $wrapper

  changeTime: (column, time) ->
    $('.time-selector[data-column='+column+']').val(time)

  renderHeaderControls: ()->
    elements = []
    elements.push $('<span>').text('Todas')

    for id in [0,1,2]
      $timeInput = $('<input type="time" class="input-small">').
        attr('name',"all-dates:"+id).
        attr('data-column',id).
        val(@default_time_values[id])
      $timeInput.change((evt)=>
        @changeTime $(evt.target).data('column'),$(evt.target).val()
      )
      $timeCheck = $('<input type="checkbox" checked="checked">').
        attr('name',"select-column:"+id).
        attr('data-column',id)
      $timeCheck.change((evt)->
        target = $(evt.target)
        $toggleableElements = $('.time-activator[data-column='+target.data('column')+']')

        if target.is(':checked')
          $toggleableElements.attr('checked','checked')
        else
          $toggleableElements.removeAttr('checked')

      )
      elements.push $timeInput
      elements.push $timeCheck
    elements
    
  triggerRender: ()->
    $presentationsHead = $('.presentations-head')
    $presentationsHeadControls = $('.presentations-head-controls')
    $seasonListContainer = $('.presentations')
    $seasonListContainer.empty();
    $presentationsHead.show()

    $presentationsHeadControls.append(@wrap(@renderHeaderControls()))
    current_date = @start_date

    while current_date < @end_date
      console.log current_date
      current_date = new Date(current_date.getFullYear(),current_date.getMonth(),current_date.getDate() + 1 )
      $seasonListContainer.append(@wrap(@renderDate(current_date)))

window.SeasonPlanner ?= new SeasonPlanner()