function paybill() {
  let billId = document.getElementById("billId").value;
  let billType = document.getElementById("type").value;
  let amount = document.getElementById("amount").value;

  let client = JSON.parse(localStorage.getItem("client"));
  let accountNo = client.account.accountNo;
  
  let pin = prompt("Enter your PIN for confirmation:");
  if (pin == null || pin == "") {
    alert("PIN must be filled out");
    return false;
  }
  const data = {
    billId: billId,
    billType: billType,
    amount: amount,
    pin: pin,
  };

  fetch(`http://127.0.0.1:8000/client/billPayment/${accountNo}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Bill payment failed");
      }
      return response.json();
    })
    .then((data) => {
      alert(data.message);
    })
    .catch((error) => {
      alert(error.message);
    });

  return false;
}
