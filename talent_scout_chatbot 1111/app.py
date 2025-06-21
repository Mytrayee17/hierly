import streamlit as st
import google.generativeai as genai
from datetime import datetime
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="Hirely AI",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- AI Configuration ---
# It's recommended to use st.secrets for API keys in a deployed app
api_key = os.getenv("GEMINI_API_KEY", "AIzaSyDxYIfsEDSDvqVOLl5Y00bOEPQ9zE73vjE")
genai.configure(api_key=api_key) # type: ignore

# --- Hirely AI Logic ---
@st.cache_resource
def get_ai_model():
    return HirelyAI()

class HirelyAI:
    def __init__(self):
        self.model = genai.GenerativeModel("models/gemini-1.5-flash-latest") # type: ignore

    def analyze(self, prompt):
        return self.model.generate_content(prompt).text

    def generate_technical_questions(self, tech_stack):
        prompt = f"""Generate 2-3 technical questions for each technology in this stack: {', '.join(tech_stack)}.
        Make questions practical and relevant to real-world development.
        Format as a list of questions."""
        return self.analyze(prompt)

    def generate_project_questions(self):
        prompt = """Generate 5 project discussion questions covering:
        1. Project goals and objectives
        2. Technologies and tools used
        3. Innovation and unique features
        4. Challenges faced and solutions
        5. Lessons learned and improvements
        
        Format as a list of questions."""
        return self.analyze(prompt)

    def check_correctness(self, question, answer):
        prompt = f"""Is this answer correct for the question?
        Question: {question}
        Answer: {answer}
        Respond with only: 'Correct' or 'Incorrect'"""
        return self.analyze(prompt)

    def detect_ai_generated_text(self, text):
        prompt = f"""Analyze if this text appears to be AI-generated. Consider:
1. Repetitive patterns or overly perfect structure
2. Generic or textbook-like language
3. Lack of personal experience or specific details
4. Overly formal or robotic tone
5. Perfect grammar and spelling that seems too polished

Text: {text}

Provide your analysis in this format:
AI-Generated: Yes/No
Confidence: High/Medium/Low
Reason: Brief explanation of why you think it's AI-generated or not
"""
        return self.analyze(prompt)

    def analyze_sentiment(self, text):
        prompt = f"Analyze the sentiment of this text. Respond with only: 'Positive', 'Negative', or 'Neutral'\n\nText: {text}"
        return self.analyze(prompt)

    def generate_final_report(self, candidate_data, history):
        prompt = f"""
        Generate a comprehensive hiring report in Markdown for:
        - **Name:** {candidate_data.get('fullName')}
        - **Email:** {candidate_data.get('email')}
        - **Phone:** {candidate_data.get('phone')}
        - **Location:** {candidate_data.get('location')}
        - **Experience:** {candidate_data.get('experience')}
        - **Desired Position(s):** {', '.join(candidate_data.get('positions', []))}
        - **Tech Stack:** {', '.join(candidate_data.get('techStack', []))}
        **Interview History:**
        {history}
        **Summary & Recommendation:**
        Provide a final summary and a hiring recommendation (e.g., 'Strong Hire', 'Proceed with caution', 'Not a good fit').
        """
        return self.analyze(prompt)

    def answer_user_question(self, question):
        prompt = f"Concisely answer the user's question in the context of a job interview.\n\nUser: {question}\nAI:"
        return self.analyze(prompt)

    def is_user_input_a_question(self, text):
        # Simple heuristic, can be replaced by a more complex check if needed
        return text.strip().endswith('?')

    def is_clarification_request(self, text):
        clarification_phrases = [
            "i didn't understand", "explain", "repeat", "clarify", 
            "what do you mean", "can you explain", "i don't get it",
            "not clear", "confused", "help me understand"
        ]
        text_lower = text.lower()
        return any(phrase in text_lower for phrase in clarification_phrases)

    def re_explain_question(self, question):
        prompt = f"""Re-explain this technical question in simple, clear terms that a candidate can easily understand:

Question: {question}

Provide a friendly, helpful explanation that breaks down the question."""
        return self.analyze(prompt)

    def fallback_response(self, context):
        return (
            "I'm sorry, I didn't quite understand your response. "
            "Could you please clarify or answer the question as best you can? "
            f"Let's stay focused on your {context} experience."
        )

hirely_ai = get_ai_model()

# --- Session State Initialization ---
if "phase" not in st.session_state:
    st.session_state.phase = "welcome"

if "candidate_data" not in st.session_state:
    st.session_state.candidate_data = {}

if "technical_questions" not in st.session_state:
    st.session_state.technical_questions = []

if "project_questions" not in st.session_state:
    st.session_state.project_questions = []

if "technical_answers" not in st.session_state:
    st.session_state.technical_answers = {}

if "project_answers" not in st.session_state:
    st.session_state.project_answers = {}

if "current_tech_q" not in st.session_state:
    st.session_state.current_tech_q = 0

if "current_proj_q" not in st.session_state:
    st.session_state.current_proj_q = 0

if "bot_message" not in st.session_state:
    st.session_state.bot_message = None

# --- UI Rendering Functions ---
def show_progress_tracker():
    st.sidebar.title("Progress Tracker")
    
    phases = {
        "welcome": "Welcome",
        "info_gathering": "Info Gathering",
        "technical_qa": "Technical Interview",
        "project_discussion": "Project Interview",
        "report": "Assessment Report"
    }
    
    phase_order = list(phases.keys())
    current_index = phase_order.index(st.session_state.phase)
    
    for i, (phase_key, phase_name) in enumerate(phases.items()):
        if i < current_index:
            st.sidebar.success(f"✅ {phase_name}")
        elif i == current_index:
            st.sidebar.info(f"🔄 {phase_name}")
        else:
            st.sidebar.text(f"⏳ {phase_name}")

def show_welcome_screen():
    st.title("🚀 Welcome to Hirely AI")
    st.markdown("### Your Intelligent Hiring Assistant")
    
    st.markdown("""
    **Hirely AI** is your advanced recruitment companion that conducts comprehensive technical interviews 
    and project assessments to help you find the perfect candidate.
    
    ### Our Process:
    1. **📝 Information Gathering** - Collect essential candidate details
    2. **🔧 Technical Assessment** - Deep dive into technical skills
    3. **💼 Project Discussion** - Explore real-world project experience
    4. **📊 Comprehensive Report** - Get detailed analysis and recommendations
    
    ### Features:
    - 🤖 AI-powered question generation based on tech stack
    - 📈 Real-time sentiment and AI detection analysis
    - 🎯 Personalized interview experience
    - 📋 Detailed assessment reports
    """)
    
    if st.button("Start Interview Process", type="primary", use_container_width=True):
        st.session_state.phase = "info_gathering"
        st.rerun()

def show_info_gathering():
    st.title("📝 Candidate Information")
    
    with st.form("candidate_info"):
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("Full Name *")
            email = st.text_input("Email Address *")
            phone = st.text_input("Phone Number *")
            experience = st.number_input("Years of Experience *", min_value=0, max_value=50, value=2)
        
        with col2:
            positions_list = st.text_input("Desired Position(s) (comma-separated) *", "Software Engineer, Data Scientist")
            location = st.text_input("Current Location *")
            tech_stack_list = st.text_input("Tech Stack (comma-separated) *", "Python, React, SQL, Docker")

        submitted = st.form_submit_button("Start Interview", type="primary")

        if submitted:
            tech_stack = [tech.strip() for tech in tech_stack_list.split(',')] if tech_stack_list else []
            positions = [pos.strip() for pos in positions_list.split(',')] if positions_list else []
            
            st.session_state.candidate_data = {
                'fullName': full_name,
                'email': email,
                'phone': phone,
                'experience': experience,
                'positions': positions,
                'location': location,
                'techStack': tech_stack
            }
            
            # Generate questions
            with st.spinner("Generating technical questions..."):
                tech_questions_text = hirely_ai.generate_technical_questions(tech_stack)
                st.session_state.technical_questions = [q.strip() for q in tech_questions_text.split('\n') if q.strip()]
            
            with st.spinner("Generating project questions..."):
                project_questions_text = hirely_ai.generate_project_questions()
                st.session_state.project_questions = [q.strip() for q in project_questions_text.split('\n') if q.strip()]
            
            st.session_state.phase = "technical_qa"
            st.rerun()

def show_technical_qa():
    st.title("🔧 Tech Stack Deep Dive")
    
    # Show bot message if exists
    if st.session_state.bot_message:
        st.info(f"**Hirely:** {st.session_state.bot_message}")
        if st.button("Continue", key="continue_bot"):
            st.session_state.bot_message = None
            st.rerun()
        return
    
    # Progress
    total_questions = len(st.session_state.technical_questions)
    if total_questions > 0:
        progress = (st.session_state.current_tech_q / total_questions) * 100
        st.progress(progress / 100)
        st.caption(f"Question {st.session_state.current_tech_q + 1} of {total_questions} ({progress:.1f}%)")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Technical Questions")

        # Show analysis of the previous question
        if st.session_state.current_tech_q > 0:
            last_answer_data = st.session_state.technical_answers.get(st.session_state.current_tech_q - 1)
            if last_answer_data:
                st.markdown("---")
                st.subheader("Feedback on Your Last Answer")
                analysis = last_answer_data['analysis']
                correctness = analysis.get('correctness', 'N/A')
                sentiment = analysis.get('sentiment', 'N/A')
                ai_detected = analysis.get('ai_detected', 'N/A')
                ai_confidence = analysis.get('ai_confidence', 'N/A')
                ai_reason = analysis.get('ai_reason', 'N/A')

                if correctness.lower() == 'correct':
                    st.success(f"**Analysis:** That seems correct!")
                elif ai_detected.lower() == 'yes':
                    st.error(f"**Analysis:** This answer appears to be AI-generated and has been marked as incorrect.")
                    st.warning(f"**AI Detection Details:**")
                    st.write(f"• **Confidence:** {ai_confidence}")
                    st.write(f"• **Reason:** {ai_reason}")
                else:
                    st.warning(f"**Analysis:** That might not be quite right. Keep trying!")
                
                st.info(f"**Sentiment:** Your response was {sentiment.lower()}.")

        # Current question
        if st.session_state.current_tech_q < len(st.session_state.technical_questions):
            current_q = st.session_state.technical_questions[st.session_state.current_tech_q]
            st.markdown(f"**Question {st.session_state.current_tech_q + 1}:** {current_q}")
            
            col_input, col_btn1, col_btn2 = st.columns([3, 1, 1])
            
            with col_input:
                answer = st.text_area("Your Answer", key=f"tech_answer_{st.session_state.current_tech_q}", 
                                    placeholder="Type your answer here...", height=100)
            
            with col_btn1:
                if st.button("🎤", key=f"voice_{st.session_state.current_tech_q}", help="Voice Input (Coming Soon)"):
                    st.info("Voice input feature coming soon!")
            
            with col_btn2:
                if st.button("Send", key=f"send_{st.session_state.current_tech_q}", type="primary"):
                    if answer.strip():
                        if hirely_ai.is_user_input_a_question(answer):
                            with st.spinner("Thinking..."):
                                bot_reply = hirely_ai.answer_user_question(answer)
                                # Fallback if bot reply is empty or off-topic
                                if not bot_reply or any(x in bot_reply.lower() for x in ["not sure", "don't know", "uncertain", "no idea"]):
                                    st.session_state.bot_message = hirely_ai.fallback_response("technical")
                                else:
                                    st.session_state.bot_message = bot_reply
                            st.rerun()
                        elif hirely_ai.is_clarification_request(answer):
                            with st.spinner("Re-explaining..."):
                                re_explanation = hirely_ai.re_explain_question(current_q)
                                st.session_state.bot_message = f"Let me clarify: {re_explanation}"
                            st.rerun()
                        elif answer.lower() in ['ok', 'continue', 'next', 'yes', 'got it']:
                            st.session_state.current_tech_q += 1
                            st.rerun()
                        else:
                            # Analyze answer
                            with st.spinner("Analyzing your answer..."):
                                ai_detected_result = hirely_ai.detect_ai_generated_text(answer)
                                correctness_result = hirely_ai.check_correctness(current_q, answer)

                                # Parse AI detection result
                                ai_generated = "No"
                                confidence = "Low"
                                reason = "Analysis not available"
                                
                                if "AI-Generated:" in ai_detected_result:
                                    lines = ai_detected_result.split('\n')
                                    for line in lines:
                                        if line.startswith("AI-Generated:"):
                                            ai_generated = line.split(":")[1].strip()
                                        elif line.startswith("Confidence:"):
                                            confidence = line.split(":")[1].strip()
                                        elif line.startswith("Reason:"):
                                            reason = line.split(":")[1].strip()

                                # Set correctness based on AI detection
                                if ai_generated.lower() == 'yes':
                                    correctness_result = "Incorrect"
                                
                                sentiment_result = hirely_ai.analyze_sentiment(answer)
                                
                                st.session_state.technical_answers[st.session_state.current_tech_q] = {
                                    'question': current_q,
                                    'answer': answer,
                                    'analysis': {
                                        'correctness': correctness_result,
                                        'sentiment': sentiment_result,
                                        'ai_detected': ai_generated,
                                        'ai_confidence': confidence,
                                        'ai_reason': reason
                                    }
                                }
                                
                                st.session_state.current_tech_q += 1
                                st.rerun()
                    else:
                        st.error("Please provide an answer before proceeding.")
        else:
            st.success("🎉 Technical assessment completed!")
            if st.button("Continue to Project Discussion", type="primary"):
                st.session_state.phase = "project_discussion"
                st.rerun()
    
    with col2:
        st.subheader("Candidate Summary")
        data = st.session_state.candidate_data
        
        st.write(f"**Name:** {data.get('fullName', 'N/A')}")
        st.write(f"**Email:** {data.get('email', 'N/A')}")
        st.write(f"**Experience:** {data.get('experience', 'N/A')} years")
        
        st.markdown("**Tech Stack:**")
        for tech in data.get('techStack', []):
            st.markdown(f"🔹 {tech}")
        
        # Scorecard
        if st.session_state.technical_answers:
            correct_answers = sum(1 for ans in st.session_state.technical_answers.values() 
                                if ans['analysis']['correctness'].lower() == 'correct')
            total_answered = len(st.session_state.technical_answers)
            score = (correct_answers / total_answered) * 100 if total_answered > 0 else 0
            
            st.markdown("---")
            st.subheader("Scorecard")
            st.metric("Correct Answers", f"{correct_answers}/{total_answered}")
            st.metric("Score", f"{score:.1f}%")

def show_project_discussion():
    st.title("💼 Project Discussion")
    
    # Show bot message if exists
    if st.session_state.bot_message:
        st.info(f"**Hirely:** {st.session_state.bot_message}")
        if st.button("Continue", key="continue_bot_proj"):
            st.session_state.bot_message = None
            st.rerun()
        return
    
    # Progress
    total_questions = len(st.session_state.project_questions)
    if total_questions > 0:
        progress = (st.session_state.current_proj_q / total_questions) * 100
        st.progress(progress / 100)
        st.caption(f"Question {st.session_state.current_proj_q + 1} of {total_questions} ({progress:.1f}%)")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Project Questions")

        # Show analysis of the previous question
        if st.session_state.current_proj_q > 0:
            last_answer_data = st.session_state.project_answers.get(st.session_state.current_proj_q - 1)
            if last_answer_data:
                st.markdown("---")
                st.subheader("Feedback on Your Last Answer")
                analysis = last_answer_data['analysis']
                sentiment = analysis.get('sentiment', 'N/A')
                ai_detected = analysis.get('ai_detected', 'N/A')
                ai_confidence = analysis.get('ai_confidence', 'N/A')
                ai_reason = analysis.get('ai_reason', 'N/A')
                
                st.info(f"**Sentiment:** Your response was {sentiment.lower()}.")
                
                if ai_detected.lower() == 'yes':
                    st.error(f"**AI Detection:** This answer appears to be AI-generated.")
                    st.warning(f"**AI Detection Details:**")
                    st.write(f"• **Confidence:** {ai_confidence}")
                    st.write(f"• **Reason:** {ai_reason}")

        # Current question
        if st.session_state.current_proj_q < len(st.session_state.project_questions):
            current_q = st.session_state.project_questions[st.session_state.current_proj_q]
            st.markdown(f"**Question {st.session_state.current_proj_q + 1}:** {current_q}")
            
            col_input, col_btn1, col_btn2 = st.columns([3, 1, 1])
            
            with col_input:
                answer = st.text_area("Your Answer", key=f"proj_answer_{st.session_state.current_proj_q}", 
                                    placeholder="Type your answer here...", height=100)
            
            with col_btn1:
                if st.button("🎤", key=f"voice_proj_{st.session_state.current_proj_q}", help="Voice Input (Coming Soon)"):
                    st.info("Voice input feature coming soon!")
            
            with col_btn2:
                if st.button("Send", key=f"send_proj_{st.session_state.current_proj_q}", type="primary"):
                    if answer.strip():
                        if hirely_ai.is_user_input_a_question(answer):
                            with st.spinner("Thinking..."):
                                bot_reply = hirely_ai.answer_user_question(answer)
                                # Fallback if bot reply is empty or off-topic
                                if not bot_reply or any(x in bot_reply.lower() for x in ["not sure", "don't know", "uncertain", "no idea"]):
                                    st.session_state.bot_message = hirely_ai.fallback_response("project")
                                else:
                                    st.session_state.bot_message = bot_reply
                            st.rerun()
                        elif hirely_ai.is_clarification_request(answer):
                            with st.spinner("Re-explaining..."):
                                re_explanation = hirely_ai.re_explain_question(current_q)
                                st.session_state.bot_message = f"Let me clarify: {re_explanation}"
                            st.rerun()
                        elif answer.lower() in ['ok', 'continue', 'next', 'yes', 'got it']:
                            st.session_state.current_proj_q += 1
                            st.rerun()
                        else:
                            with st.spinner("Analyzing your answer..."):
                                ai_detected_result = hirely_ai.detect_ai_generated_text(answer)
                                
                                # Parse AI detection result
                                ai_generated = "No"
                                confidence = "Low"
                                reason = "Analysis not available"
                                
                                if "AI-Generated:" in ai_detected_result:
                                    lines = ai_detected_result.split('\n')
                                    for line in lines:
                                        if line.startswith("AI-Generated:"):
                                            ai_generated = line.split(":")[1].strip()
                                        elif line.startswith("Confidence:"):
                                            confidence = line.split(":")[1].strip()
                                        elif line.startswith("Reason:"):
                                            reason = line.split(":")[1].strip()
                                
                                sentiment_result = hirely_ai.analyze_sentiment(answer)
                                
                                st.session_state.project_answers[st.session_state.current_proj_q] = {
                                    'question': current_q,
                                    'answer': answer,
                                    'analysis': {
                                        'sentiment': sentiment_result,
                                        'ai_detected': ai_generated,
                                        'ai_confidence': confidence,
                                        'ai_reason': reason
                                    }
                                }
                                
                                st.session_state.current_proj_q += 1
                                st.rerun()
                    else:
                        st.error("Please provide an answer before proceeding.")
        else:
            st.success("🎉 Project discussion completed!")
            if st.button("Generate Report", type="primary"):
                st.session_state.phase = "report"
                st.rerun()
    
    with col2:
        st.subheader("Candidate Summary")
        data = st.session_state.candidate_data
        
        st.write(f"**Name:** {data.get('fullName', 'N/A')}")
        st.write(f"**Email:** {data.get('email', 'N/A')}")
        st.write(f"**Experience:** {data.get('experience', 'N/A')} years")
        
        st.markdown("**Tech Stack:**")
        for tech in data.get('techStack', []):
            st.markdown(f"🔹 {tech}")

def show_report():
    st.title("📊 Assessment Report")
    
    # Generate report
    with st.spinner("Generating comprehensive report..."):
        # Prepare history
        history = "## Technical Assessment\n"
        for q_num, answer_data in st.session_state.technical_answers.items():
            history += f"**Q{q_num + 1}:** {answer_data['question']}\n"
            history += f"**Answer:** {answer_data['answer']}\n"
            analysis = answer_data['analysis']
            history += f"**Analysis:** Correctness: {analysis['correctness']}, Sentiment: {analysis['sentiment']}, AI-Detected: {analysis['ai_detected']}\n\n"
        
        history += "## Project Discussion\n"
        for q_num, answer_data in st.session_state.project_answers.items():
            history += f"**Q{q_num + 1}:** {answer_data['question']}\n"
            history += f"**Answer:** {answer_data['answer']}\n"
            analysis = answer_data['analysis']
            history += f"**Analysis:** Sentiment: {analysis['sentiment']}, AI-Detected: {analysis['ai_detected']}\n\n"
        
        report = hirely_ai.generate_final_report(st.session_state.candidate_data, history)
    
    # Display report
    st.markdown(report)
    
    # Download options
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Download as Markdown", type="primary"):
            # Save report logic here
            st.success("Report saved as markdown!")
    
    with col2:
        if st.button("🔄 Start New Interview", type="secondary"):
            # Reset session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

# --- Main App Logic ---
show_progress_tracker()

if st.session_state.phase == "welcome":
        show_welcome_screen()
elif st.session_state.phase == "info_gathering":
        show_info_gathering()
elif st.session_state.phase == "technical_qa":
    show_technical_qa()
elif st.session_state.phase == "project_discussion":
    show_project_discussion()
elif st.session_state.phase == "report":
    show_report()


