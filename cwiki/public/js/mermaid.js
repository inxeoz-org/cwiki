console.log("CWIKI: mermaid_init.js loaded MArk2");

frappe.ready(() => {
	console.log("CWIKI: frappe.ready triggered");

	if (!window.mermaid) {
		console.error("CWIKI: Mermaid NOT loaded");
		return;
	}

	mermaid.initialize({
		startOnLoad: false,
		securityLevel: "loose",
	});

	// Only target markdown code blocks
	const blocks = document.querySelectorAll("code.language-mermaid");

	console.log("CWIKI: Mermaid code blocks found:", blocks.length);

	blocks.forEach((el) => {
		const pre = el.closest("pre");
		if (!pre) return;

		const div = document.createElement("div");
		div.className = "mermaid";
		div.textContent = el.textContent.trim();

		pre.replaceWith(div);
	});

	console.log("CWIKI: Running mermaid.run()");
	mermaid.run();
});
