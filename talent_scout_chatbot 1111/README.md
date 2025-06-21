# 🚀 Hirely AI - Intelligent Hiring Assistant

**Hirely AI** is an advanced AI-powered recruitment platform that conducts comprehensive technical interviews and project assessments to help you find the perfect candidate. Built with Streamlit and powered by Google's Gemini AI, it provides a sophisticated, interactive interview experience with real-time analysis and detailed reporting.

## ✨ Features

### 🎯 **Smart Interview Process**
- **Multi-Phase Assessment**: Welcome → Information Gathering → Technical Q&A → Project Discussion → Comprehensive Report
- **Progress Tracking**: Visual progress indicator showing current phase and completion status
- **Dynamic Question Generation**: AI-powered questions based on candidate's tech stack

### 🤖 **AI-Powered Analysis**
- **Real-time Answer Analysis**: Instant feedback on technical responses
- **AI Detection**: Identifies AI-generated answers and marks them as incorrect
- **Sentiment Analysis**: Analyzes candidate's communication style and confidence
- **Correctness Assessment**: Evaluates technical answer accuracy

### 💼 **Comprehensive Assessment**
- **Technical Deep Dive**: 2-3 tailored questions per technology in candidate's stack
- **Project Discussion**: 5 structured questions covering goals, technologies, innovation, challenges, and lessons learned
- **Interactive Q&A**: Candidates can ask questions and receive clarifications
- **Fallback Mechanism**: Intelligent handling of unclear or unexpected responses

### 📊 **Detailed Reporting**
- **Comprehensive Reports**: Detailed analysis with hiring recommendations
- **Candidate Profiles**: Complete information including experience, tech stack, and desired positions
- **Performance Metrics**: Scorecards and progress tracking
- **Export Options**: Download reports in multiple formats

## 🛠️ Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **AI Engine**: Google Gemini 1.5 Flash
- **Language**: Python 3.8+
- **Dependencies**: See `requirements.txt`

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- Git (for cloning the repository)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Mytrayee17/hierly.git
   cd hierly/talent_scout_chatbot\ 1111
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Key**
   - Get your Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Update the API key in `app.py` (line 13):
   ```python
   genai.configure(api_key="YOUR_API_KEY_HERE")
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the application**
   - Open your browser and go to `http://localhost:8501`
   - The application will be available on your local network as well

## 📖 Usage Guide

### 1. **Welcome Screen**
- Review the interview process overview
- Click "Start Interview Process" to begin

### 2. **Information Gathering**
Fill in candidate details:
- **Full Name** (required)
- **Email Address** (required)
- **Phone Number** (required)
- **Years of Experience** (required)
- **Desired Position(s)** (comma-separated)
- **Current Location** (required)
- **Tech Stack** (comma-separated)

### 3. **Technical Assessment**
- Answer AI-generated questions based on your tech stack
- Each technology gets 2-3 tailored questions
- Real-time feedback on your answers
- Progress tracking shows completion percentage

### 4. **Project Discussion**
- Discuss your past projects in detail
- Cover goals, technologies, innovation, challenges, and lessons learned
- Interactive Q&A with the AI assistant

### 5. **Assessment Report**
- Comprehensive analysis of your performance
- Hiring recommendation (Strong Hire, Proceed with caution, Not a good fit)
- Detailed breakdown of technical and project responses
- Download options for the report

## 🔧 Key Features Explained

### **AI Detection**
The system automatically detects AI-generated responses and marks them as incorrect, ensuring authentic candidate responses.

### **Interactive Q&A**
Candidates can ask questions during the interview process:
- Type questions ending with "?" for clarification
- Use phrases like "I didn't understand" for question re-explanation
- Type "ok" or "continue" to proceed to the next question

### **Fallback Mechanism**
When the system doesn't understand a response, it provides helpful guidance without deviating from the interview purpose.

### **Progress Tracking**
The sidebar shows your progress through the interview phases:
- ✅ Completed phases
- 🔄 Current phase
- ⏳ Upcoming phases

## 📁 Project Structure

```
talent_scout_chatbot 1111/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── reports/           # Generated assessment reports
└── README.md         # This file
```

## 🔑 Environment Variables

For production deployment, consider using environment variables for the API key:

```python
import os
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
```

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Production Deployment
1. Set up environment variables for API keys
2. Deploy to Streamlit Cloud, Heroku, or your preferred platform
3. Configure CORS and security settings as needed

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/Mytrayee17/hierly/issues) page
2. Create a new issue with detailed information
3. Include error messages and steps to reproduce

## 🔮 Future Enhancements

- [ ] Voice input support
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Integration with HR systems
- [ ] Custom question templates
- [ ] Video interview capabilities
- [ ] Automated scheduling
- [ ] Candidate database management

## 📊 Performance Metrics

- **Response Time**: < 3 seconds for AI analysis
- **Accuracy**: High precision in AI detection and sentiment analysis
- **Scalability**: Supports multiple concurrent interviews
- **Reliability**: Robust error handling and fallback mechanisms

---

**Built with ❤️ using Streamlit and Google Gemini AI**

*Hirely AI - Making recruitment smarter, one interview at a time.* 