
document.addEventListener("DOMContentLoaded", () => {

    // Set the minimum appointment date to today
    const dateInput = document.querySelector(
        'input[name="appointment_date"]'
    );

    if (dateInput) {
        const today = new Date().toISOString().slice(0, 10);
        dateInput.min = today;
    }

});

