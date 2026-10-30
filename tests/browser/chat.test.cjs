const { test, before, after } = require("node:test");
const assert = require("node:assert/strict");
const { spawn } = require("node:child_process");
const { existsSync } = require("node:fs");
const path = require("node:path");
const { chromium } = require("playwright");
const AxeBuilder = require("@axe-core/playwright").default;

const base = "http://127.0.0.1:5174";
let browser, server;
before(async () => {
  const portable = path.resolve(".runtime/python/python.exe");
  const python = process.env.PYTHON_BIN || (existsSync(portable) ? portable : "python");
  server = spawn(python, ["-m", "http.server", "5174", "--bind", "127.0.0.1", "--directory", "frontend/public"], { stdio: "ignore", windowsHide: true });
  for (let attempt = 0; attempt < 50; attempt++) {
    try { if ((await fetch(base)).ok) break; } catch {}
    if (attempt === 49) throw new Error("Frontend test server did not start");
    await new Promise((resolve) => setTimeout(resolve, 100));
  }
  browser = await chromium.launch({ headless: true });
});
after(async () => { await browser?.close(); server?.kill(); });

async function pageFor(t) {
  const context = await browser.newContext();
  const page = await context.newPage();
  t.after(() => context.close());
  await page.route("**/api/health", (route) => route.fulfill({ json: { status: "ready", articleCount: 30, keyConfigured: true } }));
  return page;
}
async function open(page) {
  await page.goto(base);
  await page.getByRole("button", { name: "Open support chat", exact: true }).click();
  await page.waitForFunction(() => document.querySelector("#connection").textContent.includes("Connected"));
}
const source = { title: "YouTube guide", url: "https://support.optisigns.com/hc/en-us/articles/360051014713", excerpt: "Open Files/Assets, select Apps, and choose YouTube." };
const result = { mode: "search", answer: null, sources: [source], notice: "Document excerpts, not a generated answer." };

test("keyboard search renders sources as text and supports clearing", async (t) => {
  const page = await pageFor(t);
  await page.route("**/api/chat", async (route) => {
    const request = route.request().postDataJSON();
    assert.deepEqual(Object.keys(request).sort(), ["mode", "question"]);
    await route.fulfill({ json: { ...result, sources: [{ ...source, excerpt: '<img src=x onerror="window.hacked=true">' }] } });
  });
  await open(page);
  await page.getByRole("button", { name: "Add a YouTube video" }).click();
  await page.getByLabel("Your question", { exact: true }).press("Enter");
  await page.locator(".source").waitFor();
  assert.equal(await page.locator(".source img").count(), 0);
  assert.match(await page.locator(".source p").innerText(), /<img/);
  assert.equal(await page.locator(".source a").getAttribute("rel"), "noopener noreferrer");
  await page.getByRole("button", { name: "Clear", exact: true }).click();
  assert.equal(await page.locator(".source").count(), 0);
  assert.equal(await page.locator("#empty").isVisible(), true);
});

test("quota error retains question and offers search without a fake answer", async (t) => {
  const page = await pageFor(t);
  await page.route("**/api/chat", (route) => route.fulfill({ status: 503, json: { error: { code: "quota_exhausted", message: "The API project has no available credits. Use document search." } } }));
  await open(page);
  await page.getByRole("radio", { name: "Ask assistant", exact: true }).check();
  await page.locator("#question").fill("How do I add a YouTube video?");
  await page.locator("#question").press("Enter");
  await page.locator("#error").waitFor();
  assert.match(await page.locator("#error").innerText(), /credits/);
  assert.equal(await page.locator("#question").inputValue(), "How do I add a YouTube video?");
  assert.equal(await page.locator(".answer-text").count(), 0);
  await page.getByRole("button", { name: "Use document search instead" }).click();
  assert.equal(await page.getByRole("radio", { name: "Search docs", exact: true }).isChecked(), true);
});

test("loading prevents duplicate sends", async (t) => {
  const page = await pageFor(t);
  let release, requests = 0;
  const gate = new Promise((resolve) => { release = resolve; });
  await page.route("**/api/chat", async (route) => { requests++; await gate; await route.fulfill({ json: result }); });
  await open(page);
  await page.locator("#question").fill("YouTube setup");
  await page.locator("#question").press("Enter");
  await page.locator("#loading").waitFor();
  assert.equal(await page.locator("#send").isDisabled(), true);
  assert.equal(await page.locator("#question").getAttribute("readonly"), "");
  await page.locator("#question").press("Enter");
  release();
  await page.locator(".source").waitFor();
  assert.equal(requests, 1);
});

test("empty retrieval is an explicit empty state", async (t) => {
  const page = await pageFor(t);
  await page.route("**/api/chat", (route) => route.fulfill({ json: { ...result, sources: [] } }));
  await open(page);
  await page.locator("#question").fill("Unmatched topic");
  await page.locator("#question").press("Enter");
  await page.locator(".no-results").waitFor();
  assert.match(await page.locator(".no-results").innerText(), /No matching/);
});

test("responsive results do not overflow and pass accessibility checks", async (t) => {
  const page = await pageFor(t);
  await page.route("**/api/chat", (route) => route.fulfill({ json: { ...result, sources: [{ ...source, excerpt: "LongUnbrokenText".repeat(100) }] } }));
  await open(page);
  await page.locator("#question").fill("Show documentation");
  await page.locator("#question").press("Enter");
  await page.locator(".source").waitFor();
  for (const width of [320, 768, 1024, 1440]) {
    await page.setViewportSize({ width, height: 900 });
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true, `overflow at ${width}px`);
    if (width === 320) {
      const mobileFindings = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"]).analyze();
      assert.deepEqual(mobileFindings.violations.map((item) => item.id), []);
    }
  }
  const findings = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"]).analyze();
  assert.deepEqual(findings.violations.map((item) => ({ id: item.id, nodes: item.nodes.map((n) => n.target) })), []);
});

test("missing backend disables sends and explains how to start it", async (t) => {
  const page = await pageFor(t);
  await page.unroute("**/api/health");
  await page.route("**/api/health", (route) => route.abort("connectionrefused"));
  await page.goto(base);
  await page.getByRole("button", { name: "Open support chat", exact: true }).click();
  await page.getByText("Backend unavailable", { exact: true }).waitFor();
  assert.match(await page.locator("#setup-message").innerText(), /server.py/);
  assert.equal(await page.locator("#send").isDisabled(), true);
});

test("floating widget opens, closes with Escape and preserves the draft", async (t) => {
  const page = await pageFor(t);
  await page.goto(base);
  assert.equal(await page.locator("#chat-widget").isVisible(), false);
  await page.getByRole("button", { name: "Chat with OptiBot" }).click();
  assert.equal(await page.locator("#chat-launcher").getAttribute("aria-expanded"), "true");
  for (const viewport of [{ width: 320, height: 568 }, { width: 768, height: 400 }]) {
    await page.setViewportSize(viewport);
    const box = await page.locator("#chat-widget").boundingBox();
    assert.ok(box.x >= 0 && box.y >= 0 && box.x + box.width <= viewport.width && box.y + box.height <= viewport.height);
    assert.equal(await page.locator("#send").isVisible(), true);
  }
  await page.locator("#question").fill("My draft question");
  await page.locator("#question").press("Escape");
  assert.equal(await page.locator("#chat-widget").isVisible(), false);
  assert.equal(await page.locator("#chat-launcher").evaluate((el) => el === document.activeElement), true);
  await page.getByRole("button", { name: "Open support chat", exact: true }).click();
  assert.equal(await page.locator("#question").inputValue(), "My draft question");
  await page.getByRole("button", { name: "Close chat", exact: true }).click();
  assert.equal(await page.locator("#chat-widget").isVisible(), false);
});
