// Main UI logic for portfolio pages
document.addEventListener("DOMContentLoaded", function() {
    // Theme toggle initialization
    const themeToggle = document.getElementById("themeToggle");
    const themeIcon = document.getElementById("themeIcon");
    
    const activeTheme = localStorage.getItem("portfolio-theme") || "light";
    document.documentElement.setAttribute("data-bs-theme", activeTheme);
    updateIcon(activeTheme);

    if (themeToggle) {
        themeToggle.addEventListener("click", () => {
            const currentTheme = document.documentElement.getAttribute("data-bs-theme");
            const newTheme = currentTheme === "dark" ? "light" : "dark";
            
            document.documentElement.setAttribute("data-bs-theme", newTheme);
            localStorage.setItem("portfolio-theme", newTheme);
            updateIcon(newTheme);
        });
    }

    function updateIcon(theme) {
        if (!themeIcon) return;
        if (theme === "dark") {
            themeIcon.className = "bi bi-sun-fill text-warning";
        } else {
            themeIcon.className = "bi bi-moon-stars-fill";
        }
    }
});
