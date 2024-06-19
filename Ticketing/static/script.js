document.addEventListener('DOMContentLoaded', () => {
    function fetchSeats() {
        const seatClass = document.getElementById('class').value;
        fetch(`/get_seats/${seatClass}`)
            .then(response => response.json())
            .then(data => {
                const seatMap = document.getElementById('seat-map');
                seatMap.innerHTML = '';
                data.seats.forEach(seat => {
                    const seatDiv = document.createElement('div');
                    seatDiv.classList.add('seat');
                    seatDiv.dataset.seatId = seat.seat_id;
                    seatDiv.innerText = seat.seat_number;
                    seatDiv.addEventListener('click', () => {
                        seatDiv.classList.toggle('selected');
                        updateSelectedSeats(); 
                    });
                    seatMap.appendChild(seatDiv);
                });
                showPopup(); 
            })
            .catch(error => {
                console.error('Error fetching seats:', error);
            });
    }

    function updateSelectedSeats() {
        const selectedSeatIds = Array.from(document.querySelectorAll('.seat.selected'))
            .map(seat => seat.dataset.seatId);
        document.getElementById('seat').value = selectedSeatIds.join(',');
    }

    function showPopup() {
        const popupOverlay = document.querySelector('.popup-overlay');
        const popup = document.querySelector('.popup');
        popupOverlay.style.display = 'block';
        popup.style.display = 'block';
    }

    function closePopup() {
        const popupOverlay = document.querySelector('.popup-overlay');
        const popup = document.querySelector('.popup');
        popupOverlay.style.display = 'none';
        popup.style.display = 'none';
    }

    document.getElementById('select-seat-btn').addEventListener('click', fetchSeats);

    document.getElementById('close-popup').addEventListener('click', closePopup);

    const popupOverlay = document.querySelector('.popup-overlay');
    popupOverlay.addEventListener('click', closePopup);

    const numPaxSelect = document.getElementById('num_pax');
    for (let i = 1; i <= 13; i++) {
        const option = document.createElement('option');
        option.value = i;
        option.textContent = i;
        numPaxSelect.appendChild(option);
    }

    function bookSeats() {
        const formData = new FormData(document.getElementById('booking-form'));
        fetch('/book', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(message => {
            console.log('Booking response:', message);
        })
        .catch(error => {
            console.error('Error booking seats:', error);
        });
    }

    document.getElementById('booking-form').addEventListener('submit', function(event) {
        event.preventDefault(); 
        bookSeats(); 
    });

});




