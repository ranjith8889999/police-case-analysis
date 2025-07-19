# Police Case Management System

An AI-powered application for law enforcement agencies to analyze and manage case information, providing insights into case sections, bail procedures, and human behavior patterns through document analysis and AI-assisted responses.

## Features

- **Authentication System**: Secure login and registration with restricted access
- **Document Management**: Upload, categorize, and analyze various document types
- **AI-powered Analysis**: Intelligent insights based on document content
- **Case Section Analysis**: Legal statute and precedent analysis
- **Bail Analysis**: Bail procedure and decision analysis
- **Human Analysis**: Behavioral pattern recognition and analysis
- **RAG Integration**: Retrieval-Augmented Generation for context-aware AI responses

## Technology Stack

- **Backend**: Python, Flask, SQLAlchemy, LangChain
- **Frontend**: HTML, CSS, jQuery, Bootstrap 5, Font Awesome 6
- **Database**: SQL Server (LocalDB), ChromaDB (Vector Database)
- **AI**: Google Gemini 1.5 Flash, Gemini text-embedding-004

## Installation

1. Clone the repository:
```
git clone <repository-url>
cd Police-Case-Analysis
```

2. Install the required packages:
```
pip install -r requirements.txt
```

3. Set up the database:
   - Ensure LocalDB is installed on your system
   - The application will create the database and tables on first run

4. Run the application:
```
python run.py
```

5. Access the application at `http://localhost:5000`

## Project Structure

```
Police Case Analysis/
├── app/
│   ├── controllers/       # Route handlers and controllers
│   ├── models/           # Database models and schemas
│   ├── services/         # Business logic and services
│   ├── static/           # Static assets (CSS, JS, images)
│   ├── templates/        # HTML templates
│   ├── utils/            # Utility functions and helpers
│   └── __init__.py       # Application factory
├── vector_db/           # Vector database storage
├── requirements.txt     # Project dependencies
├── RELEASE_NOTES.md     # Release information
├── README.md            # Project documentation
└── run.py              # Application entry point
```

## Usage

1. **Authentication**:
   - Register with an authorized email address
   - Login with your credentials

2. **Dashboard**:
   - Access different analysis modules from the dashboard
   - Navigate using the top menu bar

3. **Document Management**:
   - Upload documents through the Admin panel
   - Categorize documents by analysis type

4. **Analysis**:
   - Use specific analysis pages to query the system
   - Chat with the AI to get insights from uploaded documents

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- This project uses Google's Gemini AI for natural language processing
- Built with Flask web framework
- Uses LangChain for connecting LLMs with external data sources
- Vector embeddings powered by Google Gemini text-embedding-004 (768 dimensions)
