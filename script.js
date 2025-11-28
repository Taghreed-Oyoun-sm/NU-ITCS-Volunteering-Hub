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

