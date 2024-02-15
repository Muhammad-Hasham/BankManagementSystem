function showUpdateForm(formId) {
  // Hide all update forms
  const forms = document.querySelectorAll(".update-form");
  forms.forEach((form) => {
    form.style.display = "none";
  });

  // Show the selected update form
  const selectedForm = document.getElementById(formId);
  if (selectedForm) {
    selectedForm.style.display = "block";
  }
}

function updateEmail() {
  let client = JSON.parse(localStorage.getItem("client"));
  let accountNo = client.account.accountNo;
 
  let email = document.getElementById("newEmail").value;

  let data = {
    newEmail: email,
  };

  fetch(`http://127.0.0.1:8000/client/updateEmail/${accountNo}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Email update failed");
      }
      return response.json();
    })
    .then((data) => {
      alert(data);
    })
    .catch((error) => {
      alert(error.message);
    });
}

function updatePhone() {
  let client = JSON.parse(localStorage.getItem("client"));
  let accountNo = client.account.accountNo;
 
  let phone = document.getElementById("newPhoneNumber").value;

  let data = {
    newPhoneNo: phone,
  };

  fetch(`http://127.0.0.1:8000/client/updatePhone/${accountNo}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Phone update failed");
      }
      return response.json();
    })
    .then((data) => {
      alert(data);
    })
    .catch((error) => {
      alert(error.message);
    });
}

function updateAddress() {
  let client = JSON.parse(localStorage.getItem("client"));
  let accountNo = client.account.accountNo;
 
  let address = document.getElementById("newAddress").value;

  let data = {
    newAddress: address,
  };

  fetch(`http://localhost:8000/client/updateAddress/${accountNo}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Address update failed");
      }
      return response.json();
    })
    .then((data) => {
      alert(data);
    })
    .catch((error) => {
      alert(error.message);
    });
}

function updateOccupation() {
  let client = JSON.parse(localStorage.getItem("client"));
  let accountNo = client.account.accountNo;
 
  let occupation = document.getElementById("newOccupation").value;

  let data = {
    newOccupation: occupation,
  };

  fetch(`http://localhost:8000/client/updateOccupation/${accountNo}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Occupation update failed");
      }
      return response.json();
    })
    .then((data) => {
      alert(data);
    })
    .catch((error) => {
      alert(error.message);
    });
}
