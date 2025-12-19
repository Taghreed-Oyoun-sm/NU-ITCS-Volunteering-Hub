const questions = [
    {
        id: 1,
        title: "How does recursion work in programming?",
        meta: "Asked in Data Structures",
        tag: "CSCI207",
        answers: "2 Answers",
        votes: 10,
        userVoted: false, // Track if user has clicked upvote
        content: "I understand that a function calls itself, but how does it know when to stop?",
        replies: ["The base case is the most important part; it acts as the exit condition.", "Think of it like a stack of plates; you add them until you're done, then take them off one by one."]
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
        replies: ["Flex-basis is preferred as it respects the flex-direction.", "Always use 'gap' instead of margins for spacing between items!"]
    }
];

let nextId = questions.length + 1;

function displayQuestions(filterTag = "") {
    const container = document.getElementById('questionsContainer');
    if (!container) return;
    container.innerHTML = "";

    const filtered = questions.filter(q => 
        q.tag.toLowerCase().includes(filterTag.toLowerCase())
    );

    filtered.forEach(q => {
        const card = document.createElement('div');
        card.className = 'question-card clickable';
        card.onclick = () => openQuestion(q.id);

        card.innerHTML = `
            <h3 class="question-title">${q.title}</h3>
            <p class="question-meta">${q.meta} * ${q.answers}</p>
            <div class="card-footer">
                <span class="votes">▲ ${q.votes} Votes</span>
                <span class="tag-label">${q.tag}</span>
            </div>
        `;
        container.appendChild(card);
    });
}

function handleUpvote(id) {
    const q = questions.find(item => item.id === id);
    
    if (q.userVoted) {
        q.votes -= 1;
        q.userVoted = false;
    } else {
        q.votes += 1;
        q.userVoted = true;
    }
    
    openQuestion(id); 
    displayQuestions(); 
}

function postAnswer(id) {
    const answerInput = document.getElementById('newAnswerText');
    const answerText = answerInput.value.trim();
    if (!answerText) return alert("Please write an answer first!");

    const q = questions.find(item => item.id === id);
    q.replies.push(answerText);
    q.answers = `${q.replies.length} Answers`;
    
    answerInput.value = "";
    openQuestion(id);
    displayQuestions();
}

function openQuestion(id) {
    const q = questions.find(item => item.id === id);
    document.getElementById('exploreSection').style.display = 'none';
    document.getElementById('singleQuestionContainer').style.display = 'block';

    document.getElementById('detailTag').innerText = q.tag;
    
    // Change button color if voted
    const voteBtnStyle = q.userVoted 
        ? "background: #0364a0; color: white;" 
        : "background: #e0f2f1; color: #0364a0;";

    document.getElementById('detailedContent').innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <h1 style="color: #333; margin-bottom: 20px; flex: 1;">${q.title}</h1>
            <button onclick="handleUpvote(${q.id})" style="${voteBtnStyle} border: 1px solid #0364a0; padding: 10px; border-radius: 8px; cursor: pointer; font-weight: bold; margin-left: 20px; transition: 0.3s;">
                ▲ ${q.votes} Votes
            </button>
        </div>
        <p style="font-size: 1.1em; color: #555; line-height: 1.6;">${q.content}</p>
        <hr style="border: 0.5px solid #eee; margin: 30px 0;">
        <h3 style="color: #fba203;">Answers:</h3>
        <div id="answersList">
            ${q.replies.length > 0 ? q.replies.map(r => `<div class="answer-card">${r}</div>`).join('') : '<p style="color: #888;">No answers yet.</p>'}
        </div>
    `;

    document.getElementById('submitAnswerBtn').onclick = () => postAnswer(id);
    window.scrollTo(0, 0);
}

function closeQuestion() {
    document.getElementById('singleQuestionContainer').style.display = 'none';
    document.getElementById('exploreSection').style.display = 'block';
}

document.addEventListener('DOMContentLoaded', () => {
    displayQuestions();

    // Form logic
    document.getElementById('askQuestionBtn').addEventListener('click', () => {
        document.getElementById('askQuestionPage').style.display = 'block';
        document.getElementById('askQuestionBtn').style.display = 'none';
    });

    document.getElementById('backFromAsk').addEventListener('click', () => {
        document.getElementById('askQuestionPage').style.display = 'none';
        document.getElementById('askQuestionBtn').style.display = 'block';
    });

    document.getElementById('submitAsk').addEventListener('click', () => {
        const title = document.getElementById('askTitle').value.trim();
        const content = document.getElementById('askContent').value.trim();
        const tag = document.getElementById('askTag').value.trim();

        if (!title || !content || !tag) return alert("Title, Content, and Tag are mandatory!");

        questions.unshift({
            id: nextId++,
            title: title,
            content: content,
            tag: tag.toUpperCase(),
            meta: document.getElementById('askMeta').value.trim() || "Asked just now",
            answers: "0 Answers",
            votes: 0,
            userVoted: false,
            replies: []
        });

        displayQuestions();
        document.getElementById('askQuestionPage').style.display = 'none';
        document.getElementById('askQuestionBtn').style.display = 'block';
    });

    // Search logic
    document.getElementById('searchBtn').addEventListener('click', () => {
        displayQuestions(document.getElementById('tagSearchInput').value.trim());
    });
});