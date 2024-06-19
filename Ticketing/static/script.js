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
                                document.querySelectorAll('.seat.selected').forEach(s => s.classList.remove('selected'));
                                seat.classList.add('selected');
                                document.getElementById('seat').value = seat.innerText;
                            });
                        }
                    });
                });
        }
    }

    document.getElementById('schedule').addEventListener('change', updateSeats);
    document.getElementById('class').addEventListener('change', updateSeats);

    const popupOverlay = document.querySelector('.popup-overlay');
    const popup = document.querySelector('.popup');
    document.getElementById('select-seat-btn').addEventListener('click', () => {
        popupOverlay.style.display = 'block';
        popup.style.display = 'block';
    });

    document.getElementById('close-popup').addEventListener('click', () => {
        popupOverlay.style.display = 'none';
        popup.style.display = 'none';
    });
});
