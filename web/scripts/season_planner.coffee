class SeasonPlanner
  constructor: () -> 
    @start_date = null; 
    @end_date = null; 
  
  dateChanged: (date, position) =>
    
    @start_date = date if position is 'start'
    @end_date = date if position is 'end'
      
    [@start_date, @end_date] = [@end_date,@start_date] if @end_date < @start_date and @start_date and @end_date
    @triggerRender() if @start_date and @end_date

  triggerRender: ()->
    $seasonListContainer = $('.presentations')
    $seasonListContainer.empty();

    current_date = @start_date

    while current_date < @end_date
      console.log current_date
      current_date = new Date(current_date.getFullYear(),current_date.getMonth(),current_date.getDate() + 1 )

window.SeasonPlanner ?= new SeasonPlanner()