# Week 3: System Integration & Application

## Resume Helper Chatbot

This project is a containerized full-stack Resume Helper Chatbot. It allows users to upload a resume PDF and ask career-related questions, such as identifying skill gaps or skills to improve.

The application integrates the skill-gap analysis logic developed in Week 2. The frontend collects the user’s resume and question, sends the data to the backend, and displays the chatbot response.

The project consists of two services:

* **Frontend** — provides the web interface for uploading a PDF resume and sending a question.
* **Backend** — provides a FastAPI API that processes the request and returns a skill-gap response.

Both services are containerized using Docker and run together using Docker Compose.

---

## Project Architecture

```text
Browser
   |
   | http://localhost:8000
   v
Frontend Container
   |
   | HTTP request through Docker network
   v
Backend Container
   |
   v
Week 2 Skill-Gap Analysis Logic and SQLite Database
```

Docker Compose automatically creates a shared Docker network. The frontend communicates with the backend through the backend service name.

---

## Prerequisites

Before running this project, install:

* Docker Desktop
* Docker Compose

Optional for manual local setup:

* Python 3.12 or later
* uv

---

## Environment Variables

The frontend uses an environment variable to identify the backend URL.

Create a `.env` file inside the `week_3` folder:

```env
BACKEND_URL=http://backend:8001
```

A sample environment file is provided as `.env.sample`.

The `.env` file should not contain passwords, API keys, or other sensitive information.

---

## Setup Instructions

1. Open a terminal and go to the Week 3 folder:

```bash
cd ~/Desktop/kyouth-data-ai/week_3
```

2. Build and start both services:

```bash
docker compose up --build
```

3. Open the frontend in a browser:

```text
http://localhost:8000
```

4. To stop the application, press:

```text
Ctrl + C
```

5. To stop and remove the containers:

```bash
docker compose down
```

---

## Usage

1. Open the application at `http://localhost:8000`.
2. Click **Choose File** and upload a resume in PDF format.
3. Enter a career-related question, for example:

```text
What skills should I improve for a junior data or software role?
```

4. Click **Send**.
5. The frontend sends the resume text and question to the backend.
6. The backend analyses the resume skills against skills found in job listings.
7. The chatbot response is displayed on the page.

Example output:

```text
Based on your resume, some skill gaps are: Docker, AWS, API integration, CI/CD and Excel.
```

---

## API / Function Reference

### `GET /`

This is a health-check endpoint for the backend.

Example response:

```json
{
  "message": "Resume Helper Chatbot backend is running"
}
```

### `POST /chat`

This endpoint receives the user’s question and resume text, then returns a skill-gap response.

Expected JSON request body:

```json
{
  "message": "What skills should I improve?",
  "resume_text": "Text extracted from the uploaded resume PDF"
}
```

Example JSON response:

```json
{
  "reply": "Based on your resume, some skill gaps are: Docker, AWS and CI/CD."
}
```

### Frontend Functions

The frontend is responsible for:

- Allowing the user to select a PDF resume file in the interface.
- Sending the user’s message and sample resume text to the backend for the current prototype.
- Displaying the skill-gap response returned by the backend.
* Displaying the user’s message in the chat area.
* Displaying the backend response in the chat area.
* Showing an error message if the backend connection fails.

---

## Data Flow

1. The user selects a PDF resume and enters a question in the browser.
2. The frontend sends a JSON request containing the user’s message and prototype resume text to the backend `/chat` endpoint.
3. The backend processes the request using the Week 2 skill-gap analysis logic.
4. The backend receives the resume text and user question.
5. The backend uses the Week 2 skill-gap logic to compare resume skills with skills from the job listings database.
6. The backend returns a JSON response containing the skill-gap result.
7. The frontend displays the response as a chatbot message.

---

## Testing

### Frontend Testing

The frontend was tested by:

* Opening `http://localhost:8000`.
* Uploading a PDF resume.
* Entering a career-related question.
* Clicking **Send**.
* Confirming that the chatbot response appears on the page.

### Backend Testing

The backend was tested using FastAPI Swagger UI:

```text
http://localhost:8001/docs
```

The `/chat` endpoint was tested by sending a JSON request containing a message and resume text.

### Docker Testing

The Docker services were tested using:

```bash
docker compose ps
```

Expected result: both `frontend` and `backend` services show a status of `Up`.

The application was also tested through the browser at:

```text
http://localhost:8000
```

This confirms that the frontend and backend communicate correctly within the Docker environment.

---

## Assumptions and Limitations

### Assumptions

* The user uploads a valid PDF resume.
* The PDF contains extractable text.
* The Week 2 SQLite job database is available to the backend.
* The user enters a non-empty career-related question.

### Limitations

* The chatbot currently focuses on skill-gap analysis and does not provide a full AI-generated career consultation.
* The response is based on skills found in the resume and job-listing data, so it may not perfectly represent the entire job market.
* Some PDF files may not extract correctly if they are scanned images or protected files.
* Chat history is not saved after the page is refreshed.
* There is no user authentication.
* The system is designed for local use and has not yet been deployed to a cloud platform.
* In the current prototype, the PDF upload interface is available, but PDF text extraction is planned as a future enhancement. The backend currently uses sample resume text for skill-gap testing.

---

## Architecture Reflection

I chose a frontend and backend separation because each service has a different responsibility. The frontend focuses on user interaction, PDF upload, and displaying the chat conversation. The backend focuses on processing requests and running the skill-gap analysis logic.

Docker was used to containerize both services so that the project can run consistently on different machines. Docker Compose makes it easier to start the complete application with one command and automatically creates a shared network for communication between the frontend and backend.

The main trade-off was prioritizing a simple and working application over advanced features. The interface is intentionally simple, and the chatbot response is based on the Week 2 skill-gap logic rather than a large language model.

With more time, I would improve the project by adding user authentication, saved chat history, better PDF validation, more detailed skill recommendations, a stronger frontend framework, and cloud deployment.
