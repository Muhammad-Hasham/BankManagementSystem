const transactions = []

document.addEventListener("DOMContentLoaded", () => {
  const client = JSON.parse(localStorage.getItem("client"));
  const accountNo = client.account.accountNo;

  fetch(`http://127.0.0.1:8000/client/transactions/${accountNo}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Transactions fetch failed");
      }
      return response.json();
    })
    .then((data) => {
      transactions.push(...data.transactions);
      populateTransactionList();
    })
    .catch((error) => {
      alert(error.message);
    });
});



// Function to generate HTML for a transaction card
function createTransactionCard(transaction) {
  const card = document.createElement("div");
  card.classList.add("transaction-card");

  const details = document.createElement("div");
  details.classList.add("transaction-details");
  details.innerHTML = `
            <p><strong>Transaction ID:</strong> ${
              transaction.transactionId || "N/A"
            }</p>
            <p><strong>To Account:</strong> ${transaction.toAccount}</p>
            <p><strong>Date:</strong> ${transaction.date}</p>
            <p><strong>Type:</strong> ${transaction.transactionType}</p>
        `;

  const amount = document.createElement("div");
  amount.classList.add("transaction-amount");
  amount.textContent = `$${transaction.amount}`;

  card.appendChild(details);
  card.appendChild(amount);

  return card;
}

// Function to populate the transaction list
function populateTransactionList() {
  const transactionList = document.querySelector(".transaction-list");
  transactions.forEach((transaction) => {
    const card = createTransactionCard(transaction);
    transactionList.appendChild(card);
  });
}

