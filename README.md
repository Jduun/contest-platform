# Contest Platform

## Table of Contents
- [About](#about)
- [Features](#features)
- [Techonologies](#technologies)
- [Installation and Setup](#installation-and-setup)
- [License](#license)

## About
It is a web platform designed for developers and enthusiasts to engage in coding competitions.

## Features
- [x] User registration, authentication and authorization
- [x] List of problems on the home page that you can solve
- [x] Immediate feedback on submitted solutions
- [x] Admin panel for admins and organizers
- [x] Intuitive and responsive user interface with light and dark mode
- [x] Built-in Code Editor
- [x] Contests
- [x] Leaderboard
- [ ] Multi-Language Support
- [ ] User profile
- [ ] Submission History
- [ ] Telegram Bot for notifications
- [ ] Problem Statements in Markdown format
- [ ] Request caching

## Technologies
1. Backend: Python, FastAPI, PostgreSQL, SQLAlchemy, Alebmic, Docker, Nginx
2. Frontend: React, TypeScript, Vite, Shadcn, TailwindCSS, Jotai

## Installation and Setup
1. Clone the repository:
    ```
    git clone https://github.com/Jduun/contest-platform.git
    ```

2. First of all you need to install and setup [Judge0](https://github.com/judge0/judge0). Judge0 is an open-source online code execution system.

3. Navigate to the project folder:
    ```
    cd contest-platform
    ```

4. Create file with environment variables:
    ```
    cp .env.example .env
    ```
    Change the values of the environment variables to your own.

5. Build project:
    ```
    ./build.sh
    ```

6. Run project:
    ```
    ./run.sh
    ```

## License
This project is licensed under the terms of the [MIT License](./LICENSE).
