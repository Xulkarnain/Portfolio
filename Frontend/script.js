"use strict";

/*=========================================================
PORTFOLIO APPLICATION
=========================================================*/

const PortfolioApp = {
  /*=====================================================
    CONFIG
    =====================================================*/
  config: {
    // Backend API
    apiBaseUrl: "http://127.0.0.1:8000/api/v1",

    // Typing animation
    typingSpeed: 90,
    deletingSpeed: 45,
    delayBetweenWords: 1800,

    // Scroll configuration
    scrollOffset: 100,
  },
  api: {
    async get(endpoint) {
      const url = `${PortfolioApp.config.apiBaseUrl}${endpoint}`;

      const response = await fetch(url);

      if (!response.ok) {
        throw new Error(
          `API request failed: ${response.status} ${response.statusText}`,
        );
      }

      return await response.json();
    },
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

      this.observeRevealElements(elements);
    },

    observeRevealElements(elements) {
      // Create the observer only once.
      if (!this.revealObserver) {
        this.revealObserver = new IntersectionObserver(
          (entries, observer) => {
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
      }

      elements.forEach((el) => {
        el.classList.add("reveal");
        this.revealObserver.observe(el);
      });
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
    EXPERIENCE
    =====================================================*/

  experience: {
    init() {
      this.loadExperiences();
    },

    async loadExperiences() {
      const timeline = document.querySelector(".timeline");

      timeline.textContent = "Loading experience...";

      try {
        const experiences = await PortfolioApp.api.get("/experiences");

        this.renderExperiences(experiences);

        const timelineItems = timeline.querySelectorAll(".timeline-item");

        PortfolioApp.animations.observeRevealElements(timelineItems);
      } catch (error) {
        console.error("Unable to load experiences:", error);

        timeline.textContent =
          "Unable to load experience. Please try again later.";
      }
    },

    renderExperiences(experiences) {
      const timeline = document.querySelector(".timeline");

      timeline.replaceChildren();

      experiences.forEach((experience) => {
        const item = this.createExperienceItem(experience);
        timeline.appendChild(item);
      });
    },

    createExperienceItem(experience) {
      const item = document.createElement("article");
      item.className = "timeline-item";

      const dot = document.createElement("div");
      dot.className = "timeline-dot";

      const content = document.createElement("div");
      content.className = "timeline-content";

      // Employment duration
      const date = document.createElement("span");
      date.className = "timeline-date";
      date.textContent = this.formatDuration(experience);

      // Job title
      const title = document.createElement("h3");
      title.textContent = experience.role_title;

      // Company
      const company = document.createElement("h4");
      company.textContent = experience.company;

      // Description
      const description = document.createElement("p");
      description.textContent = experience.description;

      // Employment details
      const details = document.createElement("p");
      details.className = "experience-details";

      details.textContent = [experience.employment_type, experience.location]
        .filter(Boolean)
        .map((value) => value.charAt(0).toUpperCase() + value.slice(1))
        .join(" · ");

      // Associated technologies
      const tech = document.createElement("div");
      tech.className = "experience-tech";

      experience.skills.forEach((skill) => {
        const tag = document.createElement("span");
        tag.textContent = skill.name;
        tag.title = `Proficiency: ${skill.proficiency_level}`;

        tech.appendChild(tag);
      });

      content.append(date, title, company, details, description, tech);

      item.append(dot, content);

      return item;
    },

    formatDuration(experience) {
      const formatDate = (dateString) => {
        const date = new Date(`${dateString}T00:00:00`);

        return date.toLocaleDateString("en-US", {
          month: "short",
          year: "numeric",
        });
      };

      const start = formatDate(experience.start_date);

      const end = experience.is_current
        ? "Present"
        : experience.end_date
          ? formatDate(experience.end_date)
          : "End date unavailable";

      return `${start} – ${end}`;
    },
  },

  /*=====================================================
    Skills
    =====================================================*/

  skills: {
    init() {
      this.loadSkills();
    },

    async loadSkills() {
      const grid = document.querySelector(".skills-grid");

      grid.textContent = "Loading skills...";

      try {
        const categories = await PortfolioApp.api.get("/skills");

        this.renderSkills(categories);

        // Find dynamically created skill cards.
        const skillCards = grid.querySelectorAll(".skill-card");

        // Apply the existing scroll-reveal animation.
        PortfolioApp.animations.observeRevealElements(skillCards);
      } catch (error) {
        console.error("Unable to load skills:", error);

        grid.textContent = "Unable to load skills. Please try again later.";
      }
    },

    renderSkills(categories) {
      const grid = document.querySelector(".skills-grid");

      // Remove the old hardcoded skill cards.
      grid.replaceChildren();

      categories.forEach((category) => {
        const card = this.createSkillCard(category);

        grid.appendChild(card);
      });
    },

    createSkillCard(category) {
      const card = document.createElement("div");
      card.className = "skill-card";

      const heading = document.createElement("h3");
      heading.textContent = category.name;

      const tags = document.createElement("div");
      tags.className = "tech-tags";

      category.skills.forEach((skill) => {
        const tag = document.createElement("span");
        tag.className = "tech-tag";

        const name = document.createElement("span");
        name.className = "skill-name";
        name.textContent = skill.name;

        const proficiency = document.createElement("small");
        proficiency.className = "skill-proficiency";
        proficiency.textContent =
          skill.proficiency_level.charAt(0).toUpperCase() +
          skill.proficiency_level.slice(1);

        tag.title = `${skill.name}: ${skill.proficiency_level}`;

        tag.append(name, proficiency);
        tags.appendChild(tag);
      });

      card.append(heading, tags);

      return card;
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
      this.loadProjects();
    },

    async loadProjects() {
      const grid = document.querySelector(".project-grid");

      grid.textContent = "Loading projects...";

      try {
        const projects = await PortfolioApp.api.get("/projects");

        this.renderProjects(projects);

        // Refresh the cached cards after dynamic rendering.
        PortfolioApp.dom.projectCards = [
          ...grid.querySelectorAll(".project-card"),
        ];
        // Apply scroll-reveal animation to dynamically created cards.
        PortfolioApp.animations.observeRevealElements(
          PortfolioApp.dom.projectCards,
        );
        // Apply the currently selected filter and search.
        this.filterProjects();
      } catch (error) {
        console.error("Unable to load projects:", error);

        grid.textContent = "Unable to load projects. Please try again later.";
      }
    },

    renderProjects(projects) {
      const grid = document.querySelector(".project-grid");

      // Remove existing hardcoded project cards.
      grid.replaceChildren();

      projects.forEach((project) => {
        const card = this.createProjectCard(project);
        grid.appendChild(card);
      });
    },

    createProjectCard(project) {
      const card = document.createElement("article");
      card.className = "project-card";

      // Categories are used by the existing category filters.
      card.dataset.category = project.categories.join(" ");

      const content = document.createElement("div");
      content.className = "project-content";

      const type = document.createElement("span");
      type.className = "project-type";
      type.textContent = project.categories.join(" / ").toUpperCase();

      const title = document.createElement("h3");
      title.textContent = project.title;

      const description = document.createElement("p");
      description.textContent = project.short_description;

      const tech = document.createElement("div");
      tech.className = "project-tech";

      project.skills.forEach((skill) => {
        const tag = document.createElement("span");
        tag.textContent = skill.name;
        tech.appendChild(tag);
      });

      const links = document.createElement("div");
      links.className = "project-links";

      if (project.github_url) {
        const githubLink = document.createElement("a");
        githubLink.href = project.github_url;
        githubLink.textContent = "GitHub";
        githubLink.target = "_blank";
        githubLink.rel = "noopener noreferrer";

        links.appendChild(githubLink);
      }

      if (project.live_url) {
        const liveLink = document.createElement("a");
        liveLink.href = project.live_url;
        liveLink.textContent = "Live Demo";
        liveLink.target = "_blank";
        liveLink.rel = "noopener noreferrer";

        links.appendChild(liveLink);
      }

      content.append(type, title, description, tech);

      if (links.children.length > 0) {
        content.appendChild(links);
      }

      card.appendChild(content);

      return card;
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
      PortfolioApp.dom.projectSearch.addEventListener("input", () =>
        this.filterProjects(),
      );
    },

    filterProjects() {
      const keyword = PortfolioApp.dom.projectSearch.value.toLowerCase().trim();

      let visibleProjects = 0;

      PortfolioApp.dom.projectCards.forEach((card) => {
        const categories = card.dataset.category.split(/\s+/);

        const content = card.textContent.toLowerCase();

        const categoryMatch =
          this.currentFilter === "all" ||
          categories.includes(this.currentFilter);

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

        const heading = document.createElement("h3");
        heading.textContent = "No Projects Found";

        const message = document.createElement("p");
        message.textContent = "Try another keyword or category.";

        empty.append(heading, message);

        document.querySelector(".project-grid").after(empty);
      }

      empty.style.display = count === 0 ? "block" : "none";
    },
  },

  /*=====================================================
    Education
    =====================================================*/

  education: {
    init() {
      this.loadEducation();
    },

    async loadEducation() {
      const container = document.querySelector(".education-card");

      container.textContent = "Loading education...";

      try {
        const records = await PortfolioApp.api.get("/education");

        this.renderEducation(records);

        PortfolioApp.animations.observeRevealElements([container]);
      } catch (error) {
        console.error("Unable to load education:", error);

        container.textContent =
          "Unable to load education. Please try again later.";
      }
    },

    renderEducation(records) {
      const container = document.querySelector(".education-card");

      container.replaceChildren();

      records.forEach((record) => {
        const icon = document.createElement("div");
        icon.className = "education-icon";

        const iconElement = document.createElement("i");
        iconElement.className = "fas fa-graduation-cap";

        icon.appendChild(iconElement);

        const content = document.createElement("div");
        content.className = "education-content";

        const degree = document.createElement("h3");
        degree.textContent = record.degree;

        const field = document.createElement("h4");
        field.textContent = record.field_of_study;

        const institution = document.createElement("p");
        institution.textContent = record.institution;

        const duration = document.createElement("span");
        duration.className = "education-duration";
        duration.textContent = this.formatDuration(record);

        content.append(degree, field, institution, duration);

        if (record.grade) {
          const grade = document.createElement("p");
          grade.textContent = `Grade: ${record.grade}`;
          content.appendChild(grade);
        }

        if (record.description) {
          const description = document.createElement("p");
          description.textContent = record.description;
          content.appendChild(description);
        }

        container.append(icon, content);
      });
    },

    formatDuration(record) {
      const formatDate = (dateString) => {
        const date = new Date(`${dateString}T00:00:00`);

        return date.toLocaleDateString("en-US", {
          month: "short",
          year: "numeric",
        });
      };

      return `${formatDate(record.start_date)} – Expected Graduation ${formatDate(record.end_date)}`;
    },
  },

  /*=====================================================
    CERTIFICATES
    =====================================================*/

  certifications: {
    init() {
      this.loadCertifications();
    },

    async loadCertifications() {
      const grid = document.querySelector(".certificate-grid");

      grid.textContent = "Loading certifications...";

      try {
        const certifications = await PortfolioApp.api.get("/certifications");

        this.renderCertifications(certifications);

        const cards = grid.querySelectorAll(".certificate-card");

        PortfolioApp.animations.observeRevealElements(cards);
      } catch (error) {
        console.error("Unable to load certifications:", error);

        grid.textContent =
          "Unable to load certifications. Please try again later.";
      }
    },

    renderCertifications(certifications) {
      const grid = document.querySelector(".certificate-grid");

      grid.replaceChildren();

      certifications.forEach((certification) => {
        const card = this.createCertificateCard(certification);

        grid.appendChild(card);
      });
    },

    createCertificateCard(certification) {
      const card = document.createElement("article");
      card.className = "certificate-card";

      const icon = document.createElement("i");
      icon.className = "fas fa-award";

      const title = document.createElement("h3");
      title.textContent = certification.title;

      const organization = document.createElement("p");
      organization.className = "certificate-issuer";
      organization.textContent = certification.issuing_organization;

      const description = document.createElement("p");
      description.textContent = certification.description;

      const date = document.createElement("span");
      date.className = "certificate-date";
      date.textContent = certification.issue_date
        ? `Issued ${this.formatDate(certification.issue_date)}`
        : "Issue date unavailable";

      card.append(icon, title, organization, description, date);

      if (certification.credential_url) {
        const link = document.createElement("a");

        link.href = certification.credential_url;
        link.textContent = "View Credential";
        link.target = "_blank";
        link.rel = "noopener noreferrer";

        card.appendChild(link);
      }

      return card;
    },

    formatDate(dateString) {
      const date = new Date(`${dateString}T00:00:00`);

      return date.toLocaleDateString("en-US", {
        month: "long",
        year: "numeric",
      });
    },
  },

  /*=====================================================
    BLOG
    =====================================================*/

  blog: {
    allPosts: [],
    searchKeyword: "",
    defaultLimit: 3,

    init() {
      this.loadPosts();
      this.setupSearch();
    },

    async loadPosts() {
      const grid = document.querySelector(".blog-grid");

      grid.textContent = "Loading articles...";

      try {
        const posts = await PortfolioApp.api.get("/blog");

        // Store all published articles.
        this.allPosts = posts;

        // Sort newest first.
        this.allPosts.sort((a, b) => {
          return new Date(b.published_at) - new Date(a.published_at);
        });

        this.renderPosts();
      } catch (error) {
        console.error("Unable to load blog posts:", error);

        grid.textContent = "Unable to load articles. Please try again later.";
      }
    },

    setupSearch() {
      const searchInput = document.getElementById("blog-search");

      if (!searchInput) return;

      searchInput.addEventListener("input", () => {
        this.searchKeyword = searchInput.value.toLowerCase().trim();

        this.renderPosts();
      });
    },

    renderPosts() {
      const grid = document.querySelector(".blog-grid");
      const resultsInfo = document.querySelector(".blog-results-info");

      grid.replaceChildren();

      let postsToDisplay;

      if (this.searchKeyword) {
        // Search across ALL published articles.
        postsToDisplay = this.allPosts.filter((post) => {
          const searchableText = [post.title, post.excerpt, post.source]
            .filter(Boolean)
            .join(" ")
            .toLowerCase();

          return searchableText.includes(this.searchKeyword);
        });

        resultsInfo.textContent = `${postsToDisplay.length} article(s) found`;
      } else {
        // Show only the latest three by default.
        postsToDisplay = this.allPosts.slice(0, this.defaultLimit);

        resultsInfo.textContent = `Showing latest ${postsToDisplay.length} article(s)`;
      }

      if (postsToDisplay.length === 0) {
        const empty = document.createElement("p");
        empty.className = "blog-empty";
        empty.textContent = "No articles found. Try another keyword.";

        grid.appendChild(empty);
        return;
      }

      postsToDisplay.forEach((post) => {
        const card = this.createPostCard(post);
        grid.appendChild(card);
      });

      // Apply animations to newly generated cards.
      PortfolioApp.animations.observeRevealElements(
        grid.querySelectorAll(".blog-card"),
      );
    },

    createPostCard(post) {
      const card = document.createElement("article");
      card.className = "blog-card";

      const category = document.createElement("span");
      category.textContent = post.source;

      const title = document.createElement("h3");
      title.textContent = post.title;

      const excerpt = document.createElement("p");
      excerpt.textContent = post.excerpt;

      const date = document.createElement("small");
      date.className = "blog-date";
      date.textContent = this.formatDate(post.published_at);

      const link = document.createElement("a");
      link.href = `blog.html?slug=${encodeURIComponent(post.slug)}`;
      link.textContent = "Read Article";

      card.append(category, title, excerpt, date, link);

      return card;
    },

    formatDate(dateString) {
      if (!dateString) return "Publication date unavailable";

      const date = new Date(dateString);

      return date.toLocaleDateString("en-US", {
        day: "numeric",
        month: "long",
        year: "numeric",
      });
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
            visitor_name: form.elements.namedItem("name").value.trim(),
            email: form.elements.namedItem("email").value.trim(),
            subject: form.elements.namedItem("subject").value.trim(),
            message: form.elements.namedItem("message").value.trim(),
          };

          if (!data.visitor_name || !data.email || !data.message) {
            throw new Error("Please fill all required fields.");
          }

          const response = await fetch(
            `${PortfolioApp.config.apiBaseUrl}/contact`,
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify(data),
            },
          );

          const result = await response.json();

          if (!response.ok) {
            const errorMessage = Array.isArray(result.detail)
              ? result.detail.map((error) => error.msg).join(", ")
              : result.detail || "Unable to send your message.";

            throw new Error(errorMessage);
          }

          this.toast(result.message || "Message sent successfully!", "success");

          form.reset();
        } catch (error) {
          console.error("Contact form error:", error);

          this.toast(error.message, "error");
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

    this.projects.init();

    this.skills.init();

    this.contact.init();

    this.experience.init();

    this.education.init();

    this.certifications.init();

    this.blog.init();

    console.log("Portfolio initialized.");
  },
};

/*=========================================================
START
=========================================================*/

document.addEventListener("DOMContentLoaded", () => {
  PortfolioApp.init();
});
