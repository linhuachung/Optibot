"use strict";

const apiBase = location.port === "5173" ? "http://127.0.0.1:8000" : "";
const byId = (id) => document.getElementById(id);
const form = byId("chat-form");
const input = byId("question");
let busy = false;
let ready = false;
let pendingReply = null;

function mode() { return document.querySelector('input[name="mode"]:checked').value; }
function updateControls() {
  input.readOnly = busy;
  byId("send").disabled = busy || !ready || !input.value.trim();
  byId("clear").disabled = busy || !byId("messages").children.length;
  document.querySelectorAll('input[name="mode"]').forEach((item) => { item.disabled = busy; });
  byId("send").firstChild.textContent = mode() === "search" ? "Search " : "Ask ";
  byId("mode-help").textContent = mode() === "search" ? "Find matching passages and their source articles." : "Get a concise answer with source citations. Available API credits are required.";
  byId("character-count").textContent = `${input.value.length.toLocaleString()} / 2,000`;
  form.setAttribute("aria-busy", String(busy));
}
function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}
function addQuestion(question) {
  const item = element("section", "message");
  item.append(element("span", "message-label", "You"), element("p", "question-text", question));
  byId("messages").append(item);
  byId("empty").hidden = true;
  document.querySelector(".conversation-area").scrollTop = document.querySelector(".conversation-area").scrollHeight;
}
function addResult(result) {
  const item = element("section", "message assistant-message");
  item.append(element("span", "message-label", result.mode === "search" ? "Documentation" : "OptiBot"));
  if (result.answer) item.append(element("p", "answer-text", result.answer));
  item.append(element("p", "result-notice", result.notice));
  const sources = element("div", "sources");
  for (const source of result.sources) {
    const url = new URL(source.url);
    if (url.protocol !== "https:" || url.hostname !== "support.optisigns.com") continue;
    const card = element("article", "source");
    const link = element("a", "", `${source.title} ↗`);
    link.href = url.href;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    card.append(link);
    if (source.excerpt) {
      const text = source.excerpt.replace(/^#[^\n]*\n+Article URL:[^\n]*\nArticle ID:[^\n]*\nSource updated:[^\n]*\n+/, "");
      const excerpt = element("p", "", text);
      excerpt.tabIndex = 0;
      card.append(excerpt);
    }
    sources.append(card);
  }
  if (!sources.children.length) sources.append(element("p", "no-results", result.mode === "search" ? "No matching passages found. Try a more specific question." : "No source citations were returned. The documentation may not support this question."));
  item.append(sources);
  byId("messages").append(item);
  revealReply(item);
}
function revealReply(item) {
  if (widget.hidden) { pendingReply = item; return; }
  const conversation = document.querySelector(".conversation-area");
  conversation.scrollTop += item.getBoundingClientRect().top - conversation.getBoundingClientRect().top - 12;
  pendingReply = null;
}
async function checkHealth() {
  try {
    const response = await fetch(`${apiBase}/api/health`);
    if (!response.ok) throw new Error("Document state could not be loaded. Check the backend setup.");
    const health = await response.json();
    ready = health.status === "ready";
    byId("article-count").textContent = health.articleCount;
    byId("connection").textContent = ready ? `${health.articleCount} articles · Connected` : "Setup needed";
    if (!ready) {
      byId("setup-message").textContent = health.keyConfigured ? "No indexed documents yet. Run python main.py on the backend, then refresh this page." : "Add an API key to the backend's .env file, then restart the backend.";
      byId("setup-message").hidden = false;
    }
  } catch (error) {
    byId("connection").textContent = "Backend unavailable";
    byId("setup-message").textContent = "Start the backend with python server.py, then refresh this page. The frontend connects to port 8000.";
    byId("setup-message").hidden = false;
  }
  updateControls();
}
form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const question = input.value.trim();
  if (!question || busy || !ready) return;
  const selectedMode = mode();
  busy = true;
  byId("error").hidden = true;
  byId("loading").hidden = false;
  byId("loading-label").textContent = selectedMode === "search" ? "Searching your documents…" : "Preparing your answer…";
  addQuestion(question);
  updateControls();
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 45000);
  try {
    const response = await fetch(`${apiBase}/api/chat`, { method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, mode: selectedMode }), signal: controller.signal });
    const result = await response.json();
    if (!response.ok) {
      const error = new Error(result.error?.message || "The request could not be completed. Please retry.");
      error.code = result.error?.code;
      throw error;
    }
    addResult(result);
    input.value = "";
  } catch (error) {
    byId("error-message").textContent = error.name === "AbortError" ? "The request took too long. Your question is still here; please retry." : error.message || "Could not reach the backend. Check that it is running.";
    byId("switch-search").hidden = error.code !== "quota_exhausted";
    byId("error").hidden = false;
  } finally {
    clearTimeout(timeout);
    busy = false;
    byId("loading").hidden = true;
    updateControls();
    input.focus({ preventScroll: true });
  }
});
input.addEventListener("input", updateControls);
input.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey && !event.isComposing) { event.preventDefault(); if (!byId("send").disabled) form.requestSubmit(); }
});
document.querySelectorAll('input[name="mode"]').forEach((item) => item.addEventListener("change", updateControls));
document.querySelectorAll("[data-question]").forEach((button) => button.addEventListener("click", () => {
  input.value = button.dataset.question; updateControls(); input.focus();
}));
byId("switch-search").addEventListener("click", () => { document.querySelector('input[value="search"]').checked = true; updateControls(); input.focus(); });
byId("clear").addEventListener("click", () => { byId("messages").replaceChildren(); byId("empty").hidden = false; byId("error").hidden = true; updateControls(); input.focus(); });
checkHealth();

const widget = byId("chat-widget");
const launcher = byId("chat-launcher");
function setChatOpen(open) {
  widget.hidden = !open;
  launcher.setAttribute("aria-expanded", String(open));
  launcher.setAttribute("aria-label", open ? "Close support chat" : "Open support chat");
  if (open) {
    if (pendingReply) revealReply(pendingReply);
    input.focus({ preventScroll: true });
  }
  else launcher.focus({ preventScroll: true });
}
launcher.addEventListener("click", () => setChatOpen(widget.hidden));
byId("open-chat").addEventListener("click", () => setChatOpen(true));
byId("close-chat").addEventListener("click", () => setChatOpen(false));
widget.addEventListener("keydown", (event) => {
  if (event.key === "Escape") { event.preventDefault(); setChatOpen(false); }
});
