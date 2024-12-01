
function showreview(className) {
    // Hide all review sections
    document.querySelectorAll('.diffreview .reviewmain').forEach(div => {
        div.style.display = 'none';
    });
    
    // Show the selected review section
    if (className) {
        const element = document.querySelector(`.${className}`);
        if (element) {
            element.style.display = 'block';
        }
    }
}
