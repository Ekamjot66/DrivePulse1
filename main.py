from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any
import json
import os

app = FastAPI(title="DrivePulse API")

# Enable CORS in case you open HTML files via Live Server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "db.json"

DEFAULT_DB = {
    "user": {
        "name": "Aarav Sharma",
        "short": "Aarav S. (CSE '26)",
        "initials": "AS",
        "branch": "B.Tech CSE · Class of 2026"
    },
    "state": {
        "voted": [101],
        "saved": [101],
        "done": {"TCS": 0}
    },
    "companies": [
        {"name": "TCS", "sector": "IT Services", "diff": "Easy", "ctc": "7 - 11.5 LPA", "cgpa": 6.5, "rounds": "3 (NQT + Tech + HR)"},
        {"name": "Infosys", "sector": "IT Consulting", "diff": "Medium", "ctc": "6.5 - 9.5 LPA", "cgpa": 6.0, "rounds": "3 (OA + Tech + HR)"},
        {"name": "Amazon", "sector": "Product / E-Commerce", "diff": "Hard", "ctc": "28 - 45 LPA", "cgpa": 7.0, "rounds": "4 (OA + 3 Tech/Bar Raiser)"},
        {"name": "Deloitte", "sector": "Consulting", "diff": "Medium", "ctc": "7.6 - 11 LPA", "cgpa": 6.5, "rounds": "3 (Aptitude + JAM/GD + Interview)"}
    ],
    "debriefs": [
        {
            "id": 101,
            "co": "Amazon",
            "role": "SDE-1",
            "diff": "Hard",
            "up": 24,
            "by": "Riya K. (CSE '25)",
            "r1": "2 DSA questions on HackerRank (Sliding Window + DP) + Work Style Assessment.",
            "r2": "Bar Raiser & Technical: Rotten Oranges (BFS) and Low-Level Design of a Parking Lot.",
            "r3": "Managerial & LP: Deep dive into resume projects and Amazon Leadership Principles.",
            "tip": "Never skip Leadership Principles. Frame every project answer in STAR format.",
            "ver": True,
            "mine": False
        },
        {
            "id": 102,
            "co": "TCS",
            "role": "Prime Developer",
            "diff": "Easy",
            "up": 15,
            "by": "Karan M. (IT '25)",
            "r1": "TCS NQT: Numerical, Verbal, Reasoning + 2 coding questions (Arrays & Strings).",
            "r2": "Technical: SQL joins, ACID properties, OOPs pillars, and live code for palindrome check.",
            "r3": "HR: Relocation willingness, night shifts, and TCS bond policy verification.",
            "tip": "Be thorough with everything written on your resume and basic DBMS queries.",
            "ver": True,
            "mine": False
        },
        {
            "id": 103,
            "co": "Deloitte",
            "role": "Analyst",
            "diff": "Medium",
            "up": 9,
            "by": "Sneha P. (ECE '25)",
            "r1": "AMCAT platform: Quantitative aptitude, logical reasoning, and verbal ability.",
            "r2": "Group Discussion / Case Study on AI adoption in banking, followed by Tech interview.",
            "r3": "Versant test + Final partner round focusing on situational problem-solving.",
            "tip": "Communication clarity during the case study matters more than complex jargon.",
            "ver": True,
            "mine": False
        }
    ],
    "pathways": {
        "TCS": [
            "Solve 15 previous TCS NQT numerical & reasoning questions",
            "Practice array & number manipulation problems in C++/Java/Python",
            "Revise OOP concepts (Polymorphism, Inheritance, Encapsulation)",
            "Practice SQL queries (INNER/LEFT JOIN, GROUP BY, HAVING)",
            "Prepare a crisp 2-minute explanation of your main academic project",
            "Review DBMS normal forms (1NF to BCNF) and OS basics",
            "Prepare standard HR answers & verify all documentation"
        ],
        "Infosys": [
            "Practice pseudocode & puzzle-solving questions (Infosys SP/DSE pattern)",
            "Solve 5 Medium Dynamic Programming and Greedy problems",
            "Revise Computer Networks (OSI model, TCP/IP, HTTP vs HTTPS)",
            "Review Software Engineering life cycle (Agile, Scrum, Waterfall)",
            "Do a line-by-line review of your resume tech stack",
            "Practice 10 common puzzles from GeeksforGeeks",
            "Mock interview with a peer focusing on clear communication"
        ],
        "Amazon": [
            "Solve 10 LeetCode Mediums on Trees, Graphs (BFS/DFS), and Heaps",
            "Solve 8 LeetCode Medium/Hard on Sliding Window, Two Pointers, and DP",
            "Write down 2 STAR stories for each of the 16 Amazon Leadership Principles",
            "Revise CS Fundamentals: OS concurrency, deadlocks, and DBMS indexing",
            "Practice Low-Level Design (LLD) & Object-Oriented Design patterns",
            "Take a timed 90-minute 2-question Online Assessment mock",
            "Review time & space complexities of all standard data structures"
        ],
        "Deloitte": [
            "Practice 20 timed Quantitative Aptitude & Data Interpretation sets",
            "Read 3 recent tech-consulting case studies (Cloud, AI, Cybersecurity)",
            "Revise SQL queries and foundational Python/Java syntax",
            "Prepare a structured intro and role-fit pitch for consulting",
            "Practice speaking for 2 minutes on abstract topics (JAM prep)",
            "Review your resume projects focusing on business impact",
            "Prepare 3 thoughtful questions to ask the interviewer"
        ]
    }
}


def read_db() -> Dict[str, Any]:
    if not os.path.exists(DB_FILE):
        write_db(DEFAULT_DB)
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def write_db(data: Dict[str, Any]):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


@app.get("/api/db")
def get_db():
    """Returns the complete db.json contents."""
    return read_db()


@app.put("/api/db")
def update_db(payload: Dict[str, Any]):
    """Saves updated state, new debriefs, upvotes, and checklist ticks to db.json."""
    write_db(payload)
    return {"status": "ok"}


@app.post("/api/reset")
def reset_db():
    """Resets db.json back to the default starting data."""
    write_db(DEFAULT_DB)
    return {"status": "reset", "data": DEFAULT_DB}


# Serve the HTML and JS files directly from the root directory
app.mount("/", StaticFiles(directory=".", html=True), name="static")