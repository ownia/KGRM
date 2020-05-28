window.MathJax.Hub.Config({
    showProcessingMessages: false,
    messageStyle: "none",
    jax: ["input/TeX", "output/HTML-CSS"],
    tex2jax: {
        inlineMath: [["$", "$"], ["\\(", "\\)"]],
        displayMath: [["$$", "$$"], ["\\[", "\\]"]],
        skipTags: ["script", "noscript", "style", "textarea", "pre", "code", "a"]
    },
    "HTML-CSS": {
        availableFonts: ["STIX", "TeX"],
        showMathMenu: false
    }
});
window.MathJax.Hub.Queue(["Typeset", MathJax.Hub, document.getElementsByClassName("ck-content")]);
