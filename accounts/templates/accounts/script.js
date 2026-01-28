const API = "http://127.0.0.1:8000/accounts/";  
const msgBox = document.getElementById('msg');

// Helper to show messages
function showMsg(text, isError = false) {
    msgBox.innerText = "Status: " + text;
    msgBox.style.color = isError ? "red" : "green";
}

// 1. REGISTRATION
async function doRegister() {
    const res = await fetch(API + 'register/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            username: document.getElementById('rUser').value,
            email: document.getElementById('rEmail').value,
            password: document.getElementById('rPass').value
        })
    });
    const data = await res.json();
    if (res.ok) {
        showMsg("Registration Successful! Please Login below.");
    } else {
        showMsg("Registration Failed: " + JSON.stringify(data), true);
    }
}

// 2. LOGIN
async function doLogin() {
    const res = await fetch(API + 'login/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            username: document.getElementById('lUser').value,
            password: document.getElementById('lPass').value
        })
    });
    const data = await res.json();
    if (res.ok) {
        localStorage.setItem('access', data.access);
        localStorage.setItem('refresh', data.refresh);
        
        // Switch Sections
        document.getElementById('authSection').classList.add('hidden');
        document.getElementById('dashSection').classList.remove('hidden');
        showMsg("Login Successful! Access Token stored.");
    } else {
        showMsg("Login Failed. Check credentials.", true);
    }
}

// 3. FORGET PASSWORD (SECTION 1)
async function doForget() {
    const res = await fetch(API + 'forget-password/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ email: document.getElementById('fEmail').value })
    });
    const data = await res.json();
    if (res.ok) {
        document.getElementById('recoveryForm').classList.remove('hidden');
        document.getElementById('fUid').value = data.uid;
        document.getElementById('fToken').value = data.token;
        showMsg("Recovery Token Generated! Finish the form below.");
    } else {
        showMsg("Email not found.", true);
    }
}

// 4. CONFIRM RECOVERY
async function doConfirmReset() {
    const res = await fetch(API + 'reset-confirm/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            uid: document.getElementById('fUid').value,
            token: document.getElementById('fToken').value,
            new_password: document.getElementById('fNewPass').value
        })
    });
    const data = await res.json();
    if (res.ok) {
        showMsg("Account Recovered! You can now login with your new password.");
        document.getElementById('recoveryForm').classList.add('hidden');
    } else {
        showMsg("Recovery Failed: " + data.error, true);
    }
}

// 5. UPDATE PASSWORD (SECTION 2 - LOGGED IN)
async function doUpdatePass() {
    const token = localStorage.getItem('access');
    const res = await fetch(API + 'update-password/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify({ new_password: document.getElementById('uNewPass').value })
    });
    const data = await res.json();
    if (res.ok) {
        showMsg("Password Updated Successfully via Secure JWT Wrapper!");
    } else {
        showMsg("Update Failed. Session might be expired.", true);
    }
}

function doLogout() {
    localStorage.clear();
    location.reload();
}