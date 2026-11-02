"use strict";

const BlogDetail = {
  apiBaseUrl: "http://127.0.0.1:8000/api/v1",

  async init() {
    const params = new URLSearchParams(window.location.search);
    const slug = params.get("slug");

    if (!slug) {
      this.showError("No article slug was provided.");
      return;
    }

    await this.loadArticle(slug);
  },

  async loadArticle(slug) {
    try {
      const response = await fetch(
        `${this.apiBaseUrl}/blog/${encodeURIComponent(slug)}`,
      );

      if (!response.ok) {
        throw new Error(
          response.status === 404
            ? "This article does not exist."
            : "Unable to load the article.",
        );
      }

      const article = await response.json();

      this.renderArticle(article);
    } catch (error) {
      console.error("Blog article error:", error);
      this.showError(error.message);
    }
  },

  renderArticle(article) {
    document.title = `${article.title} | Zulkarnain`;

    document.getElementById("article-category").textContent =
      article.source || "Article";

    document.getElementById("article-title").textContent = article.title;

    document.getElementById("article-meta").textContent = article.published_at
      ? new Date(article.published_at).toLocaleDateString("en-US", {
          day: "numeric",
          month: "long",
          year: "numeric",
        })
      : "";

    const cover = document.getElementById("article-cover");

    if (article.cover_image_url) {
      cover.src = article.cover_image_url;
      cover.alt = article.title;
      cover.hidden = false;
    }

    document.getElementById("article-content").textContent =
      article.content || article.excerpt || "";

    if (article.external_url) {
      const externalLink = document.createElement("a");

      externalLink.href = article.external_url;
      externalLink.textContent = "View Original Article";
      externalLink.target = "_blank";
      externalLink.rel = "noopener noreferrer";

      document.getElementById("article-content").appendChild(externalLink);
    }
  },

  showError(message) {
    document.getElementById("blog-article").hidden = true;
    document.getElementById("article-error").hidden = false;
    document.getElementById("error-message").textContent = message;
  },
};

document.addEventListener("DOMContentLoaded", () => {
  BlogDetail.init();
});
