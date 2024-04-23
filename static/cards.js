document.addEventListener("DOMContentLoaded", function() {
    var cards = document.querySelectorAll('.card');

    cards.forEach(function(card) {
        card.addEventListener('mousemove', function(e) {
            var rect = card.getBoundingClientRect(),
                mouseX = e.clientX - rect.left - rect.width / 2,
                mouseY = e.clientY - rect.top - rect.height / 2,
                rotationX = (-1) * (mouseY / rect.height) * 20,
                rotationY = (mouseX / rect.width) * 20;

            card.style.transform = `perspective(500px) rotateX(${rotationX}deg) rotateY(${rotationY}deg)`;
        });

        card.addEventListener('mouseleave', function() {
            card.style.transform = '';
        });
    });
});
