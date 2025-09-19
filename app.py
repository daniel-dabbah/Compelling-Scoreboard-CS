import streamlit as st
from datetime import datetime, date
import json

# Configure page
st.set_page_config(
    page_title="הערכה פנימית - לוח תוצאות",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling with RTL support, pleasant colors, and background
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;700&display=swap');
    
    * {
        font-family: 'Heebo', sans-serif;
    }
    
    .main .block-container {
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 50%, #e2e8f0 100%);
        min-height: 100vh;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f0f4f8 0%, #d6e8f5 50%, #c8d8e4 100%);
    }
    
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        text-align: center;
        color: #2D3748;
        margin-bottom: 2.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .question-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 2rem;
        border-radius: 18px;
        margin: 1.8rem 0;
        border-right: 6px solid #4299e1;
        box-shadow: 0 6px 20px rgba(66, 153, 225, 0.15);
        direction: rtl;
        text-align: right;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .question-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(66, 153, 225, 0.2);
    }
    
    .question-container h4 {
        color: #2D3748;
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
        background: linear-gradient(135deg, #4299e1 0%, #667eea 50%, #764ba2 100%);
        color: white;
        border-radius: 25px;
        margin: 2.5rem 0;
        box-shadow: 0 10px 30px rgba(66, 153, 225, 0.4);
        direction: ltr;
    }
    
    .feedback-box {
        background: linear-gradient(135deg, #e6fffa 0%, #b2f5ea 100%);
        padding: 2.2rem;
        border-radius: 18px;
        margin: 1.8rem 0;
        border: 2px solid #4fd1c7;
        box-shadow: 0 6px 20px rgba(79, 209, 199, 0.15);
        direction: rtl;
        text-align: center;
    }
    
    .improvement-box {
        background: linear-gradient(135deg, #f0fff4 0%, #c6f6d5 100%);
        padding: 2.2rem;
        border-radius: 18px;
        margin: 1.8rem 0;
        border: 2px solid #68d391;
        box-shadow: 0 6px 20px rgba(104, 211, 145, 0.15);
        direction: rtl;
        text-align: center;
    }
    
    .progress-stats {
        background: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%);
        padding: 2rem;
        border-radius: 18px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        margin: 1.2rem 0;
        border-top: 4px solid #4299e1;
        text-align: center;
        transition: transform 0.2s ease;
    }
    
    .progress-stats:hover {
        transform: translateY(-3px);
    }
    
    .chart-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 2rem;
        border-radius: 18px;
        margin: 2rem 0;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
    }
    
    .chart-title {
        text-align: center;
        font-size: 1.5rem;
        font-weight: 600;
        color: #2D3748;
        margin-bottom: 1.5rem;
    }
    
    .input-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 2rem;
        border-radius: 18px;
        margin: 1.8rem 0;
        border: 2px solid #e2e8f0;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    }
    
    .guidance-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 2.5rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
        direction: rtl;
        text-align: right;
        border-right: 5px solid #667eea;
    }
    
    .guidance-section {
        margin: 2rem 0;
        padding: 1.5rem;
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border-radius: 15px;
        border-right: 4px solid #4ade80;
    }
    
    .guidance-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #166534;
        margin-bottom: 1rem;
    }
    
    .guidance-list {
        margin-right: 1.5rem;
        line-height: 2;
        color: #2D3748;
    }
    
    .guidance-list li {
        margin: 0.8rem 0;
        font-size: 1.1rem;
    }
    
    .reminder-box {
        background: linear-gradient(135deg, #fce7f3 0%, #fbcfe8 100%);
        padding: 1.8rem;
        border-radius: 15px;
        margin: 2rem 0;
        border: 2px solid #ec4899;
        text-align: center;
        direction: rtl;
        font-size: 1.2rem;
        color: #831843;
        font-weight: 500;
    }
    
    .signature-box {
        text-align: center;
        margin-top: 3rem;
        padding: 1.5rem;
        background: linear-gradient(135deg, #f3e8ff 0%, #e9d5ff 100%);
        border-radius: 15px;
        font-size: 1.3rem;
        color: #6b21a8;
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
        background: rgba(255, 255, 255, 0.3);
        padding: 0.5rem;
        border-radius: 15px;
        justify-content: center;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
        border-radius: 12px;
        padding: 1rem 2rem;
        border: 2px solid transparent;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4299e1 0%, #667eea 100%);
        color: white;
        border-color: #4299e1;
        box-shadow: 0 4px 15px rgba(66, 153, 225, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Programming topics for assessment
PROGRAMMING_TOPICS = [
    "משתנים - טיפוס המשתנה (int, double)",
    "משתנים - הבדלים בין הטיפוסים השונים",
    "משתנים - הצהרה על משתנים",
    "משתנים - הבדלים בין הצהרה לאתחול",
    "כתיבת הוראות קלט",
    "כתיבת הוראות פלט",
    "השמת ערכים למשתנים",
    "המרה בין טיפוסים",
    "חילוק בין שלמים וקבלת מספר ממשי",
    "חלוקה בשארית"
]

# Additional questions - you can modify these as needed
ADDITIONAL_QUESTIONS = [
    "עד כמה אני מרגיש שאני מסוגל לפתור תרגילים בנושאים האלה בעצמי",
    "עד כמה אני מרגיש שאני יכול להסביר את הנושאים האלה לחברים"
]

def get_feedback_message(score):
    """Generate short feedback based on the total score"""
    if score >= 90:
        return "מצוין! אתה שולט בחומר!"
    elif score >= 80:
        return "עבודה טובה! המשך להתאמן!"
    elif score >= 70:
        return "יפה, יש התקדמות! המשך לתרגל!"
    else:
        return "כדאי לחזור על החומר ולתרגל עוד!"

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
            <h3 style="color: #2D3748; margin: 0;">הציון האחרון שלי</h3>
            <h2 style="color: #4299e1; margin: 5px 0;">{}/100</h2>
        </div>
        """.format(current_score), unsafe_allow_html=True)
    
    with col2:
        best_score = max(valid_scores) if valid_scores else 0
        st.markdown("""
        <div class="progress-stats">
            <h3 style="color: #2D3748; margin: 0;">הציון הכי טוב שלי</h3>
            <h2 style="color: #68d391; margin: 5px 0;">{}/100</h2>
        </div>
        """.format(best_score), unsafe_allow_html=True)
    
    with col3:
        total_assessments = len(valid_scores)
        st.markdown("""
        <div class="progress-stats">
            <h3 style="color: #2D3748; margin: 0;">כמה הערכות הזנתי</h3>
            <h2 style="color: #9f7aea; margin: 5px 0;">{}</h2>
        </div>
        """.format(total_assessments), unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">הערכה פנימית - נושאי תכנות</h1>', unsafe_allow_html=True)
    
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
        if st.button("הערכה חדשה", 
                    type="primary" if st.session_state.active_tab == 0 else "secondary",
                    use_container_width=True,
                    key="tab_assessment"):
            st.session_state.active_tab = 0
    
    with col2:
        if st.button("להסתכל על ההתקדמות שלי", 
                    type="primary" if st.session_state.active_tab == 1 else "secondary",
                    use_container_width=True,
                    key="tab_progress"):
            st.session_state.active_tab = 1
    
    with col3:
        if st.button("איך ניתן להתקדם אל המטרה", 
                    type="primary" if st.session_state.active_tab == 2 else "secondary",
                    use_container_width=True,
                    key="tab_guidance"):
            st.session_state.active_tab = 2
    
    st.markdown("---")
    
    # Display content based on active tab
    if st.session_state.active_tab == 0:
        # Tab 1: New Assessment
        if not st.session_state.show_results:
            st.markdown("<div style='text-align: center; margin-bottom: 2rem;'><p style='font-size: 1.1rem; color: #2D3748;'>תן לכל נושא ציון מ-1 (בכלל לא בטוח) עד 10 (מאוד בטוח) - לפי איך שאתה מרגיש ממש עכשיו.</p></div>", unsafe_allow_html=True)
            
            # Display all questions at once
            with st.form("assessment_form"):
                responses = {}
                question_index = 0
                
                # Programming topic questions
                for i, topic in enumerate(PROGRAMMING_TOPICS):
                    st.markdown(f"""
                    <div class="question-container">
                        <h4>עד כמה אני מרגיש בנוח עם הנושא: {topic}?</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    responses[question_index] = st.slider(
                        f"הציון שלי עבור {topic}:",
                        min_value=1,
                        max_value=10,
                        value=st.session_state.current_responses.get(question_index, 5),
                        key=f"q_{question_index}",
                        label_visibility="collapsed"
                    )
                    question_index += 1
                
                # Additional questions
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
                submitted = st.form_submit_button("לשלוח את ההערכה", type="primary", use_container_width=True)
                
                if submitted:
                    st.session_state.current_responses = responses
                    st.session_state.show_results = True
                    st.rerun()
        
        else:
            # Show results
            responses = st.session_state.current_responses
            total_score = round((sum(responses.values()) / ((len(PROGRAMMING_TOPICS) + len(ADDITIONAL_QUESTIONS)) * 10)) * 100, 1)
            
            # Display score
            st.markdown(f"""
            <div class="score-display">
                הציון הכללי שלי: {total_score}/100
            </div>
            """, unsafe_allow_html=True)
            
            # Display general feedback
            feedback = get_feedback_message(total_score)
            if feedback:
                st.markdown(f"""
                <div class="feedback-box">
                    <p style="font-size: 1.1rem; margin: 0; text-align: center; color: #2D3748; font-weight: 500;">{feedback}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Show areas that need improvement (scores <= 5)
            weak_areas = []
            for idx, score in responses.items():
                if score <= 5:
                    if idx < len(PROGRAMMING_TOPICS):
                        weak_areas.append(PROGRAMMING_TOPICS[idx])
                    else:
                        weak_areas.append(ADDITIONAL_QUESTIONS[idx - len(PROGRAMMING_TOPICS)])
            
            if weak_areas:
                st.markdown("""
                <div class="improvement-box">
                    <p style="font-size: 1.2rem; margin: 0; text-align: center; color: #166534; font-weight: 600;">נושאים שכדאי לחזק:</p>
                """, unsafe_allow_html=True)
                for area in weak_areas:
                    st.markdown(f"<p style='text-align: center; margin: 5px 0;'>• {area}</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Buttons - New assessment and Go to progress
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("לעשות הערכה חדשה", type="secondary", use_container_width=True):
                    st.session_state.current_responses = {}
                    st.session_state.show_results = False
                    st.rerun()
            
            with col2:
                if st.button("לעבור לדף ההתקדמות", type="primary", use_container_width=True, key="goto_progress"):
                    st.session_state.current_responses = {}
                    st.session_state.show_results = False
                    st.session_state.active_tab = 1  # Switch to progress tab
                    st.rerun()
    
    elif st.session_state.active_tab == 1:
        # Tab 2: Progress Tracking
        st.markdown("<h3 style='text-align: center;'>הזן את הציונים שלך</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #666; margin-bottom: 2rem;'>הזן ציונים מ-0 עד 100 עבור כל הערכה. הציונים יישמרו אוטומטית.</p>", unsafe_allow_html=True)
        
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
            st.markdown("<h3 style='text-align: center;'>איך אני מתקדם</h3>", unsafe_allow_html=True)
            
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
            st.info("הזן ציונים כדי לראות את הגרף והסטטיסטיקות!")
    
    else:  # active_tab == 2
        # Tab 3: How to Progress Towards the Goal - Updated for Programming
        st.markdown('<h2 style="text-align: center; color: #553c9a; margin-bottom: 2rem;">איך ניתן להתקדם אל המטרה בתכנות</h2>', unsafe_allow_html=True)
        
        # Guidance container
        st.markdown('<div class="guidance-container">', unsafe_allow_html=True)
        
        # Section 1: Areas for improvement in programming
        st.markdown("""
        <div class="guidance-section">
            <div class="guidance-title">🎯 בנושאים שבהם תרצו לשפר את הציון:</div>
            <ul class="guidance-list">
                <li>תרגלו כתיבת קוד - התחילו מתרגילים פשוטים והתקדמו בהדרגה</li>
                <li>כתבו תוכניות קטנות משלכם כדי להבין את הנושא לעומק</li>
                <li>צפו בסרטוני הסבר או קראו דוגמאות קוד באינטרנט</li>
                <li>בקשו עזרה מהמורה או מחברים שמבינים את הנושא</li>
                <li>השתמשו ב-AI כדי לקבל הסברים נוספים ותרגילים</li>
                <li>נסו לפתור בעיות מהחיים האמיתיים עם הכלים שלמדתם</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Section 2: Areas to maintain in programming
        st.markdown("""
        <div class="guidance-section" style="background: linear-gradient(135deg, #ede9fe 0%, #ddd6fe 100%); border-right-color: #a78bfa;">
            <div class="guidance-title" style="color: #5b21b6;">✨ בנושאים שבהם אתם כבר חזקים:</div>
            <ul class="guidance-list">
                <li>המשיכו לתרגל באופן קבוע כדי לא לשכוח</li>
                <li>נסו לפתור תרגילים מתקדמים יותר</li>
                <li>עזרו לחברים שמתקשים - זה יחזק את ההבנה שלכם</li>
                <li>חפשו אתגרי תכנות באינטרנט כדי להמשיך להתפתח</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Programming specific tips
        st.markdown("""
        <div class="guidance-section" style="background: linear-gradient(135deg, #fef3c7 0%, #fed7aa 100%); border-right-color: #fb923c;">
            <div class="guidance-title" style="color: #9a3412;">💻 טיפים ספציפיים לתכנות:</div>
            <ul class="guidance-list">
                <li><strong>משתנים:</strong> תרגלו הגדרת משתנים מסוגים שונים וראו איך הם מתנהגים</li>
                <li><strong>קלט/פלט:</strong> כתבו תוכניות שמתקשרות עם המשתמש</li>
                <li><strong
