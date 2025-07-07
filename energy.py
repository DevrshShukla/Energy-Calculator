import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="⚡ Energy Calculator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for calculation
if 'calculated' not in st.session_state:
    st.session_state.calculated = False
if 'energy_data' not in st.session_state:
    st.session_state.energy_data = {}

# Light theme colors (fixed)
bg_color = "#DDEFF1"
card_bg = "#ffffff"
text_color = "#000000"
secondary_text = "#FFFFFF"
border_color = "#e0e0e0"
gradient_start = "#8187a3"
gradient_end = "#764ba2"
accent_color = "#667eea"
hover_bg = "#f5f5f5"

# Dynamic CSS (light theme)
st.markdown(f"""
<style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    
    .main-header {{
        background: linear-gradient(135deg, {gradient_start} 0%, {gradient_end} 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }}
    
    .main-header h1 {{
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }}
    
    .simple-card {{
        background: {card_bg};
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid {border_color};
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }}
    
    .simple-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    }}
    
    .appliance-card {{
        background: {card_bg};
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid {border_color};
        margin: 1rem 0;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }}
    
    .appliance-card:hover {{
        border-color: {accent_color};
        transform: translateY(-3px);
        box-shadow: 0 6px 25px rgba(0, 0, 0, 0.15);
    }}
    
    .appliance-card.selected {{
        border-color: {accent_color};
        background: linear-gradient(135deg, {gradient_start} 0%, {gradient_end} 100%);
        color: white;
    }}
    
    .appliance-icon {{
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }}
    
    .appliance-title {{
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0.5rem 0;
    }}
    
    .appliance-desc {{
        font-size: 0.9rem;
        opacity: 0.8;
        margin-bottom: 0.5rem;
    }}
    
    .energy-units {{
        font-size: 0.9rem;
        font-weight: 700;
        color: {accent_color};
    }}
    
    .appliance-card.selected .energy-units {{
        color: white;
    }}
    
    .result-card {{
        background: linear-gradient(135deg, {gradient_start} 0%, {gradient_end} 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin: 2rem 0;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }}
    
    .result-card h1 {{
        font-size: 3rem;
        margin: 1rem 0;
        font-weight: 700;
    }}
    
    .stButton > button {{
        background: linear-gradient(135deg, {gradient_start} 0%, {gradient_end} 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }}
    
    .info-section {{
        background: {card_bg};
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid {accent_color};
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>⚡ Simple Energy Calculator</h1>
    <p>Calculate how much electricity your home uses every day</p>
</div>
""", unsafe_allow_html=True)

# Sidebar - Personal Info
st.sidebar.markdown("""
<div class="sidebar-section">
    <h3>👤 About You</h3>
</div>
""", unsafe_allow_html=True)

name = st.sidebar.text_input("Your Name:", placeholder="Enter your name")
age = st.sidebar.number_input("Your Age:", min_value=1, max_value=120, value=25)
city = st.sidebar.text_input("Your City:", placeholder="Which city do you live in?")

st.sidebar.markdown("""
<div class="sidebar-section">
    <h3>🏠 Your Home</h3>
</div>
""", unsafe_allow_html=True)

home_type = st.sidebar.selectbox(
    "What type of home?",
    ["Choose one", "1 Room (1BHK)", "2 Rooms (2BHK)", "3 Rooms (3BHK)"]
)

# Main content
st.markdown('<div class="section-title">🏠 What appliances do you use?</div>', unsafe_allow_html=True)
st.markdown('<p class="simple-text">Click on the appliances you use in your home. The cards will turn blue when selected.</p>', unsafe_allow_html=True)

# Appliance selection - simplified
col1, col2, col3 = st.columns(3)

with col1:
    ac_check = st.checkbox("", key="ac_check", label_visibility="hidden")
    card_class = "appliance-card selected" if ac_check else "appliance-card"
    st.markdown(f"""
    <div class="{card_class}">
        <div class="appliance-icon">❄️</div>
        <div class="appliance-title">Air Conditioner</div>
        <div class="appliance-desc">Keeps your home cool</div>
        <div class="energy-units">Uses 3 units per day</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    fridge_check = st.checkbox("", key="fridge_check", label_visibility="hidden")
    card_class = "appliance-card selected" if fridge_check else "appliance-card"
    st.markdown(f"""
    <div class="{card_class}">
        <div class="appliance-icon">🧊</div>
        <div class="appliance-title">Refrigerator</div>
        <div class="appliance-desc">Keeps food fresh</div>
        <div class="energy-units">Uses 3 units per day</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    washing_check = st.checkbox("", key="washing_check", label_visibility="hidden")
    card_class = "appliance-card selected" if washing_check else "appliance-card"
    st.markdown(f"""
    <div class="{card_class}">
        <div class="appliance-icon">👕</div>
        <div class="appliance-title">Washing Machine</div>
        <div class="appliance-desc">Washes your clothes</div>
        <div class="energy-units">Uses 3 units per day</div>
    </div>
    """, unsafe_allow_html=True)

# Basic energy info
st.markdown('<div class="section-title">📊 Basic Energy Usage</div>', unsafe_allow_html=True)

col_info1, col_info2 = st.columns(2)

with col_info1:
    st.markdown("""
    <div class="info-section">
        <h4>💡 Every home uses these basics:</h4>
        <p class="simple-text">• LED lights for brightness</p>
        <p class="simple-text">• Fans to keep cool</p>
        <p class="simple-text">• Phone chargers and small items</p>
    </div>
    """, unsafe_allow_html=True)

with col_info2:
    st.markdown("""
    <div class="info-section">
        <h4>🏠 Daily basic usage:</h4>
        <p class="simple-text">• 1 Room home: 2.4 units</p>
        <p class="simple-text">• 2 Room home: 3.6 units</p>
        <p class="simple-text">• 3 Room home: 4.8 units</p>
    </div>
    """, unsafe_allow_html=True)

# Calculate button
st.markdown("---")
col_btn = st.columns([2, 1, 2])
with col_btn[1]:
    calculate_btn = st.button("🔍 Calculate My Energy Use", key="calc_btn")

# Simple calculation function
def calculate_simple_energy(home_type, ac, fridge, washing):
    # Base energy for home
    base_energy = 0
    if "1 Room" in home_type:
        base_energy = 2.4
    elif "2 Room" in home_type:
        base_energy = 3.6
    elif "3 Room" in home_type:
        base_energy = 4.8
    
    # Add appliance energy
    appliance_energy = 0
    if ac:
        appliance_energy += 3
    if fridge:
        appliance_energy += 3
    if washing:
        appliance_energy += 3
    
    total_energy = base_energy + appliance_energy
    return total_energy, base_energy, appliance_energy

# Show results
if calculate_btn:
    if not name or "Choose" in home_type:
        st.error("🔴 Please enter your name and select your home type first!")
    else:
        total, base, appliances = calculate_simple_energy(home_type, ac_check, fridge_check, washing_check)
        
        st.session_state.energy_data = {
            'name': name,
            'age': age,
            'city': city,
            'home_type': home_type,
            'ac': ac_check,
            'fridge': fridge_check,
            'washing': washing_check,
            'total': total,
            'base': base,
            'appliances': appliances
        }
        st.session_state.calculated = True

# Display results if calculated
if st.session_state.calculated:
    data = st.session_state.energy_data
    
    st.markdown("---")
    st.markdown(f'<div class="section-title">📈 {data["name"]}\'s Energy Report</div>', unsafe_allow_html=True)
    
    # Big result card
    st.markdown(f"""
    <div class="result-card">
        <h2>⚡ Your Daily Energy Use</h2>
        <h1>{data['total']:.1f} units</h1>
        <p>This means you use about {data['total'] * 30:.0f} units per month</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Simple breakdown
    col_break1, col_break2 = st.columns(2)
    
    with col_break1:
        st.markdown(f"""
        <div class="simple-card">
            <h3>🏠 Your Home Details</h3>
            <p class="simple-text"><strong>Name:</strong> {data['name']}</p>
            <p class="simple-text"><strong>Home Type:</strong> {data['home_type']}</p>
            <p class="simple-text"><strong>City:</strong> {data['city']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_break2:
        st.markdown(f"""
        <div class="simple-card">
            <h3>🔌 Your Appliances</h3>
            <p class="simple-text">Air Conditioner: {'✅ Yes' if data['ac'] else '❌ No'}</p>
            <p class="simple-text">Refrigerator: {'✅ Yes' if data['fridge'] else '❌ No'}</p>
            <p class="simple-text">Washing Machine: {'✅ Yes' if data['washing'] else '❌ No'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Big, simple pie chart
    st.markdown('<div class="section-title">📊 Where Your Energy Goes</div>', unsafe_allow_html=True)
    
    col_pie1, col_pie2 = st.columns([3, 2])
    
    with col_pie1:
        # Create simple pie chart
        fig = go.Figure(data=[go.Pie(
            labels=['Basic Home Needs', 'Your Appliances'],
            values=[data['base'], data['appliances']],
            hole=0.4,
            textinfo='label+percent',
            textfont_size=18,
            marker=dict(colors=['#667eea', '#764ba2'], line=dict(color='white', width=3))
        )])
        
        fig.update_layout(
            title={
                'text': 'Your Energy Breakdown',
                'x': 0.5,
                'font': {'size': 24}
            },
            height=500,
            showlegend=False,
            annotations=[dict(text=f'{data["total"]:.1f}<br>Total Units', 
                            x=0.5, y=0.5, font_size=22, showarrow=False)]
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col_pie2:
        st.markdown(f"""
        <div class="simple-card">
            <h3>💰 What This Costs You</h3>
            <p class="simple-text"><strong>Daily Cost:</strong> ₹{data['total'] * 8:.0f}</p>
            <p class="simple-text"><strong>Monthly Cost:</strong> ₹{data['total'] * 30 * 8:.0f}</p>
            <p class="simple-text"><strong>Yearly Cost:</strong> ₹{data['total'] * 365 * 8:.0f}</p>
            <p class="secondary-text">*Based on ₹8 per unit</p>
        </div>
        
        <div class="simple-card">
            <h3>📋 Simple Breakdown</h3>
            <p class="simple-text"><strong>Basic needs:</strong> {data['base']:.1f} units</p>
            <p class="secondary-text">Lights, fans, phone charging</p>
            <p class="simple-text"><strong>Your appliances:</strong> {data['appliances']:.1f} units</p>
            <p class="secondary-text">AC, fridge, washing machine</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Simple tips
    st.markdown('<div class="section-title">💡 Easy Ways to Save Energy</div>', unsafe_allow_html=True)
    
    tip_col1, tip_col2, tip_col3 = st.columns(3)
    
    with tip_col1:
        st.markdown("""
        <div class="tip-card">
            <h4>❄️ Save on AC</h4>
            <p class="simple-text">• Set to 25°C instead of 18°C</p>
            <p class="simple-text">• Use fans with AC</p>
            <p class="simple-text">• Turn off when not home</p>
            <p class="simple-text"><strong>Save up to ₹500/month</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    with tip_col2:
        st.markdown("""
        <div class="tip-card">
            <h4>🧊 Save on Fridge</h4>
            <p class="simple-text">• Don't put hot food inside</p>
            <p class="simple-text">• Keep it 3/4 full</p>
            <p class="simple-text">• Clean the back coils</p>
            <p class="simple-text"><strong>Save up to ₹200/month</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    with tip_col3:
        st.markdown("""
        <div class="tip-card">
            <h4>👕 Save on Washing</h4>
            <p class="simple-text">• Wash full loads only</p>
            <p class="simple-text">• Use cold water</p>
            <p class="simple-text">• Air dry clothes</p>
            <p class="simple-text"><strong>Save up to ₹300/month</strong></p>
        </div>
        """, unsafe_allow_html=True)

# Simple footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f0f2f6 0%, #ffffff 100%); border-radius: 12px; margin-top: 2rem;">
    <h3 style="color: #667eea;">⚡ Energy Calculator</h3>
    <p style="color: #666;">Simple tool to understand your electricity usage</p>
    <p style="color: #888; font-size: 0.9rem;">Save energy, save money, help the planet! 🌍</p>
</div>
""", unsafe_allow_html=True)