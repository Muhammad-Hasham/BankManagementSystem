function changePin() {
  let oldPin = document.getElementById("oldPin").value;
  let newPin = document.getElementById("newPin").value;
  let confirmPin = document.getElementById("confirmNewPin").value;

  // check if new pin and confirm pin are same
  if (newPin != confirmPin) {
    alert("New PIN and Confirm PIN must be same");
    return false;
  }

  let client = JSON.parse(localStorage.getItem("client"));
  let accountNo = client.account.accountNo;

  let data = {
    oldPin: oldPin,
    newPin: newPin,
  };

  fetch(`http://127.0.0.1:8000/client/updatePin/${accountNo}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("PIN change failed");
      }
      return response.json();
    })
    .then((data) => {
        alert("PIN changed successfully");
        window.location.href = "index.html";
    })
    .catch((error) => {
      alert(error.message);
    });
}
