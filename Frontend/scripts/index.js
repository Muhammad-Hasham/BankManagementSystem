function showBalance() {
  let balance = 0;
  let client = JSON.parse(localStorage.getItem("client"));
  let accountNo = client.account.accountNo;

  fetch(`http://127.0.0.1:8000/client/balance/${accountNo}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Balance fetch failed");
      }
      return response.json();
    })
    .then((data) => {
      balance = data.balance;
      document.getElementById("balance").innerHTML = balance;
    })
    .catch((error) => {
      alert(error.message);
    });
}

function navigateToTransferFund() {
  window.location.href = "fundTransfer.html";
}

function navigateToPayBill() {
  window.location.href = "paybill.html";
}

function navigateToChangePin() {
  window.location.href = "changePIN.html";
}

function navigateToLogout() {
  window.location.href = "home.html";
}

function navigateToHome() {
  window.location.href = "index.html";
}

function navigateToViewTranscationHistory() {
  window.location.href = "transactions.html";
}

function navigateToUpdateProfile() {
  window.location.href = "updateProfile.html";
}

function generateEStatement() {
  let client = JSON.parse(localStorage.getItem("client"));
  let accountNo = client.account.accountNo;

  fetch(`http://127.0.0.1:8000/client/transactions/${accountNo}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Statement generation failed");
      }
      return response.json();
    })
    .then((data) => {
      console.log(data);
      let transactions = data.transactions;
      // write transaction history to a csv file
      let csvContent = "data:text/csv;charset=utf-8,";
      csvContent +=
        "Transaction ID,Transaction Type,From Account,To Account,Amount,Date\n";

      transactions.forEach((transaction) => {
        csvContent += `${transaction.transactionId},${transaction.transactionType},${transaction.fromAccount},${transaction.toAccount},${transaction.amount},${transaction.date}\n`;
      });

      var encodedUri = encodeURI(csvContent);
      var link = document.createElement("a");
      link.setAttribute("href", encodedUri);
      link.setAttribute("download", "statement.csv");
      document.body.appendChild(link); // Required for FF
      link.click();

    })
    .catch((error) => {
      alert(error.message);
    });
}
