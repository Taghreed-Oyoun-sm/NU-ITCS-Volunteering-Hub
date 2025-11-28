const signUpButton=document.getElementById('signUpButton');
const signIpButton=document.getElementById('signInButton');
const signInForm=document.getElementById('signin');
const signUpForm=document.getElementById('signup');

signUpButton.addEventListener('click',function(){
    signInForm.style.display="none";
    signUpForm.style.display="block";
});
signInButton.addEventListener('click',function(){
    signUpForm.style.display="none";
    signInForm.style.display="block";
});
registerForm.addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent page refresh

    const formData = new FormData(registerForm);
    
    // Convert string inputs to the data types required by your UserCreate DTO
    // NOTE: Values for 're' and 'jta' are strings "true"/"false" from HTML, converted to bool.
    // NOTE: 'cgpa' is converted to float. 'ID' is converted to int.
    const data = {
        student_id: parseInt(formData.get('ID')),
        name: formData.get('uName'),
        email: formData.get('email'),
        password: formData.get('password'),
        
        // Data from <select> fields:
        year: formData.get('year').replace('en', ''), // Corrects 'Freshmen' to 'Freshman' to match DTO
        track: formData.get('track'), // Requires HTML fix (see notes below)
        cgpa: parseFloat(formData.get('cgpa')),
        research_skills: formData.get('re') === 'true',
        jta_skills: formData.get('jta') === 'true',
        
        // Capitalizes the role to match the DTO ('student' -> 'Student')
        role: formData.get('role').charAt(0).toUpperCase() + formData.get('role').slice(1).split('/')[0] 
    };

    try {
        const response = await fetch(`${BACKEND_BASE_URL}/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            console.log("Signup successful:", result);
            alert("Registration Successful! Welcome, " + result.name + ".");
            // Switch to login form after successful registration
            registerForm.reset();
            signUpFormContainer.style.display = "none";
            signInFormContainer.style.display = "block";
        } else {
            console.error("Signup failed:", result);
            // Display specific error detail from the backend (e.g., "Email already registered")
            alert(`Registration Failed: ${result.detail || 'Server error occurred'}`);
        }

    } catch (error) {
        console.error("Network or fetch error:", error);
        alert("An error occurred. Check if the FastAPI backend server is running on localhost:8000.");
    }
});


// ----------------------------------------------------
// --- NEW LOGIC: LOGIN ---
// ----------------------------------------------------
loginForm.addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent page refresh

    const formData = new FormData(loginForm);
    const data = {
        email: formData.get('email'),
        password: formData.get('password')
    };

    try {
        const response = await fetch(`${BACKEND_BASE_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            // Login successful!
            const token = result.access_token;
            console.log("Login successful. Token received:", token);
            alert("Login Successful! You are now authenticated.");
            
            // Store the token (CRITICAL for protected routes)
            localStorage.setItem('access_token', token);
            
            // You can now redirect the user to a protected page
            // window.location.href = '/dashboard.html'; 

        } else {
            console.error("Login failed:", result);
            alert(`Login Failed: ${result.detail || 'Invalid email or password'}`);
        }

    } catch (error) {
        console.error("Network or fetch error:", error);
        alert("An error occurred. Check if the backend server is running.");
    }
});

