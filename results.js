function displayResults() {
  const results = JSON.parse(localStorage.getItem("results"));
  const resultsBody = document.getElementById("results-body");

  results.forEach(result => {
    const row = resultsBody.insertRow();

    const cell1 = row.insertCell(0);
    const cell2 = row.insertCell(1);
    const cell3 = row.insertCell(2);
    const cell4 = row.insertCell(3);
    const cell5 = row.insertCell(4);
    

    cell1.innerHTML = result.name;
    cell2.innerHTML = result.usage.toFixed(1);
    cell3.innerHTML = result.price.toFixed(0);
    cell4.innerHTML = result.co2.toFixed(0);
    cell5.innerHTML = result.co2Difference.toFixed(0);
  });
}

displayResults();