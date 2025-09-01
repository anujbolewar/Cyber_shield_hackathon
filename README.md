# Police AI Monitor

A social media monitoring and intelligence platform for law enforcement agencies. This application helps monitor social media platforms for potential threats and provides analytical tools for law enforcement operations.

## Getting Started

To run the application locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

The application will be available at `http://localhost:8501`

Alternatively, you can run it directly with:
```bash
streamlit run src/main.py
```

## What It Does

This tool helps law enforcement agencies by:

- **Social Media Monitoring**: Tracks posts across multiple platforms
- **Threat Detection**: Uses AI to identify potential security threats
- **Real-time Alerts**: Notifies users when suspicious activity is detected
- **Data Analysis**: Provides charts and insights from collected data
- **Evidence Management**: Helps organize and export evidence for legal purposes

## Main Features

- **Dashboard**: Overview of all monitoring activities
- **Live Feed**: Real-time social media posts
- **Alert System**: Automated threat notifications
- **Analytics**: Charts and data visualization
- **NLP Analysis**: Text analysis for sentiment and threat detection
- **Database Management**: Store and manage collected data
- **Web Scraping**: Collect data from various social platforms

## Project Structure

```
police-ai-monitor/
├── src/                    # Source code
│   ├── main.py            # Main application
│   ├── pages/             # Different app pages
│   ├── services/          # External API integrations
│   └── utils/             # Helper functions
├── config/                # Configuration files
├── data/                  # Database files
├── docs/                  # Documentation
└── requirements.txt       # Python dependencies
```

## Technology Used

- **Python**: Main programming language
- **Streamlit**: Web application framework
- **SQLite**: Database for storing data
- **NLTK/spaCy**: Natural language processing
- **Plotly**: Data visualization
- **Pandas**: Data manipulation

## Demo Mode

The application includes demo data and simulated social media posts for testing purposes. You can use the demo mode to explore features without connecting to real social media APIs.

## Deployment

You can deploy this application to:

- **Streamlit Cloud**: Upload to GitHub and deploy via share.streamlit.io
- **Heroku**: Use the included Procfile
- **Docker**: Use the included Dockerfile

## Security Note

This application is designed for legitimate law enforcement use only. It includes security features like authentication and audit logging. Always ensure compliance with local laws and regulations when using social media monitoring tools.

## License

MIT License
