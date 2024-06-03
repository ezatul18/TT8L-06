document.addEventListener('DOMContentLoaded', function() {
    const originSelect = document.getElementById('origin');
    const destinationSelect = document.getElementById('destination');
    const switchButton = document.getElementById('switch-btn');

    function updateOptions(selectedValue, selectElement) {
        const options = selectElement.options;
        for (let i = 0; i < options.length; i++) {
            const option = options[i];
            if (option.value === selectedValue) {
                option.disabled = true;
            } else {
                option.disabled = false;
            }
        }
    }

    originSelect.addEventListener('change', function() {
        updateOptions(this.value, destinationSelect);
    });

    destinationSelect.addEventListener('change', function() {
        updateOptions(this.value, originSelect);
    });

    switchButton.addEventListener('click', function() {
        const originValue = originSelect.value;
        const destinationValue = destinationSelect.value;

        originSelect.value = destinationValue;
        destinationSelect.value = originValue;

        updateOptions(destinationValue, originSelect);
        updateOptions(originValue, destinationSelect);
    });
});

$(document).ready(function() {
    $('#depart_date').datetimepicker({
      format: 'YYYY-MM-DD',
      minDate: moment(),
      useCurrent: false,
      widgetPositioning: {
        horizontal: 'auto',
        vertical: 'bottom'
      }
    });
  
    $('#arrival_date').datetimepicker({
      format: 'YYYY-MM-DD',
      minDate: moment(),
      useCurrent: false,
      widgetPositioning: {
        horizontal: 'auto',
        vertical: 'bottom'
      }
    });
  
    $("#depart_date").on("dp.change", function (e) {
      $('#arrival_date').data("DateTimePicker").minDate(e.date);
    });
    
    $("#arrival_date").on("dp.change", function (e) {
      $('#depart_date').data("DateTimePicker").maxDate(e.date);
    });
  
    $("#depart_date").focus(function() {
      $(this).data("DateTimePicker").show();
    });
  
    $("#arrival_date").focus(function() {
      $(this).data("DateTimePicker").show();
    });
  });
  