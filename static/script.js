
document.addEventListener("DOMContentLoaded", function () {

    // Mobile navigation menu
    const menuToggle = document.getElementById("menuToggle");
    const navLinks = document.getElementById("navLinks");

    if (menuToggle && navLinks) {
        menuToggle.addEventListener("click", function () {
            navLinks.classList.toggle("active");

            const isOpen = navLinks.classList.contains("active");
            menuToggle.setAttribute("aria-expanded", String(isOpen));
            menuToggle.textContent = isOpen ? "✕" : "☰";
        });

        // Close menu after clicking a navigation link
        navLinks.querySelectorAll("a").forEach(function (link) {
            link.addEventListener("click", function () {
                navLinks.classList.remove("active");
                menuToggle.setAttribute("aria-expanded", "false");
                menuToggle.textContent = "☰";
            });
        });
    }

    // Appointment form validation
    const bookingForm = document.querySelector(".booking-form");

    if (bookingForm) {
        bookingForm.addEventListener("submit", function (event) {
            const phoneField = bookingForm.querySelector(
                'input[type="tel"]'
            );

            if (phoneField) {
                const phone = phoneField.value.trim();

                if (!/^[0-9]{10}$/.test(phone)) {
                    event.preventDefault();
                    alert("Please enter a valid 10-digit mobile number.");
                    phoneField.focus();
                }
            }
        });
    }

    // Customer review form validation
    const feedbackForm = document.querySelector(".feedback-form");

    if (feedbackForm) {
        feedbackForm.addEventListener("submit", function (event) {
            const rating = feedbackForm.querySelector(
                'select[name="rating"]'
            );

            const reviewText = feedbackForm.querySelector(
                'textarea'
            );

            if (rating && !rating.value) {
                event.preventDefault();
                alert("Please select your rating.");
                rating.focus();
                return;
            }

            if (reviewText && reviewText.value.trim().length < 5) {
                event.preventDefault();
                alert("Please write a little more about your experience.");
                reviewText.focus();
            }
        });
    }

    // Update footer year when the element is present
    const yearElement = document.getElementById("currentYear");

    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }

});
