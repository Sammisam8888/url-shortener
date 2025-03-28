
function copyToClipboard() {
    let shortUrlInput = document.getElementById("short-link");
    if (shortUrlInput.value) {
        shortUrlInput.select();
        document.execCommand("copy");
        alert("Short URL copied to clipboard!");
    } else {
        alert("No URL to copy!");
    }
}
