async function performSearch() {
  const query = document.getElementById("query").value;
  const Category = document.getElementById("category").value;
  const resultsDiv = document.getElementById("results");
 
  if (!query) {
    resultsDiv.innerHTML = '<p class="error-message">Please enter a query!</p>';
    return;
  }
 
 
resultsDiv.innerHTML = `
    <div class="loading">
      <span></span><span></span><span></span><span></span><span></span>
    </div>
  `;
 
  const functionUrl = "http://localhost:7071/api/HttpTrigger1";
  const url = new URL(functionUrl);
  url.searchParams.append("query", query);
  if (Category) url.searchParams.append("Category", Category);
 
  try {
    const response = await fetch(url);
    const data = await response.json();
 
    if (response.ok) {
      const gptResponse = `
        <div class="gpt-response">
          <strong>Response:</strong>
          <p>${data.gpt_response}</p>
        </div>
      `;
 
      const searchResults = data.results
  .map(
    (result) => `
    <div class="result-item" onclick="showModal('${result.name}', '${result.Category}', '${result.url}', '${result.score}')">
      <h4>${result.name}</h4>
      <p><strong>Category:</strong> ${result.Category}</p>
      <p class="score"><strong>Score:</strong> ${result.score}</p>
      <a href="${result.url}" target="_blank" class="reference-button">Reference Document</a>
    </div>
  `
  )
  .join("");
 
      if (data.gpt_response === "NOTFOUND") {
        resultsDiv.innerHTML = gptResponse;
      } else if (data.gpt_response !== "NOTFOUND") {
        resultsDiv.innerHTML = gptResponse + searchResults;
      }
    } else {
      resultsDiv.innerHTML = `<p class="error-message">Error: ${data.error}</p>`;
    }
  } catch (error) {
    resultsDiv.innerHTML = `<p class="error-message">An unexpected error occurred. Please try again later.</p>`;
    console.error(error);
  }
}
 
function showModal(name, Category, url, score) {
  const modal = document.getElementById("modal");
  const modalBody = document.getElementById("modal-body");
  modalBody.innerHTML = `
    <h2>${name}</h2>
    <p><strong>Category:</strong> ${Category}</p>
    <p class="score"><strong>Score:</strong> ${score}</p>
    <a href="${url}" target="_blank" class="reference-button">Reference Document</a>
  `;
  modal.style.display = "block";
}
 
 
function closeModal() {
  const modal = document.getElementById("modal");
  modal.style.display = "none";
}
 
window.onclick = function (event) {
  const modal = document.getElementById("modal");
  if (event.target == modal) {
    modal.style.display = "none";
  }
};
 
 