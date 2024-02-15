function transferFunds() {
  let toAccount = document.getElementById("toAccountNumber").value;
  let client = JSON.parse(localStorage.getItem("client"));
  let accountNo = client.account.accountNo;
  let amount = document.getElementById("amount").value;
  amount = parseFloat(amount);

  let pin = prompt("Enter your PIN for confirmation:");
  if (pin == null || pin == "") {
    alert("PIN must be filled out");
    return false;
  }

  let data = {
    fromAccount: accountNo,
    toAccount: toAccount,
    amount: amount,
    pin: pin,
  };

  fetch("http://127.0.0.1:8000/client/transfer", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Transfer failed");
      }
      return response.json();
    })
    .then((data) => {
      alert(data.message);
    })
    .catch((error) => {
      alert(error.message);
    });
}
