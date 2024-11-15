// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', () => {
    // Navbar Entrance Animations
    gsap.fromTo(".nav-logo-svg", {
        opacity: 0,
        scale: 0,
        rotation: -180
    }, {
        opacity: 1,
        scale: 1,
        rotation: 0,
        duration: 1.2,
        ease: "elastic.out(1, 0.5)"
    });

    gsap.fromTo(".brand-text", {
        opacity: 0,
        x: -20
    }, {
        opacity: 1,
        x: 0,
        duration: 0.8,
        delay: 0.3,
        ease: "power2.out"
    });

    // Staggered animation for nav links
    gsap.fromTo(".nav-link", {
        opacity: 0,
        y: -20
    }, {
        opacity: 1,
        y: 0,
        duration: 0.5,
        stagger: 0.1,
        delay: 0.5,
        ease: "power2.out"
    });

    // Interactive hover animations for nav links
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('mouseenter', () => {
            gsap.to(link, {
                scale: 1.1,
                duration: 0.3,
                ease: "power2.out"
            });
        });

        link.addEventListener('mouseleave', () => {
            gsap.to(link, {
                scale: 1,
                duration: 0.3,
                ease: "power2.out"
            });
        });
    });

    // Logo spin animation on hover
    const logo = document.querySelector('.nav-logo-svg');
    
    logo.addEventListener('mouseenter', () => {
        gsap.to(logo, {
            rotation: 360,
            duration: 0.8,
            ease: "power2.out"
        });
    });

    logo.addEventListener('mouseleave', () => {
        gsap.to(logo, {
            rotation: 0,
            duration: 0.8,
            ease: "power2.out"
        });
    });

    // Navbar scroll effect
    let prevScrollPos = window.pageYOffset;
    
    window.addEventListener('scroll', () => {
        const currentScrollPos = window.pageYOffset;
        const navbar = document.querySelector('.navbar');
        
        if (prevScrollPos > currentScrollPos) {
            // Scrolling up
            gsap.to(navbar, {
                y: 0,
                duration: 0.3,
                ease: "power2.out"
            });
        } else {
            // Scrolling down
            gsap.to(navbar, {
                y: -80,
                duration: 0.3,
                ease: "power2.out"
            });
        }
        
        prevScrollPos = currentScrollPos;

        // Add blur effect based on scroll
        const scrollPercentage = Math.min(currentScrollPos / 100, 1);
        navbar.style.backdropFilter = `blur(${10 * scrollPercentage}px)`;
    });

    // Page transition animation
    const pageTransition = () => {
        const tl = gsap.timeline();
        
        tl.to('body', {
            duration: 0.1,
            css: { overflow: 'hidden' }
        })
        .to('.page-transition', {
            duration: 0.5,
            scaleY: 1,
            transformOrigin: 'top',
            ease: "power4.inOut"
        })
        .to('.page-transition', {
            duration: 0.5,
            scaleY: 0,
            transformOrigin: 'bottom',
            ease: "power4.inOut",
            delay: 0.1
        })
        .set('body', {
            css: { overflow: 'auto' }
        });
    };

    // Add page transition to all internal links
    document.querySelectorAll('a').forEach(link => {
        if (link.href.includes(window.location.origin)) {
            link.addEventListener('click', e => {
                e.preventDefault();
                const target = link.href;
                pageTransition();
                setTimeout(() => {
                    window.location.href = target;
                }, 1000);
            });
        }
    });
});

// Add smooth scroll behavior
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            gsap.to(window, {
                duration: 1,
                scrollTo: {
                    y: target,
                    offsetY: 80
                },
                ease: "power2.inOut"
            });
        }
    });
});

// Hero section animations (if present)
if (document.querySelector('.hero-section')) {
    gsap.from(".hero-content", {
        opacity: 0,
        y: 30,
        duration: 1,
        delay: 1.2,
        ease: "power3.out"
    });

    gsap.from(".floating-elements > div", {
        opacity: 0,
        scale: 0,
        y: 50,
        duration: 1,
        stagger: 0.2,
        delay: 1.5,
        ease: "back.out(1.7)"
    });
}