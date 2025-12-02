document.addEventListener("DOMContentLoaded", () => {
  const quoteTextEl = document.getElementById("quoteText");
  const quoteAuthorEl = document.getElementById("quoteAuthor");
  const btnRandom = document.getElementById("btnRandom");
  const btnList = document.getElementById("btnList");
  const addForm = document.getElementById("addForm");
  const msgEl = document.getElementById("msg");

  function showMessage(text, type = "success") {
    if (!msgEl) {
      console.warn("Message element missing:", text);
      return;
    }
    msgEl.innerHTML = `<div class="alert alert-${type}" role="alert">${text}</div>`;
    setTimeout(() => (msgEl.innerHTML = ""), 3500);
  }

  async function fetchRandom() {
    try {
      const res = await fetch("/api/quote");
      if (!res.ok) {
        let body;
        try {
          body = await res.json();
        } catch (e) {
          body = { message: await res.text() };
        }
        showMessage(body.message || `Error ${res.status}`, "danger");
        return;
      }
      const q = await res.json();

      if (!quoteTextEl || !quoteAuthorEl) {
        console.error("Missing DOM elements: quoteText or quoteAuthor");
        showMessage("UI not loaded correctly", "danger");
        return;
      }

      // The API returns an object with `text` and `author`
      quoteTextEl.innerText = q.text || q.quote || "No text";
      quoteAuthorEl.innerText = q.author ? `— ${q.author}` : "";
    } catch (e) {
      console.error("fetchRandom error:", e);
      showMessage(e.message || "Network error", "danger");
    }
  }

  async function listAll() {
    try {
      const res = await fetch("/api/quotes");
      if (!res.ok) {
        const txt = await res.text();
        throw new Error(`Server returned ${res.status}: ${txt}`);
      }
      const arr = await res.json();
      console.table(arr);
      showMessage("Quotes printed to console (open DevTools).", "info");
    } catch (e) {
      console.error("listAll error:", e);
      showMessage(e.message || "Cannot list quotes", "danger");
    }
  }

  async function addQuoteHandler(ev) {
    ev.preventDefault();
    const textInput = document.getElementById("inputText");
    const authorInput = document.getElementById("inputAuthor");
    const text = textInput?.value?.trim();
    const author = authorInput?.value?.trim();

    if (!text) {
      showMessage("Quote text required", "warning");
      return;
    }

    try {
      const res = await fetch("/api/quotes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, author }),
      });

      let payload;
      try {
        payload = await res.json();
      } catch (err) {
        const textBody = await res.text();
        throw new Error("Server returned non-JSON: " + textBody);
      }

      if (!res.ok) {
        showMessage(payload.message || `Failed to add (${res.status})`, "danger");
        console.error("Server error adding quote:", payload);
        return;
      }

      showMessage("Added quote (id: " + payload.id + ")", "success");
      if (textInput) textInput.value = "";
      if (authorInput) authorInput.value = "";
    } catch (e) {
      console.error("Add quote error:", e);
      showMessage(e.message || "Network error", "danger");
    }
  }

  btnRandom?.addEventListener("click", fetchRandom);
  btnList?.addEventListener("click", listAll);
  addForm?.addEventListener("submit", addQuoteHandler);
});
