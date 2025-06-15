# TalentScout AI Chatbot - User Manual

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [System Requirements](#system-requirements)
4. [Installation Guide](#installation-guide)
5. [User Guide](#user-guide)
6. [Features Overview](#features-overview)
7. [API Configuration](#api-configuration)
8. [Troubleshooting](#troubleshooting)
9. [Support](#support)

## Introduction

TalentScout is an AI-powered hiring assistant designed to streamline the candidate screening process. The application uses advanced AI technology to conduct technical interviews, analyze responses, and generate comprehensive assessment reports.

### Key Features
- **AI-Generated Response Detection**: Identifies whether candidate responses are AI-generated or human-written
- **Sentiment Analysis**: Analyzes the emotional tone of candidate responses
- **Technical Interview Automation**: Generates relevant technical questions based on candidate's tech stack
- **Project Experience Assessment**: Conducts structured interviews about candidate's project experience
- **Comprehensive Reporting**: Generates detailed assessment reports in multiple formats
- **User-Friendly Interface**: Modern, responsive web interface built with Streamlit

## Getting Started

### Quick Start
1. Access the application through your web browser
2. Click "Start Application" on the welcome screen
3. Fill in candidate information
4. Complete the technical interview
5. Answer project experience questions
6. Review the generated assessment report
7. Provide feedback on the interview process

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10, macOS 10.14, or Linux Ubuntu 18.04+
- **Python**: Version 3.11 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **Internet**: Stable internet connection required for AI analysis

### Browser Compatibility
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Installation Guide

### Prerequisites
1. Python 3.11 installed
2. Google API key for Generative AI
3. Virtual environment (recommended)

### Step-by-Step Installation

1. **Clone or Download the Project**
   ```bash
   # If using git
   git clone <repository-url>
   cd talent_scout_chatbot
   ```

2. **Create Virtual Environment**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install streamlit google-generativeai pandas
   ```

4. **Configure API Key**
   - Open `ai_analysis.py`
   - Replace the API key with your Google Generative AI key
   - Alternatively, set the `GOOGLE_API_KEY` environment variable

5. **Run the Application**
   ```bash
   streamlit run app.py --server.port 8501 --server.address 0.0.0.0
   ```

6. **Access the Application**
   - Open your browser and navigate to `http://localhost:8501`

## User Guide

### 1. Welcome Screen
- The application starts with a welcome screen introducing TalentScout
- Click "Start Application" to begin the interview process
- The progress tracker on the left shows your current stage

### 2. Information Gathering
Fill in the following required information:
- **Full Name**: Candidate's complete name
- **Email Address**: Valid email address
- **Phone Number**: Contact number (optional)
- **Current Location**: City and country (optional)
- **Years of Experience**: Select from dropdown options
- **Desired Position**: Target job role
- **Tech Stack**: List of technologies and skills

**Tip**: Mention your strongest technologies to get more relevant technical questions.

### 3. Technical Interview
- The AI generates technical questions based on your tech stack
- Type your answers in the provided text area
- Click "Submit Answer" to proceed to the next question
- Use "Skip to Projects" to move directly to project interview
- Your responses are analyzed for AI detection and sentiment

### 4. Project Interview
Answer questions about your project experience:
1. Project description and problem it solves
2. Technologies used and rationale
3. Novel or innovative approaches
4. Challenges faced and solutions
5. Quality assurance methods

- Use "Skip Question" if you prefer not to answer
- Progress indicator shows completion status

### 5. Assessment Report
Review your comprehensive assessment including:
- Technical interview summary
- Project interview analysis
- AI-generated overall assessment
- Performance metrics
- Detailed question-by-question breakdown

### 6. Feedback Collection
Provide feedback about the interview process:
- Rate your overall experience
- Share comments about the process
- Suggest improvements
- Submit feedback to help improve the system

## Features Overview

### AI Analysis Capabilities

#### AI-Generated Text Detection
- Uses advanced language models to identify AI-generated responses
- Helps ensure authentic candidate evaluation
- Results displayed as "AI Generated" or "Human Written"

#### Sentiment Analysis
- Analyzes emotional tone of responses
- Categories: Positive, Negative, Neutral
- Helps assess candidate engagement and attitude

#### Answer Quality Assessment
- Evaluates technical depth and understanding
- Assesses problem-solving approach
- Measures communication clarity

### Reporting Features

#### Multiple Report Formats
- **JSON**: Machine-readable format for integration
- **Markdown**: Human-readable format
- **PDF**: Professional presentation format
- **CSV**: Data analysis and spreadsheet import

#### Report Contents
- Candidate information summary
- Technical interview results
- Project interview analysis
- AI-generated assessment
- Overall performance metrics
- Feedback data

### Security and Privacy

#### Data Protection
- Candidate data is processed securely
- No personal information is stored permanently
- API communications are encrypted
- Session data is cleared after completion

#### API Security
- Google API key should be kept confidential
- Use environment variables for production deployment
- Regular key rotation recommended

## API Configuration

### Google Generative AI Setup

1. **Get API Key**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy the key for configuration

2. **Configure in Application**
   ```python
   # Method 1: Direct configuration (development only)
   api_key = "your-api-key-here"
   
   # Method 2: Environment variable (recommended)
   import os
   api_key = os.getenv("GOOGLE_API_KEY")
   ```

3. **Model Selection**
   - Default model: `models/gemini-1.5-flash-latest`
   - Alternative models available based on requirements
   - Check model availability and quotas

### Rate Limits and Quotas
- Free tier has daily and per-minute limits
- Monitor usage to avoid quota exhaustion
- Consider upgrading for production use

## Troubleshooting

### Common Issues

#### Application Won't Start
- **Check Python version**: Ensure Python 3.11+ is installed
- **Verify dependencies**: Run `pip install -r requirements.txt`
- **Port conflicts**: Try a different port with `--server.port 8502`

#### API Errors
- **Invalid API key**: Verify the Google API key is correct
- **Quota exceeded**: Check your API usage limits
- **Network issues**: Ensure stable internet connection

#### UI Issues
- **Blank screen**: Clear browser cache and refresh
- **Slow loading**: Check internet connection and API response times
- **Button not working**: Try refreshing the page

#### Analysis Errors
- **"Error in analysis"**: Usually indicates API issues
- **Inconsistent results**: May be due to model variations
- **Missing results**: Check if all required fields are filled

### Performance Optimization

#### Improve Response Times
- Use faster model variants when available
- Implement response caching for repeated queries
- Optimize network connectivity

#### Memory Management
- Restart application periodically for long sessions
- Clear browser cache if experiencing slowdowns
- Monitor system resources

## Support

### Getting Help
- **Documentation**: Refer to this user manual
- **Error Messages**: Check console output for detailed error information
- **Community**: Search for similar issues online

### Reporting Issues
When reporting issues, please include:
- Operating system and version
- Python version
- Browser type and version
- Error messages (if any)
- Steps to reproduce the issue

### Feature Requests
We welcome suggestions for new features:
- Enhanced AI analysis capabilities
- Additional report formats
- Integration with HR systems
- Mobile application support

---

**Version**: 1.0  
**Last Updated**: June 2025  
**Developed by**: TalentScout Team

