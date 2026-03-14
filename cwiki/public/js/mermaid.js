console.log("CWIKI: mermaid_init.js loaded");

frappe.ready(() => {
	console.log("CWIKI: frappe.ready triggered");

	if (!window.mermaid) {
		console.error("Mermaid not loaded");
		return;
	}

	mermaid.initialize({
		startOnLoad: false,
		securityLevel: "loose",
	});

	const blocks = document.querySelectorAll("code.language-mermaid");

	blocks.forEach((el) => {
		const pre = el.closest("pre");
		if (!pre) return;

		// prevent double conversion
		if (pre.dataset.mermaidProcessed) return;

		const div = document.createElement("div");
		div.className = "mermaid";
		div.textContent = el.textContent.trim();

		pre.dataset.mermaidProcessed = "true";
		pre.replaceWith(div);
	});

	// only run on unprocessed mermaid containers
	mermaid.run({
		querySelector: ".mermaid:not([data-processed])",
	});

	document.querySelectorAll(".mermaid").forEach((el) => {
		el.dataset.processed = "true";
	});
});
