// ---------------- CONFIG ----------------
const API_BASE = "http://127.0.0.1:8000"; // can still be used if backend needed

// ---------------- STATIC QUESTIONS ----------------
let questions = JSON.parse(localStorage.getItem("questions")) || [
    {
        id: 1,
        title: "How does recursion work in programming?",
        meta: "Asked in Data Structures",
        tag: "CSCI207",
        answers: "2 Answers",
        votes: 10,
        userVoted: false,
        content: "I understand that a function calls itself, but how does it know when to stop?",
        replies: [
            "The base case is the most important part; it acts as the exit condition.",
            "Think of it like a stack of plates; you add them until you're done, then take them off one by one."
        ]
    },
    {
        id: 2,
        title: "What are the best practices for CSS Flexbox?",
        meta: "Asked in Software Engineering",
        tag: "CSCI313",
        answers: "3 Answers",
        votes: 20,
        userVoted: false,
        content: "Is it better to use flex-basis or just set the width?",
        replies: [
            "Flex-basis is preferred as it respects the flex-direction.",
            "Always use 'gap' instead of margins for spacing between items!"
        ]
    },
    {
        id: 3,
        title: "How to solve second-order differential equations?",
        meta: "Asked in Differential Equations",
        tag: "MATH203",
        answers: "1 Answer",
        votes: 5,
        userVoted: false,
        content: "I’m trying to understand the method of solving second-order differential equations with constant coefficients.",
        replies: [
            "You can try the characteristic equation method; it helps determine the solution type.",
            "Don’t forget to check if it’s homogeneous or non-homogeneous."
        ]
    },
    {
        id: 4,
        title: "What are the key concepts in Logic Design?",
        meta: "Asked in Logic Design",
        tag: "CSCI221",
        answers: "2 Answers",
        votes: 8,
        userVoted: false,
        content: "I’m learning about combinational and sequential circuits. What should I focus on first?",
        replies: [
            "Start with truth tables and Boolean algebra.",
            "Then move to combinational circuits before tackling sequential logic."
        ]
    }
];

let nextId = questions.length + 1;
let currentPostId = null;

// ---------------- SAVE TO LOCALSTORAGE ----------------
function saveQuestions() {
    localStorage.setItem("questions", JSON.stringify(questions));
}

// ---------------- DISPLAY QUESTIONS ----------------
function displayQuestions(filter = "") {
    const container = document.getElementById("questionsContainer");
    container.innerHTML = "";

    questions
        .filter(q => q.tag.toLowerCase().includes(filter.toLowerCase()))
        .forEach(q => {
            const card = document.createElement("div");
            card.className = "question-card";
            card.onclick = () => openQuestion(q.id);

            card.innerHTML = `
                <h3>${q.title}</h3>
                <p>${q.tag} | ${q.meta}</p>
                <span>▲ ${q.votes} Votes</span>
            `;
            container.appendChild(card);
        });

    saveQuestions();
}



// ---------------- OPEN SINGLE QUESTION ----------------
function openQuestion(id) {
    const q = questions.find(item => item.id === id);
    if (!q) return;

    currentPostId = id;
    document.getElementById("exploreSection").style.display = "none";
    document.getElementById("singleQuestionContainer").style.display = "block";
    document.getElementById("detailTag").textContent = q.tag;

    document.getElementById("detailedContent").innerHTML = `
        <h1>${q.title}</h1>
        <p>${q.content}</p>
        <hr>
        <h3>Answers</h3>
        ${q.replies.length
            ? q.replies.map(a => `<div class="answer-card">${a}</div>`).join("")
            : "<p>No answers yet</p>"
        }
    `;
}

// ---------------- POST ANSWER ----------------
document.getElementById("submitAnswerBtn").addEventListener("click", () => {
    const text = document.getElementById("newAnswerText").value.trim();
    if (!text) return alert("Please write an answer first!");

    const q = questions.find(item => item.id === currentPostId);
    q.replies.push(text);
    document.getElementById("newAnswerText").value = "";
    openQuestion(currentPostId);
    displayQuestions();
});

// ---------------- SUBMIT NEW QUESTION ----------------
document.getElementById('submitAsk').addEventListener('click', () => {
    const title = document.getElementById('askTitle').value.trim();
    const content = document.getElementById('askContent').value.trim();
    const tag = document.getElementById('askTag').value.trim();

    if (!title || !content || !tag) return alert("Title, Content, and Tag are required!");

    questions.unshift({
        id: nextId++,
        title,
        content,
        tag,
        meta: "Asked just now",
        votes: 0,
        userVoted: false,
        replies: []
    });

    displayQuestions();

    document.getElementById('askQuestionPage').style.display = 'none';
    document.getElementById('askQuestionBtn').style.display = 'block';
    document.getElementById('askTitle').value = "";
    document.getElementById('askContent').value = "";
    document.getElementById('askTag').value = "";
});

// ---------------- SEARCH ----------------
document.getElementById('searchBtn').addEventListener('click', () => {
    const tag = document.getElementById("tagSearchInput").value.trim();
    displayQuestions(tag);
});

// ---------------- SHOW/HIDE ASK FORM ----------------
document.getElementById('askQuestionBtn').addEventListener('click', () => {
    document.getElementById('askQuestionPage').style.display = 'block';
    document.getElementById('askQuestionBtn').style.display = 'none';
});
document.getElementById('backFromAsk').addEventListener('click', () => {
    document.getElementById('askQuestionPage').style.display = 'none';
    document.getElementById('askQuestionBtn').style.display = 'block';
});

// ---------------- CLOSE SINGLE QUESTION ----------------
function closeQuestion() {
    document.getElementById('singleQuestionContainer').style.display = 'none';
    document.getElementById('exploreSection').style.display = 'block';
}

// ---------------- INITIALIZE ----------------
document.addEventListener('DOMContentLoaded', () => {
    displayQuestions();
});
