document.addEventListener('DOMContentLoaded', (event) => {
    fetch('/get_schedules')
        .then(response => response.json())
        .then(data => {
            const scheduleSelect = document.getElementById('schedule');
            data.schedules.forEach(schedule => {
                const option = document.createElement('option');
                option.value = schedule.schedule_id;
                option.text = `Train: ${schedule.train_name} Departure: ${schedule.departure_time} Arrival: ${schedule.arrival_time}`;
                scheduleSelect.appendChild(option);
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
