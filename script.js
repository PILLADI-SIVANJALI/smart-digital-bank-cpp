// ===============================
// SMART DIGITAL BANK - script.js
// ===============================

// Show / Hide Password
console.log("Script loaded");
console.log("JavaScript connected");
const togglePassword = document.getElementById("togglePassword");
const pinInput = document.getElementById("pin");

if (togglePassword && pinInput) {

    togglePassword.addEventListener("click", function () {

        if (pinInput.type === "password") {
            pinInput.type = "text";
            this.innerHTML = '<i class="fa-solid fa-eye-slash"></i>';
        }
        else {
            pinInput.type = "password";
            this.innerHTML = '<i class="fa-solid fa-eye"></i>';
        }

    });

}

// =========================
// Register Validation
// =========================

const registerForm = document.getElementById("registerForm");

if(registerForm){

registerForm.addEventListener("submit",function(e){

e.preventDefault();

let name=document.getElementById("name").value.trim();
let age=document.getElementById("age").value;
let mobile=document.getElementById("mobile").value.trim();
let email=document.getElementById("email").value.trim();
let deposit=document.getElementById("deposit").value;
let pin=document.getElementById("newPin").value.trim();
let confirm=document.getElementById("confirmPin").value.trim();

if(name.length<3){

alert("Enter a valid name.");
return;

}

if(age<18){

alert("Applicant must be at least 18 years old.");
return;

}

if(!/^[0-9]{10}$/.test(mobile)){

alert("Enter a valid 10-digit mobile number.");
return;

}

if(deposit<1000){

alert("Minimum opening balance is ₹1000.");
return;

}

if(!/^[0-9]{4}$/.test(pin)){

alert("PIN must contain exactly 4 digits.");
return;

}

if(pin!==confirm){

alert("PINs do not match.");
return;

}

alert("Account Created Successfully!");

window.location.href="login.html";

});

}


function login(event)
{
    event.preventDefault();

    let account = document.getElementById("account").value.trim();
    let pin = document.getElementById("pin").value.trim();

    fetch("/login",
    {
        method:"POST",

        headers:
        {
            "Content-Type":"application/json"
        },

        body:JSON.stringify(
        {
            account:account,
            pin:pin
        })

    })

    .then(response=>response.json())

    .then(data=>{

        if(data.status=="success")
        {
            localStorage.setItem("account", account);
            localStorage.setItem("name", data.name);
            localStorage.setItem("balance", data.balance);

            window.location.href="dashboard.html";
        }

        else
        {
            alert(data.message);
        }

    })

    .catch(error=>{

        console.log(error);

        alert("Cannot connect to Flask Server");

    });

}

function logout()
{
    localStorage.clear();

    window.location.href="login.html";
}


function depositMoney(event)
{
    event.preventDefault();

    let account = localStorage.getItem("account");

    let amount = document.getElementById("depositAmount").value;

    fetch("/deposit",
    {
        method:"POST",

        headers:
        {
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            account:account,
            amount:amount

        })

    })

    .then(response=>response.json())

    .then(data=>{

        if(data.status=="success")
        {
            alert("Deposit Successful");

            localStorage.setItem("balance",data.balance);

            document.getElementById("currentBalance").innerHTML=
            "₹"+data.balance;

            window.location.href="dashboard.html";
        }

        else
        {
            alert(data.message);
        }

    })

    .catch(error=>{

        console.log(error);

        alert("Server Error");

    });

}

function withdrawMoney(event)
{
    event.preventDefault();

    let account = localStorage.getItem("account");

    let amount = document.getElementById("withdrawAmount").value;

    fetch("/withdraw",
    {
        method:"POST",

        headers:
        {
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            account:account,
            amount:amount
        })

    })

    .then(response=>response.json())

    .then(data=>{

        if(data.status=="success")
        {
            alert("Withdrawal Successful");

            localStorage.setItem("balance",data.balance);

            window.location.href="dashboard.html";
        }

        else
        {
            alert(data.message);
        }

    })

    .catch(error=>{

        console.log(error);

        alert("Server Error");

    });

}


function transferMoney(event)
{
    event.preventDefault();

    let account = localStorage.getItem("account");

    let receiver =
    document.getElementById("receiverAccount").value;

    let amount =
    document.getElementById("transferAmount").value;

    fetch("/transfer",
    {
        method:"POST",

        headers:
        {
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            sender:account,
            receiver:receiver,
            amount:amount

        })

    })

    .then(response=>response.json())

    .then(data=>{

        if(data.status=="success")
        {
            alert("Transfer Successful");

            localStorage.setItem("balance",data.balance);

            window.location.href="dashboard.html";
        }

        else
        {
            alert(data.message);
        }

    })

    .catch(error=>{

        console.log(error);

        alert("Server Error");

    });

}

// ===============================
// LOAD INVOICES
// ===============================

function loadInvoices()
{
    let account = localStorage.getItem("account");

    if(!account)
    {
        document.getElementById("invoiceContainer").innerHTML =
        "<div class='no-invoice'>" +
        "<h2>Please Login First</h2>" +
        "<p>Please login to view your invoices.</p>" +
        "</div>";

        return;
    }

    fetch("/invoices?account=" + account)
    .then(response => response.json())

    .then(data => {

        if(data.success)
        {
            let invoices = data.invoices;

            if(!invoices || invoices.length === 0)
            {
                document.getElementById("invoiceContainer").innerHTML =
                "<div class='no-invoice'>" +
                "<h2>No Transactions Yet</h2>" +
                "<p>Your invoices will appear here after a successful transaction.</p>" +
                "</div>";

                return;
            }


            let html = "";


            invoices.forEach(invoice => {

                html +=

                "<div class='invoice-card'>" +

                "<div class='invoice-header'>" +

                "<div>" +

                "<h2>" +
                "<i class='fa-solid fa-building-columns'></i> " +
                "Smart Digital Bank" +
                "</h2>" +

                "<p>Transaction Invoice</p>" +

                "</div>" +

                "<i class='fa-solid fa-file-invoice'></i>" +

                "</div>" +

                "<hr>" +

                "<div class='invoice-details'>" +

                "<p><strong>Transaction ID:</strong> " +
                (invoice.transaction_id || "N/A") +
                "</p>" +

                "<p><strong>Account Number:</strong> " +
                (invoice.account || account) +
                "</p>" +

                "<p><strong>Customer Name:</strong> " +
                (invoice.name || "N/A") +
                "</p>" +

                "<p><strong>Transaction Type:</strong> " +
                (invoice.type || "N/A") +
                "</p>" +

                "<p><strong>Amount:</strong> ₹" +
                (invoice.amount || "0") +
                "</p>" +

                "<p><strong>Previous Balance:</strong> ₹" +
                (invoice.old_balance || "0") +
                "</p>" +

                "<p><strong>New Balance:</strong> ₹" +
                (invoice.balance || "0") +
                "</p>";


                if(invoice.receiver)
                {
                    html +=
                    "<p><strong>Receiver Account:</strong> " +
                    invoice.receiver +
                    "</p>";
                }


                html +=

                "</div>" +

                "<div class='success'>" +
                "<i class='fa-solid fa-circle-check'></i> " +
                "Transaction Successful" +
                "</div>" +

                "<button class='print-button' onclick='window.print()'>" +
                "<i class='fa-solid fa-print'></i> " +
                "Print Invoice" +
                "</button>" +

                "</div>";

            });


            document.getElementById("invoiceContainer").innerHTML =
            html;

        }

        else
        {
            document.getElementById("invoiceContainer").innerHTML =
            "<div class='no-invoice'>" +
            "<h2>Error</h2>" +
            "<p>" + data.message + "</p>" +
            "</div>";
        }

    })

    .catch(error => {

        console.log(error);

        document.getElementById("invoiceContainer").innerHTML =
        "<div class='no-invoice'>" +
        "<h2>Cannot Connect to Server</h2>" +
        "<p>Please make sure Flask is running on port 5000.</p>" +
        "</div>";

    });
}