# NU ITCS Volunteering Hub  
**Help Each Other. Grow Together.**

A trusted platform where ITCS students, TAs, faculty, and clubs collaborate academically and in department events — turning volunteering into recognized achievement.

Live Demo (coming soon)

Backend API: Fast APIs

---

### Project Overview
The **NU ITCS Volunteering Hub** connects students who need help with those who can give it — safely, smartly, and with credibility.

- Students volunteer in subjects they excel at (DSA, Logic Design, Math, etc.)  
- TAs & faculty endorse strong helpers  
- Clubs post event volunteering opportunities  
- Admins moderate everything  
- A notification system that alerts volunteers whenever a new opportunity matches their skills.

---

### Features (Phase-wise)

| Phase    | Features                                                | Status      |
|----------|---------------------------------------------------------|-------------|
| Sprint 1 | Register • Login • Profile (CGPA + Skills)              | Done        |
| Sprint 2 | Strengths • Create Posts • Tags (#DSA, #EventVolunteer) | Done        |
| Sprint 3 | Smart Recommendations • Notifications • Endorsements    | Planned     |
| Sprint 4 | Admin Dashboard • Post Approval • Reports • Full Launch | Planned     |

---

### Official Branding
- **Primary Green 
- **Primary Blue 
- **Accent Yellow
- **Tagline**:ITCS Safe Space Hub.

---

### Tech Stack
| Layer        | Technology                |
|-------------|----------------------------|
| Frontend    | HTML/CSS                   |
| Backend     | FastAPI (Python)           |
| Database    | MySQL                      |
| Auth        | JWT + bcrypt               |
| Deployment  | GitHub Pages               |
| Version Control |GitHub Projects (Agile) |

---
Our Wedsite Link: [https://taghreed-oyoun-sm.github.io/NU-ITCS-Volunteering-Hub/frontend/index.html]
### Quick Start (Run Locally)

#### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate    # Windows
# source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
python -m uvicorn APIs.main:app --reload
