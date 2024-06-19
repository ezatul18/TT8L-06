document.addEventListener('DOMContentLoaded', (event) => {
    fetch('/get_stations')
        .then(response => response.json())
        .then(data => {
            const departureStationSelect = document.getElementById('departure_station');
            const arrivalStationSelect = document.getElementById('arrival_station');
            data.stations.forEach(station => {
                const option = document.createElement('option');
                option.value = station.station_id;
                option.text = station.station_name;
                departureStationSelect.appendChild(option);
                arrivalStationSelect.appendChild(option.cloneNode(true));
            });
        });

    function updateSchedules() {
        const departureStationId = document.getElementById('departure_station').value;
        const arrivalStationId = document.getElementById('arrival_station').value;
        if (departureStationId && arrivalStationId) {
            fetch(`/get_schedules?departure_station_id=${departureStationId}&arrival_station_id=${arrivalStationId}`)
                .then(response => response.json())
                .then(data => {
                    const scheduleSelect = document.getElementById('schedule');
                    scheduleSelect.innerHTML = '';
                    data.schedules.forEach(schedule => {
                        const option = document.createElement('option');
                        option.value = schedule.schedule_id;
                        option.text = `Train: ${schedule.train_name} Departure: ${schedule.departure_time} Arrival: ${schedule.arrival_time}`;
                        scheduleSelect.appendChild(option);
                    });
                });
        }
    }

    document.getElementById('departure_station').addEventListener('change', updateSchedules);
    document.getElementById('arrival_station').addEventListener('change', updateSchedules);

    function updateSeats() {
        const scheduleId = document.getElementById('schedule').value;
        const seatClass = document.getElementById('class').value;
        if (scheduleId && seatClass) {
            fetch(`/get_seats/${scheduleId}/${seatClass}`)
                .then(response => response.json())
                .then(data => {
                    const seatMap = document.getElementById('seat-map');
                    seatMap.innerHTML = '';
                    data.seats.forEach(seat => {
                        const seatDiv = document.createElement('div');
                        seatDiv.classList.add('seat');
                        if (!seat.is_available) {
                            seatDiv.classList.add('unavailable');
                        }
                        seatDiv.dataset.seatId = seat.seat_id;
                        seatDiv.innerText = seat.seat_number;
                        seatMap.appendChild(seatDiv);
                    });

                    document.querySelectorAll('.seat').forEach(seat => {
                        if (!seat.classList.contains('unavailable')) {
                            seat.addEventListener('click', function() {
                                const selectedSeats = document.querySelectorAll('.seat.selected').length;
                                const maxPax = parseInt(document.getElementById('num_pax').value);
                                if (selectedSeats < maxPax) {
                                    seat.classList.toggle('selected');
                                } else if (seat.classList.contains('selected')) {
                                    seat.classList.remove('selected');
                                }

                                const selectedSeatNumbers = Array.from(document.querySelectorAll('.seat.selected')).map(s => s.innerText);
                                document.getElementById('seat').value = selectedSeatNumbers.join(', ');
                            });
                        }
                    });

                    showPopup();
                })
                .catch(error => {
                    console.error('Error fetching seats:', error);
                });
        }
    }

    document.getElementById('schedule').addEventListener('change', updateSeats);
    document.getElementById('class').addEventListener('change', updateSeats);
    document.getElementById('num_pax').addEventListener('change', updateSeats);

    function showPopup() {
        const popupOverlay = document.querySelector('.popup-overlay');
        const popup = document.querySelector('.popup');
        popupOverlay.style.display = 'block';
        popup.style.display = 'block';
    }

    document.getElementById('select-seat-btn').addEventListener('click', () => {
        updateSeats();
    });

    document.getElementById('close-popup').addEventListener('click', () => {
        const popupOverlay = document.querySelector('.popup-overlay');
        const popup = document.querySelector('.popup');
        popupOverlay.style.display = 'none';
        popup.style.display = 'none';
    });

    const popupOverlay = document.querySelector('.popup-overlay');
    popupOverlay.addEventListener('click', () => {
        const popupOverlay = document.querySelector('.popup-overlay');
        const popup = document.querySelector('.popup');
        popupOverlay.style.display = 'none';
        popup.style.display = 'none';
    });

    const numPaxSelect = document.getElementById('num_pax');
    for (let i = 1; i <= 13; i++) {
        const option = document.createElement('option');
        option.value = i;
        option.text = i;
        numPaxSelect.appendChild(option);
    }
});

