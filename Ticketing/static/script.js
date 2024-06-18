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


        document.getElementById('departure_station').addEventListener('change', function() {
            fetch(`/get_schedules?departure_station_id=${this.value}&arrival_station_id=${document.getElementById('arrival_station').value}`)
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
        });

        document.getElementById('arrival_station').addEventListener('change', function() {
            fetch(`/get_schedules?departure_station_id=${document.getElementById('departure_station').value}&arrival_station_id=${this.value}`)
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
        });

    document.getElementById('schedule').addEventListener('change', function() {
        const scheduleId = this.value;
        fetch(`/get_seats/${scheduleId}`)
            .then(response => response.json())
            .then(data => {
                const seatSelect = document.getElementById('seat');
                seatSelect.innerHTML = '';
                data.seats.forEach(seat => {
                    const option = document.createElement('option');
                    option.value = seat.seat_id;
                    option.text = `Seat: ${seat.seat_number} (${seat.seat_class})`;
                    seatSelect.appendChild(option);
                });
            });
    });
});
