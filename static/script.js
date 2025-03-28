document.getElementById("shorten-form").addEventListener("submit", function(event) {
    event.preventDefault();
    let originalUrl = document.getElementById("original_url").value;

    fetch("/", {
        method: "POST",
        body: new URLSearchParams({ "original_url": originalUrl }),
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
    })
    .then(response => response.json())
    .then(data => {
        let shortUrl = data.short_url;
        document.getElementById("short-url").value = shortUrl;
        document.getElementById("result").style.display = "block";
    });
});

function copyToClipboard() {
    let shortUrlInput = document.getElementById("short-url");
    shortUrlInput.select();
    document.execCommand("copy");
    alert("Short URL copied to clipboard!");
}
