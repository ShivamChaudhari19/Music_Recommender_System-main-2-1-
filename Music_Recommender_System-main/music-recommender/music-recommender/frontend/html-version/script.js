document.getElementById("recommendBtn").addEventListener("click", async () => {
  const songInput = document.getElementById("song").value.trim();

  if (!songInput) {
    alert("Please enter a song name.");
    return;
  }

  try {
    console.log("Sending request to backend...");

    const response = await fetch("http://127.0.0.1:5000/recommend", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ song: songInput }),
    });

    if (!response.ok) {
      throw new Error("Failed to fetch recommendations");
    }

    const data = await response.json();
    console.log("Response:", data);

    const recommendations = data.recommendations;
    const resultBox = document.getElementById("recommendations");

    if (recommendations.length === 0) {
      resultBox.innerHTML = "<p>No recommendations found.</p>";
    } else {
      resultBox.innerHTML = "<h3>Recommended Songs:</h3><ul>" +
        recommendations.map(song => `<li>${song}</li>`).join("") +
        "</ul>";
    }

  } catch (error) {
    console.error(error);
    alert("Error: Could not get recommendations. Make sure the backend is running.");
  }
});

