const navSlide = () => {
    const navLine = document.querySelector('.navline');
    const nav = document.querySelector('.nav-links');
    const navLinks = document.querySelectorAll('.nav-links li');


    navLine.addEventListener('click', () => {
        // Toggle the nav-active class on the navigation menu
        nav.classList.toggle('nav-active');
       
        // Toggle navline animation
        navLine.classList.toggle('toggle');


        // Apply animation to nav links
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
    // Toggle the visibility of the About button
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
  

navSlide();