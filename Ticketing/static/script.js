document.addEventListener('DOMContentLoaded', () => {
    let maxPassengers = 1; 

    function updateSeats() {
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
                        if (seatDiv.classList.contains('selected')) {
                            seatDiv.classList.remove('selected');
                        } else {
                            const selectedSeats = document.querySelectorAll('.seat.selected').length;
                            if (selectedSeats < maxPassengers) {
                                seatDiv.classList.add('selected');
                            }
                        }
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
        const selectedSeats = document.querySelectorAll('.seat.selected');
        const selectedSeatNumbers = Array.from(selectedSeats)
            .map(seat => seat.innerText);
        document.getElementById('seat').value = selectedSeatNumbers.join(', ');
    }

    document.getElementById('select-seat-btn').addEventListener('click', () => {
        maxPassengers = parseInt(document.getElementById('num_pax').value) || 1;
        updateSeats();
    });

    function showPopup() {
        const popupOverlay = document.querySelector('.popup-overlay');
        const popup = document.querySelector('.popup');
        popupOverlay.style.display = 'block';
        popup.style.display = 'block';
    }

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
    numPaxSelect.addEventListener('change', () => {
        maxPassengers = parseInt(numPaxSelect.value) || 1;
        const selectedSeats = document.querySelectorAll('.seat.selected');
        if (selectedSeats.length > maxPassengers) {
            selectedSeats.forEach(seat => seat.classList.remove('selected'));
        }
        updateSelectedSeats();
    });

    for (let i = 1; i <= 13; i++) {
        const option = document.createElement('option');
        option.value = i;
        option.textContent = i;
        numPaxSelect.appendChild(option);
    }
});






