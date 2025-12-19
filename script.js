document.addEventListener('DOMContentLoaded', function() {
    const signInContainer = document.getElementById('signin');
    const signUpContainer = document.getElementById('signup');
    const signUpButton = document.getElementById('signUpButton'); // Button to switch to Sign Up form
    const signInButton = document.getElementById('signInButton'); // Button to switch to Sign In form
    const signUPIContainer = document.getElementById('signUPI');
    const signUPIButton = document.getElementById('signUPIbutton');
    const signInButtonInstructor = document.getElementById('signInButtonInstructor');
    const signUpButtonInstructor = document.getElementById('signUpButtonInstructor');
    const signUPIbuttonStudent = document.getElementById('signUPIbuttonStudent');
    // Get the actual form elements directly by ID
    const signInForm = document.getElementById('login-form');   // Login form
    const signUpForm = document.getElementById('signup-form');   // Signup form
    const signUPIForm = document.getElementById('signUPI-form');

    // Base URL for the FastAPI backend
    const BASE_URL = 'http://127.0.0.1:8000/students';

    // --- Form Switching Logic ---

    function showSignUp() {
        if (signInContainer) signInContainer.style.display = 'none';
        if (signUPIContainer) signUPIContainer.style.display = 'none';
        if (signUpContainer) signUpContainer.style.display = 'block';
    }

    function showSignIn() {
        if (signUpContainer) signUpContainer.style.display = 'none';
        if (signUPIContainer) signUPIContainer.style.display = 'none';
        if (signInContainer) signInContainer.style.display = 'block';
    }

    function showSignUPI() {
        if (signUpContainer) signUpContainer.style.display = 'none';
        if (signInContainer) signInContainer.style.display = 'none';
        if (signUPIContainer) signUPIContainer.style.display = 'block';
    }

    if (signUpButton) {
        signUpButton.addEventListener('click', showSignUp);
    }

    if (signInButton) {
        signInButton.addEventListener('click', showSignIn);
    }

    if (signUPIButton) {
        signUPIButton.addEventListener('click', showSignUPI);
    }
    if (signInButtonInstructor) {
    signInButtonInstructor.addEventListener('click', showSignIn);
    }

    if (signUpButtonInstructor) {
        signUpButtonInstructor.addEventListener('click', showSignUp);
    }

    if (signUPIbuttonStudent) {
        signUPIbuttonStudent.addEventListener('click', showSignUPI);
    }
    
    // --- API Communication Functions ---

    // 1. Handle Sign Up Form Submission
    if (signUpForm) {
        signUpForm.addEventListener('submit', async function(event) {
            event.preventDefault();

            const signUpData = {
                student_id: parseInt(this.ID.value),
                name: this.uName.value,
                email: this['signup-email'].value,
                year: this.year.value,
                track: this.track.value,
                role: this.role.value,
                password: this['signup-password'].value
            };

            try {
                const response = await fetch(`${BASE_URL}/signup`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(signUpData)
                });

                const result = await response.json();

                if (response.ok) {
                    // alert('✅ Registration Successful! Student ID: ' + result.student_id);
                    // Optionally switch to sign-in form
                    window.location.href = 'profile.html';
                } else {
                    let errorMsg = '';
                    if (result.detail) {
                        if (Array.isArray(result.detail)) {
                            errorMsg = result.detail.map(d => d.msg || d).join('\n');
                        } else {
                            errorMsg = result.detail;
                        }
                    } else {
                        errorMsg = JSON.stringify(result);
                    }
                    alert('❌ Registration Failed: ' + errorMsg);
                    console.error('Signup error:', result);
                }

            } catch (error) {
                console.error('Network error:', error);
                alert('⚠️ Connection Error. Make sure the backend server is running at http://127.0.0.1:8000.');
            }
        });
    }

    // 2. Handle Log In Form Submission
    if (signInForm) {
        signInForm.addEventListener('submit', async function(event) {
            event.preventDefault(); // prevent default form submission

            // Read values from input fields
            const email = document.getElementById('signin-email').value.trim();
            const password = document.getElementById('signin-password').value.trim();

            // Simple frontend validation
            if (!email || !password) {
                alert('⚠️ Please enter both email and password.');
                return;
            }

            const loginData = { email, password };

            try {
                const response = await fetch(`${BASE_URL}/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(loginData)
                });

                // Debug logs
                console.log('Login response status:', response.status);
                
                const result = await response.json();
                console.log('Login response JSON:', result);

                if (response.ok) {
                    // Save JWT to localStorage
                    localStorage.setItem('access_token', result.access_token);

                    // alert('🎉 Login Successful!');
                    // Redirect to homepage
                    window.location.href = 'profile.html';
                } else {
                    alert('❌ Login Failed: ' + (result.detail || JSON.stringify(result)));
                }
            } catch (error) {
                console.error('Network error:', error);
                alert('⚠️ Connection Error. Make sure the backend is running at http://127.0.0.1:8000.');
            }
        });
    }
});