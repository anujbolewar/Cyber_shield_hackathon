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

## Screenshots

### Login Screen
*Secure authentication system requiring authorized law enforcement personnel credentials. The interface features a professional police-themed design with proper security protocols.*

### Main Dashboard
*Comprehensive overview of all monitoring activities including system metrics, active alerts, intelligence reports, and system health indicators. Quick action buttons allow rapid access to key functions.*

### Real-Time Intelligence Feed
*Live monitoring interface showing social media posts with sentiment analysis, engagement metrics, and threat classification. The system tracks multiple platforms simultaneously and provides detailed analytics for each post.*

### Alert Management System
*Advanced alert management showing active threats, alert trends over time, and critical notifications. The system provides real-time monitoring with customizable alert thresholds and response coordination tools.*

### API Management Center
*Comprehensive API configuration interface for managing external service connections. Features secure token management for social media platforms (Twitter/X, Facebook, Telegram, Reddit, YouTube), with encryption enabled and session-only storage. Includes demo mode for testing and quick setup guides for each platform.*

### NLP Analysis Engine
*Advanced Natural Language Processing engine with multi-language support, threat detection, and risk assessment capabilities. Provides AI-powered content analysis for threat detection and intelligence gathering with comprehensive analysis controls and history tracking.*

### Data Visualization & Analytics
*Comprehensive threat assessment dashboard featuring real-time threat level gauges, risk score distribution analysis, and advanced monitoring metrics for law enforcement operations.*

### Geographic Threat Analysis
*Interactive map showing geographic distribution of threats across India, with platform-specific analytics and keyword frequency analysis for better situational awareness.*

### Network Analysis
*Advanced network analysis showing account relationships and connection patterns. This helps identify bot networks, suspicious account clusters, and coordinated threat activities.*

### Trend Analysis
*Detailed trend analysis showing threat activity over time, content volume patterns, and bot activity detection to help predict and prevent potential security incidents.*

> **Note:** Screenshots will be added soon. The application is fully functional and can be tested by running `python run.py`.

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
