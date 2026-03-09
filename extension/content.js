(function () {
  if (document.getElementById("leadmind-linkedin-btn")) return;

  const btn = document.createElement("button");
  btn.id = "leadmind-linkedin-btn";
  btn.innerText = "Analyze with LeadMind AI";
  btn.style.position = "fixed";
  btn.style.bottom = "20px";
  btn.style.right = "20px";
  btn.style.zIndex = "999999";
  btn.style.background = "#0A66C2";
  btn.style.color = "white";
  btn.style.border = "none";
  btn.style.padding = "10px 14px";
  btn.style.borderRadius = "10px";
  btn.style.cursor = "pointer";

  document.body.appendChild(btn);

  btn.onclick = async () => {
    const text = document.body.innerText.slice(0, 16000);
    btn.innerText = "Analyzing...";
    try {
      const res = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content: text, source_type: "linkedin", tone: "professional" })
      });
      const data = await res.json();
      alert(data.result || data.detail || "No response");
    } catch (e) {
      alert(`LeadMind failed: ${e}`);
    } finally {
      btn.innerText = "Analyze with LeadMind AI";
    }
  };
})();
