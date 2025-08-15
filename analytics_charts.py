import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import os

try:
    import openai
except ImportError:
    openai = None

def render_analytics_charts(answers):
    """
    Render analytics graphs and charts based on answers and gaps.
    Args:
        answers (dict): Should contain 'fixed' and 'open' lists as in Mongo records.
    """
    # Initialize all variables at the start
    fixed = []
    open_blocks = []
    common = []
    safety_score = 0
    pos_count = 0
    neg_count = 0
    expert_output = ""

    # Safely get data from answers
    if isinstance(answers, dict):
        fixed_temp = answers.get("fixed", [])
        if isinstance(fixed_temp, list):
            fixed = fixed_temp
        open_temp = answers.get("open", [])
        if isinstance(open_temp, list):
            open_blocks = open_temp

    st.subheader("Analytics & Visual Insights")
    # Example: Bar chart of answered vs missing
    q_labels = [q.get("question", f"Q{q.get('id','')}") for q in fixed]
    q_answers = [str(q.get("answer", "")).strip() for q in fixed]
    missing = [1 if not a or len(a) < 3 else 0 for a in q_answers]
    df_missing = pd.DataFrame({"Question": q_labels, "Missing": missing})
    st.write("### Missing Answers (Fixed Questions)")
    fig1 = px.bar(df_missing, x="Question", y="Missing", title="Missing Answers (Fixed)", labels={"Missing": "Missing (1=Yes)"})
    st.plotly_chart(fig1, use_container_width=True)

    # Pie chart of answered vs missing (open-ended)
    open_labels = [op.get("prompt", f"Open {i+1}") for i, op in enumerate(open_blocks)]
    open_answers = [str(op.get("answer", "")).strip() for op in open_blocks]
    open_missing = sum(1 if not a or len(a) < 3 else 0 for a in open_answers)
    open_answered = len(open_answers) - open_missing
    st.write("### Open-Ended Answers Completion")
    fig2 = px.pie(names=["Answered", "Missing"], values=[open_answered, open_missing], title="Open-Ended Completion")
    st.plotly_chart(fig2, use_container_width=True)

    # Example: Show gaps in follow-ups
    followup_gaps = 0
    total_followups = 0
    for op in open_blocks:
        fus = op.get("followups", [])
        total_followups += len(fus)
        followup_gaps += sum(1 for fu in fus if not fu.get("a", "").strip())
    if total_followups > 0:
        st.write("### Follow-up Answers Completion")
        fig3 = px.pie(names=["Answered", "Missing"], values=[total_followups-followup_gaps, followup_gaps], title="Follow-up Completion")
        st.plotly_chart(fig3, use_container_width=True)

    # --- AI Safety Posture Meter ---
    st.markdown("---")
    st.subheader("AI Safety Posture Meter")
    
    # Example keywords for AI safety
    safety_keywords = ["bias", "fairness", "ethics", "content", "monitor", "red-team", "risk", "compliance", "security", "privacy"]
    all_text = " ".join([str(q.get("answer", "")) for q in fixed] + [str(op.get("answer", "")) for op in open_blocks]).lower()
    safety_hits = sum(1 for kw in safety_keywords if kw in all_text)
    safety_score = min(1 + safety_hits * 3, 20)
    st.progress(safety_score / 20, text=f"AI Safety Posture: {safety_score}/20")
    if safety_score < 10:
        st.warning("AI Safety posture is below recommended threshold. Consider addressing more safety, risk, and compliance topics.")
    else:
        st.success("AI Safety posture is satisfactory.")

    # --- Mini Red-Team Prompts ---
    #st.markdown("---")
    #st.subheader("Mini Red-Team Prompts")
    #red_team_prompts = [
    #    "How could this system be misused or abused?",
    #    "What is the worst-case scenario if the AI fails?",
    #    "Are there any hidden biases in the data or process?",
    #    "How would you detect and respond to adversarial attacks?",
    #    "What safeguards are in place for privacy and security?"
    #]
    #for i, prompt in enumerate(red_team_prompts, 1):
    #    st.text_area(f"Red-Team Q{i}", value=prompt, key=f"red_team_prompt_{i}")

    # --- Spider Web Chart (Radar) ---
    st.markdown("---")
    st.subheader("AI Maturity Spider Web Chart")
    pillar_names = [
        "Business & Strategic Alignment",
        "Scope & Use Cases",
        "Technology & Integration",
        "Risk, Governance & Operations",
        "Infrastructure, AI Readiness & Security",
        "Model & Platform",
        "Validation & Testing"
    ]
    
    # Try to get pillar scores from answers if present
    pillar_scores = None
    if isinstance(answers, dict) and "pillar_scores" in answers:
        pillar_scores = answers["pillar_scores"]
    else:
        # Try to infer from text (simple keyword scan)
        seeds = {
            "Business & Strategic Alignment": ["kpi","csat","nps","journey","omni","target","conversion"],
            "Scope & Use Cases": ["intent","journey","transfer","transaction","multilingual","language"],
            "Technology & Integration": ["api","middleware","sso","otp","biometric","whatsapp","ivr"],
            "Risk, Governance & Operations": ["handoff","sla","monitor","feedback","bias","fairness","ethics","content"],
            "Infrastructure, AI Readiness & Security": ["gpu","h100","a100","mlops","databricks","sagemaker","vertex","gateway","apigee","kong","mulesoft","prometheus","grafana","elastic","dr","ha","sandbox"],
            "Model & Platform": ["openai","azure","anthropic","cohere","dbrx","llama","embedding","fine-tune"],
            "Validation & Testing": ["eval","dataset","metrics","red-team","test","qa","sign-off","sandbox"]
        }
        pillar_scores = []
        for name, kws in seeds.items():
            hits = sum(1 for kw in kws if kw in all_text)
            score = min(1 + hits*2, 20)
            pillar_scores.append(score)

    radar_df = pd.DataFrame({"Pillar": pillar_names, "Score": pillar_scores})
    fig_radar = px.line_polar(radar_df, r="Score", theta="Pillar", line_close=True, title="AI Maturity Spider Web Chart", range_r=[0,20])
    st.plotly_chart(fig_radar, use_container_width=True)
    st.info("This chart visualizes the AI maturity posture across key pillars. Scores are based on keyword analysis of answers.")

    # --- Wow Analytics Section ---
    st.markdown("---")
    st.subheader("✨ Wow Analytics")
    # Example: Highlight most positive/negative answers, longest answer, most frequent keywords
    all_answers = [str(q.get("answer", "")) for q in fixed] + [str(op.get("answer", "")) for op in open_blocks]
    longest = max(all_answers, key=lambda x: len(x), default="")
    shortest = min([a for a in all_answers if a.strip()], key=lambda x: len(x), default="")
    st.write(f"**Longest Answer:** {longest if longest else 'N/A'}")
    st.write(f"**Shortest Answer:** {shortest if shortest else 'N/A'}")

    # Most frequent keywords
    words = [w for a in all_answers for w in str(a).lower().split() if len(w) > 3]
    common = Counter(words).most_common(5)
    st.write("**Top 5 Keywords:**", ", ".join([f"{w} ({c})" for w, c in common]) if common else "N/A")

    # Sentiment analysis (simple)
    pos_words = ["success","growth","positive","improve","efficient","secure","compliant"]
    neg_words = ["risk","fail","blocker","issue","problem","bias","concern"]
    pos_count = sum(1 for w in words if w in pos_words)
    neg_count = sum(1 for w in words if w in neg_words)
    st.write(f"**Positive Sentiment Hits:** {pos_count}")
    st.write(f"**Negative Sentiment Hits:** {neg_count}")
    st.info("These analytics highlight interesting patterns and outliers in the survey responses.")

    # --- Executive Summary Section ---
    st.markdown("---")
    st.subheader("Executive Summary")
    summary = f"""
    This survey analysis provides a comprehensive overview of the organization's conversational banking maturity, AI safety posture, and key gaps. 
    
    Key Findings:
    - AI Safety Score: {safety_score}/20
    - Positive Indicators: {pos_count}
    - Risk Indicators: {neg_count}
    - Most Common Topics: {', '.join([w for w, _ in common[:3]]) if common else 'N/A'}
    
    For detailed recommendations, refer to the Insights and Next Steps section.
    """
    st.write(summary)

    # --- Expert AI Consolidated Analysis Section ---
    st.markdown("---")
    st.subheader("🤖 Expert AI Consolidated Analysis")
    try:
        import openai
    except ImportError:
        openai = None
        
    def get_expert_analysis(questions, answers, analytics_summary):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or openai is None:
            st.error("OpenAI API key not found or openai package missing.")
            return ""
        client = openai.OpenAI(api_key=api_key)
        prompt = f"""
You are an AI agent with the DNA of a top Business Requirements Expert and Technical Architect (think Google-level). Given the following survey questions, answers, and analytics, provide a consolidated analysis, requirements summary, and actionable recommendations for building a Conversational Banking Chatbot.

Questions:
{questions}

Answers:
{answers}

Analytics Summary:
{analytics_summary}

Your response should be structured, insightful, and cover both business and technical perspectives.
"""
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            st.error(f"Error calling OpenAI API: {str(e)}")
            return ""

    # Prepare data for expert analysis
    questions_list = [q.get("question", f"Q{q.get('id','')}") for q in fixed]
    answers_list = [str(q.get("answer", "")) for q in fixed]
    open_questions = [op.get("prompt", f"Open {i+1}") for i, op in enumerate(open_blocks)]
    open_answers = [str(op.get("answer", "")) for op in open_blocks]
    analytics_summary = f"Safety Score: {safety_score}/20, Top Keywords: {', '.join([w for w, c in common])}, Positive Sentiment: {pos_count}, Negative Sentiment: {neg_count}"
    all_questions = questions_list + open_questions
    all_answers = answers_list + open_answers

    expert_output = ""
    if st.button("Get Expert AI Analysis", key="get_expert_analysis"):
        if not openai:
            st.error("OpenAI package is not installed. Please install it first.")
            return
        with st.spinner("Generating expert analysis..."):
            try:
                client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                expert_prompt = f"""Analyze these survey responses and provide insights:\nQuestions: {questions_list}\nAnswers: {answers_list}\nOpen Questions: {open_questions}\nOpen Answers: {open_answers}"""
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": expert_prompt}],
                    max_tokens=1000
                )
                expert_output = response.choices[0].message.content
                st.write(f"[DEBUG] OpenAI raw response: {repr(response)}")
                if not expert_output or len(expert_output) < 10:
                    st.error("OpenAI did not return a valid expert analysis. Please try again or check your API usage.")
                    st.write(f"[DEBUG] OpenAI response: {repr(expert_output)}")
                    return
                st.session_state['expert_output'] = expert_output
                st.markdown("### Expert AI Analysis")
                st.write(expert_output)
            except Exception as e:
                st.error(f"Error generating expert analysis: {str(e)}")
                st.write(f"[DEBUG] Exception: {repr(e)}")

    # Functional Specification Button
    st.markdown("---")
    st.subheader("Generate Functional Specification")
    if st.button("Create Functional Specification", key="create_func_spec"):
        if not openai:
            st.error("OpenAI package is not installed. Please install it first.")
            return
        stored_expert_output = st.session_state.get('expert_output', '')
        if not stored_expert_output or not isinstance(stored_expert_output, str) or len(stored_expert_output.strip()) < 10:
            st.warning("Please generate Expert AI Analysis first! (No valid expert output found)")
            st.write(f"[DEBUG] expert_output: {repr(stored_expert_output)}")
            return
        with st.spinner("Generating functional specification..."):
            try:
                client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                func_spec_prompt = f"""As a senior Business and Technical Analyst, create a comprehensive Functional Specification for a Conversational Banking application based on this analysis:\n\nExpert Analysis:\n{stored_expert_output}\n\nSurvey Data:\nQuestions: {questions_list}\nAnswers: {answers_list}\nOpen Questions: {open_questions}\nOpen Answers: {open_answers}\n\nInclude detailed sections for:\n1. System Overview\n2. User Requirements\n3. Functional Requirements\n4. Technical Architecture\n5. Security & Compliance\n6. Performance Requirements\n7. User Interface\n8. Testing Requirements\n9. Implementation Plan\n10. Success Metrics"""
                func_spec = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a senior Business and Technical Analyst at a top-tier technology consulting firm, specializing in AI and Banking solutions."},
                        {"role": "user", "content": func_spec_prompt}
                    ],
                    max_tokens=3000,
                    temperature=0.2
                )
                spec_output = func_spec.choices[0].message.content.strip()
                st.write(f"[DEBUG] OpenAI raw response: {repr(func_spec)}")
                if not spec_output or len(spec_output) < 20:
                    st.error("OpenAI did not return a valid functional specification. Please try again or check your API usage.")
                    st.write(f"[DEBUG] OpenAI response: {repr(spec_output)}")
                    return
                st.markdown("### 📋 Functional Specification")
                st.markdown(spec_output)
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                spec_filename = f"Functional_Spec_{timestamp}.md"
                st.download_button(
                    label="Download Functional Spec",
                    data=spec_output,
                    file_name=spec_filename,
                    mime="text/markdown"
                )
            except Exception as e:
                st.error(f"Error generating functional specification: {str(e)}")
                st.write(f"[DEBUG] Exception: {repr(e)}")
