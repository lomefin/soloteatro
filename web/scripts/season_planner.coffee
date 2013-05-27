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
    elements.push $('<input type="checkbox" checked="checked" class="day-activator">').
      attr('name',date.toJSON()+"@selected").
      attr('data-date',date)

    for id in [0,1,2]
      elements.push $('<input type="time" class="input-small time-selector" >').
        attr('name',date.toJSON()+"@"+id).
        attr('data-column',id).
        val(@default_time_values[id])
      elements.push $('<input type="checkbox" checked="checked" class="time-activator">').
        attr('name',date.toJSON()+"@"+id+"@valid").
        attr('data-column',id)
    elements
    

  wrap: ($elements,rowAttrs=null)->
    $wrapper = $('<tr class="rendered-row">')
    console.log "wrapping", rowAttrs
    for attr,value of rowAttrs 
      $wrapper.attr(attr,value)
    $wrapper.append($('<td>').append($element)) for $element in $elements
    $wrapper

  changeTime: (column, time) ->
    $('.time-selector[data-column='+column+']').val(time)

  toggleDay: ($element,value) ->
    $element = $($element)
    $element.toggle(value)
    inputs = $element.find('input')
    if value
      inputs.removeAttr("disabled")
    else
      inputs.attr("disabled","disabled")

  toggleDays: (evt) =>

    $target = $(evt.target)
    target_dow = $target.data('dow')
    for daySelector in $('.day-selector')
      target_dow = $(daySelector).data('dow')
      for row in $('.rendered-row')
        dow = new Date($(row).data('date')).getDay()
        if dow == target_dow
          @toggleDay(row,$(daySelector).is(":checked"))

  renderWeekdaySelectors: ()->
    days = []
    
    daysOfWeek = ['lunes','martes','miércoles','jueves','viernes','sábado','domingo']

    dayCounter = 1
    for weekDay in daysOfWeek
      elements = []
      elements.push $('<label>').attr('for','weekDay:'+weekDay).text(weekDay)
      elements.push $('<input type="checkbox" checked="checked" class="day-selector">')
        .attr('name','weekDay:'+weekDay)
        .attr('data-dow',dayCounter++)
        .change(@toggleDays)
      if dayCounter == 7 
        dayCounter = 0
      days.push elements

    days

  renderHeaderControls: ()->
    elements = []
    elements.push $('<span>').text('Todas')
    elements.push $('<span>')
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
    $weekdaysControls = $('.weekdays-controls')
    $seasonListContainer = $('.presentations')
    $seasonListContainer.empty();
    $weekdaysControls.empty();

    $presentationsHeadControls.append(@wrap(@renderHeaderControls()))
    for $weekday in @renderWeekdaySelectors()
      $weekdaysControls.append(@wrap($weekday))

    current_date = @start_date

    while current_date < @end_date
      $seasonListContainer.append(@wrap(@renderDate(current_date),'data-date':current_date))
      current_date = new Date(current_date.getFullYear(),current_date.getMonth(),current_date.getDate() + 1 )
      @renderDate(current_date,$seasonListContainer)

    $presentationsHead.show()

window.SeasonPlanner ?= new SeasonPlanner()