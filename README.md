# GitHub Authenticated Application

This application allows users to authenticate via GitHub, upload projects to GitHub, and build/run projects locally using Docker. Additionally, it features a frontend where users can upload and write code for their locally installed applications to practice testing. Moreover, users can interact with the OpenAI LLM (Large Language Model) ChatGPT directly from the application.

## Features

- **GitHub Authentication**: Users can log in using their GitHub accounts.
- **Project Upload to GitHub**: Users can upload their projects directly to GitHub from the application.
- **Local Project Building and Running with Docker**: Users can build and run their projects locally using Docker.
- **Frontend Code Editor**: The frontend provides a code editor where users can write and test their code.
- **OpenAI ChatGPT Integration**: Users can interact with the OpenAI LLM ChatGPT from within the application.

## Getting Started

### Prerequisites

- [Python](https://www.python.org/) installed on your machine.
- [Node.js](https://nodejs.org/) installed on your machine.
- [Docker](https://www.docker.com/) installed on your machine.

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your_username/your_project.git
   ```

2. Navigate to the project directory:

   ```bash
   cd your_project
   ```

3. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Install Node.js dependencies for the frontend:

   ```bash
   cd frontend
   npm install
   ```

### Usage

1. Set up GitHub OAuth:

   - Create a GitHub OAuth App.
   - Set the client ID, client secret, and redirect URI in the environment variables or `.env` file.

2. Run the backend server:

   ```bash
   uvicorn main:app --reload
   ```

3. Run the frontend:

   ```bash
   cd frontend
   npm run dev
   ```

4. Access the application at `http://localhost:3000` in your web browser.

## Contributing

Contributions are welcome! Please open an issue or pull request to suggest changes or report bugs.

## License

This project is licensed under the [MIT License](LICENSE).
