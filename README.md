# Python-Future-Self-Analyser

PROJECT REPORT
Future Self Analyzer
A Career Readiness Assessment Desktop Application

Technology Stack

Python  •  CustomTkinter  •  SQLite  •  Matplotlib  •  NumPy

Submitted: 22 April 2026
 
1. Project Overview
Future Self Analyzer is a desktop application built with Python that enables students and aspiring professionals to assess their career readiness across eight major technology domains. The application collects self-reported skill ratings, study habits, and consistency metrics, then uses a weighted scoring algorithm to generate a personalized career readiness score along with actionable improvement suggestions.

1.1 Objectives
•	Help students identify skill gaps relative to industry-standard benchmarks
•	Provide a quantified, trackable career readiness score (0–100)
•	Offer personalized recommendations to accelerate skill development
•	Persist assessment history in a local database for progress tracking
•	Visualize skill performance against target levels via interactive charts

1.2 Project Information
Application Name	Future Self Analyzer
Version	2.0 (Professional Edition)
Language	Python 3.8+
GUI Framework	CustomTkinter (modern dark-themed UI)
Database	SQLite (via Python sqlite3 module)
Platform	Windows / macOS / Linux
IDE Used	PyCharm

2. Key Features
2.1 Career Path Assessment
The application supports eight career domains, each with five domain-specific skills:

Career Path	Skills Assessed
Data Science	Python, Statistics, Machine Learning, Data Analysis, Visualization
Web Development	HTML/CSS, JavaScript, React, Backend, Database
AI/ML	Python, ML Algorithms, Deep Learning, Math, Projects
Cyber Security	Networking, Security Basics, Ethical Hacking, Linux, Cryptography
App Development	Java/Kotlin, UI Design, API Handling, Database, Debugging
Cloud Computing	AWS/Azure, Linux, Networking, Docker, Security
Game Development	Unity/Unreal, C++/C#, Game Design, Physics, Animation
UI/UX Design	Figma, User Research, Wireframing, Prototyping, Creativity

2.2 Scoring Algorithm
The scoring engine uses a weighted multi-factor formula:

Component	Formula	Max Contribution
Weighted Skill Score	Σ (skill × weight)	80 points
Study Hours Bonus	study × 0.1 × 10	10 points
Consistency Bonus	consistency × 0.1 × 10	10 points
Total Score	Weighted + Bonus	100 points

2.3 Result Levels
Level	Score Range	Description
ADVANCED	76 – 100	Strong profile, ready to apply for roles
GROWING	51 – 75	On track, needs targeted improvement
BEGINNER	0 – 50	Foundation-building phase

3. System Architecture
3.1 Module Breakdown
The application is structured into five logical modules:

Module	Responsibility
UI Layer	CustomTkinter-based dark-themed interface with scrollable layout, cards, and input groups
Data Layer	SQLite database stores student name, career path, score, and timestamp
Scoring Engine	Weighted formula computes career readiness score from skills, study hours, and consistency
Visualization	Matplotlib renders a dark-themed bar chart comparing user skills vs. target levels
Suggestion Engine	Rule-based logic generates personalized recommendations based on score gaps

3.2 Data Flow
•	User fills in Name, Career Path, Study Hours, Consistency, and 5 Skill Ratings
•	Scoring Engine applies domain-specific weights and computes final score (0–100)
•	Result is classified as BEGINNER / GROWING / ADVANCED
•	Record is upserted into the SQLite database with timestamp
•	Suggestion Engine generates personalized tips based on weak areas
•	Matplotlib chart is rendered showing performance vs. target

4. Technology Stack

Technology	Version	Purpose
Python	3.8+	Core programming language
CustomTkinter	Latest	Modern, themed GUI framework
SQLite3	Built-in	Local database for records persistence
Matplotlib	3.x	Skill assessment visualization charts
NumPy	1.x	Array operations for graph rendering
PyCharm	2023+	Development IDE

4.1 Installation
Install required third-party packages using pip in PyCharm Terminal:

pip install customtkinter matplotlib numpy

5. User Interface
5.1 Design Philosophy
The UI was redesigned from the default tkinter widgets to a professional dark-themed interface using CustomTkinter. The design takes inspiration from modern developer tools such as GitHub Dark and VS Code.

5.2 UI Components
Component	Description
Header Bar	Fixed top bar with app name and accent color branding
Identity Card	Name input and career path dropdown grouped in a card
Daily Habits Card	Two-column layout for Study Hours and Consistency inputs
Skill Ratings Card	Dynamic 2-column grid of 5 skill sliders with weight labels
Action Buttons	Primary Analyze button + secondary View Records button
Result Card	Large score display, status text, and color-coded level badge
Records Window	Popup table showing all saved assessments with formatted columns

6. Future Enhancements
•	Export assessment report as a PDF from within the application
•	Add a progress timeline chart showing score improvement over time
•	Integrate online learning resource links for each weak skill
•	Add multi-user support with login authentication
•	Deploy as a web app using Flask or Streamlit for broader access
•	Include a resume strength analyzer based on the career path chosen
•	Add gamification elements such as badges and streaks to boost motivation

7. Conclusion
Future Self Analyzer demonstrates how a practical, data-driven approach can guide students toward their career goals. By combining a weighted scoring model with clear visual feedback and personalized suggestions, the application bridges the gap between self-assessment and actionable learning plans.

The professional redesign using CustomTkinter elevates the project's presentation quality, making it suitable for portfolio showcasing, GitHub publication, and academic submission. The modular architecture also makes it straightforward to extend with new career paths, scoring models, or UI enhancements.
