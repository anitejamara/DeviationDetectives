# DeviationDetectives

Deviation Detectives is a project that identifies deviations in business contract documents from a given template by finding additions, modifications, or deletions. The project includes a backend built with FastAPI and a frontend built with React.

Feel free to check our project presentation below!
https://drive.google.com/file/d/1OeZYC9GYdLUt4LNX-ejmnJ857lto0DYV/view?usp=sharing

## Project Structure

- **L1_IndividualComponents**: Contains individual Python files used in the project.
- **L2_StreamlitApplication**: Contains the Streamlit application files.
- **L3_FastAPI**: Contains the FastAPI backend files.
- **L4_DOCKER**: Contains Docker configurations for both the backend and frontend.
- **L5_Frontend**: Contains the frontend code built with React.

## Getting Started

### Prerequisites

- [Python 3.8+](https://www.python.org/downloads/)
- [Node.js 14+](https://nodejs.org/en/download/)
- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Running the Backend

1. Navigate to the backend directory:

    ```bash
    cd L4_DOCKER/backend
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Start the FastAPI server:

    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```

### Running the Frontend

1. Navigate to the frontend directory:

    ```bash
    cd L5_Frontend
    ```

2. Install the required Node.js packages:

    ```bash
    npm install
    ```

3. Start the React development server:

    ```bash
    npm start
    ```

### Running with Docker Compose

1. Navigate to the Docker directory:

    ```bash
    cd L4_DOCKER
    ```

2. Build and start the containers:

    ```bash
    docker-compose up --build
    ```

3. The backend will be available at [http://localhost:8000](http://localhost:8000) and the frontend at [http://localhost:3000](http://localhost:3000).

## Usage

Once the services are running, you can interact with the frontend to upload and analyze contract documents. The backend will handle the analysis and return the results to the frontend for display.
