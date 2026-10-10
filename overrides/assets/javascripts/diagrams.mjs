const codeBlocks = [...document.querySelectorAll(
  "pre > code.language-mermaid, pre.mermaid-source > code"
)];

if (codeBlocks.length) {
  const { default: mermaid } = await import(
    "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs"
  );
  const diagrams = codeBlocks.map(code => {
    const container = document.createElement("div");
    container.className = "mermaid";
    const source = code.textContent;
    code.parentElement.replaceWith(container);
    return { container, source };
  });

  async function renderDiagrams() {
    mermaid.initialize({
      startOnLoad: false,
      theme: document.body.dataset.mdColorScheme === "slate" ? "dark" : "default"
    });
    for (const { container, source } of diagrams) {
      container.removeAttribute("data-processed");
      container.textContent = source;
    }
    await mermaid.run({ nodes: diagrams.map(d => d.container) });
  }

  await renderDiagrams();
  new MutationObserver(renderDiagrams).observe(document.body, {
    attributes: true,
    attributeFilter: ["data-md-color-scheme"]
  });
}

