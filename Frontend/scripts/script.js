document
  .getElementById("loginForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();
  });

function login() {
  let accountNumber = document.getElementById("accountNumber").value;
  let pin = document.getElementById("pin").value;

  let data = {
    accountNo: accountNumber,
    pin: pin,
  };

  fetch("http://127.0.0.1:8000/client/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Login failed");
      }
      return response.json();
    })
    .then((data) => {
      alert("Login successful!");
      localStorage.setItem("client", JSON.stringify(data.data));
      window.location.href = "index.html";
    })
    .catch((error) => {
      alert(error.message);
    });
}

