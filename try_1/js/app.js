function analyze() {

  const city = document.getElementById("city").value;

  // Save results (replace with API later)
  localStorage.setItem("disease","Leaf Blight");
  localStorage.setItem("confidence","87%");
  localStorage.setItem("risk","63%");
  localStorage.setItem("weather","32°C, Humidity 78%");

  window.location.href = "results.html";
}

// Display results
window.onload = () => {
  if(document.getElementById("disease")){
    document.getElementById("disease").innerText =
      "Disease: " + localStorage.getItem("disease");

    document.getElementById("confidence").innerText =
      "Confidence: " + localStorage.getItem("confidence");

    document.getElementById("risk").innerText =
      "Risk: " + localStorage.getItem("risk");

    document.getElementById("weather").innerText =
      "Weather: " + localStorage.getItem("weather");
  }
}