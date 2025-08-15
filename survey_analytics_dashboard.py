import streamlit as st
import pandas as pd
from datetime import datetime
import re
from collections import Counter
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import time
import random
import math

def render_survey_analytics_dashboard(fixed_answers, section2_questions, section2_answers, org_name="", contact="", role="", username=""):
    """
    Display a mega-spectacular analytics dashboard with 8 different visualization experiences
    """
    
    # Custom CSS for animations and styling
    st.markdown("""
    <style>
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { box-shadow: 0 8px 32px rgba(102,126,234,0.3); }
        to { box-shadow: 0 8px 32px rgba(102,126,234,0.8); }
    }
    
    .big-metric {
        font-size: 3em;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .dashboard-header {
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #feca57);
        background-size: 300% 300%;
        animation: gradient 3s ease infinite;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .wow-card {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 20px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .viz-selector {
        background: linear-gradient(45deg, #1e3c72, #2a5298);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Spectacular Header
    st.markdown("""
    <div class="dashboard-header">
        <h1>🚀 MEGA ANALYTICS COMMAND CENTER 🚀</h1>
        <h2>8 Spectacular Visualization Experiences</h2>
        <p>Choose Your Data Adventure • Powered by Advanced AI Analytics Engine</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Prepare comprehensive data analysis
    all_text_data = []
    question_data = []
    
    # Collect all text and metadata
    for answer_data in fixed_answers:
        answer = answer_data.get('answer', '')
        question_data.append({
            'type': answer_data.get('type', 'text'),
            'question': answer_data.get('question', ''),
            'answer': answer,
            'pillar': answer_data.get('pillar', 'General'),
            'category': answer_data.get('category', 'Standard')
        })
        
        if isinstance(answer, list):
            all_text_data.extend([str(item) for item in answer])
        else:
            all_text_data.append(str(answer))
    
    # Add section 2 data
    for i, (question, answer) in enumerate(zip(section2_questions, section2_answers)):
        if answer and answer.strip():
            question_data.append({
                'type': 'open-ended',
                'question': question,
                'answer': answer,
                'pillar': 'Strategic',
                'category': 'Deep-Dive'
            })
            all_text_data.append(str(answer))
    
    combined_text = ' '.join(all_text_data).lower()
    words = re.findall(r'\b\w+\b', combined_text)
    
    # ===== VISUALIZATION SELECTOR =====
    st.markdown("""
    <div class="viz-selector">
        <h2 style="color: white; text-align: center;">🎭 CHOOSE YOUR SPECTACULAR VISUALIZATION EXPERIENCE</h2>
        <p style="color: white; text-align: center;">Each option transforms your data into a unique, mind-blowing experience</p>
    </div>
    """, unsafe_allow_html=True)
    
    viz_options = [
        "🧬 Knowledge DNA Double Helix (3D Molecular)",
        "🌟 Standard Dashboard (Current 5 Features)",
        "🌌 Knowledge Galaxy Explorer (3D Universe)",
        "🧠 Neural Network Brain (3D Synaptic)",
        "🚀 Space Station Command Center (Sci-Fi)",
        "🏗️ Knowledge Architecture Builder (3D City)",
        "🌊 Knowledge Ocean Depths (Underwater)",
        "🌋 Knowledge Volcano Cross-Section (Geological)",
        "🎭 Knowledge Theater Stage (Performance)",
        "🏰 Knowledge Castle Fortress (Medieval)"
    ]
    
    selected_viz = st.selectbox(
        "Select Your Visualization Adventure:",
        viz_options,
        index=0  # Default to DNA Double Helix
    )
    
    # Show preview description
    viz_descriptions = {
        "🧬 Knowledge DNA Double Helix (3D Molecular)": "Visualize your knowledge as a 3D DNA double helix showing the genetic code of your business and technical expertise intertwined in spectacular molecular detail.",
        "🌟 Standard Dashboard (Current 5 Features)": "The original spectacular dashboard with Neural Language Analysis, Response Intelligence Matrix, Strategic Pillar Constellation, Knowledge DNA Double Helix, and Achievement System.",
        "🌌 Knowledge Galaxy Explorer (3D Universe)": "Transform your responses into a 3D galaxy where each answer becomes a star system with orbiting planets. Fly through space and explore your knowledge universe!",
        "🧠 Neural Network Brain (3D Synaptic)": "Visualize your knowledge as a 3D brain with neural pathways, synaptic connections, and electrical firing patterns. Watch your thoughts come alive!",
        "🚀 Space Station Command Center (Sci-Fi)": "Experience a futuristic mission control center with holographic displays, satellite views, and real-time data streams in a sci-fi environment.",
        "🏗️ Knowledge Architecture Builder (3D City)": "Build a futuristic 3D city where your responses construct skyscrapers, districts, and infrastructure representing your organizational knowledge.",
        "🌊 Knowledge Ocean Depths (Underwater)": "Dive into an underwater ecosystem where your knowledge forms coral reefs, fish schools, and bioluminescent creatures in the deep sea.",
        "🌋 Knowledge Volcano Cross-Section (Geological)": "Explore your knowledge as geological layers in a 3D volcano cross-section with magma cores, rock strata, and crystal formations.",
        "🎭 Knowledge Theater Stage (Performance)": "Watch your data perform on a 3D theatrical stage with dramatic lighting, actors, and scene changes representing different aspects of your responses.",
        "🏰 Knowledge Castle Fortress (Medieval)": "Build a medieval castle where your knowledge areas become towers, walls, and defensive structures in a fantasy fortress setting."
    }
    
    st.info(f"**{selected_viz}**: {viz_descriptions[selected_viz]}")
    
    # Render selected visualization
    if selected_viz == "🧬 Knowledge DNA Double Helix (3D Molecular)":
        render_dna_double_helix(question_data, words, combined_text)
    elif selected_viz == "🌟 Standard Dashboard (Current 5 Features)":
        render_standard_dashboard(question_data, all_text_data, words, combined_text, fixed_answers, section2_answers, org_name, contact, role, username)
    elif selected_viz == "🌌 Knowledge Galaxy Explorer (3D Universe)":
        render_galaxy_explorer(question_data, words, combined_text)
    elif selected_viz == "🧠 Neural Network Brain (3D Synaptic)":
        render_neural_brain(question_data, words, combined_text)
    elif selected_viz == "🚀 Space Station Command Center (Sci-Fi)":
        render_space_station(question_data, words, combined_text)
    elif selected_viz == "🏗️ Knowledge Architecture Builder (3D City)":
        render_architecture_builder(question_data, words, combined_text)
    elif selected_viz == "🌊 Knowledge Ocean Depths (Underwater)":
        render_ocean_depths(question_data, words, combined_text)
    elif selected_viz == "🌋 Knowledge Volcano Cross-Section (Geological)":
        render_volcano_section(question_data, words, combined_text)
    elif selected_viz == "🎭 Knowledge Theater Stage (Performance)":
        render_theater_stage(question_data, words, combined_text)
    elif selected_viz == "🏰 Knowledge Castle Fortress (Medieval)":
        render_castle_fortress(question_data, words, combined_text)

def render_dna_double_helix(question_data, words, combined_text):
    """🧬 Knowledge DNA Double Helix - 3D Molecular Visualization"""
    
    st.markdown("## 🧬 KNOWLEDGE DNA DOUBLE HELIX")
    st.markdown("*The genetic code of your organizational expertise*")
    
    # Enhanced data analysis including all Q&A and functional specifications
    business_terms = ['strategy', 'customer', 'business', 'process', 'system', 'technology', 'digital', 'innovation', 'experience', 'solution', 'service', 'value', 'market', 'competitive', 'growth']
    tech_terms = ['api', 'integration', 'platform', 'cloud', 'data', 'analytics', 'ai', 'automation', 'security', 'infrastructure', 'database', 'software', 'application', 'interface', 'architecture']
    
    # Enhanced analysis including functional specifications
    functional_terms = ['requirement', 'specification', 'function', 'feature', 'capability', 'performance', 'scalability', 'reliability', 'availability', 'usability']
    
    business_score = sum(1 for word in words if word in business_terms)
    tech_score = sum(1 for word in words if word in tech_terms)
    functional_score = sum(1 for word in words if word in functional_terms)
    
    # Create enhanced double helix visualization
    fig = go.Figure()
    
    # Generate helix parameters
    t = np.linspace(0, 6*np.pi, 200)  # More points for smoother helix
    
    # Business strand (Blue)
    x1 = np.cos(t) * (1 + business_score * 0.1)
    y1 = np.sin(t) * (1 + business_score * 0.1)
    z1 = t * 0.5
    
    # Technical strand (Red) - offset by π
    x2 = np.cos(t + np.pi) * (1 + tech_score * 0.1)
    y2 = np.sin(t + np.pi) * (1 + tech_score * 0.1)
    z2 = t * 0.5
    
    # Functional strand (Green) - third helix for functional specs
    x3 = np.cos(t + 2*np.pi/3) * (0.5 + functional_score * 0.1)
    y3 = np.sin(t + 2*np.pi/3) * (0.5 + functional_score * 0.1)
    z3 = t * 0.5
    
    # Add business knowledge strand
    fig.add_trace(go.Scatter3d(
        x=x1, y=y1, z=z1,
        mode='lines+markers',
        line=dict(color='blue', width=8),
        marker=dict(size=4, color='blue', opacity=0.8),
        name=f'Business Knowledge ({business_score})',
        hovertemplate=f"<b>Business Strand</b><br>Knowledge Score: {business_score}<br>Detected Terms: {business_score}<extra></extra>"
    ))
    
    # Add technical knowledge strand
    fig.add_trace(go.Scatter3d(
        x=x2, y=y2, z=z2,
        mode='lines+markers',
        line=dict(color='red', width=8),
        marker=dict(size=4, color='red', opacity=0.8),
        name=f'Technical Knowledge ({tech_score})',
        hovertemplate=f"<b>Technical Strand</b><br>Knowledge Score: {tech_score}<br>Detected Terms: {tech_score}<extra></extra>"
    ))
    
    # Add functional specification strand
    fig.add_trace(go.Scatter3d(
        x=x3, y=y3, z=z3,
        mode='lines+markers',
        line=dict(color='green', width=6),
        marker=dict(size=3, color='green', opacity=0.8),
        name=f'Functional Specs ({functional_score})',
        hovertemplate=f"<b>Functional Strand</b><br>Specification Score: {functional_score}<br>Detected Terms: {functional_score}<extra></extra>"
    ))
    
    # Add connecting base pairs between strands
    connection_points = range(0, len(t), 20)  # Every 20th point
    for i in connection_points:
        # Business-Technical connections
        fig.add_trace(go.Scatter3d(
            x=[x1[i], x2[i]], y=[y1[i], y2[i]], z=[z1[i], z2[i]],
            mode='lines',
            line=dict(color='rgba(255,255,255,0.3)', width=2),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # Technical-Functional connections
        if i < len(x3):
            fig.add_trace(go.Scatter3d(
                x=[x2[i], x3[i]], y=[y2[i], y3[i]], z=[z2[i], z3[i]],
                mode='lines',
                line=dict(color='rgba(255,255,255,0.2)', width=1),
                showlegend=False,
                hoverinfo='skip'
            ))
    
    # Add knowledge markers for key responses
    for i, item in enumerate(question_data[:10]):  # Limit to 10 for performance
        # Position marker along the helix
        marker_t = (i / 10) * 6 * np.pi
        marker_x = np.cos(marker_t) * 1.5
        marker_y = np.sin(marker_t) * 1.5
        marker_z = marker_t * 0.5
        
        # Determine marker color based on response type
        if any(term in str(item['answer']).lower() for term in business_terms):
            marker_color = 'blue'
            marker_type = 'Business'
        elif any(term in str(item['answer']).lower() for term in tech_terms):
            marker_color = 'red'
            marker_type = 'Technical'
        elif any(term in str(item['answer']).lower() for term in functional_terms):
            marker_color = 'green'
            marker_type = 'Functional'
        else:
            marker_color = 'purple'
            marker_type = 'General'
        
        fig.add_trace(go.Scatter3d(
            x=[marker_x], y=[marker_y], z=[marker_z],
            mode='markers+text',
            marker=dict(
                size=12,
                color=marker_color,
                opacity=0.9,
                symbol='diamond',
                line=dict(width=2, color='white')
            ),
            text=f"Q{i+1}",
            textposition="middle center",
            textfont=dict(size=10, color='white'),
            name=f"Response {i+1}",
            hovertemplate=f"<b>Response {i+1}</b><br>Type: {marker_type}<br>Length: {len(str(item['answer']))}<br>Category: {item.get('pillar', 'General')}<extra></extra>"
        ))
    
    # Style the DNA helix
    fig.update_layout(
        title="🧬 YOUR KNOWLEDGE DNA - Triple Helix Molecular Structure",
        scene=dict(
            bgcolor='rgba(0,0,0,0.9)',
            xaxis=dict(showgrid=True, gridcolor='rgba(100,100,100,0.2)', showbackground=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(100,100,100,0.2)', showbackground=False),
            zaxis=dict(showgrid=True, gridcolor='rgba(100,100,100,0.2)', showbackground=False),
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=700,
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Enhanced DNA analysis metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(45deg, #1e3c72, #2a5298); padding: 15px; border-radius: 10px; text-align: center; color: white;">
            <div style="font-size: 2em;">🧬</div>
            <div style="font-size: 1.5em; font-weight: bold;">{business_score}</div>
            <div>BUSINESS GENES</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(45deg, #c31432, #240b36); padding: 15px; border-radius: 10px; text-align: center; color: white;">
            <div style="font-size: 2em;">⚙️</div>
            <div style="font-size: 1.5em; font-weight: bold;">{tech_score}</div>
            <div>TECHNICAL GENES</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background: linear-gradient(45deg, #11998e, #38ef7d); padding: 15px; border-radius: 10px; text-align: center; color: white;">
            <div style="font-size: 2em;">📋</div>
            <div style="font-size: 1.5em; font-weight: bold;">{functional_score}</div>
            <div>FUNCTIONAL GENES</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        total_complexity = business_score + tech_score + functional_score
        complexity_level = "EXPERT" if total_complexity > 15 else "ADVANCED" if total_complexity > 8 else "DEVELOPING"
        st.markdown(f"""
        <div style="background: linear-gradient(45deg, #667eea, #764ba2); padding: 15px; border-radius: 10px; text-align: center; color: white;">
            <div style="font-size: 2em;">🎯</div>
            <div style="font-size: 1.5em; font-weight: bold;">{complexity_level}</div>
            <div>DNA COMPLEXITY</div>
        </div>
        """, unsafe_allow_html=True)
    
    # DNA Interpretation Guide
    st.markdown("### 🔬 DNA ANALYSIS INTERPRETATION")
    
    interpretation_col1, interpretation_col2 = st.columns(2)
    
    with interpretation_col1:
        st.markdown("""
        **🧬 Your Knowledge DNA Profile:**
        
        - **Blue Strand (Business)**: Strategic thinking and customer focus
        - **Red Strand (Technical)**: Implementation and technical capability  
        - **Green Strand (Functional)**: Requirements and specifications clarity
        
        **Helix Thickness** = Knowledge depth in each area
        **Connection Points** = Integration between knowledge domains
        **Diamond Markers** = Key insights from your responses
        """)
    
    with interpretation_col2:
        # Generate personalized insights
        if business_score > tech_score and business_score > functional_score:
            dominant_strand = "Business-Dominant DNA"
            insight = "Strong strategic and customer-focused thinking. Consider strengthening technical implementation knowledge."
        elif tech_score > business_score and tech_score > functional_score:
            dominant_strand = "Technical-Dominant DNA"
            insight = "Excellent technical capabilities. Consider enhancing business strategy alignment."
        elif functional_score > business_score and functional_score > tech_score:
            dominant_strand = "Specification-Dominant DNA"
            insight = "Clear requirements thinking. Balance with strategic vision and technical depth."
        else:
            dominant_strand = "Balanced DNA"
            insight = "Well-rounded knowledge across all domains. Excellent foundation for complex projects."
        
        st.markdown(f"""
        **🎯 Your DNA Type: {dominant_strand}**
        
        {insight}
        
        **Recommended Development:**
        - Continue building on your strengths
        - Focus on areas with thinner strands
        - Seek cross-functional collaboration opportunities
        """)

def render_standard_dashboard(question_data, all_text_data, words, combined_text, fixed_answers, section2_answers, org_name, contact, role, username):
    """Original spectacular dashboard with 5 features"""
    
    # ===== SPECTACULAR FEATURE 1: NEURAL LANGUAGE ANALYSIS =====
    st.markdown("## 🧠 NEURAL LANGUAGE ANALYSIS ENGINE")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_words = len(words)
        st.markdown(f"""
        <div class="metric-container">
            <div class="big-metric">{total_words:,}</div>
            <h3>TOTAL WORDS</h3>
            <p>Neural Processing Complete</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        unique_words = len(set(words))
        complexity_score = (unique_words / total_words * 100) if total_words > 0 else 0
        st.markdown(f"""
        <div class="metric-container">
            <div class="big-metric">{complexity_score:.1f}%</div>
            <h3>COMPLEXITY INDEX</h3>
            <p>Vocabulary Sophistication</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        linguistic_depth = "EXPERT" if avg_word_length > 6 else "ADVANCED" if avg_word_length > 5 else "STANDARD"
        st.markdown(f"""
        <div class="metric-container">
            <div class="big-metric">{linguistic_depth}</div>
            <h3>LINGUISTIC DEPTH</h3>
            <p>{avg_word_length:.1f} avg chars/word</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        sentences = len(re.findall(r'[.!?]+', combined_text))
        readability = "EXECUTIVE" if sentences > 20 else "PROFESSIONAL" if sentences > 10 else "CONCISE"
        st.markdown(f"""
        <div class="metric-container">
            <div class="big-metric">{readability}</div>
            <h3>COMMUNICATION STYLE</h3>
            <p>{sentences} sentences detected</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Continue with other standard dashboard features...
    # (Include all the existing dashboard code here)

def render_galaxy_explorer(question_data, words, combined_text):
    """🌌 Knowledge Galaxy Explorer - 3D Universe Visualization"""
    
    st.markdown("## 🌌 KNOWLEDGE GALAXY EXPLORER")
    st.markdown("*Navigate through your personal knowledge universe*")
    
    # Create 3D galaxy visualization
    fig = go.Figure()
    
    # Generate star systems for each response
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3', '#54A0FF']
    
    for i, item in enumerate(question_data):
        # Main star (response)
        response_length = len(str(item['answer']))
        
        # Generate 3D coordinates for star system
        theta = 2 * np.pi * i / len(question_data)
        phi = np.pi * (i % 3) / 3
        r = 5 + response_length / 20
        
        x = r * np.sin(phi) * np.cos(theta)
        y = r * np.sin(phi) * np.sin(theta)
        z = r * np.cos(phi)
        
        # Add main star
        fig.add_trace(go.Scatter3d(
            x=[x], y=[y], z=[z],
            mode='markers+text',
            marker=dict(
                size=max(response_length / 10, 10),
                color=colors[i % len(colors)],
                opacity=0.8,
                symbol='diamond',
                line=dict(width=2, color='white')
            ),
            text=f"Q{i+1}",
            textposition="middle center",
            textfont=dict(size=12, color='white'),
            name=f"Question {i+1}",
            hovertemplate=f"<b>Question {i+1}</b><br>Response Length: {response_length}<br>Type: {item['type']}<extra></extra>"
        ))
        
        # Add orbiting planets (keywords)
        answer_words = re.findall(r'\b\w+\b', str(item['answer']).lower())
        important_words = [w for w in answer_words if len(w) > 4][:3]  # Top 3 important words
        
        for j, word in enumerate(important_words):
            # Generate orbit
            orbit_radius = 1 + j * 0.5
            orbit_points = 20
            orbit_theta = np.linspace(0, 2*np.pi, orbit_points)
            
            orbit_x = x + orbit_radius * np.cos(orbit_theta)
            orbit_y = y + orbit_radius * np.sin(orbit_theta)
            orbit_z = z + orbit_radius * 0.1 * np.sin(orbit_theta * 3)
            
            # Add orbit path
            fig.add_trace(go.Scatter3d(
                x=orbit_x, y=orbit_y, z=orbit_z,
                mode='lines',
                line=dict(color=colors[i % len(colors)], width=2, dash='dot'),
                opacity=0.3,
                showlegend=False,
                hoverinfo='skip'
            ))
            
            # Add planet
            planet_pos = orbit_points // 4  # Position planet at 1/4 of orbit
            fig.add_trace(go.Scatter3d(
                x=[orbit_x[planet_pos]], y=[orbit_y[planet_pos]], z=[orbit_z[planet_pos]],
                mode='markers+text',
                marker=dict(
                    size=8,
                    color=colors[i % len(colors)],
                    opacity=0.6,
                    symbol='circle'
                ),
                text=word.upper(),
                textposition="top center",
                textfont=dict(size=8, color='white'),
                showlegend=False,
                hovertemplate=f"<b>{word}</b><br>Keyword from Q{i+1}<extra></extra>"
            ))
    
    # Add connecting lines between related responses
    for i in range(len(question_data)):
        for j in range(i+1, min(i+3, len(question_data))):  # Connect to next 2 responses
            # Calculate positions
            theta1, phi1 = 2 * np.pi * i / len(question_data), np.pi * (i % 3) / 3
            theta2, phi2 = 2 * np.pi * j / len(question_data), np.pi * (j % 3) / 3
            
            r1 = 5 + len(str(question_data[i]['answer'])) / 20
            r2 = 5 + len(str(question_data[j]['answer'])) / 20
            
            x1 = r1 * np.sin(phi1) * np.cos(theta1)
            y1 = r1 * np.sin(phi1) * np.sin(theta1)
            z1 = r1 * np.cos(phi1)
            
            x2 = r2 * np.sin(phi2) * np.cos(theta2)
            y2 = r2 * np.sin(phi2) * np.sin(theta2)
            z2 = r2 * np.cos(phi2)
            
            fig.add_trace(go.Scatter3d(
                x=[x1, x2], y=[y1, y2], z=[z1, z2],
                mode='lines',
                line=dict(color='rgba(255,255,255,0.1)', width=1),
                showlegend=False,
                hoverinfo='skip'
            ))
    
    # Style the galaxy
    fig.update_layout(
        title="🌟 YOUR KNOWLEDGE GALAXY - Interactive 3D Universe",
        scene=dict(
            bgcolor='rgba(0,0,0,0.9)',
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False, showbackground=False),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False, showbackground=False),
            zaxis=dict(showgrid=False, showticklabels=False, zeroline=False, showbackground=False),
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=600,
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Galaxy statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🌟 Star Systems", len(question_data))
    with col2:
        total_planets = sum(min(len(re.findall(r'\b\w+\b', str(item['answer']))), 3) for item in question_data)
        st.metric("🪐 Planets", total_planets)
    with col3:
        st.metric("🌌 Galaxy Density", f"{len(words)//100}x")
    with col4:
        st.metric("🚀 Exploration Level", "COMPLETE")

def render_neural_brain(question_data, words, combined_text):
    """🧠 Neural Network Brain - 3D Synaptic Visualization"""
    
    st.markdown("## 🧠 NEURAL NETWORK BRAIN")
    st.markdown("*Watch your knowledge form neural pathways*")
    
    # Define brain regions
    business_terms = ['strategy', 'customer', 'business', 'process', 'system', 'technology', 'digital', 'innovation', 'experience', 'solution']
    tech_terms = ['api', 'integration', 'platform', 'cloud', 'data', 'analytics', 'ai', 'automation', 'security', 'infrastructure']
    
    business_score = sum(1 for word in words if word in business_terms)
    tech_score = sum(1 for word in words if word in tech_terms)
    
    fig = go.Figure()
    
    # Create brain regions
    regions = {
        'business_cortex': {'center': [0, 0, 2], 'color': 'blue', 'score': business_score},
        'technical_lobe': {'center': [2, 0, 0], 'color': 'red', 'score': tech_score},
        'strategic_center': {'center': [0, 2, 0], 'color': 'green', 'score': len(question_data)//2},
        'innovation_stem': {'center': [0, 0, -1], 'color': 'purple', 'score': len(set(words))//10}
    }
    
    # Generate neurons for each response
    neurons = []
    for i, item in enumerate(question_data):
        # Classify response to brain region
        answer_text = str(item['answer']).lower()
        if any(term in answer_text for term in business_terms):
            region = 'business_cortex'
        elif any(term in answer_text for term in tech_terms):
            region = 'technical_lobe'
        elif item['type'] == 'open-ended':
            region = 'strategic_center'
        else:
            region = 'innovation_stem'
        
        # Generate neuron position near region center
        center = regions[region]['center']
        offset = np.random.normal(0, 0.5, 3)
        position = [center[0] + offset[0], center[1] + offset[1], center[2] + offset[2]]
        
        activation = len(str(item['answer'])) / 100  # Activation based on response length
        
        neurons.append({
            'position': position,
            'activation': activation,
            'region': region,
            'color': regions[region]['color'],
            'response_id': i
        })
    
    # Add neurons to plot
    for neuron in neurons:
        fig.add_trace(go.Scatter3d(
            x=[neuron['position'][0]],
            y=[neuron['position'][1]],
            z=[neuron['position'][2]],
            mode='markers',
            marker=dict(
                size=max(neuron['activation'] * 20, 5),
                color=neuron['color'],
                opacity=0.7,
                symbol='circle',
                line=dict(width=1, color='white')
            ),
            name=f"Neuron {neuron['response_id']+1}",
            hovertemplate=f"<b>Neural Response {neuron['response_id']+1}</b><br>Region: {neuron['region']}<br>Activation: {neuron['activation']:.2f}<extra></extra>"
        ))
    
    # Add synaptic connections
    for i, neuron1 in enumerate(neurons):
        for j, neuron2 in enumerate(neurons[i+1:], i+1):
            # Calculate connection strength based on similarity
            distance = np.sqrt(sum((a-b)**2 for a, b in zip(neuron1['position'], neuron2['position'])))
            if distance < 2:  # Only connect nearby neurons
                connection_strength = max(0.1, 1 - distance/2)
                
                fig.add_trace(go.Scatter3d(
                    x=[neuron1['position'][0], neuron2['position'][0]],
                    y=[neuron1['position'][1], neuron2['position'][1]],
                    z=[neuron1['position'][2], neuron2['position'][2]],
                    mode='lines',
                    line=dict(
                        color=f'rgba(255,255,255,{connection_strength})',
                        width=connection_strength * 3
                    ),
                    showlegend=False,
                    hoverinfo='skip'
                ))
    
    # Add brain region labels
    for region_name, region_data in regions.items():
        fig.add_trace(go.Scatter3d(
            x=[region_data['center'][0]],
            y=[region_data['center'][1]],
            z=[region_data['center'][2] + 1],
            mode='text',
            text=[region_name.replace('_', ' ').title()],
            textfont=dict(size=14, color=region_data['color']),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Style the brain
    fig.update_layout(
        title="🧠 YOUR KNOWLEDGE BRAIN - Neural Network Visualization",
        scene=dict(
            bgcolor='rgba(0,0,0,0.9)',
            xaxis=dict(showgrid=True, gridcolor='rgba(100,100,100,0.2)', showbackground=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(100,100,100,0.2)', showbackground=False),
            zaxis=dict(showgrid=True, gridcolor='rgba(100,100,100,0.2)', showbackground=False),
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Brain statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🧠 Active Neurons", len(neurons))
    with col2:
        total_connections = sum(1 for i, n1 in enumerate(neurons) for n2 in neurons[i+1:] 
                              if np.sqrt(sum((a-b)**2 for a, b in zip(n1['position'], n2['position']))) < 2)
        st.metric("⚡ Synaptic Connections", total_connections)
    with col3:
        avg_activation = np.mean([n['activation'] for n in neurons])
        st.metric("🔥 Neural Activity", f"{avg_activation:.2f}")
    with col4:
        st.metric("🎯 Brain Efficiency", "OPTIMAL")

def render_space_station(question_data, words, combined_text):
    """🚀 Space Station Command Center - Sci-Fi Visualization"""
    
    st.markdown("## 🚀 SPACE STATION COMMAND CENTER")
    st.markdown("*Mission Control for Your Knowledge Data*")
    
    # Create multiple viewports layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📡 HOLOGRAPHIC DISPLAY")
        
        # Create holographic-style 3D surface
        x = np.linspace(-2, 2, 20)
        y = np.linspace(-2, 2, 20)
        X, Y = np.meshgrid(x, y)
        
        # Generate surface based on response data
        Z = np.zeros_like(X)
        for i, item in enumerate(question_data):
            response_strength = len(str(item['answer'])) / 100
            center_x = (i % 3 - 1) * 1.5
            center_y = ((i // 3) % 3 - 1) * 1.5
            
            Z += response_strength * np.exp(-((X - center_x)**2 + (Y - center_y)**2))
        
        fig1 = go.Figure()
        
        # Add holographic surface
        fig1.add_trace(go.Surface(
            x=X, y=Y, z=Z,
            colorscale='Viridis',
            opacity=0.7,
            showscale=False
        ))
        
        # Add glowing grid lines
        for i in range(0, 20, 4):
            fig1.add_trace(go.Scatter3d(
                x=X[i, :], y=Y[i, :], z=Z[i, :] + 0.1,
                mode='lines',
                line=dict(color='cyan', width=4),
                showlegend=False,
                hoverinfo='skip'
            ))
            fig1.add_trace(go.Scatter3d(
                x=X[:, i], y=Y[:, i], z=Z[:, i] + 0.1,
                mode='lines',
                line=dict(color='cyan', width=4),
                showlegend=False,
                hoverinfo='skip'
            ))
        
        # Style as holographic display
        fig1.update_layout(
            scene=dict(
                bgcolor='rgba(0,0,0,0.9)',
                xaxis=dict(showgrid=False, showticklabels=False, zeroline=False, showbackground=False),
                yaxis=dict(showgrid=False, showticklabels=False, zeroline=False, showbackground=False),
                zaxis=dict(showgrid=False, showticklabels=False, zeroline=False, showbackground=False),
                camera=dict(eye=dict(x=1.2, y=1.2, z=1.2))
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.markdown("### 🛰️ SATELLITE VIEW")
        
        # Create satellite view of organizational reach
        fig2 = go.Figure()
        
        # Add Earth-like sphere
        u = np.linspace(0, 2 * np.pi, 50)
        v = np.linspace(0, np.pi, 50)
        x_sphere = np.outer(np.cos(u), np.sin(v))
        y_sphere = np.outer(np.sin(u), np.sin(v))
        z_sphere = np.outer(np.ones(np.size(u)), np.cos(v))
        
        fig2.add_trace(go.Surface(
            x=x_sphere, y=y_sphere, z=z_sphere,
            colorscale='Blues',
            opacity=0.3,
            showscale=False
        ))
        
        # Add data points as satellites
        for i, item in enumerate(question_data):
            # Generate satellite positions
            theta = 2 * np.pi * i / len(question_data)
            phi = np.pi * (0.3 + 0.4 * (i % 3) / 3)  # Keep satellites in visible hemisphere
            r = 1.5  # Distance from Earth center
            
            x_sat = r * np.sin(phi) * np.cos(theta)
            y_sat = r * np.sin(phi) * np.sin(theta)
            z_sat = r * np.cos(phi)
            
            fig2.add_trace(go.Scatter3d(
                x=[x_sat], y=[y_sat], z=[z_sat],
                mode='markers',
                marker=dict(
                    size=8,
                    color='red',
                    symbol='diamond',
                    line=dict(width=2, color='white')
                ),
                name=f"Data Satellite {i+1}",
                hovertemplate=f"<b>Satellite {i+1}</b><br>Data Type: {item['type']}<br>Signal Strength: {len(str(item['answer']))}<extra></extra>"
            ))
            
            # Add communication beam
            fig2.add_trace(go.Scatter3d(
                x=[0, x_sat], y=[0, y_sat], z=[0, z_sat],
                mode='lines',
                line=dict(color='rgba(255,0,0,0.3)', width=2),
                showlegend=False,
                hoverinfo='skip'
            ))
        
        fig2.update_layout(
            scene=dict(
                bgcolor='rgba(0,0,0,0.9)',
                xaxis=dict(showgrid=False, showticklabels=False, zeroline=False, showbackground=False),
                yaxis=dict(showgrid=False, showticklabels=False, zeroline=False, showbackground=False),
                zaxis=dict(showgrid=False, showticklabels=False, zeroline=False, showbackground=False),
                camera=dict(eye=dict(x=2, y=2, z=1))
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400,
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    # Mission Control Status Board
    st.markdown("### 🎛️ MISSION CONTROL STATUS")
    
    status_col1, status_col2, status_col3, status_col4, status_col5 = st.columns(5)
    
    with status_col1:
        st.markdown("""
        <div style="background: linear-gradient(45deg, #0f3460, #0e4b99); padding: 15px; border-radius: 10px; text-align: center; color: white;">
            <div style="font-size: 2em;">🛰️</div>
            <div style="font-size: 1.5em; font-weight: bold;">{}</div>
            <div>SATELLITES ONLINE</div>
        </div>
        """.format(len(question_data)), unsafe_allow_html=True)
    
    with status_col2:
        st.markdown("""
        <div style="background: linear-gradient(45deg, #0f3460, #0e4b99); padding: 15px; border-radius: 10px; text-align: center; color: white;">
            <div style="font-size: 2em;">📡</div>
            <div style="font-size: 1.5em; font-weight: bold;">100%</div>
            <div>SIGNAL STRENGTH</div>
        </div>
        """, unsafe_allow_html=True)
    
    with status_col3:
        st.markdown("""
        <div style="background: linear-gradient(45deg, #0f3460, #0e4b99); padding: 15px; border-radius: 10px; text-align: center; color: white;">
            <div style="font-size: 2em;">⚡</div>
            <div style="font-size: 1.5em; font-weight: bold;">OPTIMAL</div>
            <div>POWER LEVELS</div>
        </div>
        """, unsafe_allow_html=True)
    
    with status_col4:
        st.markdown("""
        <div style="background: linear-gradient(45deg, #0f3460, #0e4b99); padding: 15px; border-radius: 10px; text-align: center; color: white;">
            <div style="font-size: 2em;">🎯</div>
            <div style="font-size: 1.5em; font-weight: bold;">LOCKED</div>
            <div>TARGET ACQUIRED</div>
        </div>
        """, unsafe_allow_html=True)
    
    with status_col5:
        st.markdown("""
        <div style="background: linear-gradient(45deg, #0f3460, #0e4b99); padding: 15px; border-radius: 10px; text-align: center; color: white;">
            <div style="font-size: 2em;">✅</div>
            <div style="font-size: 1.5em; font-weight: bold;">SUCCESS</div>
            <div>MISSION STATUS</div>
        </div>
        """, unsafe_allow_html=True)

def render_architecture_builder(question_data, words, combined_text):
    """🏗️ Knowledge Architecture Builder - 3D City Visualization"""
    
    st.markdown("## 🏗️ KNOWLEDGE ARCHITECTURE BUILDER")
    st.markdown("*Build your organizational knowledge city*")
    
    fig = go.Figure()
    
    # Define city districts
    districts = {
        'business_district': {'center': [0, 0], 'color': 'blue', 'buildings': []},
        'tech_quarter': {'center': [5, 0], 'color': 'red', 'buildings': []},
        'innovation_hub': {'center': [0, 5], 'color': 'green', 'buildings': []},
        'strategic_center': {'center': [5, 5], 'color': 'purple', 'buildings': []}
    }
    
    # Classify responses into districts and create buildings
    business_terms = ['strategy', 'customer', 'business', 'process', 'experience']
    tech_terms = ['api', 'integration', 'platform', 'cloud', 'data', 'ai']
    
    for i, item in enumerate(question_data):
        answer_text = str(item['answer']).lower()
        
        # Determine district
        if any(term in answer_text for term in business_terms):
            district = 'business_district'
        elif any(term in answer_text for term in tech_terms):
            district = 'tech_quarter'
        elif item['type'] == 'open-ended':
            district = 'innovation_hub'
        else:
            district = 'strategic_center'
        
        # Building properties
        building_height = max(len(str(item['answer'])) / 20, 1)
        building_width = 0.8
        
        # Position in district
        district_center = districts[district]['center']
        building_count = len(districts[district]['buildings'])
        
        # Arrange buildings in grid within district
        grid_x = building_count % 3
        grid_y = building_count // 3
        
        x_pos = district_center[0] + (grid_x - 1) * 1.5
        y_pos = district_center[1] + (grid_y - 1) * 1.5
        
        # Create building as 3D box
        building_x = [x_pos - building_width/2, x_pos + building_width/2, x_pos + building_width/2, x_pos - building_width/2,
                     x_pos - building_width/2, x_pos + building_width/2, x_pos + building_width/2, x_pos - building_width/2]
        building_y = [y_pos - building_width/2, y_pos - building_width/2, y_pos + building_width/2, y_pos + building_width/2,
                     y_pos - building_width/2, y_pos - building_width/2, y_pos + building_width/2, y_pos + building_width/2]
        building_z = [0, 0, 0, 0, building_height, building_height, building_height, building_height]
        
        # Add building to plot
        fig.add_trace(go.Mesh3d(
            x=building_x, y=building_y, z=building_z,
            i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
            j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
            k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
            color=districts[district]['color'],
            opacity=0.7,
            name=f"Building {i+1}",
            hovertemplate=f"<b>Building {i+1}</b><br>District: {district}<br>Height: {building_height:.1f}<br>Type: {item['type']}<extra></extra>"
        ))
        
        districts[district]['buildings'].append({
            'position': [x_pos, y_pos, building_height/2],
            'height': building_height,
            'response_id': i
        })
    
    # Add district labels
    for district_name, district_data in districts.items():
        if district_data['buildings']:  # Only add label if district has buildings
            center = district_data['center']
            fig.add_trace(go.Scatter3d(
                x=[center[0]], y=[center[1]], z=[5],
                mode='text',
                text=[district_name.replace('_', ' ').title()],
                textfont=dict(size=16, color=district_data['color']),
                showlegend=False,
                hoverinfo='skip'
            ))
    
    # Add roads connecting districts
    road_connections = [
        ([0, 0, 0], [5, 0, 0]),  # business to tech
        ([0, 0, 0], [0, 5, 0]),  # business to innovation
        ([5, 0, 0], [5, 5, 0]),  # tech to strategic
        ([0, 5, 0], [5, 5, 0])   # innovation to strategic
    ]
    
    for start, end in road_connections:
        fig.add_trace(go.Scatter3d(
            x=[start[0], end[0]], y=[start[1], end[1]], z=[start[2], end[2]],
            mode='lines',
            line=dict(color='gray', width=8),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Style the city
    fig.update_layout(
        title="🏗️ YOUR KNOWLEDGE CITY - 3D Architecture",
        scene=dict(
            bgcolor='rgba(135,206,235,0.3)',  # Sky blue background
            xaxis=dict(showgrid=True, gridcolor='rgba(200,200,200,0.3)', title="East-West"),
            yaxis=dict(showgrid=True, gridcolor='rgba(200,200,200,0.3)', title="North-South"),
            zaxis=dict(showgrid=True, gridcolor='rgba(200,200,200,0.3)', title="Height"),
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.2))
        ),
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # City statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_buildings = sum(len(d['buildings']) for d in districts.values())
        st.metric("🏢 Total Buildings", total_buildings)
    with col2:
        active_districts = sum(1 for d in districts.values() if d['buildings'])
        st.metric("🏙️ Active Districts", active_districts)
    with col3:
        avg_height = np.mean([b['height'] for d in districts.values() for b in d['buildings']]) if total_buildings > 0 else 0
        st.metric("📏 Avg Building Height", f"{avg_height:.1f}")
    with col4:
        st.metric("🚧 Construction Status", "COMPLETE")

def render_ocean_depths(question_data, words, combined_text):
    """🌊 Knowledge Ocean Depths - Underwater Visualization"""
    
    st.markdown("## 🌊 KNOWLEDGE OCEAN DEPTHS")
    st.markdown("*Dive into your underwater knowledge ecosystem*")
    
    fig = go.Figure()
    
    # Create ocean floor
    x_floor = np.linspace(-10, 10, 20)
    y_floor = np.linspace(-10, 10, 20)
    X_floor, Y_floor = np.meshgrid(x_floor, y_floor)
    Z_floor = -8 + 0.5 * np.sin(X_floor/2) * np.cos(Y_floor/2)  # Wavy ocean floor
    
    fig.add_trace(go.Surface(
        x=X_floor, y=Y_floor, z=Z_floor,
        colorscale='Earth',
        opacity=0.6,
        showscale=False,
        name="Ocean Floor"
    ))
    
    # Create coral reefs for complex responses
    coral_colors = ['coral', 'orange', 'pink', 'yellow', 'lightgreen']
    
    for i, item in enumerate(question_data):
        response_complexity = len(str(item['answer']))
        
        if response_complexity > 50:  # Create coral reef for detailed responses
            # Position coral reef
            reef_x = (i % 4 - 1.5) * 4
            reef_y = ((i // 4) % 4 - 1.5) * 4
            reef_z = -6 + response_complexity / 100
            
            # Create branching coral structure
            for branch in range(min(response_complexity // 20, 5)):
                branch_angle = 2 * np.pi * branch / 5
                branch_x = reef_x + 0.5 * np.cos(branch_angle)
                branch_y = reef_y + 0.5 * np.sin(branch_angle)
                
                # Coral branch points
                branch_points = 10
                t = np.linspace(0, 1, branch_points)
                coral_x = branch_x + 0.3 * t * np.cos(branch_angle + t * np.pi)
                coral_y = branch_y + 0.3 * t * np.sin(branch_angle + t * np.pi)
                coral_z = reef_z + t * 2
                
                fig.add_trace(go.Scatter3d(
                    x=coral_x, y=coral_y, z=coral_z,
                    mode='lines+markers',
                    line=dict(color=coral_colors[branch % len(coral_colors)], width=6),
                    marker=dict(size=4, color=coral_colors[branch % len(coral_colors)]),
                    showlegend=False,
                    hovertemplate=f"<b>Coral Reef {i+1}</b><br>Complexity: {response_complexity}<br>Branch: {branch+1}<extra></extra>"
                ))
    
    # Add fish schools for keywords
    important_words = [word for word in set(words) if len(word) > 4][:10]  # Top 10 important words
    
    for i, word in enumerate(important_words):
        # School position
        school_x = np.random.uniform(-8, 8)
        school_y = np.random.uniform(-8, 8)
        school_z = np.random.uniform(-7, -2)
        
        # Create fish school (small cluster of points)
        fish_count = min(len([w for w in words if w == word]) * 3, 15)  # School size based on word frequency
        
        school_positions_x = school_x + np.random.normal(0, 0.5, fish_count)
        school_positions_y = school_y + np.random.normal(0, 0.5, fish_count)
        school_positions_z = school_z + np.random.normal(0, 0.3, fish_count)
        
        fig.add_trace(go.Scatter3d(
            x=school_positions_x,
            y=school_positions_y,
            z=school_positions_z,
            mode='markers',
            marker=dict(
                size=4,
                color='lightblue',
                opacity=0.8,
                symbol='diamond'
            ),
            name=f"School: {word}",
            hovertemplate=f"<b>Fish School</b><br>Keyword: {word}<br>School Size: {fish_count}<extra></extra>"
        ))
    
    # Add bioluminescent creatures for unique insights
    unique_responses = [item for item in question_data if len(str(item['answer'])) > 100]
    
    for i, item in enumerate(unique_responses):
        creature_x = np.random.uniform(-9, 9)
        creature_y = np.random.uniform(-9, 9)
        creature_z = np.random.uniform(-8, -1)
        
        fig.add_trace(go.Scatter3d(
            x=[creature_x], y=[creature_y], z=[creature_z],
            mode='markers',
            marker=dict(
                size=15,
                color='cyan',
                opacity=0.9,
                symbol='diamond',  # Changed from 'star' to 'diamond'
                line=dict(width=2, color='white')
            ),
            name=f"Deep Insight {i+1}",
            hovertemplate=f"<b>Bioluminescent Insight</b><br>Response Length: {len(str(item['answer']))}<br>Type: {item['type']}<extra></extra>"
        ))
    
    # Add water surface
    x_surface = np.linspace(-10, 10, 10)
    y_surface = np.linspace(-10, 10, 10)
    X_surface, Y_surface = np.meshgrid(x_surface, y_surface)
    Z_surface = np.zeros_like(X_surface)
    
    fig.add_trace(go.Surface(
        x=X_surface, y=Y_surface, z=Z_surface,
        colorscale=[[0, 'rgba(0,100,200,0.3)'], [1, 'rgba(0,150,255,0.3)']],
        opacity=0.4,
        showscale=False,
        name="Water Surface"
    ))
    
    # Style the ocean
    fig.update_layout(
        title="🌊 YOUR KNOWLEDGE OCEAN - Underwater Ecosystem",
        scene=dict(
            bgcolor='rgba(0,50,100,0.8)',  # Deep blue ocean background
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False, showbackground=False),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False, showbackground=False),
            zaxis=dict(showgrid=False, showticklabels=False, zeroline=False, showbackground=False),
            camera=dict(eye=dict(x=1.5, y=1.5, z=0.5))
        ),
        plot_bgcolor='rgba(0,50,100,0.8)',
        paper_bgcolor='rgba(0,50,100,0.8)',
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Ocean statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        coral_reefs = len([item for item in question_data if len(str(item['answer'])) > 50])
        st.metric("🪸 Coral Reefs", coral_reefs)
    with col2:
        st.metric("🐠 Fish Schools", len(important_words))
    with col3:
        st.metric("✨ Bioluminescent Creatures", len(unique_responses))
    with col4:
        st.metric("🌊 Ocean Depth", "EXPLORED")

def render_volcano_section(question_data, words, combined_text):
    """🌋 Knowledge Volcano Cross-Section - Geological Visualization"""
    
    st.markdown("## 🌋 KNOWLEDGE VOLCANO CROSS-SECTION")
    st.markdown("*Explore the geological layers of your knowledge*")
    
    fig = go.Figure()
    
    # Create volcano cross-section
    # Outer volcano shape
    theta = np.linspace(0, 2*np.pi, 50)
    r_outer = 8
    r_inner = 2
    
    # Volcano surface
    volcano_x = []
    volcano_y = []
    volcano_z = []
    
    for i, t in enumerate(theta):
        for r in np.linspace(r_inner, r_outer, 20):
            x = r * np.cos(t)
            y = r * np.sin(t)
            z = max(0, 6 - (r - r_inner) * 1.5 + np.random.normal(0, 0.2))  # Volcano shape
            
            volcano_x.append(x)
            volcano_y.append(y)
            volcano_z.append(z)
    
    # Add volcano surface
    fig.add_trace(go.Scatter3d(
        x=volcano_x, y=volcano_y, z=volcano_z,
        mode='markers',
        marker=dict(size=2, color='brown', opacity=0.3),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Create knowledge layers (geological strata)
    layer_colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
    layer_names = ['Core Strategy', 'Business Process', 'Technology', 'Innovation', 'Customer Focus', 'Future Vision']
    
    for layer_idx in range(6):
        layer_height = layer_idx * 1.2
        layer_responses = question_data[layer_idx::6] if layer_idx < len(question_data) else []
        
        if layer_responses:
            # Create geological layer
            layer_theta = np.linspace(0, 2*np.pi, 30)
            layer_r = np.linspace(1, 6 - layer_idx * 0.5, 15)
            
            layer_x = []
            layer_y = []
            layer_z = []
            
            for t in layer_theta:
                for r in layer_r:
                    x = r * np.cos(t)
                    y = r * np.sin(t)
                    z = layer_height + np.random.normal(0, 0.1)
                    
                    layer_x.append(x)
                    layer_y.append(y)
                    layer_z.append(z)
            
            fig.add_trace(go.Scatter3d(
                x=layer_x, y=layer_y, z=layer_z,
                mode='markers',
                marker=dict(
                    size=3,
                    color=layer_colors[layer_idx],
                    opacity=0.6
                ),
                name=layer_names[layer_idx],
                hovertemplate=f"<b>{layer_names[layer_idx]}</b><br>Layer Depth: {layer_height}<br>Responses: {len(layer_responses)}<extra></extra>"
            ))
    
    # Add magma core (central strategy)
    core_theta = np.linspace(0, 2*np.pi, 20)
    core_z = np.linspace(0, 7, 30)
    
    for z in core_z:
        core_r = max(0.5, 2 - z * 0.2)  # Tapering core
        for t in core_theta[::2]:  # Sparse points for performance
            x = core_r * np.cos(t) + np.random.normal(0, 0.1)
            y = core_r * np.sin(t) + np.random.normal(0, 0.1)
            
            fig.add_trace(go.Scatter3d(
                x=[x], y=[y], z=[z],
                mode='markers',
                marker=dict(
                    size=6,
                    color='red',
                    opacity=0.8,
                    symbol='circle'
                ),
                showlegend=False,
                hovertemplate=f"<b>Magma Core</b><br>Strategic Center<br>Depth: {z:.1f}<extra></extra>"
            ))
    
    # Add crystal formations (valuable insights)
    valuable_responses = [item for item in question_data if len(str(item['answer'])) > 80]
    
    for i, item in enumerate(valuable_responses):
        crystal_x = np.random.uniform(-7, 7)
        crystal_y = np.random.uniform(-7, 7)
        crystal_z = np.random.uniform(1, 6)
        
        # Create crystal cluster
        for j in range(5):
            offset_x = crystal_x + np.random.normal(0, 0.3)
            offset_y = crystal_y + np.random.normal(0, 0.3)
            offset_z = crystal_z + np.random.normal(0, 0.2)
            
            fig.add_trace(go.Scatter3d(
                x=[offset_x], y=[offset_y], z=[offset_z],
                mode='markers',
                marker=dict(
                    size=8,
                    color='cyan',
                    opacity=0.9,
                    symbol='diamond',
                    line=dict(width=2, color='white')
                ),
                showlegend=False if j > 0 else True,
                name=f"Crystal Formation {i+1}" if j == 0 else "",
                hovertemplate=f"<b>Knowledge Crystal</b><br>Valuable Insight<br>Response Length: {len(str(item['answer']))}<extra></extra>"
            ))
    
    # Style the volcano
    fig.update_layout(
        title="🌋 YOUR KNOWLEDGE VOLCANO - Geological Cross-Section",
        scene=dict(
            bgcolor='rgba(50,25,0,0.8)',  # Earth-like background
            xaxis=dict(showgrid=True, gridcolor='rgba(100,50,25,0.3)', title="Width"),
            yaxis=dict(showgrid=True, gridcolor='rgba(100,50,25,0.3)', title="Depth"),
            zaxis=dict(showgrid=True, gridcolor='rgba(100,50,25,0.3)', title="Height"),
            camera=dict(eye=dict(x=1.5, y=1.5, z=1))
        ),
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Geological statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🏔️ Geological Layers", 6)
    with col2:
        st.metric("💎 Crystal Formations", len(valuable_responses))
    with col3:
        st.metric("🌋 Magma Activity", "ACTIVE")
    with col4:
        st.metric("⛏️ Mining Status", "RICH DEPOSITS")

def render_theater_stage(question_data, words, combined_text):
    """🎭 Knowledge Theater Stage - Performance Visualization"""
    
    st.markdown("## 🎭 KNOWLEDGE THEATER STAGE")
    st.markdown("*Watch your data perform on the grand stage*")
    
    fig = go.Figure()
    
    # Create theater stage
    stage_width = 10
    stage_depth = 6
    stage_height = 0.5
    
    # Stage platform
    stage_x = [-stage_width/2, stage_width/2, stage_width/2, -stage_width/2, -stage_width/2]
    stage_y = [-stage_depth/2, -stage_depth/2, stage_depth/2, stage_depth/2, -stage_depth/2]
    stage_z = [stage_height] * 5
    
    fig.add_trace(go.Scatter3d(
        x=stage_x, y=stage_y, z=stage_z,
        mode='lines',
        line=dict(color='brown', width=8),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Add stage floor
    fig.add_trace(go.Mesh3d(
        x=[-stage_width/2, stage_width/2, stage_width/2, -stage_width/2],
        y=[-stage_depth/2, -stage_depth/2, stage_depth/2, stage_depth/2],
        z=[0, 0, 0, 0],
        i=[0, 0], j=[1, 2], k=[2, 3],
        color='saddlebrown',
        opacity=0.8,
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Create performers (responses as actors)
    performer_positions = []
    act_colors = ['red', 'blue', 'green', 'purple', 'orange']
    
    for i, item in enumerate(question_data):
        # Position actors on stage
        if len(question_data) <= 5:
            x_pos = (i - len(question_data)/2 + 0.5) * 2
        else:
            row = i // 5
            col = i % 5
            x_pos = (col - 2) * 2
            y_pos_offset = row * 1.5
        
        y_pos = np.random.uniform(-2, 2) + (y_pos_offset if len(question_data) > 5 else 0)
        z_pos = stage_height + 0.1
        
        # Actor size based on response importance
        actor_size = max(len(str(item['answer'])) / 20, 5)
        
        fig.add_trace(go.Scatter3d(
            x=[x_pos], y=[y_pos], z=[z_pos],
            mode='markers+text',
            marker=dict(
                size=actor_size,
                color=act_colors[i % len(act_colors)],
                opacity=0.8,
                symbol='circle',
                line=dict(width=2, color='white')
            ),
            text=f"Act {i+1}",
            textposition="top center",
            textfont=dict(size=10, color='white'),
            name=f"Performer {i+1}",
            hovertemplate=f"<b>Act {i+1}</b><br>Performance Length: {len(str(item['answer']))}<br>Type: {item['type']}<extra></extra>"
        ))
        
        performer_positions.append([x_pos, y_pos, z_pos])
    
    # Add stage lighting (spotlights)
    for i, pos in enumerate(performer_positions[:5]):  # Limit to 5 spotlights
        # Create light beam effect
        light_x = [pos[0], pos[0]]
        light_y = [pos[1], pos[1]]
        light_z = [pos[2], pos[2] + 5]
        
        fig.add_trace(go.Scatter3d(
            x=light_x, y=light_y, z=light_z,
            mode='lines',
            line=dict(color='yellow', width=15, dash='dot'),
            opacity=0.6,
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # Light source
        fig.add_trace(go.Scatter3d(
            x=[pos[0]], y=[pos[1]], z=[pos[2] + 5],
            mode='markers',
            marker=dict(size=8, color='yellow', opacity=0.9, symbol='diamond'),  # Changed from 'star' to 'diamond'
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Add theater curtains
    curtain_height = 8
    curtain_positions = [
        # Left curtain
        ([-stage_width/2 - 1, -stage_width/2 - 1], [-stage_depth/2, stage_depth/2], [0, curtain_height]),
        # Right curtain  
        ([stage_width/2 + 1, stage_width/2 + 1], [-stage_depth/2, stage_depth/2], [0, curtain_height])
    ]
    
    for curtain_x, curtain_y, curtain_z in curtain_positions:
        fig.add_trace(go.Scatter3d(
            x=curtain_x * 2, y=curtain_y, z=curtain_z * 2,
            mode='lines',
            line=dict(color='darkred', width=20),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Add audience (represented by dots)
    audience_rows = 5
    audience_cols = 8
    
    for row in range(audience_rows):
        for col in range(audience_cols):
            audience_x = (col - audience_cols/2 + 0.5) * 1.2
            audience_y = -stage_depth/2 - 2 - row * 0.8
            audience_z = 0
            
            fig.add_trace(go.Scatter3d(
                x=[audience_x], y=[audience_y], z=[audience_z],
                mode='markers',
                marker=dict(size=3, color='gray', opacity=0.5),
                showlegend=False,
                hoverinfo='skip'
            ))
    
    # Style the theater
    fig.update_layout(
        title="🎭 YOUR KNOWLEDGE THEATER - Grand Performance",
        scene=dict(
            bgcolor='rgba(0,0,0,0.9)',  # Dark theater background
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False, showbackground=False),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False, showbackground=False),
            zaxis=dict(showgrid=False, showticklabels=False, zeroline=False, showbackground=False),
            camera=dict(eye=dict(x=0, y=-2, z=1))
        ),
        plot_bgcolor='rgba(0,0,0,0.9)',
        paper_bgcolor='rgba(0,0,0,0.9)',
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Theater statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🎭 Performers", len(question_data))
    with col2:
        st.metric("💡 Spotlights", min(len(question_data), 5))
    with col3:
        audience_size = audience_rows * audience_cols
        st.metric("👥 Audience", audience_size)
    with col4:
        st.metric("🎪 Show Status", "STANDING OVATION")

def render_castle_fortress(question_data, words, combined_text):
    """🏰 Knowledge Castle Fortress - Medieval Visualization"""
    
    st.markdown("## 🏰 KNOWLEDGE CASTLE FORTRESS")
    st.markdown("*Defend your knowledge kingdom*")
    
    fig = go.Figure()
    
    # Define castle components
    castle_components = {
        'main_keep': {'position': [0, 0, 0], 'height': 8, 'width': 3},
        'towers': [
            {'position': [-4, -4, 0], 'height': 6, 'width': 1.5},
            {'position': [4, -4, 0], 'height': 6, 'width': 1.5},
            {'position': [-4, 4, 0], 'height': 6, 'width': 1.5},
            {'position': [4, 4, 0], 'height': 6, 'width': 1.5}
        ]
    }
    
    # Build main keep (central knowledge)
    keep = castle_components['main_keep']
    keep_responses = question_data[:len(question_data)//2] if question_data else []
    
    # Main keep structure
    keep_x = [keep['position'][0] - keep['width']/2, keep['position'][0] + keep['width']/2, 
              keep['position'][0] + keep['width']/2, keep['position'][0] - keep['width']/2,
              keep['position'][0] - keep['width']/2, keep['position'][0] + keep['width']/2,
              keep['position'][0] + keep['width']/2, keep['position'][0] - keep['width']/2]
    keep_y = [keep['position'][1] - keep['width']/2, keep['position'][1] - keep['width']/2,
              keep['position'][1] + keep['width']/2, keep['position'][1] + keep['width']/2,
              keep['position'][1] - keep['width']/2, keep['position'][1] - keep['width']/2,
              keep['position'][1] + keep['width']/2, keep['position'][1] + keep['width']/2]
    keep_z = [0, 0, 0, 0, keep['height'], keep['height'], keep['height'], keep['height']]
    
    fig.add_trace(go.Mesh3d(
        x=keep_x, y=keep_y, z=keep_z,
        i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
        j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
        k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
        color='gray',
        opacity=0.8,
        name="Main Keep",
        hovertemplate=f"<b>Main Keep</b><br>Central Knowledge<br>Responses: {len(keep_responses)}<extra></extra>"
    ))
    
    # Build towers (specialized knowledge areas)
    tower_names = ['Business Tower', 'Technical Tower', 'Strategic Tower', 'Innovation Tower']
    tower_colors = ['blue', 'red', 'green', 'purple']
    
    for i, tower in enumerate(castle_components['towers']):
        if i < len(question_data):
            tower_height = max(tower['height'], len(str(question_data[i]['answer'])) / 20)
            
            # Tower structure
            tower_x = [tower['position'][0] - tower['width']/2, tower['position'][0] + tower['width']/2,
                      tower['position'][0] + tower['width']/2, tower['position'][0] - tower['width']/2,
                      tower['position'][0] - tower['width']/2, tower['position'][0] + tower['width']/2,
                      tower['position'][0] + tower['width']/2, tower['position'][0] - tower['width']/2]
            tower_y = [tower['position'][1] - tower['width']/2, tower['position'][1] - tower['width']/2,
                      tower['position'][1] + tower['width']/2, tower['position'][1] + tower['width']/2,
                      tower['position'][1] - tower['width']/2, tower['position'][1] - tower['width']/2,
                      tower['position'][1] + tower['width']/2, tower['position'][1] + tower['width']/2]
            tower_z = [0, 0, 0, 0, tower_height, tower_height, tower_height, tower_height]
            
            fig.add_trace(go.Mesh3d(
                x=tower_x, y=tower_y, z=tower_z,
                i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
                j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
                k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
                color=tower_colors[i],
                opacity=0.7,
                name=tower_names[i],
                hovertemplate=f"<b>{tower_names[i]}</b><br>Height: {tower_height:.1f}<br>Specialization: {question_data[i]['type'] if i < len(question_data) else 'N/A'}<extra></extra>"
            ))
            
            # Add flags on towers
            flag_x = tower['position'][0]
            flag_y = tower['position'][1]
            flag_z = tower_height + 0.5
            
            fig.add_trace(go.Scatter3d(
                x=[flag_x], y=[flag_y], z=[flag_z],
                mode='markers+text',
                marker=dict(size=8, color=tower_colors[i], symbol='diamond'),
                text="🏴",
                textfont=dict(size=16),
                showlegend=False,
                hoverinfo='skip'
            ))
    
    # Add castle walls connecting towers
    wall_connections = [
        ([-4, -4, 0], [4, -4, 0]),  # Front wall
        ([4, -4, 0], [4, 4, 0]),   # Right wall
        ([4, 4, 0], [-4, 4, 0]),   # Back wall
        ([-4, 4, 0], [-4, -4, 0])  # Left wall
    ]
    
    wall_height = 3
    for start, end in wall_connections:
        # Wall segments
        wall_segments = 10
        for i in range(wall_segments):
            t = i / wall_segments
            x = start[0] + t * (end[0] - start[0])
            y = start[1] + t * (end[1] - start[1])
            
            fig.add_trace(go.Scatter3d(
                x=[x, x], y=[y, y], z=[0, wall_height],
                mode='lines',
                line=dict(color='gray', width=8),
                showlegend=False,
                hoverinfo='skip'
            ))
    
    # Add moat (knowledge barriers)
    moat_radius = 7
    moat_theta = np.linspace(0, 2*np.pi, 50)
    moat_x = moat_radius * np.cos(moat_theta)
    moat_y = moat_radius * np.sin(moat_theta)
    moat_z = [-1] * len(moat_theta)
    
    fig.add_trace(go.Scatter3d(
        x=moat_x, y=moat_y, z=moat_z,
        mode='lines',
        line=dict(color='blue', width=6),
        name="Moat",
        hovertemplate="<b>Knowledge Moat</b><br>Protective Barrier<extra></extra>"
    ))
    
    # Add drawbridge
    bridge_x = [0, 0]
    bridge_y = [-moat_radius, -4]
    bridge_z = [-0.5, 0]
    
    fig.add_trace(go.Scatter3d(
        x=bridge_x, y=bridge_y, z=bridge_z,
        mode='lines',
        line=dict(color='brown', width=12),
        name="Drawbridge",
        hovertemplate="<b>Knowledge Bridge</b><br>Access Point<extra></extra>"
    ))
    
    # Style the castle
    fig.update_layout(
        title="🏰 YOUR KNOWLEDGE FORTRESS - Medieval Castle",
        scene=dict(
            bgcolor='rgba(135,206,235,0.3)',  # Sky background
            xaxis=dict(showgrid=True, gridcolor='rgba(100,100,100,0.2)', title="East-West"),
            yaxis=dict(showgrid=True, gridcolor='rgba(100,100,100,0.2)', title="North-South"),
            zaxis=dict(showgrid=True, gridcolor='rgba(100,100,100,0.2)', title="Height"),
            camera=dict(eye=dict(x=1.5, y=-1.5, z=1))
        ),
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Castle statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        active_towers = min(len(question_data), 4)
        st.metric("🗼 Active Towers", active_towers)
    with col2:
        st.metric("🏰 Main Keep", "FORTIFIED")
    with col3:
        st.metric("🌊 Moat Status", "FILLED")
    with col4:
        st.metric("⚔️ Defense Level", "IMPREGNABLE")

    return True

