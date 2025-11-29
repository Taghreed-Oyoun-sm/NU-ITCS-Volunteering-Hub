document.addEventListener('DOMContentLoaded', function() {
    const signInContainer = document.getElementById('signin');
    const signUpContainer = document.getElementById('signup');
    const signUpButton = document.getElementById('signUpButton'); // Button to switch to Sign Up form
    const signInButton = document.getElementById('signInButton'); // Button to switch to Sign In form
    
    // Get the actual form elements
    // The Log In form is inside the #signin container
    const signInForm = signInContainer ? signInContainer.querySelector('form') : null;
    // The Sign Up form is inside the #signup container
    const signUpForm = signUpContainer ? signUpContainer.querySelector('form') : null;

    // Base URL for the FastAPI backend
    const BASE_URL = 'http://127.0.0.1:8000/students';

    // --- Form Switching Logic ---

    function showSignUp() {
        if (signInContainer) signInContainer.style.display = 'none';
        if (signUpContainer) signUpContainer.style.display = 'block';
    }

    function showSignIn() {
        if (signUpContainer) signUpContainer.style.display = 'none';
        if (signInContainer) signInContainer.style.display = 'block';
    }

    if (signUpButton) {
        signUpButton.addEventListener('click', showSignUp);
    }

    if (signInButton) {
        signInButton.addEventListener('click', showSignIn);
    }
    
    // --- API Communication Functions ---

    // 1. Handle Sign Up Form Submission
    if (signUpForm) {
        signUpForm.addEventListener('submit', async function(event) {
            event.preventDefault(); // Stop default form submission

            // Get form data and map it to the UserCreate DTO structure
            const signUpData = {
                // student_id is the 'ID' input
                student_id: parseInt(this.ID.value), 
                name: this.uName.value,
                email: this.email.value,
                
                // Get value from select menus
                year: this.year.value,
                track: this.track.value,
                
                cgpa: parseFloat(this.cgpa.value),
                
                // Note: The role field is included in the HTML/DTO but not used in the Python create_user function.
                // Assuming you will add 'role' to the DTO and need it here:
                // role: this.role.value, 
                
                // Convert select values ("true"/"false") to booleans
                research_skills: this.re.value === 'true', 
                jta_skills: this.jta.value === 'true',     
                password: this.password.value
            };

            try {
                const response = await fetch(`${BASE_URL}/register`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(signUpData)
                });

                if (response.ok) {
                    const result = await response.json();
                    alert('✅ Registration Successful! Student ID: ' + result.student_id);
                    showSignIn(); // Switch to login form after successful registration
                } else {
                    const error = await response.json();
                    alert('❌ Registration Failed: ' + (error.detail || 'Server error. Check backend logs.'));
                }
            } catch (error) {
                console.error('Network Error:', error);
                alert('⚠️ Connection Error. Make sure the backend server is running on http://127.0.0.1:8000.');
            }
        });
    }

    // 2. Handle Log In Form Submission
    if (signInForm) {
        signInForm.addEventListener('submit', async function(event) {
            event.preventDefault(); // Stop default form submission
            
            // FastAPI's OAuth2PasswordRequestForm expects data as application/x-www-form-urlencoded
            // with keys 'username' (for email) and 'password'.
            const loginData = new URLSearchParams();
            loginData.append('username', this.email.value); 
            loginData.append('password', this.password.value);

            try {
                // The backend /login endpoint returns a JWT token
                const response = await fetch(`${BASE_URL}/login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded' 
                    },
                    body: loginData.toString()
                });

                if (response.ok) {
                    const token = await response.json();
                    // Store the JWT token (critical for accessing protected pages)
                    localStorage.setItem('access_token', token.access_token);
                    alert('🎉 Login Successful! Welcome.');
                    
                    // Redirect to the home page (home.html)
                    window.location.href = 'home.html'; 
                } else {
                    const error = await response.json();
                    alert('❌ Login Failed: ' + (error.detail || 'Invalid Credentials'));
                }
            } catch (error) {
                console.error('Network Error:', error);
                alert('⚠️ Connection Error. Make sure the backend server is running on http://127.0.0.1:8000.');
            }
        });
    }
});