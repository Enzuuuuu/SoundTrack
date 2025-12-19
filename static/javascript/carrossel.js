document.addEventListener("DOMContentLoaded", () => {
    const track = document.querySelector('.carousel-track');
    const items = document.querySelectorAll('.carousel-item');
    const total = items.length;

    let index = 0;

    function updateSlide() {
        const position = index * -100;
        track.style.transform = `translateX(${position}%)`;
    }

    document.querySelector('.next').addEventListener('click', () => {
        index = (index + 1) % total;
        updateSlide();
    });

    document.querySelector('.prev').addEventListener('click', () => {
        index = (index - 1 + total) % total;
        updateSlide();
    });

    // Auto-play opcional
    setInterval(() => {
        index = (index + 1) % total;
        updateSlide();
    }, 4000);
});
