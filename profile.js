// --- Profile Data Management ---
function updateUserInfo() {
    const name = document.getElementById('updateName').value.trim();
    const email = document.getElementById('updateEmail').value.trim();

    if (name && email) {
        document.getElementById('displayUserName').innerText = name;
        document.getElementById('displayUserEmail').innerText = email;
        alert("Information saved!");
    } else {
        alert("Please fill in both name and email.");
    }
}

function changePassword() {
    const pass = document.getElementById('newPass').value;
    if (pass.length > 0) {
        alert("Password updated!");
        document.getElementById('newPass').value = "";
    }
}

// --- Custom Logout Modal Logic ---
function showLogoutModal() {
    document.getElementById('logoutModal').style.display = 'flex';
}

function closeLogoutModal() {
    document.getElementById('logoutModal').style.display = 'none';
}

function confirmLogout() {
    // Redirects to your login/signup page
    window.location.href = "signup_signin.html";
}