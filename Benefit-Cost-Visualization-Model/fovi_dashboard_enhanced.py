"""
Florida Olympic Viability Index (FOVI) Dashboard - Enhanced Edition
Comprehensive economic impact analysis with full benefit accounting
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Florida Olympic Viability Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# McKinsey-style CSS
st.markdown("""
<style>
    /* McKinsey Color Palette */
    :root {
        --mckinsey-navy: #003366;
        --mckinsey-teal: #00A8B5;
        --mckinsey-gray: #5F6062;
        --mckinsey-light-gray: #E6E7E8;
        --mckinsey-white: #FFFFFF;
        --mckinsey-accent: #FF6B35;
    }
    
    /* Main Background */
    .main {
        background-color: #FFFFFF;
    }
    
    /* Headers - McKinsey style */
    .main-header {
        font-family: 'Arial', 'Helvetica', sans-serif;
        font-size: 2.2rem;
        font-weight: 600;
        color: #003366;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    .sub-header {
        font-family: 'Arial', 'Helvetica', sans-serif;
        font-size: 1.1rem;
        font-weight: 400;
        color: #5F6062;
        margin-bottom: 2rem;
    }
    
    /* Metric Cards - McKinsey style */
    .metric-card {
        background: #FFFFFF;
        padding: 1.5rem;
        border-radius: 4px;
        border-left: 4px solid #003366;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
    }
    
    .metric-card.viable {
        border-left-color: #00A8B5;
        background: linear-gradient(to right, #f0fffe 0%, #FFFFFF 100%);
    }
    
    .metric-card.not-viable {
        border-left-color: #FF6B35;
        background: linear-gradient(to right, #fff5f2 0%, #FFFFFF 100%);
    }
    
    /* Decision Banner */
    .decision-banner {
        font-family: 'Arial', 'Helvetica', sans-serif;
        font-size: 1.8rem;
        font-weight: 600;
        padding: 2rem;
        border-radius: 4px;
        text-align: center;
        margin: 2rem 0;
        letter-spacing: 0.5px;
    }
    
    .decision-banner.viable {
        background: linear-gradient(135deg, #00A8B5 0%, #00C6D7 100%);
        color: white;
        border: none;
    }
    
    .decision-banner.not-viable {
        background: linear-gradient(135deg, #5F6062 0%, #7F8082 100%);
        color: white;
        border: none;
    }
    
    /* Section Headers */
    .section-header {
        font-family: 'Arial', 'Helvetica', sans-serif;
        font-size: 1.3rem;
        font-weight: 600;
        color: #003366;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #E6E7E8;
    }
    
    /* Info boxes */
    .info-box {
        background: #F8F9FA;
        border-left: 3px solid #00A8B5;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 2px;
        font-family: 'Arial', 'Helvetica', sans-serif;
        font-size: 0.9rem;
        color: #5F6062;
    }
    
    /* Data source footer */
    .data-source {
        font-family: 'Arial', 'Helvetica', sans-serif;
        font-size: 0.75rem;
        color: #A0A0A0;
        font-style: italic;
        margin-top: 0.5rem;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Arial', 'Helvetica', sans-serif;
        font-weight: 500;
        color: #5F6062;
        background-color: #F8F9FA;
        border-radius: 4px 4px 0 0;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #003366;
        color: white;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #F8F9FA;
    }
    
    /* Remove Streamlit branding for professional look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Professional metric styling */
    [data-testid="stMetricValue"] {
        font-family: 'Arial', 'Helvetica', sans-serif;
        font-size: 1.8rem;
        font-weight: 600;
        color: #003366;
    }
    
    [data-testid="stMetricLabel"] {
        font-family: 'Arial', 'Helvetica', sans-serif;
        font-size: 0.9rem;
        font-weight: 500;
        color: #5F6062;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Mobile Responsive Styles */
    @media (max-width: 768px) {
        /* Headers */
        .main-header {
            font-size: 1.5rem;
            margin-bottom: 0.5rem;
        }
        
        .sub-header {
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }
        
        /* Decision banner */
        .decision-banner {
            font-size: 1.2rem;
            padding: 1rem;
            margin: 1rem 0;
        }
        
        /* Metric cards */
        .metric-card {
            padding: 1rem;
            margin-bottom: 0.75rem;
        }
        
        [data-testid="stMetricValue"] {
            font-size: 1.3rem;
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 0.75rem;
        }
        
        /* Columns - stack vertically on mobile */
        [data-testid="column"] {
            width: 100% !important;
            flex: 100% !important;
            min-width: 100% !important;
            margin-bottom: 1rem;
        }
        
        /* Plotly charts - make them scrollable if needed */
        .js-plotly-plot {
            width: 100% !important;
            overflow-x: auto;
        }
        
        /* Sidebar full width on mobile when open */
        section[data-testid="stSidebar"] {
            width: 100% !important;
        }
        
        /* Tabs text smaller */
        .stTabs [data-baseweb="tab"] {
            font-size: 0.85rem;
            padding: 0.5rem 0.75rem;
        }
        
        /* Tables responsive */
        table {
            font-size: 0.75rem;
        }
        
        /* Expander headers */
        .streamlit-expanderHeader {
            font-size: 0.9rem;
        }
    }
    
    /* Small mobile devices */
    @media (max-width: 480px) {
        .main-header {
            font-size: 1.2rem;
        }
        
        .decision-banner {
            font-size: 1rem;
            padding: 0.75rem;
        }
        
        [data-testid="stMetricValue"] {
            font-size: 1.1rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            font-size: 0.75rem;
            padding: 0.4rem 0.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# McKinsey color palette for charts
MCKINSEY_COLORS = {
    'primary': '#003366',
    'secondary': '#00A8B5',
    'tertiary': '#5F6062',
    'accent': '#FF6B35',
    'success': '#00A8B5',
    'warning': '#FFB81C',
    'light_gray': '#E6E7E8',
    'palette': ['#003366', '#00A8B5', '#5F6062', '#FF6B35', '#FFB81C', '#7FCDCD']
}

def load_gdp_data():
    """Load Florida GDP data"""
    try:
        df = pd.read_csv('Growth/Industries/SAGDP8_FL_1997_2024.csv')
        florida_gdp = df[df['Description'] == 'All industry total '].iloc[0]
        years = [col for col in df.columns if col.isdigit()]
        gdp_values = {int(year): float(florida_gdp[year]) for year in years}
        
        # Calculate CAGR
        recent_years = sorted([y for y in gdp_values.keys() if y >= 2019])
        if len(recent_years) >= 2:
            start_val = gdp_values[recent_years[0]]
            end_val = gdp_values[recent_years[-1]]
            years_span = recent_years[-1] - recent_years[0]
            cagr = (end_val / start_val) ** (1/years_span) - 1
            return gdp_values, cagr
        return gdp_values, 0.0456
    except:
        return {2020: 105.677, 2021: 115.548, 2022: 122.768, 2023: 129.021, 2024: 133.247}, 0.0456

def calculate_comprehensive_tourism(baseline_visitors, uplift_pct, crowd_out_pct, spend_per_visitor,
                                   tax_rate, legacy_years, legacy_uplift, discount_rate,
                                   olympic_year, current_year, inflation_rate, tourism_growth_rate):
    """
    Enhanced tourism calculation with timeline and growth adjustments
    """
    years_until_games = olympic_year - current_year
    
    # Project baseline to Olympic year
    future_baseline = baseline_visitors * ((1 + tourism_growth_rate) ** years_until_games)
    future_spend = spend_per_visitor * ((1 + inflation_rate) ** years_until_games)
    
    # Games year calculation
    games_uplift = future_baseline * uplift_pct
    net_visitors = games_uplift * (1 - crowd_out_pct)
    incremental_spending = net_visitors * future_spend
    games_year_tax_nominal = (incremental_spending * tax_rate) / 1_000_000
    
    # Discount back to present
    games_year_tax_pv = games_year_tax_nominal / ((1 + discount_rate) ** years_until_games)
    
    # Legacy calculation
    legacy_pv = 0
    legacy_breakdown = []
    
    for year in range(1, legacy_years + 1):
        decay_factor = np.exp(-0.2 * year)
        legacy_visitors = net_visitors * legacy_uplift * decay_factor
        legacy_spending = legacy_visitors * future_spend * ((1 + inflation_rate) ** year)
        legacy_tax_nominal = (legacy_spending * tax_rate) / 1_000_000
        
        actual_year_from_now = years_until_games + year
        pv_tax = legacy_tax_nominal / ((1 + discount_rate) ** actual_year_from_now)
        legacy_pv += pv_tax
        
        legacy_breakdown.append({
            'Year': f'+{year}',
            'Visitors': legacy_visitors,
            'Tax_PV': pv_tax
        })
    
    return {
        'games_year_tax_pv': games_year_tax_pv,
        'games_year_tax_nominal': games_year_tax_nominal,
        'legacy_pv': legacy_pv,
        'total_tax_pv': games_year_tax_pv + legacy_pv,
        'future_baseline': future_baseline,
        'legacy_breakdown': legacy_breakdown
    }

def calculate_property_tax_benefits(median_home_value, total_properties, appreciation_pct,
                                   affected_pct, property_tax_rate, olympic_year, current_year,
                                   discount_rate, benefit_years):
    """
    Calculate property value appreciation and resulting tax revenue
    Source: Barcelona (150% in Olympic zones), Atlanta (20-30% citywide), London (40% in Olympic boroughs)
    """
    years_until_games = olympic_year - current_year
    
    value_increase = (total_properties * affected_pct * median_home_value * appreciation_pct)
    annual_tax_increase = (value_increase * property_tax_rate) / 1_000_000
    
    total_pv = 0
    # Benefits start in Olympic year and continue
    for year in range(benefit_years):
        actual_year = years_until_games + year
        year_benefit = annual_tax_increase / ((1 + discount_rate) ** actual_year)
        total_pv += year_benefit
    
    return {
        'annual_tax': annual_tax_increase,
        'total_pv': total_pv,
        'value_increase': value_increase / 1_000_000
    }

def calculate_corporate_relocation_benefits(num_companies, avg_tax_per_company, olympic_year,
                                           current_year, discount_rate, benefit_years,
                                           construction_tax_one_time):
    """
    Corporate relocations and business development
    Source: Barcelona (500+ companies), Atlanta (300+ HQs), London (major financial services growth)
    """
    years_until_games = olympic_year - current_year
    annual_corporate_tax = (num_companies * avg_tax_per_company) / 1_000_000
    
    # One-time construction phase tax (in Olympic year)
    construction_pv = construction_tax_one_time / ((1 + discount_rate) ** years_until_games)
    
    # Ongoing annual tax
    ongoing_pv = 0
    for year in range(benefit_years):
        actual_year = years_until_games + year + 1  # Starts year after Olympics
        year_benefit = annual_corporate_tax / ((1 + discount_rate) ** actual_year)
        ongoing_pv += year_benefit
    
    return {
        'annual_tax': annual_corporate_tax,
        'total_pv': construction_pv + ongoing_pv,
        'construction_pv': construction_pv,
        'ongoing_pv': ongoing_pv
    }

def calculate_construction_sales_tax(public_spending, sales_tax_rate, olympic_year, current_year, discount_rate):
    """
    Sales tax revenue from construction spending - offsets public cost
    This is REAL revenue Florida receives during construction
    """
    years_until_games = olympic_year - current_year
    
    # Spread construction over 6 years before Olympics
    construction_start = max(0, years_until_games - 6)
    annual_spending = public_spending / 6
    annual_sales_tax = annual_spending * sales_tax_rate
    
    total_pv = 0
    for year in range(6):
        actual_year = construction_start + year
        if actual_year >= 0:
            year_tax = annual_sales_tax / ((1 + discount_rate) ** actual_year)
            total_pv += year_tax
    
    return {
        'total_tax': public_spending * sales_tax_rate,
        'total_pv': total_pv
    }

def calculate_major_events_pipeline(events_per_year, avg_tax_per_event, olympic_year, current_year,
                                   discount_rate, benefit_years):
    """
    Super Bowls, World Cups, NCAA championships enabled by Olympic venues
    Source: Miami Super Bowl $572M impact, Tampa $407M impact, ~$35M tax revenue per event
    """
    years_until_games = olympic_year - current_year
    
    total_pv = 0
    for year in range(benefit_years):
        actual_year = years_until_games + year + 1
        annual_revenue = (events_per_year * avg_tax_per_event)
        year_pv = annual_revenue / ((1 + discount_rate) ** actual_year)
        total_pv += year_pv
    
    return {
        'annual_revenue': events_per_year * avg_tax_per_event,
        'total_pv': total_pv,
        'total_events': events_per_year * benefit_years
    }

def calculate_convention_business(baseline_convention_revenue, increase_pct, tax_rate, olympic_year,
                                 current_year, discount_rate, benefit_years):
    """
    Convention and conference business growth
    Source: Barcelona convention attendees 100K→2.5M (25x growth), Atlanta $1B+ annual impact
    """
    years_until_games = olympic_year - current_year
    additional_revenue = baseline_convention_revenue * increase_pct
    annual_tax = additional_revenue * tax_rate
    
    total_pv = 0
    for year in range(benefit_years):
        actual_year = years_until_games + year + 1
        year_tax = annual_tax / ((1 + discount_rate) ** actual_year)
        total_pv += year_tax
    
    return {
        'annual_tax': annual_tax,
        'total_pv': total_pv,
        'additional_revenue': additional_revenue
    }

def calculate_economic_roi(public_spending, tax_benefit_pv, gdp_multiplier, employment_multiplier):
    """Standard ROI calculation"""
    roi = tax_benefit_pv / public_spending if public_spending > 0 else 0
    gdp_impact = public_spending * gdp_multiplier
    jobs_created = public_spending * employment_multiplier
    
    return {
        'roi': roi,
        'gdp_impact': gdp_impact,
        'jobs_created': jobs_created
    }

def calculate_infrastructure_npv(transit_benefits, resilience_benefits, incremental_costs,
                                years, discount_rate, olympic_year, current_year):
    """Infrastructure NPV with proper timeline"""
    years_until_games = olympic_year - current_year
    npv = 0
    
    for year in range(years + 1):
        actual_year = years_until_games + year
        utilization_factor = min(1.0, 0.3 + (year * 0.035))
        
        transit_benefit = transit_benefits * utilization_factor
        resilience_benefit = resilience_benefits * utilization_factor
        
        if year <= 5:
            cost = incremental_costs * (0.3 if year <= 2 else 0.1)
        else:
            cost = incremental_costs * 0.02
        
        net_benefit = transit_benefit + resilience_benefit - cost
        pv_benefit = net_benefit / ((1 + discount_rate) ** actual_year)
        npv += pv_benefit
    
    return {'npv': npv}

def calculate_migration_value(net_migrants_annual, fiscal_contribution, years, discount_rate,
                             olympic_year, current_year):
    """Migration value with proper timeline"""
    years_until_games = olympic_year - current_year
    total_pv = 0
    
    for year in range(1, years + 1):
        actual_year = years_until_games + year
        cumulative_migrants = net_migrants_annual * year * 1.05
        annual_contribution = (cumulative_migrants * fiscal_contribution) / 1_000_000
        pv_contribution = annual_contribution / ((1 + discount_rate) ** actual_year)
        total_pv += pv_contribution
    
    return {'total_pv': total_pv}

def normalize_score(value, min_val, max_val):
    """Normalize to [0,1]"""
    if max_val == min_val:
        return 0.5
    normalized = (value - min_val) / (max_val - min_val)
    return max(0, min(1, normalized))

def calculate_bcr(total_benefits, total_costs):
    """
    Calculate Benefit-Cost Ratio (BCR)
    BCR = Total Benefits / Total Costs
    
    Interpretation:
    - BCR < 1.0: Not viable (costs exceed benefits)
    - BCR = 1.0: Break-even
    - BCR > 1.0: Viable (benefits exceed costs)
    """
    if total_costs <= 0:
        return 0.0
    return total_benefits / total_costs

def get_bcr_status(bcr):
    """Get viability status based on BCR"""
    if bcr < 1.0:
        return "❌ NOT VIABLE", MCKINSEY_COLORS['accent']
    elif bcr < 1.2:
        return "⚠️ MARGINAL", MCKINSEY_COLORS['warning']
    elif bcr < 1.5:
        return "✓ VIABLE", MCKINSEY_COLORS['success']
    else:
        return "✓✓ HIGHLY VIABLE", MCKINSEY_COLORS['success']

def create_mckinsey_chart(fig):
    """Apply McKinsey styling to plotly charts"""
    fig.update_layout(
        font=dict(family="Arial, Helvetica, sans-serif", size=12, color=MCKINSEY_COLORS['tertiary']),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=50, r=50, t=50, b=50),
        title_font=dict(size=16, color=MCKINSEY_COLORS['primary'], family="Arial, Helvetica, sans-serif"),
        showlegend=True,
        legend=dict(
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor=MCKINSEY_COLORS['light_gray'],
            borderwidth=1
        ),
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor=MCKINSEY_COLORS['light_gray'],
            showline=True,
            linewidth=1,
            linecolor=MCKINSEY_COLORS['light_gray']
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor=MCKINSEY_COLORS['light_gray'],
            showline=True,
            linewidth=1,
            linecolor=MCKINSEY_COLORS['light_gray']
        ),
        autosize=True,
        height=None
    )
    
    # Mobile-specific adjustments
    fig.update_layout(
        modebar=dict(orientation='v', bgcolor='rgba(255,255,255,0.7)'),
        dragmode='pan'
    )
    
    return fig

# Main application
def main():
    # Header
    st.markdown('<div class="main-header">Florida Olympic Games Economic Viability Analysis</div>', 
                unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Comprehensive fiscal impact assessment with historical validation</div>', 
                unsafe_allow_html=True)
    
    # Load economic data
    gdp_data, gdp_cagr = load_gdp_data()
    
    # Sidebar
    st.sidebar.title("Analysis Parameters")
    
    # Analysis Mode
    st.sidebar.markdown("### Analysis Mode")
    analysis_mode = st.sidebar.radio(
        "Select analysis scope:",
        ["Basic Tourism Model", "Comprehensive Benefits Model", "Full Economic Impact"],
        index=2,
        help="Basic: Tourism only | Comprehensive: +Property, Corporate, Events | Full: All parameters + timeline"
    )
    
    include_comprehensive = analysis_mode in ["Comprehensive Benefits Model", "Full Economic Impact"]
    include_timeline = analysis_mode == "Full Economic Impact"
    
    # Timeline Parameters
    if include_timeline:
        st.sidebar.markdown("### Timeline")
        current_year = 2024
        olympic_year = st.sidebar.number_input(
            "Olympic Games Year",
            min_value=2032, max_value=2048, value=2036, step=2,
            help="Expected year of hosting"
        )
        years_until = olympic_year - current_year
        st.sidebar.info(f"📅 {years_until} years until Games")
        
        inflation_rate = st.sidebar.slider(
            "Inflation Rate (%)",
            min_value=0.01, max_value=0.05, value=0.03, step=0.005,
            format="%.1f%%"
        )
        
        tourism_growth_rate = st.sidebar.slider(
            "Tourism Growth Rate (%)",
            min_value=0.0, max_value=0.05, value=0.025, step=0.005,
            format="%.1f%%"
        )
    else:
        current_year = 2024
        olympic_year = 2024
        inflation_rate = 0.03
        tourism_growth_rate = 0.025
    
    # Tourism Parameters
    st.sidebar.markdown("### Core Tourism Parameters")
    baseline_visitors = st.sidebar.number_input(
        "Baseline Annual Visitors (millions)",
        min_value=50.0, max_value=200.0, value=140.0, step=5.0
    )
    
    uplift_pct = st.sidebar.slider(
        "Visitor Uplift (%)",
        min_value=0.0, max_value=0.30, value=0.10, step=0.01,
        format="%.0f%%"
    )
    
    crowd_out_pct = st.sidebar.slider(
        "Crowd-out Effect (%)",
        min_value=0.0, max_value=0.80, value=0.50, step=0.05,
        format="%.0f%%"
    )
    
    spend_per_visitor = st.sidebar.number_input(
        "Spend per Visitor ($)",
        min_value=500, max_value=5000, value=1200, step=50
    )
    
    tax_rate = st.sidebar.slider(
        "Effective Tax Rate (%)",
        min_value=0.03, max_value=0.12, value=0.065, step=0.005,
        format="%.1f%%"
    )
    
    legacy_uplift = st.sidebar.slider(
        "Legacy Tourism Uplift (%)",
        min_value=0.0, max_value=0.30, value=0.15, step=0.01,
        format="%.0f%%"
    )
    
    legacy_years = st.sidebar.slider(
        "Legacy Duration (years)",
        min_value=3, max_value=10, value=5
    )
    
    # Comprehensive Benefits Parameters
    if include_comprehensive:
        st.sidebar.markdown("### Comprehensive Benefits")
        
        with st.sidebar.expander("🏠 Property Value Effects", expanded=False):
            st.caption("Historical: Barcelona +150% (zones), Atlanta +20-30%, London +40%")
            property_appreciation = st.slider(
                "Property Appreciation (%)",
                min_value=0.0, max_value=0.30, value=0.10, step=0.01,
                format="%.0f%%",
                key="prop_app"
            )
            affected_properties_pct = st.slider(
                "Properties Affected (%)",
                min_value=0.01, max_value=0.20, value=0.05, step=0.01,
                format="%.0f%%",
                key="prop_aff"
            )
        
        with st.sidebar.expander("🏢 Corporate Relocations", expanded=False):
            st.caption("Historical: Barcelona 500+, Atlanta 300+, London major growth")
            num_companies = st.number_input(
                "Companies Relocated",
                min_value=0, max_value=1000, value=200, step=25,
                key="corp_num"
            )
            avg_corp_tax = st.number_input(
                "Avg Tax per Company ($K/year)",
                min_value=500, max_value=5000, value=2000, step=100,
                key="corp_tax"
            ) * 1000
        
        with st.sidebar.expander("🏟️ Major Events Pipeline", expanded=False):
            st.caption("Super Bowls, World Cups, championships ($35M tax/event avg)")
            events_per_year = st.slider(
                "Major Events per Year",
                min_value=0.0, max_value=5.0, value=0.5, step=0.5,
                key="events_year"
            )
            avg_event_tax = st.number_input(
                "Avg Tax per Event ($M)",
                min_value=10, max_value=100, value=35, step=5,
                key="event_tax"
            )
        
        with st.sidebar.expander("🎤 Convention Business", expanded=False):
            st.caption("Barcelona: 100K→2.5M attendees (25x), Atlanta $1B+ impact")
            convention_baseline = st.number_input(
                "Baseline Convention Revenue ($M/year)",
                min_value=1000, max_value=10000, value=3000, step=500,
                key="conv_base"
            )
            convention_increase = st.slider(
                "Convention Increase (%)",
                min_value=0.0, max_value=1.0, value=0.30, step=0.05,
                format="%.0f%%",
                key="conv_inc"
            )
    else:
        property_appreciation = 0.0
        affected_properties_pct = 0.0
        num_companies = 0
        avg_corp_tax = 0
        events_per_year = 0.0
        avg_event_tax = 0
        convention_baseline = 0
        convention_increase = 0.0
    
    # Economic Parameters
    st.sidebar.markdown("### Economic Parameters")
    public_spending = st.sidebar.number_input(
        "Public Spending ($M)",
        min_value=5000, max_value=20000, value=10000, step=500
    )
    
    private_share = st.sidebar.slider(
        "Private Investment Share (%)",
        min_value=0.0, max_value=0.70, value=0.30, step=0.05,
        format="%.0f%%"
    )
    
    gdp_multiplier = st.sidebar.slider(
        "GDP Multiplier",
        min_value=1.0, max_value=3.0, value=1.8, step=0.1
    )
    
    employment_multiplier = st.sidebar.number_input(
        "Jobs per $1M",
        min_value=5, max_value=20, value=12
    )
    
    # Infrastructure
    st.sidebar.markdown("### Infrastructure")
    transit_benefits = st.sidebar.number_input(
        "Transit Benefits ($M/year)",
        min_value=100, max_value=1000, value=350, step=50
    )
    
    resilience_benefits = st.sidebar.number_input(
        "Resilience Benefits ($M/year)",
        min_value=50, max_value=500, value=150, step=25
    )
    
    incremental_costs = st.sidebar.number_input(
        "Incremental Costs ($M)",
        min_value=1000, max_value=8000, value=3000, step=250
    )
    
    infrastructure_years = st.sidebar.slider(
        "Infrastructure Horizon (years)",
        min_value=10, max_value=30, value=20
    )
    
    # Migration
    st.sidebar.markdown("### Migration")
    net_migrants_annual = st.sidebar.number_input(
        "Net Migrants per Year",
        min_value=1000, max_value=50000, value=8000, step=500
    )
    
    fiscal_contribution = st.sidebar.number_input(
        "Fiscal Contribution per Resident ($)",
        min_value=500, max_value=5000, value=1500, step=100
    )
    
    migration_years = st.sidebar.slider(
        "Migration Duration (years)",
        min_value=5, max_value=15, value=10
    )
    
    # Financial
    st.sidebar.markdown("### Financial")
    discount_rate = st.sidebar.slider(
        "Discount Rate (%)",
        min_value=0.02, max_value=0.08, value=0.045, step=0.005,
        format="%.1f%%"
    )
    
    # ==================== CALCULATIONS ====================
    
    # Tourism
    tourism_results = calculate_comprehensive_tourism(
        baseline_visitors * 1_000_000, uplift_pct, crowd_out_pct, spend_per_visitor,
        tax_rate, legacy_years, legacy_uplift, discount_rate,
        olympic_year, current_year, inflation_rate, tourism_growth_rate
    )
    
    # Comprehensive benefits
    if include_comprehensive:
        # Property tax
        property_results = calculate_property_tax_benefits(
            306000, 10_000_000, property_appreciation, affected_properties_pct,
            0.015, olympic_year, current_year, discount_rate, 20
        )
        
        # Corporate relocations
        corporate_results = calculate_corporate_relocation_benefits(
            num_companies, avg_corp_tax, olympic_year, current_year,
            discount_rate, 20, 150
        )
        
        # Construction sales tax
        construction_tax_results = calculate_construction_sales_tax(
            public_spending, 0.06, olympic_year, current_year, discount_rate
        )
        
        # Major events
        events_results = calculate_major_events_pipeline(
            events_per_year, avg_event_tax, olympic_year, current_year,
            discount_rate, 20
        )
        
        # Convention business
        convention_results = calculate_convention_business(
            convention_baseline, convention_increase, tax_rate,
            olympic_year, current_year, discount_rate, 20
        )
    else:
        property_results = {'total_pv': 0, 'annual_tax': 0, 'value_increase': 0}
        corporate_results = {'total_pv': 0, 'annual_tax': 0}
        construction_tax_results = {'total_pv': 0}
        events_results = {'total_pv': 0, 'annual_revenue': 0}
        convention_results = {'total_pv': 0, 'annual_tax': 0}
    
    # Infrastructure
    infrastructure_results = calculate_infrastructure_npv(
        transit_benefits, resilience_benefits, incremental_costs,
        infrastructure_years, discount_rate, olympic_year, current_year
    )
    
    # Migration
    migration_results = calculate_migration_value(
        net_migrants_annual, fiscal_contribution, migration_years,
        discount_rate, olympic_year, current_year
    )
    
    # Economic ROI
    total_tax_benefits = (tourism_results['total_tax_pv'] + 
                          property_results['total_pv'] + 
                          corporate_results['total_pv'] +
                          events_results['total_pv'] +
                          convention_results['total_pv'])
    
    economic_results = calculate_economic_roi(
        public_spending, total_tax_benefits, gdp_multiplier, employment_multiplier
    )
    
    # Calculate net fiscal gain
    total_benefits = (tourism_results['total_tax_pv'] +
                     property_results['total_pv'] +
                     corporate_results['total_pv'] +
                     construction_tax_results['total_pv'] +
                     events_results['total_pv'] +
                     convention_results['total_pv'] +
                     infrastructure_results['npv'] +
                     migration_results['total_pv'])
    
    net_public_cost = (public_spending * (1 - private_share)) - construction_tax_results['total_pv']
    net_fiscal_gain = total_benefits - net_public_cost
    
    # Calculate Benefit-Cost Ratio (BCR) - PRIMARY VIABILITY METRIC
    bcr = calculate_bcr(total_benefits, net_public_cost)
    viability_status, status_color = get_bcr_status(bcr)
    
    # Component contributions
    tourism_contribution = tourism_results['total_tax_pv']
    property_contribution = property_results['total_pv']
    corporate_contribution = corporate_results['total_pv']
    infrastructure_contribution = infrastructure_results['npv']
    migration_contribution = migration_results['total_pv']
    events_contribution = events_results['total_pv']
    convention_contribution = convention_results['total_pv']
    
    # Legacy FOVI calculation (for informational purposes only)
    tourism_score = normalize_score(tourism_results['total_tax_pv'], 0, 15000)
    economic_score = normalize_score(economic_results['roi'], 0.5, 2.0)
    infrastructure_score = normalize_score(infrastructure_results['npv'], 0, 10000)
    migration_score = normalize_score(migration_results['total_pv'], 0, 5000)
    
    if include_comprehensive:
        total_revenue_benefits = (tourism_results['total_tax_pv'] + 
                                 property_results['total_pv'] + 
                                 corporate_results['total_pv'] +
                                 events_results['total_pv'] +
                                 convention_results['total_pv'])
        enhanced_tourism_score = normalize_score(total_revenue_benefits, 0, 20000)
    else:
        enhanced_tourism_score = tourism_score
    
    fovi_score = (0.3 * enhanced_tourism_score + 
                  0.3 * economic_score + 
                  0.25 * infrastructure_score + 
                  0.15 * migration_score)
    
    is_viable = bcr >= 1.0
    
    # ==================== DISPLAY ====================
    
    # Decision Banner
    st.markdown("---")
    decision_class = "viable" if is_viable else "not-viable"
    decision_text = f"{viability_status}" if is_viable else viability_status
    
    st.markdown(f"""
    <div class="decision-banner {decision_class}">
        BENEFIT-COST RATIO: {bcr:.2f} → {decision_text}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    <b>BCR Interpretation:</b> BCR < 1.0 = Not Viable | BCR = 1.0 = Break-Even | BCR > 1.0 = Viable | BCR > 1.5 = Highly Viable<br>
    <i>Standard used by World Bank, OECD, and U.S. OMB for infrastructure assessment</i>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📊 Benefit-Cost Ratio",
            f"{bcr:.2f}",
            f"{viability_status}",
            delta_color="normal" if bcr >= 1.0 else "inverse"
        )
        st.markdown('<p class="data-source">Primary viability metric</p>', unsafe_allow_html=True)
    
    with col2:
        st.metric(
            "Net Fiscal Gain",
            f"${net_fiscal_gain:,.0f}M",
            f"{'Surplus' if net_fiscal_gain >= 0 else 'Deficit'}",
            delta_color="normal" if net_fiscal_gain >= 0 else "inverse"
        )
        st.markdown('<p class="data-source">Benefits - Costs (PV)</p>', unsafe_allow_html=True)
    
    with col3:
        st.metric(
            "Total Benefits",
            f"${total_benefits:,.0f}M",
            f"vs ${net_public_cost:,.0f}M Cost"
        )
        st.markdown('<p class="data-source">All revenue streams (PV)</p>', unsafe_allow_html=True)
    
    with col4:
        st.metric(
            "GDP Impact",
            f"${economic_results['gdp_impact']:,.0f}M",
            f"{economic_results['jobs_created']:,.0f} jobs"
        )
        st.markdown(f'<p class="data-source">{gdp_multiplier}x multiplier applied</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # BCR Breakdown by Component
    st.markdown('<div class="section-header">BCR Component Analysis</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    <b>How Benefits Combine to Create BCR</b><br>
    Each revenue stream contributes to the total benefit pool. BCR shows how much value each dollar of public investment generates.
    </div>
    """, unsafe_allow_html=True)
    
    # Component BCR contributions
    st.markdown("### Benefit Components (Individual BCR Contributions)")
    
    component_bcr_data = []
    if tourism_contribution > 1:
        component_bcr_data.append(("Core Tourism Revenue", tourism_contribution, tourism_contribution / net_public_cost))
    if property_contribution > 1:
        component_bcr_data.append(("Property Tax Growth", property_contribution, property_contribution / net_public_cost))
    if corporate_contribution > 1:
        component_bcr_data.append(("Corporate Relocations", corporate_contribution, corporate_contribution / net_public_cost))
    if infrastructure_contribution > 1:
        component_bcr_data.append(("Infrastructure Value", infrastructure_contribution, infrastructure_contribution / net_public_cost))
    if migration_contribution > 1:
        component_bcr_data.append(("Migration Benefits", migration_contribution, migration_contribution / net_public_cost))
    if events_contribution > 1:
        component_bcr_data.append(("Major Events Pipeline", events_contribution, events_contribution / net_public_cost))
    if convention_contribution > 1:
        component_bcr_data.append(("Convention Business", convention_contribution, convention_contribution / net_public_cost))
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown("**Component**")
    with col2:
        st.markdown("**Benefit ($M)**")
    with col3:
        st.markdown("**Individual BCR**")
    
    for comp, benefit, comp_bcr in component_bcr_data:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"• {comp}")
        with col2:
            st.markdown(f"${benefit:,.0f}M")
        with col3:
            st.markdown(f"{comp_bcr:.3f}")
    
    st.markdown("---")
    st.markdown(f"**COMBINED BCR: {bcr:.2f}** (Sum of all benefits ÷ Net public cost)")
    st.markdown("---")
    
    # Benefits Breakdown
    st.markdown('<div class="section-header">Benefit-Cost Analysis</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    <b>Present Value Methodology:</b> All future cash flows discounted to 2024 using 4.5% rate (Florida Treasury standard).
    Benefits occur {}-{} (Games year through legacy period). Costs spread over construction phase.
    </div>
    """.format(olympic_year, olympic_year + 20), unsafe_allow_html=True)
    
    benefit_data = {
        'Category': [],
        'Amount ($M)': [],
        'Share (%)': []
    }
    
    categories = [
        ('Core Tourism Revenue', tourism_results['total_tax_pv']),
        ('Property Tax Growth', property_results['total_pv']),
        ('Corporate Relocations', corporate_results['total_pv']),
        ('Construction Tax Offset', construction_tax_results['total_pv']),
        ('Major Events Pipeline', events_results['total_pv']),
        ('Convention Business', convention_results['total_pv']),
        ('Infrastructure NPV', infrastructure_results['npv']),
        ('Migration Value', migration_results['total_pv'])
    ]
    
    # Only include non-zero categories
    for cat, amt in categories:
        if amt > 1.0:  # More than $1M
            benefit_data['Category'].append(cat)
            benefit_data['Amount ($M)'].append(amt)
            benefit_data['Share (%)'].append((amt / total_benefits * 100) if total_benefits > 1 else 0)
    
    # Benefits vs Costs Comparison
    st.markdown("### Benefits vs. Costs (Present Value to 2024)")
    
    # Create comparison dataframe
    comparison_df = pd.DataFrame(benefit_data)
    
    if len(comparison_df) > 0:
        # Add better formatting
        comparison_df['Amount'] = comparison_df['Amount ($M)'].apply(lambda x: f"${x:,.0f}M")
        comparison_df['Percentage'] = comparison_df['Share (%)'].apply(lambda x: f"{x:.1f}%")
        comparison_df = comparison_df[['Category', 'Amount', 'Percentage']]
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Horizontal bar chart - better for comparing values
            fig = go.Figure()
            
            # Sort by amount for better readability
            sorted_idx = sorted(range(len(benefit_data['Amount ($M)'])), 
                              key=lambda i: benefit_data['Amount ($M)'][i], reverse=True)
            
            sorted_categories = [benefit_data['Category'][i] for i in sorted_idx]
            sorted_amounts = [benefit_data['Amount ($M)'][i] for i in sorted_idx]
            sorted_shares = [benefit_data['Share (%)'][i] for i in sorted_idx]
            
            fig.add_trace(go.Bar(
                y=sorted_categories,
                x=sorted_amounts,
                orientation='h',
                text=[f"${val:,.0f}M ({share:.1f}%)" for val, share in zip(sorted_amounts, sorted_shares)],
                textposition='outside',
                marker=dict(
                    color=sorted_amounts,
                    colorscale=[[0, MCKINSEY_COLORS['secondary']], [1, MCKINSEY_COLORS['primary']]],
                    showscale=False
                ),
                hovertemplate='<b>%{y}</b><br>Amount: $%{x:,.0f}M<extra></extra>'
            ))
            
            fig.update_layout(
                title="Benefit Components (Ranked by Value)",
                xaxis_title="$ Millions (Present Value)",
                yaxis_title="",
                height=400,
                margin=dict(l=200)
            )
            fig = create_mckinsey_chart(fig)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Benefit Summary")
            st.dataframe(comparison_df, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            st.markdown("**Key Totals:**")
            st.markdown(f"**Total Benefits:** ${total_benefits:,.0f}M")
            st.markdown(f"**Net Public Cost:** ${net_public_cost:,.0f}M")
            st.markdown(f"**Benefit-Cost Ratio:** {total_benefits/net_public_cost:.2f}x" if net_public_cost > 0 else "N/A")
    else:
        st.warning("Enable comprehensive benefits to see detailed breakdown")
    
    # Cost Breakdown
    st.markdown("### Cost Structure")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        cost_data = {
            'Component': ['Gross Public Investment', 'Private Investment Share', 'Construction Tax Credit', 'Net Public Cost'],
            'Amount ($M)': [
                public_spending * (1 - private_share),
                -public_spending * private_share,
                -construction_tax_results['total_pv'],
                net_public_cost
            ],
            'Type': ['cost', 'offset', 'offset', 'net']
        }
        
        cost_df = pd.DataFrame(cost_data)
        
        fig = go.Figure(go.Waterfall(
            name="Costs",
            orientation="v",
            measure=["relative", "relative", "relative", "total"],
            x=cost_df['Component'],
            y=cost_df['Amount ($M)'],
            text=[f"${abs(val):,.0f}M" for val in cost_df['Amount ($M)']],
            textposition="outside",
            connector={"line": {"color": MCKINSEY_COLORS['light_gray']}},
            decreasing={"marker": {"color": MCKINSEY_COLORS['success']}},
            increasing={"marker": {"color": MCKINSEY_COLORS['accent']}},
            totals={"marker": {"color": MCKINSEY_COLORS['primary']}}
        ))
        
        fig.update_layout(
            title="Cost Waterfall: From Gross to Net",
            yaxis_title="$ Millions (Present Value)",
            height=400
        )
        fig = create_mckinsey_chart(fig)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Net position chart
        net_data = pd.DataFrame({
            'Category': ['Total Benefits', 'Net Public Cost', 'Net Fiscal Gain'],
            'Amount': [total_benefits, net_public_cost, net_fiscal_gain],
            'Color': [MCKINSEY_COLORS['success'], MCKINSEY_COLORS['accent'], 
                     MCKINSEY_COLORS['success'] if net_fiscal_gain > 0 else MCKINSEY_COLORS['accent']]
        })
        
        fig = go.Figure(data=[
            go.Bar(
                x=net_data['Category'],
                y=net_data['Amount'],
                text=[f"${val:,.0f}M" for val in net_data['Amount']],
                textposition='outside',
                marker=dict(color=net_data['Color']),
                hovertemplate='<b>%{x}</b><br>$%{y:,.0f}M<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title="Net Fiscal Position",
            yaxis_title="$ Millions (Present Value)",
            height=400,
            showlegend=False
        )
        fig = create_mckinsey_chart(fig)
        st.plotly_chart(fig, use_container_width=True)
    
    # Financial Summary Table
    st.markdown('<div class="section-header">Executive Financial Summary</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    <b>Interpretation Guide:</b><br>
    • <b>Benefit-Cost Ratio > 1.0:</b> Project generates more value than it costs<br>
    • <b>ROI > 1.0x:</b> Tax revenues exceed net public investment<br>
    • <b>Positive Net Fiscal Gain:</b> Government realizes surplus after all costs
    </div>
    """, unsafe_allow_html=True)
    
    financial_summary = pd.DataFrame({
        'Metric': [
            'Total Benefits (PV)',
            'Gross Public Investment',
            'Private Investment (Offset)',
            'Construction Tax Credit (Offset)',
            'Net Public Cost',
            '',
            '📊 BENEFIT-COST RATIO (BCR)',
            'Net Fiscal Gain',
            'Internal Rate of Return',
            'Payback Period (Est.)'
        ],
        'Amount': [
            f"${total_benefits:,.0f}M",
            f"${public_spending * (1 - private_share):,.0f}M",
            f"${public_spending * private_share:,.0f}M",
            f"${construction_tax_results['total_pv']:,.0f}M",
            f"${net_public_cost:,.0f}M",
            "",
            f"{bcr:.2f}",
            f"${net_fiscal_gain:,.0f}M",
            f"{((bcr ** (1/20)) - 1) * 100:.1f}%" if bcr > 0 else "N/A",
            f"{20 / bcr:.1f} years" if bcr > 0 else "Never"
        ],
        'Status': [
            "✓" if total_benefits > 0 else "",
            "",
            "Credit",
            "Credit",
            "",
            "",
            viability_status,
            "✓ Positive" if net_fiscal_gain > 0 else "✗ Negative",
            "✓ Strong" if bcr > 1.5 else ("✓ Moderate" if bcr > 1.2 else "⚠ Weak"),
            "✓ Excellent" if bcr > 2.0 else ("✓ Good" if bcr > 1.5 else "⚠ Extended")
        ]
    })
    
    st.dataframe(financial_summary, use_container_width=True, hide_index=True)
    
    # Methodology Section
    st.markdown('<div class="section-header">Methodology & Assumptions</div>', unsafe_allow_html=True)
    
    method_tab1, method_tab2, method_tab3 = st.tabs(["Calculation Methods", "Data Sources", "Historical Validation"])
    
    with method_tab1:
        st.markdown("""
        ### Key Calculation Methodologies
        
        #### 1. Benefit-Cost Ratio (BCR) - Primary Viability Metric
        ```
        BCR = Total Benefits (PV) / Net Public Cost (PV)
        ```
        <b>Interpretation:</b>
        - BCR < 1.0: Project destroys value (costs > benefits)
        - BCR = 1.0: Break-even point
        - BCR > 1.0: Project creates value (benefits > costs)
        - BCR > 1.5: Strong return on investment
        
        <b>Industry Standards:</b>
        - World Bank: Minimum BCR of 1.0, target 1.5+
        - U.S. OMB Circular A-94: BCR ≥ 1.0 for approval
        - OECD Infrastructure: BCR 1.2-1.5 = acceptable, > 1.5 = excellent
        
        #### 2. Present Value Discounting
        All future cash flows converted to 2024 dollars using:
        ```
        PV = Future Value / (1 + discount_rate)^years
        ```
        - Discount rate: 4.5% (Florida Treasury standard)
        - Timeline: 2024 → {} (Games) → {} (End of analysis)
        
        #### 2. Tourism Revenue
        ```
        Games Year Tax = Net Visitors × Spend per Visitor × Tax Rate
        Net Visitors = Baseline × Uplift% × (1 - Crowd-out%)
        
        Legacy Tax (Years 1-5) = Net Visitors × Legacy% × e^(-0.2×year) × Spend × Tax
        ```
        - Exponential decay models declining interest post-Games
        - Historical precedent: Barcelona sustained 15% uplift for 5+ years
        
        #### 3. Property Tax Effects
        ```
        Annual Property Tax = Properties Affected × Median Value × 
                             Appreciation% × Property Tax Rate
        ```
        - Historical: Barcelona +150% (Olympic zones), Atlanta +20-30%, London +40%
        - Conservative estimate: {}% appreciation on {}% of properties
        
        #### 4. Economic Multipliers
        ```
        GDP Impact = Public Spending × GDP Multiplier
        Jobs = Public Spending × Employment Multiplier
        ```
        - Multipliers from FDOT Macroeconomic Evaluation (2024)
        - Construction: 1.5-1.8x | Mixed: 1.8-2.2x | Services: 1.3-1.5x
        
        #### 5. Total Benefits Calculation
        ```
        Total Benefits = Tourism + Property + Corporate + Construction Tax +
                        Events + Convention + Infrastructure + Migration
        ```
        All components discounted to present value (2024) for consistent comparison.
        
        #### 6. Net Public Cost Calculation
        ```
        Gross Public Investment = Total Spending × (1 - Private Share)
        Construction Tax Offset = Spending × Sales Tax Rate × PV Factor
        Net Public Cost = Gross Investment - Construction Tax Offset
        ```
        Private share reduces government burden; construction generates immediate tax revenue
        """.format(olympic_year, olympic_year + 20, property_appreciation * 100, affected_properties_pct * 100))
    
    with method_tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### Primary Data Sources
            
            **Economic Base Data:**
            - U.S. Bureau of Economic Analysis
              - SAGDP8 Tables (FL GDP 1997-2024)
              - Real GDP Index: {} (2024)
              - 5-year CAGR: {:.2%}
            
            **Tourism Data:**
            - Visit Florida Annual Reports
            - Tourism spending price indices
            - International visitor summaries
            - Baseline: {}M visitors/year
            
            **Fiscal Parameters:**
            - Florida Department of Revenue
            - Sales tax: 6% + local option
            - Property tax: ~1.5% avg effective rate
            - Discount rate: 4.5% (FL Treasury)
            """.format(gdp_data.get(2024, 133.247), gdp_cagr, baseline_visitors))
        
        with col2:
            st.markdown("""
            ### Validation Sources
            
            **Infrastructure:**
            - FDOT Macroeconomic Reports (2024)
            - Economic multipliers validated
            - Employment factors verified
            
            **Demographics:**
            - U.S. Census Bureau
            - State-to-state migration flows
            - FL net migration: 80K-250K/year (2018-2022)
            
            **Housing:**
            - Zillow Home Value Index (ZHVI)
            - Current median: $306,497
            - Used for property tax projections
            
            **Historical Olympics:**
            - Barcelona 1992 Impact Study
            - Atlanta 1996 Economic Review  
            - Sydney 2000 Legacy Report
            - London 2012 Comprehensive Study
            """)
    
    with method_tab3:
        st.markdown("""
        ### Historical Olympic Outcomes (Validation)
        
        This analysis uses conservative estimates based on documented outcomes from previous Olympics:
        """)
        
        validation_data = pd.DataFrame({
            'Parameter': [
                'Property Value Increase',
                'Corporate Relocations',
                'Tourism Legacy Uplift',
                'Convention Business Growth',
                'Major Events Attracted',
                'Economic Multiplier'
            ],
            'Barcelona 1992': [
                '+150% (zones)',
                '500+ companies',
                '+15% (5+ years)',
                '100K → 2.5M (25x)',
                'Ongoing',
                '1.8x'
            ],
            'Atlanta 1996': [
                '+20-30%',
                '300+ HQs',
                '+12% (3 years)',
                '$1B+ annual',
                'Super Bowls, NCAA',
                '1.7x'
            ],
            'London 2012': [
                '+40% (boroughs)',
                'Major FDI growth',
                '+8% (4 years)',
                'Financial services',
                'World Cups, etc.',
                '1.4x'
            ],
            'This Model (Conservative)': [
                f'+{property_appreciation*100:.0f}% ({affected_properties_pct*100:.0f}% properties)',
                f'{num_companies} companies',
                f'+{legacy_uplift*100:.0f}% ({legacy_years} years)',
                f'+{convention_increase*100:.0f}%',
                f'{events_per_year}/year',
                f'{gdp_multiplier}x'
            ]
        })
        
        st.dataframe(validation_data, use_container_width=True, hide_index=True)
        
        st.markdown("""
        **Key Takeaway:** Model parameters are at or below historical precedents, providing conservative estimates 
        of economic impact while maintaining academic rigor and defensibility.
        """)
    
    # Analysis Mode Comparison
    if include_comprehensive:
        st.markdown('<div class="section-header">Analysis Mode Comparison</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
        <b>Transparency Note:</b> Three analysis modes allow stakeholders to evaluate impact under different assumptions. 
        Basic model includes only direct tourism. Comprehensive adds documented secondary effects. Full includes timeline corrections.
        </div>
        """, unsafe_allow_html=True)
        
        basic_benefits = tourism_results['total_tax_pv'] + infrastructure_results['npv'] + migration_results['total_pv']
        basic_net = basic_benefits - net_public_cost
        basic_bcr = calculate_bcr(basic_benefits, net_public_cost)
        
        basic_fovi = (0.3 * tourism_score + 0.3 * normalize_score(basic_benefits/public_spending, 0.5, 2.0) + 
                     0.25 * infrastructure_score + 0.15 * migration_score)
        
        comparison_data = pd.DataFrame({
            'Metric': ['Benefit-Cost Ratio (BCR)', 'Net Fiscal Gain ($M)', 'Total Benefits ($M)', 'Viability'],
            'Basic Tourism Model': [
                f"{basic_bcr:.2f}",
                f"${basic_net:,.0f}",
                f"${basic_benefits:,.0f}",
                "✓ Viable" if basic_bcr >= 1.0 else "✗ Not Viable"
            ],
            'Full Impact Model': [
                f"{bcr:.2f}",
                f"${net_fiscal_gain:,.0f}",
                f"${total_benefits:,.0f}",
                viability_status
            ],
            'Difference': [
                f"+{(bcr - basic_bcr):.2f}",
                f"+${(net_fiscal_gain - basic_net):,.0f}",
                f"+${(total_benefits - basic_benefits):,.0f}",
                f"{'Improved' if bcr > basic_bcr else 'Same'}"
            ]
        })
        
        st.dataframe(comparison_data, use_container_width=True, hide_index=True)
    
    # Data Sources
    st.markdown("---")
    st.markdown('<div class="section-header">Data Sources & Validation</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Economic Data**
        - BEA SAGDP Tables (FL GDP 1997-2024)
        - FDOT Macroeconomic Reports
        - Florida Treasury Guidelines
        """)
    
    with col2:
        st.markdown("""
        **Tourism & Migration**
        - Visit Florida Annual Reports
        - Census Migration Flows
        - Zillow Housing Index
        """)
    
    with col3:
        st.markdown("""
        **Historical Validation**
        - Barcelona 1992 Impact Study
        - Atlanta 1996 Economic Review
        - London 2012 Legacy Report
        """)
    
    st.markdown('<p class="data-source" style="text-align: center; margin-top: 2rem;">Analysis framework developed using FDOT-validated multipliers and historical Olympic economic outcomes</p>', 
                unsafe_allow_html=True)

if __name__ == "__main__":
    main()

