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

const depart_picker_element = document.querySelector('.depart-picker');
const selected_date_element = document.querySelector('.depart-picker .selected-date');
const dates_element = document.querySelector('.depart-picker .dates');
const mth_element = document.querySelector('.depart-picker .dates .month .mth');
const next_mth_element = document.querySelector('.depart-picker .dates .month .next-mth');
const prev_mth_element = document.querySelector('.depart-picker .dates .month .prev-mth');
const days_element = document.querySelector('.depart-picker .dates .days');

const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

let date = new Date();
let day = date.getDate();
let month = date.getMonth();
let year = date.getFullYear();

let selectedDate = date;
let selectedDay = day;
let selectedMonth = month;
let selectedYear = year;

mth_element.textContent = months[month] + ' ' + year;

selected_date_element.textContent = formatDate(date);
selected_date_element.dataset.value = selectedDate;

populateDates();

depart_picker_element.addEventListener('click', toggleDatePicker);
next_mth_element.addEventListener('click', goToNextMonth);
prev_mth_element.addEventListener('click', goToPrevMonth);

function toggleDatePicker (e) {
    if (!checkEventPathForClass(e.path, 'dates')) {
        dates_element.classList.toggle('active');
    }
}

function goToNextMonth (e) {
    month++;
    if (month > 11) {
        month = 0;
        year++;
    }
    mth_element.textContent = months[month] + ' ' + year;
    populateDates();
}

function goToPrevMonth (e) {
    month--;
    if (month < 0) {
        month = 11;
        year--;
    }
    mth_element.textContent = months[month] + ' ' + year;
    populateDates();
}

function populateDates (e) {
    days_element.innerHTML = '';
    let amount_days = 31;

    if  (month == 1) {
        amount_days = 28;
    }

    for (let i = 0; i < amount_days; i++) {
        const day_element = document.createElement('div');
        day_element.classList.add('day');
        day_element.textContent = i + 1;

        if (selectedDay = (i + 1) && selectedYear == year && selectedMonth == month) {
            day_element.classList.add('selected');
        }

        day_element.addEventListener('click', function () {
            selectedDate = new Date(year + '-' + (month + 1) + '-' + (i + 1) );
            selectedDay = (i + 1);
            selectedMonth = month;
            selectedYear = year;

            selected_date_element.textContent = formatDate(selectedDate);
            selected_date_element.dataset.value = selectedDate;

            populateDates();
        });

        days_element.appendChild(day_element);
    }
}

function checkEventPathForClass (path, selector) {
    for (let i = 0; i < path; i++) {
        if (path[i].classList && path[i].classList.contains(selector)) {
            return true;
        }
    }
    
    return false;
}

function formatDate (d) {
    let day = d.getDate();
    if (day < 10) {
        day = '0' + day;
    }

    let month = d.getMonth() + 1;
    if (month < 10) {
        month = '0' + month;
    }

    let year = d.getFullYear();

    return day + ' / ' + month + ' / ' + year;
}