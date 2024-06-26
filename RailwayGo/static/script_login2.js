// swiper.js

const prevBtn = document.querySelector('.swiper-button-prev');
const nextBtn = document.querySelector('.swiper-button-next');
const cardsSlider = document.querySelector('.swiper-wrapper');
const cardWidth = document.querySelector('.swiper-slide').offsetWidth;
let currentPosition = 0;

prevBtn.addEventListener('click', () => {
    if (currentPosition > 0) {
        currentPosition -= cardWidth;
        cardsSlider.style.transform = `translateX(-${currentPosition}px)`;
    }
});

nextBtn.addEventListener('click', () => {
    const maxPosition = (cardsSlider.children.length - 1) * cardWidth;
    if (currentPosition < maxPosition) {
        currentPosition += cardWidth;
        cardsSlider.style.transform = `translateX(-${currentPosition}px)`;
    }
});

// Initialize Swiper
var swiper = new Swiper(".slide-container", {
    slidesPerView: 3,
    spaceBetween: 9, 
    loop: true,
    grabCursor: true,
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    autoplay: {
        delay: 4000, 
        disableOnInteraction: false, 
    },
    breakpoints: {
        0: {
            slidesPerView: 1,
            spaceBetween: 5, 
        },
        520: {
            slidesPerView: 2,
            spaceBetween: 5, 
        },
        950: {
            slidesPerView: 3,
            spaceBetween: 9, 
        },
    },
});



