// nav.js

const navSlide = () => {
  const navLine = document.querySelector('.navline');
  const nav = document.querySelector('.nav-links');
  const navLinks = document.querySelectorAll('.nav-links li');

  navLine.addEventListener('click', () => {
      nav.classList.toggle('nav-active');
      navLine.classList.toggle('toggle');

      navLinks.forEach((link, index) => {
          if (link.style.animation) {
              link.style.animation = '';
          } else {
              link.style.animation = `navLinkFade 0.5s ease forwards ${index / 7 + 0.5}s`;
          }
      });
  });
}

function toggleAbout(element, transportation) {
  var aboutButton = element.parentElement.querySelector('.about-button');
  if (aboutButton) {
      aboutButton.style.display = (aboutButton.style.display === 'none') ? 'block' : 'none';
      aboutButton.textContent = 'About ' + transportation;
  }
}

function scrollToTransportation() {
  const transportationSection = document.getElementById('transportation');
  transportationSection.scrollIntoView({ behavior: 'smooth' });
}

const handleFixedNavbar = () => {
  const nav = document.querySelector('nav');
  const navHeight = nav.offsetHeight;

  window.addEventListener('scroll', () => {
      if (window.scrollY > navHeight) {
          nav.classList.add('nav-fixed');
      } else {
          nav.classList.remove('nav-fixed');
      }
  });
};

// Call the functions
navSlide();
handleFixedNavbar();
