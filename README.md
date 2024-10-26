\documentclass{article}
\usepackage{hyperref}

\title{Python Script Executor API}
\author{}
\date{}

\begin{document}

\maketitle

\section*{Project Overview}
This project is a Flask-based API service designed to execute arbitrary Python scripts securely within a sandboxed environment using \texttt{nsjail}. The API allows users to upload a Python script, specifically a \texttt{main()} function, and returns the function's JSON output. The service includes validation to ensure that only valid Python code with a JSON-compatible \texttt{main()} function can be executed.

\section*{Features}
\begin{itemize}
    \item \textbf{Secure Execution}: Scripts are executed within an \texttt{nsjail} sandbox to limit system access and prevent malicious actions.
    \item \textbf{Error Handling}: Validates the uploaded script, checking for a \texttt{main()} function that returns JSON. Errors are raised if these conditions are not met.
    \item \textbf{Cloud Ready}: The API is containerized with Docker and deployable on Google Cloud Run.
\end{itemize}

\section*{Technical Details}
\begin{itemize}
    \item \textbf{API Endpoint}: Accepts POST requests with the script file in JSON format. Returns the JSON output of the \texttt{main()} function or an error message.
    \item \textbf{Dockerized}: Lightweight Docker image using \texttt{python:3.9-slim-buster} for efficient cloud deployment.
    \item \textbf{Google Cloud Run}: Second-generation runtime compatibility allows easy cloud deployment.
    \item \textbf{Libraries Available}: Basic libraries like \texttt{os}, \texttt{pandas}, and \texttt{numpy} are accessible for script execution.
\end{itemize}

\section*{Deployment}
\begin{itemize}
    \item \textbf{Local Testing}: The Docker image can be built and tested locally using \texttt{docker build} and \texttt{docker run}.
    \item \textbf{Cloud Deployment}: Deployable on Google Cloud Run with the second-generation environment. Google Cloud Run URL will be generated upon deployment.
\end{itemize}

\section*{Requirements}
\begin{itemize}
    \item \texttt{Python 3.9+}
    \item \texttt{Docker}
    \item \texttt{Google Cloud SDK} for deployment
\end{itemize}

\section*{Estimated Setup Time}
The estimated setup and deployment time for this project is approximately 1-2 hours.

\end{document}
