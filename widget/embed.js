(function () {
  const root = document.createElement("div");
  root.id = "leadmind-widget";
  root.style = "position:fixed;bottom:20px;right:20px;width:320px;background:#fff;border:1px solid #ddd;border-radius:12px;padding:12px;z-index:99999;font-family:Arial,sans-serif;box-shadow:0 6px 24px rgba(0,0,0,.15);";

  root.innerHTML = `
    <h4 style="margin:0 0 8px;color:#0A66C2;">LeadMind AI</h4>
    <textarea id="lm-input" style="width:100%;height:90px;border:1px solid #ccc;border-radius:8px;padding:8px;" placeholder="Paste profile/company info..."></textarea>
    <button id="lm-run" style="margin-top:8px;width:100%;background:#0A66C2;color:#fff;border:none;border-radius:8px;padding:8px;cursor:pointer;">Analyze</button>
    <pre id="lm-output" style="white-space:pre-wrap;font-size:12px;max-height:180px;overflow:auto;margin-top:8px;background:#f8fafc;padding:8px;border-radius:8px;"></pre>
  `;

  document.body.appendChild(root);

  document.getElementById("lm-run").onclick = async () => {
    const text = document.getElementById("lm-input").value;
    const out = document.getElementById("lm-output");
    out.textContent = "Analyzing...";

    try {
      const res = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content: text, source_type: "mixed", tone: "professional" })
      });
      const data = await res.json();
      out.textContent = data.result || data.detail || "No response";
    } catch (e) {
      out.textContent = `Error: ${e}`;
    }
  };
})();
