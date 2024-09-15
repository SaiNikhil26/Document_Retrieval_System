# Document Retrieval System - Flask API

This is a document retrieval system built using Flask, MongoDB, Redis, and Docker. The system allows users to search documents using a custom retrieval-augmented generation (RAG) model and rate-limiting with caching mechanisms. It also scrapes news articles from The Guardian in the background and stores them in MongoDB.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
- [API Endpoints](#api-endpoints)

---

## Project Overview

This project provides a RESTful API to:

- Search for relevant documents from a MongoDB collection using text-based queries.
- Rate-limit API requests using Redis.
- Cache search results for faster retrieval.
- Scrape news articles from The Guardian and store them in MongoDB for use in the search system.

The system is built using:

- **Flask** for the web server.
- **MongoDB** for document storage.
- **Redis** for rate-limiting and caching.
- **Docker** to containerize the application.

---

## Features

- Document retrieval with a custom RAG search.
- Rate limiting (5 requests per minute per user).
- Cached search results for faster retrieval.
- Background news scraper.
- Real-time status checks for the API.

---

## Installation

### Prerequisites

- Docker
- Redis
- MongoDB Atlas (or local MongoDB instance)

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/SaiNikhil26/21BAI1398_ML
   ```

2. **Create a Virtual Environment and install depepndencies**

   ```bash
   python -m venv venv
   .\venv\Scripts\Activate
   pip install -r requirements.txt
   ```

## Configuration

1. **Database configuration and Redis Server Configuration**

   - Configure the MongoDB Database with your MongoDB connection URL
   - Configure the Redis Server with your Redis connection URL

## Running the Project

1. **Run in Local Environment**

   ```bash
   python app.py
   ```

   - Make sure Redis-Server is running locally.

2. **Dockerize the application**

   ````bash
   docker build -t document-retrieval-app -f Dockerfile.app .
   docker run -p 5000:5000 document-retrieval-app
   ````

## API Endpoints

1. `\search` Endpoint
   - **Description**: Perform a search using the RAG model.
   - The payload should contain user_id, query(text), top_k(no. of top results) and threshold
   - **Output**: Contains the results generated along with the inference time
   - **Error Codes**:
     1. 400: If user_id or text is missing
     2. 429: If rate limit has exceeded.

2. `\health` Endpoint
   - **Description**: Check if the API is running
   - **Output**: JSON output alongw ith status


This `README.md` file includes installation steps, Docker setup, endpoint explanations, a section for caching methods, and rate-limiting strategies.
Thank you


