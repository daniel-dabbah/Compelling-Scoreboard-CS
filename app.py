import streamlit as st
from datetime import datetime, date
import json

# Configure page
st.set_page_config(
    page_title="הערכה פנימית - לוח תוצאות",
    page_icon="🏰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for jungle-ocean theme with green and blue colors
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;700&display=swap');
    
    * {
        font-family: 'Heebo', sans-serif;
    }
    
    .main .block-container {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 30%, #a5d6a7 60%, #81c784 100%);
        min-height: 100vh;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f1f8e9 0%, #dcedc8 25%, #c5e1a5 50%, #aed581 75%, #9ccc65 100%);
    }
    
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        text-align: center;
        color: #33691e;
        margin-bottom: 2.5rem;
        background: linear-gradient(135deg, #558b2f 0%, #689f38 50%, #7cb342 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 2px 4px rgba(51,105,30,0.2);
    }
    
    .topic-header {
        background: linear-gradient(135deg, #6d4c41 0%, #8d6e63 50%, #a1887f 100%);
        color: #fafafa;
        padding: 1rem;
        border-radius: 12px;
        margin: 2rem 0 1rem 0;
        text-align: center;
        font-size: 1.4rem;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(109, 76, 65, 0.4);
    }
    
    .question-container {
        background: linear-gradient(135deg, #ffffff 0%, #f9fbe7 100%);
        padding: 2rem;
        border-radius: 18px;
        margin: 1.8rem 0;
        border-right: 6px solid #7cb342;
        box-shadow: 0 6px 20px rgba(124, 179, 66, 0.25);
        direction: rtl;
        text-align: right;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .question-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(124, 179, 66, 0.35);
    }
    
    .question-container h4 {
        color: #33691e;
        font-weight: 500;
        font-size: 1.3rem;
        margin: 0;
        direction: rtl;
        line-height: 1.6;
    }
    
    .score-display {
        font-size: 3.2rem;
        font-weight: bold;
        text-align: center;
        padding: 3rem;
        background: linear-gradient(135deg, #558b2f 0%, #689f38 50%, #7cb342 100%);
        color: white;
        border-radius: 25px;
        margin: 2.5rem 0;
        box-shadow: 0 10px 30px rgba(85, 139, 47, 0.4);
        direction: ltr;
    }
    
    .feedback-box {
        background: linear-gradient(135deg, #fff9c4 0%, #fff59d 100%);
        padding: 2.2rem;
        border-radius: 18px;
        margin: 1.8rem 0;
        border: 2px solid #fbc02d;
        box-shadow: 0 6px 20px rgba(251, 192, 45, 0.25);
        direction: rtl;
        text-align: center;
    }
    
    .improvement-box {
        background: linear-gradient(135deg, #dcedc8 0%, #c5e1a5 100%);
        padding: 2.2rem;
        border-radius: 18px;
        margin: 1.8rem 0;
        border: 2px solid #8bc34a;
        box-shadow: 0 6px 20px rgba(139, 195, 74, 0.25);
        direction: rtl;
        text-align: center;
    }
    
    .progress-stats {
        background: linear-gradient(135deg, #ffffff 0%, #f1f8e9 100%);
        padding: 2rem;
        border-radius: 18px;
        box-shadow: 0 6px 20px rgba(85, 139, 47, 0.2);
        margin: 1.2rem 0;
        border-top: 4px solid #689f38;
        text-align: center;
        transition: transform 0.2s ease;
    }
    
    .progress-stats:hover {
        transform: translateY(-3px);
    }
    
    .chart-container {
        background: linear-gradient(135deg, #ffffff 0%, #f9fbe7 100%);
        padding: 2rem;
        border-radius: 18px;
        margin: 2rem 0;
        box-shadow: 0 6px 20px rgba(124, 179, 66, 0.2);
        border: 1px solid #c5e1a5;
    }
    
    .chart-title {
        text-align: center;
        font-size: 1.5rem;
        font-weight: 600;
        color: #33691e;
        margin-bottom: 1.5rem;
    }
    
    .input-container {
        background: linear-gradient(135deg, #ffffff 0%, #f9fbe7 100%);
        padding: 2rem;
        border-radius: 18px;
        margin: 1.8rem 0;
        border: 2px solid #c5e1a5;
        box-shadow: 0 6px 20px rgba(124, 179, 66, 0.15);
    }
    
    .guidance-container {
        background: linear-gradient(135deg, #ffffff 0%, #f1f8e9 100%);
        padding: 2.5rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 8px 25px rgba(85, 139, 47, 0.2);
        direction: rtl;
        text-align: right;
        border-right: 5px solid #558b2f;
    }
    
    .guidance-section {
        margin: 2rem 0;
        padding: 1.5rem;
        background: linear-gradient(135deg, #dcedc8 0%, #c5e1a5 100%);
        border-radius: 15px;
        border-right: 4px solid #689f38;
    }
    
    .guidance-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #33691e;
        margin-bottom: 1rem;
    }
    
    .guidance-list {
        margin-right: 1.5rem;
        line-height: 2;
        color: #33691e;
    }
    
    .guidance-list li {
        margin: 0.8rem 0;
        font-size: 1.1rem;
    }
    
    .reminder-box {
        background: linear-gradient(135deg, #fff9c4 0%, #fff59d 100%);
        padding: 1.8rem;
        border-radius: 15px;
        margin: 2rem 0;
        border: 2px solid #fbc02d;
        text-align: center;
        direction: rtl;
        font-size: 1.2rem;
        color: #f57f17;
        font-weight: 500;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #ffecb3 0%, #ffe082 100%);
        padding: 1.8rem;
        border-radius: 15px;
        margin: 2rem 0;
        border: 2px solid #ffa726;
        text-align: center;
        direction: rtl;
        font-size: 1.15rem;
        color: #e65100;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(255, 167, 38, 0.25);
    }
    
    .signature-box {
        text-align: center;
        margin-top: 3rem;
        padding: 1.5rem;
        background: linear-gradient(135deg, #dcedc8 0%, #c5e1a5 100%);
        border-radius: 15px;
        font-size: 1.3rem;
        color: #33691e;
        font-weight: 600;
    }
    
    .stSlider > div > div {
        direction: ltr;
    }
    
    .stNumberInput > div > div {
        direction: ltr;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: rgba(197, 225, 165, 0.3);
        padding: 0.5rem;
        border-radius: 15px;
        justify-content: center;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #ffffff 0%, #f9fbe7 100%);
        border-radius: 12px;
        padding: 1rem 2rem;
        border: 2px solid transparent;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #558b2f 0%, #689f38 100%);
        color: white;
        border-color: #558b2f;
        box-shadow: 0 4px 15px rgba(85, 139, 47, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Assessment questions organized by topics
TOPICS_AND_QUESTIONS = [
    {
        "topic": "מבנה לולאות for",
        "questions": [
            "עד כמה אני מרגיש שאני שולט בנושא: מבנה לולאות for"
        ]
    },
    {
        "topic": "לולאות שבהן צריך לעדכן מונה / צובר / מכפלה",
        "questions": [
            "עד כמה אני מרגיש שאני שולט בנושא: לולאות שבהן צריך לעדכן מונה / צובר / מכפלה"
        ]
    },
    {
        "topic": "לולאות שבהן מוצאים את האיבר הגדול ביותר ויודעים את טווח הערכים האפשרי",
        "questions": [
            "עד כמה אני מרגיש שאני שולט בנושא: לולאות שבהן מוצאים את האיבר הגדול ביותר ויודעים את טווח הערכים האפשרי"
        ]
    },
    {
        "topic": "לולאות שבהן מוצאים את האיבר הגדול ביותר ולא יודעים את טווח הערכים האפשרי",
        "questions": [
            "עד כמה אני מרגיש שאני שולט בנושא: לולאות שבהן מוצאים את האיבר הגדול ביותר ולא יודעים את טווח הערכים האפשרי"
        ]
    },
    {
        "topic": "שימוש באיטרציה בלולאה במשתנה שקיבל ערך באיטרציה הקודמת",
        "questions": [
            "עד כמה אני מרגיש שאני שולט בנושא: שימוש באיטרציה בלולאה במשתנה שקיבל ערך באיטרציה הקודמת, ועדכון הערך כך שהאיטרציה הבאה תשתמש בערך החדש (השאלה של הטמפרטורות)"
        ]
    },
    {
        "topic": "טבלת מעקב - כתיבה",
        "questions": [
            "עד כמה אני מרגיש שאני שולט בנושא: טבלת מעקב - כתיבה"
        ]
    },
    {
        "topic": "קריאת קוד והסבר מה הוא עושה",
        "questions": [
            "עד כמה אני מרגיש שאני שולט בנושא: קריאת קוד והסבר מה הוא עושה"
        ]
    },
    {
        "topic": "כל הנושאים של פרק אחד",
        "questions": [
            "עד כמה אני מרגיש שאני שולט בנושא: כל הנושאים של פרק אחד"
        ]
    },
    {
        "topic": "כל הנושאים של פרק 2 (תנאים, פונקציות מתמטיות, פונקציות רנדומליות)",
        "questions": [
            "עד כמה אני מרגיש שאני שולט בנושא: כל הנושאים של פרק 2 (תנאים, פונקציות מתמטיות, פונקציות רנדומליות)"
        ]
    }
]

ADDITIONAL_QUESTIONS = [
    "עד כמה אני מרגיש שאני מצליח להחזיר לעצמי את האנרגיה שאני מוציא על הלימודים",
    "עד כמה אני מרגיש שאני עוזר לאחרים מהכיתה"
]

def get_feedback_message(score):
    """Generate short feedback based on the total score"""
    if score >= 90:
        return "מצוין! כל הכבוד! 🏆"
    elif score >= 80:
        return "עבודה טובה! 🌲"
    elif score >= 70:
        return "יפה, ממשיכים לעבוד! 🗡️"
    else:
        return "עבודה טובה, בוא נשפר עוד קצת! 🛡️"

def load_manual_scores():
    """Load manually entered scores from session state"""
    if 'manual_scores' not in st.session_state:
        st.session_state.manual_scores = {}
    return st.session_state.manual_scores

def save_manual_scores(scores):
    """Save manually entered scores to session state"""
    st.session_state.manual_scores = scores

def create_simple_progress_chart(scores_dict):
    """Create a simple progress chart using Streamlit's built-in chart"""
    if not scores_dict:
        return None
    
    # Filter out empty scores and sort by assessment number
    valid_scores = {k: v for k, v in scores_dict.items() if v is not None and v != ""}
    if not valid_scores:
        return None
    
    # Sort by assessment number
    sorted_items = sorted(valid_scores.items(), key=lambda x: int(x[0]))
    
    return {f"הערכה {num}": score for num, score in sorted_items}

def display_statistics_from_manual(scores_dict):
    """Display progress statistics from manually entered scores"""
    valid_scores = [score for score in scores_dict.values() if score is not None and score != ""]
    
    if not valid_scores:
        st.info("הזן ציונים כדי לראות סטטיסטיקות")
        return
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        current_score = valid_scores[-1] if valid_scores else 0
        st.markdown("""
        <div class="progress-stats">
            <h3 style="color: #33691e; margin: 0;">הציון האחרון שלי</h3>
            <h2 style="color: #558b2f; margin: 5px 0;">{}/100</h2>
        </div>
        """.format(current_score), unsafe_allow_html=True)
    
    with col2:
        best_score = max(valid_scores) if valid_scores else 0
        st.markdown("""
        <div class="progress-stats">
            <h3 style="color: #33691e; margin: 0;">הציון הכי טוב שלי</h3>
            <h2 style="color: #689f38; margin: 5px 0;">{}/100</h2>
        </div>
        """.format(best_score), unsafe_allow_html=True)
    
    with col3:
        total_assessments = len(valid_scores)
        st.markdown("""
        <div class="progress-stats">
            <h3 style="color: #33691e; margin: 0;">כמה הערכות הזנתי</h3>
            <h2 style="color: #7cb342; margin: 5px 0;">{}</h2>
        </div>
        """.format(total_assessments), unsafe_allow_html=True)

def calculate_total_questions():
    """Calculate total number of questions"""
    total = 0
    for topic_group in TOPICS_AND_QUESTIONS:
        total += len(topic_group["questions"])
    total += len(ADDITIONAL_QUESTIONS)
    return total

def main():
    # Header
    st.markdown('<h1 class="main-header">🌲 הערכה פנימית - לוח תוצאות 🏰</h1>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'current_responses' not in st.session_state:
        st.session_state.current_responses = {}
    if 'show_results' not in st.session_state:
        st.session_state.show_results = False
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = 0  # 0 for first tab, 1 for second tab, 2 for third tab
    
    # Check if we need to switch to progress tab
    if st.session_state.get('switch_to_progress', False):
        st.session_state.active_tab = 1
        st.session_state.switch_to_progress = False
    
    # Create tabs with manual selection - now with 3 tabs
    tab_names = ["הערכה חדשה", "להסתכל על ההתקדמות שלי", "איך ניתן להתקדם אל המטרה"]
    
    # Create tab selection buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🌲 הערכה חדשה", 
                    type="primary" if st.session_state.active_tab == 0 else "secondary",
                    use_container_width=True,
                    key="tab_assessment"):
            st.session_state.active_tab = 0
    
    with col2:
        if st.button("📜 להסתכל על ההתקדמות שלי", 
                    type="primary" if st.session_state.active_tab == 1 else "secondary",
                    use_container_width=True,
                    key="tab_progress"):
            st.session_state.active_tab = 1
    
    with col3:
        if st.button("🎯 איך ניתן להתקדם אל המטרה", 
                    type="primary" if st.session_state.active_tab == 2 else "secondary",
                    use_container_width=True,
                    key="tab_guidance"):
            st.session_state.active_tab = 2
    
    st.markdown("---")
    
    # Display content based on active tab
    if st.session_state.active_tab == 0:
        # Tab 1: New Assessment
        if not st.session_state.show_results:
            st.markdown("<div style='text-align: center; margin-bottom: 2rem;'><p style='font-size: 1.1rem; color: #33691e;'>תן לכל נושא ציון מ-1 (בכלל לא בטוח) עד 10 (מאוד בטוח) - לפי איך שאתה מרגיש ממש עכשיו.</p></div>", unsafe_allow_html=True)
            
            # Important warning box
            st.markdown("""
            <div class="warning-box">
                ⚠️ <strong>שימו לב:</strong> יכול להיות נושא במבחן שלא היה כתוב בדף ההערכה הפנימית. 
                הוא נועד לעזור לכם להתכונן, אבל השאלות במבחן לא בהכרח יהיו רק מהנושאים האלו.
            </div>
            """, unsafe_allow_html=True)
            
            # Display all questions at once
            with st.form("assessment_form"):
                responses = {}
                question_index = 0
                
                # Topic-based questions
                for topic_group in TOPICS_AND_QUESTIONS:
                    questions = topic_group["questions"]
                    
                    # Display questions without topic header
                    for question in questions:
                        st.markdown(f"""
                        <div class="question-container">
                            <h4>{question}?</h4>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        responses[question_index] = st.slider(
                            f"השאלה מס׳ {question_index + 1}:",
                            min_value=1,
                            max_value=10,
                            value=st.session_state.current_responses.get(question_index, 5),
                            key=f"q_{question_index}",
                            label_visibility="collapsed"
                        )
                        question_index += 1
                
                # Additional questions section
                st.markdown('<div class="topic-header">שאלות נוספות</div>', unsafe_allow_html=True)
                
                for i, question in enumerate(ADDITIONAL_QUESTIONS):
                    st.markdown(f"""
                    <div class="question-container">
                        <h4>{question}?</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    responses[question_index] = st.slider(
                        f"השאלה מס׳ {question_index + 1}:",
                        min_value=1,
                        max_value=10,
                        value=st.session_state.current_responses.get(question_index, 5),
                        key=f"q_{question_index}",
                        label_visibility="collapsed"
                    )
                    question_index += 1
                
                # Submit button
                submitted = st.form_submit_button("🏰 לשלוח את ההערכה", type="primary", use_container_width=True)
                
                if submitted:
                    st.session_state.current_responses = responses
                    st.session_state.show_results = True
                    st.rerun()
        
        else:
            # Show results
            responses = st.session_state.current_responses
            total_questions = calculate_total_questions()
            total_score = round((sum(responses.values()) / (total_questions * 10)) * 100, 1)
            
            # Display score
            st.markdown(f"""
            <div class="score-display">
                🏆 הציון הכללי שלי: {total_score}/100 🏆
            </div>
            """, unsafe_allow_html=True)
            
            # Display general feedback
            feedback = get_feedback_message(total_score)
            if feedback:
                st.markdown(f"""
                <div class="feedback-box">
                    <p style="font-size: 1.1rem; margin: 0; text-align: center; color: #33691e; font-weight: 500;">{feedback}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Buttons - New assessment and Go to progress
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🔄 לעשות הערכה חדשה", type="secondary", use_container_width=True):
                    st.session_state.current_responses = {}
                    st.session_state.show_results = False
                    st.rerun()
            
            with col2:
                if st.button("📜 לעבור לדף ההתקדמות", type="primary", use_container_width=True, key="goto_progress"):
                    st.session_state.current_responses = {}
                    st.session_state.show_results = False
                    st.session_state.active_tab = 1  # Switch to progress tab
                    st.rerun()
    
    elif st.session_state.active_tab == 1:
        # Tab 2: Progress Tracking
        st.markdown("<h3 style='text-align: center; color: #33691e;'>הזן את הציונים שלך</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #558b2f; margin-bottom: 2rem;'>הזן ציונים מ-0 עד 100 עבור כל הערכה. הציונים יישמרו אוטומטית.</p>", unsafe_allow_html=True)
        
        # Load existing scores
        manual_scores = load_manual_scores()
        
        # Create input fields for 20 assessments
        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        
        # Create 4 columns with 5 assessments each
        cols = st.columns(4)
        
        updated_scores = {}
        
        for i in range(20):
            assessment_num = i + 1
            col_idx = i // 5  # Which column (0-3)
            
            with cols[col_idx]:
                current_value = manual_scores.get(str(assessment_num), None)
                if current_value == "":
                    current_value = None
                    
                score = st.number_input(
                    f"הערכה {assessment_num}",
                    min_value=0,
                    max_value=100,
                    value=current_value,
                    step=1,
                    key=f"manual_score_{assessment_num}",
                    help=f"ציון עבור הערכה מספר {assessment_num}"
                )
                
                updated_scores[str(assessment_num)] = score
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Save scores automatically when they change
        save_manual_scores(updated_scores)
        
        # Display statistics and charts
        valid_scores_dict = {k: v for k, v in updated_scores.items() if v is not None and v != ""}
        
        if valid_scores_dict:
            st.markdown("---")
            st.markdown("<h3 style='text-align: center; color: #33691e;'>🌲 איך אני מתקדם 🏰</h3>", unsafe_allow_html=True)
            
            # Progress chart - FIRST
            chart_data = create_simple_progress_chart(updated_scores)
            if chart_data:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<div class="chart-title">הגרף של ההתקדמות שלי</div>', unsafe_allow_html=True)
                
                # Display as line chart
                st.line_chart(chart_data, height=400)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Statistics - SECOND
            display_statistics_from_manual(updated_scores)
            
            # Recent scores table
            st.markdown("### הציונים שהזנתי")
            table_data = []
            for num, score in sorted(valid_scores_dict.items(), key=lambda x: int(x[0])):
                table_data.append({
                    'הערכה מספר': int(num),
                    'ציון': f"{score}/100"
                })
            
            if table_data:
                st.dataframe(table_data, use_container_width=True, hide_index=True)
        else:
            st.info("הזן ציונים כדי לראות את הגרף והסטטיסטיקות! 🌲")
    
    else:  # active_tab == 2
        # Tab 3: How to Progress Towards the Goal
        st.markdown('<h2 style="text-align: center; color: #33691e; margin-bottom: 2rem;">🎯 איך ניתן להתקדם אל המטרה 🌲</h2>', unsafe_allow_html=True)
        
        # Guidance container
        st.markdown('<div class="guidance-container">', unsafe_allow_html=True)
        
        # Section 1: Areas for improvement
        st.markdown("""
        <div class="guidance-section">
            <div class="guidance-title">🎯 בתחומים שבהם תרצו לשפר את הציון:</div>
            <ul class="guidance-list">
                <li>אתרו את הנושאים שיש צורך להשלים או לחזור עליהם, וצרו רשימה מסודרת</li>
                <li>קבעו פגישה פרטנית עם המורה</li>
                <li>היעזרו ב-AI לתרגול וחיזוק</li>
                <li><strong style="color: #000000; font-size: 1.4rem;">חשוב מאוד! לתרגל לתרגל לתרגל - כתבו תכניות וקוד בעצמכם! זאת הדרך היעילה ביותר להבין כמה שיותר חומר בכמה שפחות זמן</strong></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Section 2: Areas to maintain
        st.markdown("""
        <div class="guidance-section" style="background: linear-gradient(135deg, #ccfbf1 0%, #99f6e4 100%); border-right-color: #14b8a6;">
            <div class="guidance-title" style="color: #115e59;">✨ בתחומים שבהם תרצו לשמר את הציון:</div>
            <ul class="guidance-list">
                <li>קבעו חזרות קבועות על החומר</li>
                <li><strong style="color: #000000; font-size: 1.4rem;">חשוב מאוד! לתרגל לתרגל לתרגל - כתבו תכניות וקוד בעצמכם! זאת הדרך היעילה ביותר להבין כמה שיותר חומר בכמה שפחות זמן</strong></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Reminder about rest
        st.markdown("""
        <div class="reminder-box">
            💫 זכרו גם לנוח ולעשות דברים שמחזירים לכם אנרגיה! 🌲
        </div>
        """, unsafe_allow_html=True)
        
        # Action steps
        st.markdown("""
        <div class="guidance-section" style="background: linear-gradient(135deg, #fef3c7 0%, #fed7aa 100%); border-right-color: #f59e0b;">
            <div class="guidance-title" style="color: #78350f;">📋 לאחר שזיהיתם מה צריך לעשות:</div>
            <p style="font-size: 1.2rem; margin-right: 1.5rem; color: #78350f; font-weight: 500;">
                קבעו יעדים יומיים ושבועיים
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Signature
        st.markdown("""
        <div class="signature-box">
            סומך עליכם! 💪🏰<br>
            דניאל
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
