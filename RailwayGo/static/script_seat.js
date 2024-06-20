// script.js
document.addEventListener('DOMContentLoaded', () => {
    const selectSeatBtn = document.getElementById('select-seat-btn');
    const seatMap = document.getElementById('seat-map');
    const seatInput = document.getElementById('seat');
    const numPaxSelect = document.getElementById('num_pax');
    const popupOverlay = document.querySelector('.popup-overlay');
    const popup = document.querySelector('.popup');
    let selectedSeats = [];

    for (let i = 1; i <= 13; i++) {
        const option = document.createElement('option');
        option.value = i;
        option.textContent = i;
        numPaxSelect.appendChild(option);
    }

    function updateSelectedSeats() {
        seatInput.value = selectedSeats.join(',');
    }

    function handleSeatSelection(seatDiv) {
        const seatNumber = seatDiv.innerText;

        seatDiv.classList.toggle('selected');

        if (seatDiv.classList.contains('selected')) {
            selectedSeats.push(seatNumber);
        } else {
            selectedSeats = selectedSeats.filter(seat => seat !== seatNumber);
        }

        updateSelectedSeats();
    }

    function updateSeats() {
        const seatClass = document.getElementById('class').value;
        fetch(`/get_seats/${seatClass}`)
            .then(response => response.json())
            .then(data => {
                seatMap.innerHTML = '';
                data.seats.forEach(seat => {
                    const seatDiv = document.createElement('div');
                    seatDiv.classList.add('seat');
                    seatDiv.dataset.seatId = seat.seat_id;
                    seatDiv.innerText = seat.seat_number;

                    if (selectedSeats.includes(seat.seat_number)) {
                        seatDiv.classList.add('selected');
                    }

                    if (!seat.is_available) {
                        seatDiv.classList.add('unavailable');
                        seatDiv.removeEventListener('click', handleSeatSelection);
                    } else {
                        seatDiv.addEventListener('click', () => handleSeatSelection(seatDiv));
                    }

                    seatMap.appendChild(seatDiv);
                });
                showPopup();
            })
            .catch(error => {
                console.error('Error fetching seats:', error);
            });
    }

    function showPopup() {
        popupOverlay.style.display = 'block';
        popup.style.display = 'block';
    }

    function closePopup() {
        popupOverlay.style.display = 'none';
        popup.style.display = 'none';
    }

    selectSeatBtn.addEventListener('click', updateSeats);
    document.getElementById('close-popup').addEventListener('click', closePopup);
    popupOverlay.addEventListener('click', closePopup);
});
