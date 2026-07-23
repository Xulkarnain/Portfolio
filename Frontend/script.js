"use strict";

/*=========================================================
PORTFOLIO APPLICATION
=========================================================*/

const PortfolioApp = {
  /*=====================================================
    CONFIG
    =====================================================*/

  config: {
    typingSpeed: 90,

    deletingSpeed: 45,

    delayBetweenWords: 1800,

    scrollOffset: 100,
  },

  /*=====================================================
    STATE
    =====================================================*/

  state: {
    darkMode: true,

    currentWord: 0,

    currentCharacter: 0,

    deleting: false,
  },

  /*=====================================================
    DOM CACHE
    =====================================================*/

  dom: {},

  /*=====================================================
    CACHE DOM
    =====================================================*/

  cacheDom() {
    this.dom = {
      body: document.body,

      header: document.getElementById("site-header"),

      scrollProgress: document.getElementById("scroll-progress"),

      themeToggle: document.getElementById("theme-toggle"),

      menuToggle: document.getElementById("menu-toggle"),

      mobileMenu: document.getElementById("mobile-menu"),

      typingText: document.getElementById("typing-text"),

      backToTop: document.getElementById("back-to-top"),

      projectSearch: document.getElementById("project-search"),

      filterButtons: [...document.querySelectorAll(".filter-btn")],

      projectCards: [...document.querySelectorAll(".project-card")],

      navLinks: [...document.querySelectorAll(".nav-menu a")],

      sections: [...document.querySelectorAll("section")],

      progressBars: [...document.querySelectorAll(".progress-fill")],

      counters: [...document.querySelectorAll("[data-count]")],

      contactForm: document.getElementById("contact-form"),
    };
  },

  /*=====================================================
    UTILITIES
    =====================================================*/

  utils: {
    clamp(value, min, max) {
      return Math.min(Math.max(value, min), max);
    },

    debounce(fn, delay) {
      let timeout;

      return (...args) => {
        clearTimeout(timeout);

        timeout = setTimeout(() => fn(...args), delay);
      };
    },
  },

  /*=====================================================
    THEME
    =====================================================*/

  theme: {
    init() {
      const savedTheme = localStorage.getItem("theme");

      if (savedTheme) {
        PortfolioApp.dom.body.classList.toggle("light", savedTheme === "light");
      } else {
        const prefersLight = window.matchMedia(
          "(prefers-color-scheme: light)",
        ).matches;

        PortfolioApp.dom.body.classList.toggle("light", prefersLight);
      }

      this.updateIcon();

      PortfolioApp.dom.themeToggle.addEventListener("click", () =>
        this.toggle(),
      );
    },

    toggle() {
      PortfolioApp.dom.body.classList.toggle("light");

      const currentTheme = PortfolioApp.dom.body.classList.contains("light")
        ? "light"
        : "dark";

      localStorage.setItem("theme", currentTheme);

      this.updateIcon();
    },

    updateIcon() {
      const icon = PortfolioApp.dom.themeToggle.querySelector("i");

      if (PortfolioApp.dom.body.classList.contains("light")) {
        icon.className = "fas fa-sun";
      } else {
        icon.className = "fas fa-moon";
      }
    },
  },

  /*=====================================================
    NAVIGATION
    =====================================================*/

  navigation: {
    init() {
      this.mobileMenu();

      this.activeLinks();
    },

    mobileMenu() {
      const {
        menuToggle,

        mobileMenu,
      } = PortfolioApp.dom;

      menuToggle.addEventListener("click", () => {
        mobileMenu.classList.toggle("open");

        menuToggle.classList.toggle("active");
      });

      document.addEventListener("click", (event) => {
        const clickedInside =
          mobileMenu.contains(event.target) ||
          menuToggle.contains(event.target);

        if (!clickedInside) {
          mobileMenu.classList.remove("open");

          menuToggle.classList.remove("active");
        }
      });

      mobileMenu.querySelectorAll("a").forEach((link) => {
        link.addEventListener("click", () => {
          mobileMenu.classList.remove("open");

          menuToggle.classList.remove("active");
        });
      });
    },

    activeLinks() {
      const {
        sections,

        navLinks,
      } = PortfolioApp.dom;

      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (!entry.isIntersecting) return;

            const id = entry.target.id;

            navLinks.forEach((link) => {
              link.classList.remove("active");

              if (link.getAttribute("href") === `#${id}`) {
                link.classList.add("active");
              }
            });
          });
        },

        {
          threshold: 0.45,
        },
      );

      sections.forEach((section) => observer.observe(section));
    },
  },

  /*=====================================================
    SCROLL
    =====================================================*/

  scroll: {
    ticking: false,

    init() {
      this.handleScroll();

      window.addEventListener("scroll", () => {
        if (!this.ticking) {
          window.requestAnimationFrame(() => {
            this.update();

            this.ticking = false;
          });

          this.ticking = true;
        }
      });
    },

    update() {
      this.progressBar();

      this.header();

      this.backToTop();
    },

    progressBar() {
      const { scrollProgress } = PortfolioApp.dom;

      const scrollTop = window.scrollY;

      const documentHeight =
        document.documentElement.scrollHeight - window.innerHeight;

      const progress = (scrollTop / documentHeight) * 100;

      scrollProgress.style.width = `${progress}%`;
    },

    header() {
      const { header } = PortfolioApp.dom;

      if (window.scrollY > 40) {
        header.classList.add("scrolled");
      } else {
        header.classList.remove("scrolled");
      }
    },

    backToTop() {
      const { backToTop } = PortfolioApp.dom;

      if (window.scrollY > 500) {
        backToTop.classList.add("show");
      } else {
        backToTop.classList.remove("show");
      }
    },

    handleScroll() {
      PortfolioApp.dom.backToTop.addEventListener(
        "click",

        () => {
          window.scrollTo({
            top: 0,

            behavior: "smooth",
          });
        },
      );
    },
  },

  /*=====================================================
    ANIMATIONS
    =====================================================*/

  animations: {
    typingWords: [
      "AI Engineer",

      "Machine Learning Engineer",

      "Backend Developer",

      "FastAPI Developer",

      "Building Intelligent Systems",
    ],

    init() {
      this.typingEffect();

      this.counterAnimation();

      this.revealAnimation();

      this.progressBars();
    },

    /*=================================================
        TYPING EFFECT
        =================================================*/

    typingEffect() {
      const element = PortfolioApp.dom.typingText;

      const {
        typingSpeed,

        deletingSpeed,

        delayBetweenWords,
      } = PortfolioApp.config;

      const state = PortfolioApp.state;

      const words = this.typingWords;

      const type = () => {
        const word = words[state.currentWord];

        if (!state.deleting) {
          state.currentCharacter++;
        } else {
          state.currentCharacter--;
        }

        element.textContent = word.substring(0, state.currentCharacter);

        let speed = state.deleting ? deletingSpeed : typingSpeed;

        if (!state.deleting && state.currentCharacter === word.length) {
          speed = delayBetweenWords;

          state.deleting = true;
        }

        if (state.deleting && state.currentCharacter === 0) {
          state.deleting = false;

          state.currentWord++;

          state.currentWord %= words.length;
        }

        setTimeout(type, speed);
      };

      type();
    },

    /*=================================================
        COUNTERS
        =================================================*/

    counterAnimation() {
      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (!entry.isIntersecting) return;

            const element = entry.target;

            const target = Number(element.dataset.count);

            let current = 0;

            const increment = Math.ceil(target / 80);

            const animate = () => {
              current += increment;

              if (current > target) current = target;

              element.textContent = current;

              if (current < target) {
                requestAnimationFrame(animate);
              }
            };

            animate();

            observer.unobserve(element);
          });
        },

        {
          threshold: 0.6,
        },
      );

      PortfolioApp.dom.counters.forEach((counter) => {
        observer.observe(counter);
      });
    },

    /*=================================================
        SCROLL REVEAL
        =================================================*/

    revealAnimation() {
      const elements = document.querySelectorAll(
        ".section-header,.project-card,.skill-card,.timeline-item,.focus-card,.blog-card,.certificate-card,.education-card,.highlight-card,.contact-wrapper",
      );

      elements.forEach((el) => el.classList.add("reveal"));

      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              entry.target.classList.add("active");

              observer.unobserve(entry.target);
            }
          });
        },

        {
          threshold: 0.15,
        },
      );

      elements.forEach((el) => observer.observe(el));
    },

    /*=================================================
        PROGRESS BARS
        =================================================*/

    progressBars() {
      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (!entry.isIntersecting) return;

            const bar = entry.target;

            bar.style.width = bar.dataset.progress + "%";

            observer.unobserve(bar);
          });
        },

        {
          threshold: 0.5,
        },
      );

      PortfolioApp.dom.progressBars.forEach((bar) => {
        observer.observe(bar);
      });
    },
  },

  /*=====================================================
    PROJECTS
    =====================================================*/

  projects: {
    currentFilter: "all",

    init() {
      this.filterButtons();

      this.searchProjects();
    },

    filterButtons() {
      PortfolioApp.dom.filterButtons.forEach((button) => {
        button.addEventListener("click", () => {
          PortfolioApp.dom.filterButtons.forEach((btn) =>
            btn.classList.remove("active"),
          );

          button.classList.add("active");

          this.currentFilter = button.dataset.filter;

          this.filterProjects();
        });
      });
    },

    searchProjects() {
      PortfolioApp.dom.projectSearch.addEventListener(
        "input",

        () => this.filterProjects(),
      );
    },

    filterProjects() {
      const keyword = PortfolioApp.dom.projectSearch.value

        .toLowerCase()

        .trim();

      let visibleProjects = 0;

      PortfolioApp.dom.projectCards.forEach((card) => {
        const category = card.dataset.category;

        const content = card.textContent.toLowerCase();

        const categoryMatch =
          this.currentFilter === "all" || category.includes(this.currentFilter);

        const keywordMatch = content.includes(keyword);

        if (categoryMatch && keywordMatch) {
          visibleProjects++;

          card.classList.remove("hide");
        } else {
          card.classList.add("hide");
        }
      });

      this.emptyState(visibleProjects);
    },

    emptyState(count) {
      let empty = document.querySelector(".empty-projects");

      if (!empty) {
        empty = document.createElement("div");

        empty.className = "empty-projects";

        empty.innerHTML = `

                    <h3>No Projects Found</h3>

                    <p>

                        Try another keyword or category.

                    </p>

                `;

        document

          .querySelector(".project-grid")

          .after(empty);
      }

      empty.style.display = count === 0 ? "block" : "none";
    },
  },

  /*=====================================================
    CONTACT
    =====================================================*/

  contact: {
    init() {
      this.form();

      this.copyEmail();
    },

    form() {
      const form = PortfolioApp.dom.contactForm;

      if (!form) return;

      form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const submitButton = form.querySelector("button");

        const originalText = submitButton.textContent;

        submitButton.disabled = true;

        submitButton.textContent = "Sending...";

        try {
          const data = {
            name: form.name.value.trim(),

            email: form.email.value.trim(),

            subject: form.subject.value.trim(),

            message: form.message.value.trim(),
          };

          if (!data.name || !data.email || !data.message) {
            throw new Error("Please fill all required fields.");
          }

          /*
                    FASTAPI ENDPOINT

                    await fetch("/api/contact",{

                        method:"POST",

                        headers:{
                            "Content-Type":"application/json"
                        },

                        body:JSON.stringify(data)

                    });

                    */

          await new Promise((resolve) => setTimeout(resolve, 1200));

          this.toast(
            "Message sent successfully!",

            "success",
          );

          form.reset();
        } catch (error) {
          this.toast(
            error.message,

            "error",
          );
        } finally {
          submitButton.disabled = false;

          submitButton.textContent = originalText;
        }
      });
    },

    copyEmail() {
      const emailLink = document.querySelector(
        '.contact-links a[href^="mailto"]',
      );

      if (!emailLink) return;

      emailLink.addEventListener(
        "dblclick",

        async () => {
          try {
            await navigator.clipboard.writeText("darzulkarnain@gmail.com");

            this.toast(
              "Email copied!",

              "success",
            );
          } catch {
            this.toast(
              "Unable to copy email.",

              "error",
            );
          }
        },
      );
    },

    toast(message, type = "success") {
      const toast = document.createElement("div");

      toast.className = `toast ${type}`;

      toast.textContent = message;

      document.body.appendChild(toast);

      requestAnimationFrame(() => {
        toast.classList.add("show");
      });

      setTimeout(() => {
        toast.classList.remove("show");

        setTimeout(() => {
          toast.remove();
        }, 300);
      }, 3000);
    },
  },

  /*=====================================================
    INITIALIZE
    =====================================================*/

  init() {
    this.cacheDom();

    this.theme.init();

    this.navigation.init();

    this.scroll.init();

    this.animations.init();

    this.projects.init();

    this.contact.init();

    console.log("Portfolio initialized.");
  },
};

/*=========================================================
START
=========================================================*/

document.addEventListener("DOMContentLoaded", () => {
  PortfolioApp.init();
});
