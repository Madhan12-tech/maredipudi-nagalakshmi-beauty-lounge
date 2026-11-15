
document.addEventListener("DOMContentLoaded", () => {

    // 1. MOBILE NAVIGATION
    const menuToggle = document.getElementById("menuToggle");
    const navLinks = document.getElementById("navLinks");

    function closeMenu() {
        if (!menuToggle || !navLinks) return;

        navLinks.classList.remove("active");
        menuToggle.setAttribute("aria-expanded", "false");
        menuToggle.textContent = "☰";
    }

    if (menuToggle && navLinks) {
        menuToggle.addEventListener("click", () => {
            const isOpen = navLinks.classList.toggle("active");

            menuToggle.setAttribute("aria-expanded", String(isOpen));
            menuToggle.textContent = isOpen ? "✕" : "☰";
        });

        navLinks.querySelectorAll("a").forEach(link => {
            link.addEventListener("click", closeMenu);
        });

        document.addEventListener("click", event => {
            if (
                !navLinks.contains(event.target) &&
                !menuToggle.contains(event.target)
            ) {
                closeMenu();
            }
        });

        window.addEventListener("resize", () => {
            if (window.innerWidth > 820) closeMenu();
        });
    }


    // 2. AUTOMATIC FOOTER YEAR
    const yearElement = document.getElementById("currentYear");

    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }


    // 3. SCROLL REVEAL ANIMATIONS
    const revealElements = document.querySelectorAll(
        ".section-heading, .about-content, .about-visual, " +
        ".service-card, .package-card, .gallery-item, " +
        ".booking-form, .booking-copy, .contact-item, " +
        ".contact-heading, .experience-section > *"
    );

    if ("IntersectionObserver" in window) {
        const revealObserver = new IntersectionObserver(
            (entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("revealed");
                        observer.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.12 }
        );

        revealElements.forEach(element => {
            element.classList.add("reveal");
            revealObserver.observe(element);
        });
    } else {
        revealElements.forEach(element => {
            element.classList.add("revealed");
        });
    }


    // 4. 3D HERO IMAGE MOVEMENT
    const heroArt = document.querySelector(".hero-art");
    const heroFrame = document.querySelector(".hero-image-frame");

    const canUseHover =
        window.matchMedia("(hover: hover) and (pointer: fine)").matches;

    if (heroArt && heroFrame && canUseHover) {
        heroArt.addEventListener("mousemove", event => {
            const rect = heroArt.getBoundingClientRect();

            const x = (event.clientX - rect.left) / rect.width;
            const y = (event.clientY - rect.top) / rect.height;

            const rotateY = (x - 0.5) * 12;
            const rotateX = (0.5 - y) * 9;

            heroFrame.style.transform =
                `rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
        });

        heroArt.addEventListener("mouseleave", () => {
            heroFrame.style.transform = "rotateY(-7deg) rotateX(2deg)";
        });
    }


    // 5. SMALL FLOATING PARTICLES
    const hero = document.querySelector(".hero");

    if (hero) {
        const particleContainer = document.createElement("div");
        particleContainer.className = "particle-container";
        particleContainer.setAttribute("aria-hidden", "true");

        hero.appendChild(particleContainer);

        for (let i = 0; i < 18; i++) {
            const particle = document.createElement("span");

            particle.className = "particle";
            particle.textContent = i % 3 === 0 ? "✦" : "·";

            particle.style.left = `${Math.random() * 100}%`;
            particle.style.top = `${Math.random() * 100}%`;
            particle.style.animationDelay = `${Math.random() * 6}s`;
            particle.style.animationDuration =
                `${5 + Math.random() * 7}s`;

            particleContainer.appendChild(particle);
        }
    }


    // 6. APPOINTMENT DATE VALIDATION
    const dateInput = document.getElementById("appointment_date");

    if (dateInput) {
        const localDate = new Date();
        const year = localDate.getFullYear();
        const month = String(localDate.getMonth() + 1).padStart(2, "0");
        const day = String(localDate.getDate()).padStart(2, "0");

        dateInput.min = `${year}-${month}-${day}`;

        dateInput.addEventListener("change", () => {
            if (dateInput.value && dateInput.value < dateInput.min) {
                alert("Please select today or a future date.");
                dateInput.value = "";
            }
        });
    }


    // 7. APPOINTMENT FORM VALIDATION
    const bookingForm = document.querySelector(".booking-form");

    if (bookingForm) {
        bookingForm.addEventListener("submit", event => {
            const phoneInput = document.getElementById("phone");

            if (phoneInput) {
                const phone = phoneInput.value.trim();

                if (!/^[0-9]{10}$/.test(phone)) {
                    event.preventDefault();
                    alert("Please enter a valid 10-digit mobile number.");
                    phoneInput.focus();
                    return;
                }
            }

            if (!bookingForm.checkValidity()) {
                event.preventDefault();
                bookingForm.reportValidity();
            }
        });
    }


    // 8. BUTTON CLICK FEEDBACK
    document.querySelectorAll(".button").forEach(button => {
        button.addEventListener("pointerdown", () => {
            button.classList.add("button-pressed");
        });

        button.addEventListener("pointerup", () => {
            button.classList.remove("button-pressed");
        });

        button.addEventListener("pointerleave", () => {
            button.classList.remove("button-pressed");
        });
    });


    // 9. NAVIGATION ACTIVE SECTION
    const sections = document.querySelectorAll("main section[id]");
    const navItems = document.querySelectorAll(
        ".nav-links a[href^='#']"
    );

    if ("IntersectionObserver" in window) {
        const sectionObserver = new IntersectionObserver(
            entries => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        navItems.forEach(link => {
                            link.classList.toggle(
                                "nav-active",
                                link.getAttribute("href") ===
                                `#${entry.target.id}`
                            );
                        });
                    }
                });
            },
            { rootMargin: "-30% 0px -60% 0px" }
        );

        sections.forEach(section => sectionObserver.observe(section));
    }


    // 10. IMAGE LOADING FALLBACK
    document.querySelectorAll("img").forEach(img => {
        img.addEventListener("error", () => {
            img.classList.add("image-unavailable");
            img.alt = "Beauty lounge image temporarily unavailable";
        });
    });

});
