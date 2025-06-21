import streamlit as st
import google.generativeai as genai
from datetime import datetime
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="TalentScout AI",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- AI Configuration ---
# It's recommended to use st.secrets for API keys in a deployed app
genai.configure(api_key="AIzaSyDxYIfsEDSDvqVOLl5Y00bOEPQ9zE73vjE") # type: ignore

# --- TalentScout AI Logic ---
@st.cache_resource
def get_ai_model():
    return TalentScoutAI()

class TalentScoutAI:
    def __init__(self):
        self.model = genai.GenerativeModel("models/gemini-1.5-flash-latest") # type: ignore

    def analyze(self, prompt):
        return self.model.generate_content(prompt).text.strip() # type: ignore

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
        prompt = f"Analyze the sentiment of this text. Respond with only: 'Positive', 'Negative', or 'Neutral'.\n\nText: {text}"
        return self.analyze(prompt)

    def check_correctness(self, question, answer):
        prompt = f"Evaluate if this answer correctly addresses the technical question. Consider accuracy, completeness, and relevance. Respond with only: 'Correct' or 'Incorrect'.\n\nQuestion: {question}\nAnswer: {answer}"
        return self.analyze(prompt)

    def generate_tech_questions(self, tech_stack):
        questions = []
        for tech in tech_stack:
            tech_questions = [
                f"What are the core principles and best practices of {tech}?",
                f"Describe a challenging problem you solved using {tech}. What was your approach?",
                f"What are the common pitfalls and how do you avoid them when working with {tech}?"
            ]
            questions.extend(tech_questions)
        return questions

    def generate_project_questions(self):
        return [
            "Please describe a significant project you've worked on recently. What was the goal and your role?",
            "What technologies did you use in this project and why did you choose them?",
            "What was the most innovative or novel aspect of your approach?",
            "What were the biggest challenges you faced and how did you overcome them?",
            "What were the outcomes and what did you learn from this project?"
        ]

    def generate_final_report(self, candidate_data, technical_answers, project_answers):
        prompt = f"""
        Generate a comprehensive hiring report in Markdown for:
        
        **Candidate Information:**
        - **Name:** {candidate_data.get('fullName')}
        - **Email:** {candidate_data.get('email')}
        - **Phone:** {candidate_data.get('phone')}
        - **Location:** {candidate_data.get('location')}
        - **Experience:** {candidate_data.get('experience')}
        - **Desired Position(s):** {', '.join(candidate_data.get('positions', []))}
        - **Tech Stack:** {', '.join(candidate_data.get('techStack', []))}
        
        **Technical Assessment:**
        {technical_answers}
        
        **Project Discussion:**
        {project_answers}
        
        **Analysis & Recommendation:**
        Provide a detailed analysis including:
        1. Technical competency assessment
        2. Problem-solving ability
        3. Communication skills
        4. Overall fit for the role
        5. Final recommendation: 'Strong Hire', 'Proceed with Caution', or 'Not a Good Fit'
        6. Specific feedback and areas for improvement
        """
        return self.analyze(prompt)

    def answer_user_question(self, question):
        prompt = f"Concisely answer the user's question in the context of a job interview.\n\nUser: {question}\nAI:"
        return self.analyze(prompt)

    def is_user_input_a_question(self, text):
        # Simple heuristic, can be replaced by a more complex check if needed
        return text.strip().endswith('?')

talentscout_ai = get_ai_model()

# --- Interview Content ---
PROJECT_QUESTIONS = [
    "Please describe a significant project you've worked on recently. What was the goal and your role?",
    "What technologies did you use in this project and why did you choose them?",
    "What was the most innovative or novel aspect of your approach?",
    "What were the biggest challenges you faced and how did you overcome them?",
    "What were the outcomes and what did you learn from this project?"
]

# --- Session State Initialization ---
if "phase" not in st.session_state:
    st.session_state.phase = "welcome"
    st.session_state.candidate_data = {}
    st.session_state.chat_history = []
    st.session_state.technical_questions = []
    st.session_state.technical_answers = {}
    st.session_state.project_questions = PROJECT_QUESTIONS
    st.session_state.project_answers = {}
    st.session_state.current_tech_q = 0
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
    current_phase_key = st.session_state.phase
    current_index = phase_order.index(current_phase_key)

    for i, (phase_key, phase_name) in enumerate(phases.items()):
        if i < current_index:
            st.sidebar.markdown(f"- ✅ {phase_name}")
        elif i == current_index:
            st.sidebar.markdown(f"**- ⏳ {phase_name}**")
        else:
            st.sidebar.markdown(f"- ⚪ {phase_name}")

def show_welcome_screen():
    st.title("TalentScout - Your Virtual Hiring Assistant")
    st.markdown("Hello! I'm **hierly**, your AI-powered hiring assistant. I'll help you through our comprehensive interview process designed to assess your technical skills and project experience.")
    st.markdown("---")
    st.subheader("The process includes:")
    st.markdown("""
        - Basic information collection
        - Technical skill assessment
        - Project experience discussion
        - Comprehensive evaluation report
    """)
    if st.button("Start Application", type="primary"):
        st.session_state.phase = "info_gathering"
        st.rerun()

def show_info_gathering():
    st.title("👤 Your Information")
    st.markdown("Please provide your details below. This will help us tailor the interview.")

    with st.form("info_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("Full Name *")
            email = st.text_input("Email Address *")
            phone = st.text_input("Phone Number *")
            experience = st.selectbox("Years of Experience *", ["< 1 year", "1-3 years", "3-5 years", "5-10 years", "10+ years"])
        
        with col2:
            positions_list = st.text_input("Desired Position(s) (comma-separated) *", "Software Engineer, Data Scientist")
            location = st.text_input("Current Location *")
            tech_stack_list = st.text_input("Tech Stack (comma-separated) *", "Python, React, SQL, Docker")

        submitted = st.form_submit_button("Start Interview", type="primary")

        if submitted:
            tech_stack = [tech.strip() for tech in tech_stack_list.split(',')] if tech_stack_list else []
            positions = [pos.strip() for pos in positions_list.split(',')] if positions_list else []
            data = {
                "fullName": full_name,
                "email": email,
                "phone": phone,
                "experience": experience,
                "positions": positions,
                "location": location,
                "techStack": tech_stack,
            }

            if all([full_name, email, phone, experience, positions, location, tech_stack]):
                st.session_state.candidate_data = data
                st.session_state.technical_questions = talentscout_ai.generate_tech_questions(tech_stack)
                st.session_state.phase = "technical_qa"
                st.rerun()
            else:
                st.error("Please fill in all required fields (*).")

def show_technical_qa():
    st.title("🔧 Tech Stack Deep Dive")
    
    # Progress meter
    total_questions = len(st.session_state.technical_questions)
    progress = st.session_state.current_tech_q / total_questions if total_questions > 0 else 0
    st.progress(progress, text=f"Question {st.session_state.current_tech_q + 1} of {total_questions}")
    
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
                    st.warning(f"**Analysis:** That doesn't seem quite right. No worries, let's keep going!")

                st.info(f"**Sentiment:** Your response was {sentiment.lower()}.")
                
                # Show AI detection info even if not flagged
                if ai_detected.lower() == 'no':
                    st.success(f"**AI Detection:** Your answer appears to be original and authentic.")
                    if ai_confidence != 'N/A':
                        st.write(f"• **Confidence:** {ai_confidence}")
                
                st.markdown("---")

        # Display any message from the bot (e.g., answer to user's question)
        if st.session_state.bot_message:
            st.info(st.session_state.bot_message)
            st.session_state.bot_message = None

        if st.session_state.current_tech_q < len(st.session_state.technical_questions):
            current_q = st.session_state.technical_questions[st.session_state.current_tech_q]
            
            st.markdown(f"**Question {st.session_state.current_tech_q + 1}:**")
            st.write(current_q)
            
            # Answer input
            answer = st.text_area("Your Answer:", key=f"tech_ans_{st.session_state.current_tech_q}", 
                                placeholder="Type your answer here...", height=150)
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
            with col_btn1:
                if st.button("🎤 Voice", key=f"voice_{st.session_state.current_tech_q}"):
                    st.info("Voice input feature coming soon!")
            
            with col_btn2:
                if st.button("Send", key=f"send_{st.session_state.current_tech_q}", type="primary"):
                    if answer.strip():
                        if talentscout_ai.is_user_input_a_question(answer):
                            with st.spinner("Thinking..."):
                                st.session_state.bot_message = talentscout_ai.answer_user_question(answer)
                            st.rerun()
                        elif answer.lower().strip() in ["ok", "okay", "got it", "continue", "next"]:
                            st.session_state.current_tech_q += 1
                st.rerun()
    else:
                            # Analyze answer
                            with st.spinner("Analyzing your answer..."):
                                ai_detected_result = talentscout_ai.detect_ai_generated_text(answer)
                                correctness_result = talentscout_ai.check_correctness(current_q, answer)

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

                                # If AI-generated, mark as incorrect
                                if ai_generated.lower() == 'yes':
                                    correctness_result = 'Incorrect'
                                
                                analysis = {
                                    'sentiment': talentscout_ai.analyze_sentiment(answer),
                                    'ai_detected': ai_generated,
                                    'ai_confidence': confidence,
                                    'ai_reason': reason,
                                    'correctness': correctness_result
                                }
                            
                            st.session_state.technical_answers[st.session_state.current_tech_q] = {
                                'question': current_q,
                                'answer': answer,
                                'analysis': analysis
                            }
                            
                            st.session_state.current_tech_q += 1
                            st.rerun()
                    else:
                        st.error("Please provide an answer before proceeding.")
        else:
            st.success("Technical Q&A completed! Moving to project discussion...")
            if st.button("Continue to Projects", type="primary"):
                st.session_state.phase = "project_discussion"
                st.rerun()
    
    with col2:
        st.subheader("Candidate Summary")
        
        data = st.session_state.candidate_data
        st.write(f"**Name:** {data.get('fullName', 'N/A')}")
        st.write(f"**Email:** {data.get('email', 'N/A')}")
        st.write(f"**Experience:** {data.get('experience', 'N/A')}")
        
        st.write("**Tech Stack:**")
        for tech in data.get('techStack', []):
            st.markdown(f"`{tech}`")
        
        # Scorecard
        if st.session_state.technical_answers:
            st.subheader("Scorecard")
            correct_answers = sum(1 for ans in st.session_state.technical_answers.values() 
                                if ans['analysis']['correctness'].lower() == 'correct')
            total_answered = len(st.session_state.technical_answers)
            score = (correct_answers / total_answered * 100) if total_answered > 0 else 0
            
            st.metric("Correct Answers", f"{correct_answers}/{total_answered}")
            st.metric("Accuracy", f"{score:.1f}%")

def show_project_discussion():
    st.title("📋 Project Discussion")
    
    # Progress meter
    total_questions = len(st.session_state.project_questions)
    progress = st.session_state.current_proj_q / total_questions if total_questions > 0 else 0
    st.progress(progress, text=f"Question {st.session_state.current_proj_q + 1} of {total_questions}")
    
    col1, col2 = st.columns([2, 1])
    
        with col1:
        st.subheader("Project Questions")
        
        # Show analysis of the previous question
        if st.session_state.current_proj_q > 0:
            last_answer_data = st.session_state.project_answers.get(st.session_state.current_proj_q - 1)
            if last_answer_data and 'analysis' in last_answer_data:
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
                else:
                    st.success(f"**AI Detection:** Your answer appears to be original and authentic.")
                    if ai_confidence != 'N/A':
                        st.write(f"• **Confidence:** {ai_confidence}")
                
                st.markdown("---")

        if st.session_state.current_proj_q < len(st.session_state.project_questions):
            current_q = st.session_state.project_questions[st.session_state.current_proj_q]
            
            st.markdown(f"**Question {st.session_state.current_proj_q + 1}:**")
            st.write(current_q)
            
            # Answer input
            answer = st.text_area("Your Answer:", key=f"proj_ans_{st.session_state.current_proj_q}", 
                                placeholder="Type your answer here...", height=150)
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
            with col_btn1:
                if st.button("🎤 Voice", key=f"proj_voice_{st.session_state.current_proj_q}"):
                    st.info("Voice input feature coming soon!")
            
            with col_btn2:
                if st.button("Send", key=f"proj_send_{st.session_state.current_proj_q}", type="primary"):
                    if answer.strip():
                        with st.spinner("Analyzing your answer..."):
                            ai_detected_result = talentscout_ai.detect_ai_generated_text(answer)
                            
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
                            
                            analysis = {
                                'sentiment': talentscout_ai.analyze_sentiment(answer),
                                'ai_detected': ai_generated,
                                'ai_confidence': confidence,
                                'ai_reason': reason,
                            }
                        st.session_state.project_answers[st.session_state.current_proj_q] = {
                            'question': current_q,
                            'answer': answer,
                            'analysis': analysis
                        }
                        
                        st.session_state.current_proj_q += 1
                        st.rerun()
                    else:
                        st.error("Please provide an answer before proceeding.")
        else:
            st.success("Project discussion completed! Generating your report...")
            if st.button("View Report", type="primary"):
                st.session_state.phase = "report"
                st.rerun()
    
    with col2:
        st.subheader("Candidate Summary")
        
        data = st.session_state.candidate_data
        st.write(f"**Name:** {data.get('fullName', 'N/A')}")
        st.write(f"**Email:** {data.get('email', 'N/A')}")
        st.write(f"**Experience:** {data.get('experience', 'N/A')}")
        
        st.write("**Tech Stack:**")
        for tech in data.get('techStack', []):
            st.markdown(f"`{tech}`")
        
        # Technical Scorecard
        if st.session_state.technical_answers:
            st.subheader("Technical Scorecard")
            correct_answers = sum(1 for ans in st.session_state.technical_answers.values() 
                                if ans['analysis']['correctness'].lower() == 'correct')
            total_answered = len(st.session_state.technical_answers)
            score = (correct_answers / total_answered * 100) if total_answered > 0 else 0
            
            st.metric("Correct Answers", f"{correct_answers}/{total_answered}")
            st.metric("Accuracy", f"{score:.1f}%")

def show_report():
    st.title("📊 Interview Report")
    
    # Generate comprehensive report
    with st.spinner("Generating your comprehensive report..."):
        technical_summary = "\n".join([
            f"**Q{idx+1}:** {ans['question']}\n**A:** {ans['answer']}\n**Analysis:** Correctness: {ans['analysis'].get('correctness', 'N/A')}, Sentiment: {ans['analysis'].get('sentiment', 'N/A')}, AI-Generated: {ans['analysis'].get('ai_detected', 'N/A')}\n"
            for idx, ans in st.session_state.technical_answers.items()
        ])
        
        project_summary = "\n".join([
            f"**Q{idx+1}:** {ans['question']}\n**A:** {ans['answer']}\n**Analysis:** Sentiment: {ans.get('analysis', {}).get('sentiment', 'N/A')}, AI-Generated: {ans.get('analysis', {}).get('ai_detected', 'N/A')}\n"
            for idx, ans in st.session_state.project_answers.items()
        ])
        
        report = talentscout_ai.generate_final_report(
            st.session_state.candidate_data,
            technical_summary,
            project_summary
        )
    
    # Display report
    st.markdown(report)
    
    # Candidate feedback section
    st.subheader("📝 Interview Feedback")
    st.write("We'd love to hear your thoughts about this interview experience!")
    
    feedback = st.text_area("Your Feedback:", placeholder="Please share your experience, suggestions, or any comments...", height=100)
    
    if st.button("Submit Feedback", type="primary"):
        if feedback.strip():
            st.success("Thank you for your feedback! A recruiter will be in touch soon.")
        else:
            st.info("Thank you for completing the interview! A recruiter will be in touch soon.")
    
    if st.button("Start New Interview"):
        st.session_state.clear()
        st.rerun()

# --- Main App Router ---
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


