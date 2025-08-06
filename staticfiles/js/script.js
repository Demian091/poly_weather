document.addEventListener("DOMContentLoaded", () => {
    // Fade out alerts manually (backup if CSS fails)
    const alerts = document.querySelectorAll(".alert");
    setTimeout(() => {
        alerts.forEach(alert => {
            alert.style.opacity = "0";
            setTimeout(() => alert.style.display = "none", 500);
        });
    }, 4000);
});

