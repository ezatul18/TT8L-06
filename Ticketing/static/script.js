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
const depart_selected_date_element = document.querySelector('.depart-picker .selected-date');
const depart_dates_element = document.querySelector('.depart-picker .dates');
const depart_mth_element = document.querySelector('.depart-picker .dates .month .mth');
const depart_next_mth_element = document.querySelector('.depart-picker .dates .month .next-mth');
const depart_prev_mth_element = document.querySelector('.depart-picker .dates .month .prev-mth');
const depart_days_element = document.querySelector('.depart-picker .dates .days');

const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

let departDate = new Date();
let departDay = departDate.getDate();
let departMonth = departDate.getMonth();
let departYear = departDate.getFullYear();

let departSelectedDate = departDate;
let departSelectedDay = departDay;
let departSelectedMonth = departMonth;
let departSelectedYear = departYear;

depart_mth_element.textContent = months[departMonth] + ' ' + departYear;

depart_selected_date_element.textContent = formatDate(departDate);
depart_selected_date_element.dataset.value = departSelectedDate;

populateDepartDates();

depart_picker_element.addEventListener('click', toggleDatePicker(e, depart_dates_element));
depart_next_mth_element.addEventListener('click', goToNextMonth(e, 'depart'));
depart_prev_mth_element.addEventListener('click', goToPrevMonth(e, 'depart'));

const arrival_picker_element = document.querySelector('.arrival-picker');
const arrival_selected_date_element = document.querySelector('.arrival-picker .selected-date');
const arrival_dates_element = document.querySelector('.arrival-picker .dates');
const arrival_mth_element = document.querySelector('.arrival-picker .dates .month .mth');
const arrival_next_mth_element = document.querySelector('.arrival-picker .dates .month .next-mth');
const arrival_prev_mth_element = document.querySelector('.arrival-picker .dates .month .prev-mth');
const arrival_days_element = document.querySelector('.arrival-picker .dates .days');

let arrivalDate = new Date();
let arrivalDay = arrivalDate.getDate();
let arrivalMonth = arrivalDate.getMonth();
let arrivalYear = arrivalDate.getFullYear();

let arrivalSelectedDate = arrivalDate;
let arrivalSelectedDay = arrivalDay;
let arrivalSelectedMonth = arrivalMonth;
let arrivalSelectedYear = arrivalYear;

arrival_mth_element.textContent = months[arrivalMonth] + ' ' + arrivalYear;

arrival_selected_date_element.textContent = formatDate(arrivalDate);
arrival_selected_date_element.dataset.value = arrivalSelectedDate;

populateArrivalDates();

arrival_picker_element.addEventListener('click', toggleDatePicker(e, arrival_dates_element));
arrival_next_mth_element.addEventListener('click', goToNextMonth(e, 'arrival'));
arrival_prev_mth_element.addEventListener('click', goToPrevMonth(e, 'arrival'));

function toggleDatePicker (e) {
    if (!checkEventPathForClass(e.path, 'dates')) {
        dates_element.classList.toggle('active');
    }
}

function goToNextMonth (e, type) {
    if (type === 'depart') {
        departMonth++;
        if (departMonth > 11) {
            departMonth = 0;
            departYear++;
        }
        depart_mth_element.textContent = months[departMonth] + ' ' + departYear;
        populateDepartDates();
    }
    else {
        arrivalMonth++;
        if (arrivalMonth > 11) {
            arrivalMonth = 0;
            arrivalYear++;
        }
        arrival_mth_element.textContent = months[arrivalMonth] + ' ' + arrivalYear;
        populateArrivalDates();
    }
}

function goToPrevMonth (e, type) {
    if (type === 'depart') {
        departMonth--;
        if (departMonth < 0) {
            departMonth = 11;
            departYear--;
        }
        depart_mth_element.textContent = months[departMonth] + ' ' + departYear;
        populateDepartDates();
    }
    else {
        arrivalMonth--;
        if (arrivalMonth < 0) {
            arrivalMonth = 11;
            arrivalYear--;
        }
        arrival_mth_element.textContent = months[arrivalMonth] + ' ' + arrivalYear;
        populateArrivalDates();
    }
}

function populateDepartDates (e) {
    depart_days_element.innerHTML = '';
    let amount_days = 31;

    if  (departMonth == 1) {
        amount_days = 28;
    }

    for (let i = 0; i < amount_days; i++) {
        const day_element = document.createElement('div');
        day_element.classList.add('day');
        day_element.textContent = i + 1;

        if (departSelectedDay = (i + 1) && departSelectedYear == departYear && departSelectedMonth == departMonth) {
            day_element.classList.add('selected');
        }

        day_element.addEventListener('click', function () {
            departSelectedDate = new Date(departYear + '-' + (departMonth + 1) + '-' + (i + 1) );
            departSelectedDay = (i + 1);
            departSelectedMonth = departMonth;
            departSelectedYear = departYear;

            depart_selected_date_element.textContent = formatDate(departSelectedDate);
            depart_selected_date_element.dataset.value = departSelectedDate;

            populateDepartDates();
        });

        depart_days_element.appendChild(day_element);
    }
}

function populateArrivalDates (e) {
    arrival_days_element.innerHTML = '';
    let amount_days = 31;

    if  (departMonth == 1) {
        amount_days = 28;
    }

    for (let i = 0; i < amount_days; i++) {
        const day_element = document.createElement('div');
        day_element.classList.add('day');
        day_element.textContent = i + 1;

        if (arrivalSelectedDay = (i + 1) && arrivalSelectedYear == arrivalYear && arrivalSelectedMonth == arrivalMonth) {
            day_element.classList.add('selected');
        }

        day_element.addEventListener('click', function () {
            arrivalSelectedDate = new Date(arrivalYear + '-' + (arrivalMonth + 1) + '-' + (i + 1) );
            arrivalSelectedDay = (i + 1);
            arrivalSelectedMonth = arrivalMonth;
            arrivalSelectedYear = arrivalYear;

            arrival_selected_date_element.textContent = formatDate(arrivalSelectedDate);
            arrival_selected_date_element.dataset.value = arrivalSelectedDate;

            populateArrivalDates();
        });

        arrival_days_element.appendChild(day_element);
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