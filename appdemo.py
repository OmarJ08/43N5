import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.colors as mcolors

# Set page configuration
st.set_page_config(page_title="43North Connectivity Matrix", layout="wide")

# Inject custom CSS for 43North Triadic Branding (White, Black, Cyan)
st.markdown(
    """
    <style>
        /* Apply Helvetica safely without breaking Streamlit's internal icon fonts */
        html, body, p, h1, h2, h3, h4, h5, h6, [data-testid="stMetricLabel"], [data-testid="stMetricValue"], .stMarkdown {
            font-family: 'Helvetica', 'Arial', sans-serif !important;
        }
        
        /* 43North Cyan Structural Accents (#00C2CB) */
        h1 { 
            border-bottom: 4px solid #00C2CB; 
            padding-bottom: 10px; 
            margin-bottom: 20px;
        }
        h2 { 
            border-left: 5px solid #00C2CB; 
            padding-left: 10px; 
        }
        
        /* Force the Metric Values to White, Normal Font Size, and allow text wrapping */
        [data-testid="stMetricValue"] { 
            color: #FFFFFF !important; 
            font-weight: 600 !important; 
            font-size: 16px !important; 
            white-space: normal !important; 
        }
        
        /* Force Info Boxes (Pilot Scope) to Transparent 43North Cyan */
        div[data-testid="stAlert"] { 
            background-color: rgba(0, 194, 203, 0.15) !important; 
            border: 1px solid rgba(0, 194, 203, 0.4) !important; 
            border-radius: 6px !important; 
        }
        div[data-testid="stAlert"], div[data-testid="stAlert"] * { 
            color: #FFFFFF !important; 
        }

        /* Force the Sidebar Multiselect Filter Tags to 43North Cyan */
        span[data-baseweb="tag"] {
            background-color: #00C2CB !important;
            color: #FFFFFF !important; 
            border: none !important;
        }
        
        /* Make the 'x' close button on the filter tags white */
        span[data-baseweb="tag"] svg {
            color: #FFFFFF !important;
            fill: #FFFFFF !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title(" 43North Corporate Connectivity Platform")
st.subheader("Proof of Concept: Startup-to-Corporate Pilot Matchmaking Engine")
st.markdown("---")


# =========================================================================
# 1. NEW COMPONENT: RAW INTAKE DATABASE 
# =========================================================================
# Distilled to 5 high-growth corporate focus tracks for the POC
raw_startups_intake = [
    {"Startup": "PhysicianX", "Sector": "MedTech", "ICP": "Enterprise Hospital Networks", "Executive Summary": "PhysicianX is an AI-powered career intelligence and talent acquisition platform designed to combat physician burnout and high turnover. For doctors, it acts as a digital career agent, optimizing CVs, analyzing contracts, and matching them to roles. For enterprise healthcare employers, it bypasses traditional job boards by using generative AI and a proprietary psychometric framework to source physicians validated not just for specialty, but for work environment and team dynamic fit.", "Pilot Ready": "90-day clinical workflow integration.", "compliance_score": 2, "architecture_score": 2, "uptime_score": 2, "data_points": 2, "labor_points": 3},
    {"Startup": "Verivend", "Sector": "FinTech", "ICP": "Private Equity Firms", "Executive Summary": "Verivend serves as the digital infrastructure for private capital markets, providing a painless, paperless way to manage investment syndicates. Operating as a highly secure, tokenized digital ledger, the platform automates B2B invoicing, capital calls, secure distributions, and entity management. It eliminates manual banking bottlenecks and delivers unprecedented transparency and speed for general partners (GPs) and their investors.", "Pilot Ready": "Process B2B invoicing for 10 isolated vendor accounts.", "compliance_score": 3, "architecture_score": 3, "uptime_score": 3, "data_points": 5, "labor_points": 5},
    {"Startup": "Spiky.ai", "Sector": "SalesTech", "ICP": "B2B Enterprise Sales Divisions", "Executive Summary": "Spiky.ai is an AI-powered meeting intelligence platform designed to optimize remote and hybrid commercial revenue teams. By analyzing video conversations in real-time, it generates dynamic battlecards, transcription summaries, active coaching cues, and automated CRM updates. The platform unifies revenue conversations, allowing enterprise sales divisions to rapidly replicate top-performing behaviors, track client sentiment, and close B2B deals faster.", "Pilot Ready": "Analyze conversational analytics data from 20 sales accounts.", "compliance_score": 2, "architecture_score": 3, "uptime_score": 2, "data_points": 2, "labor_points": 5},
    {"Startup": "HiOperator", "Sector": "SupportTech", "ICP": "Enterprise Customer Support", "Executive Summary": "HiOperator scales high-volume customer service and support queues by fusing human agents with proprietary generative AI automation. Their dynamic HiQ platform orchestrates the customer journey across email, SMS, and live chat, accurately resolving Tier 2 and Tier 3 complex issues that break standard chatbots. Operating on a strict Pay-Per-Resolution model, they eliminate ticket backlogs and scale dynamically without requiring enterprise teams to manage offshore call centers.", "Pilot Ready": "Onboard AI agents to resolve 25% of ticket backlogs.", "compliance_score": 2, "architecture_score": 3, "uptime_score": 2, "data_points": 2, "labor_points": 5},
    {"Startup": "HelixIntel", "Sector": "PropTech", "ICP": "Enterprise Facility Managers", "Executive Summary": "HelixIntel provides a cloud-native Computerized Maintenance Management System (CMMS) known as PropertyOS™. The platform transitions enterprises from reactive to predictive maintenance by tracking unlimited equipment inventory, automating work orders, and utilizing IoT sensor integrations to predict equipment failures. By keeping building operations running without interruption, it actively reduces enterprise-wide insurance claims and capital asset depreciation.", "Pilot Ready": "Predictive asset tracking across 50 enterprise utility machines.", "compliance_score": 2, "architecture_score": 3, "uptime_score": 2, "data_points": 2, "labor_points": 5}
]

# Complete, uniform alignment database mapping all sectors for every corporation
# 5 = Primary Match | 4 = Secondary Match | 1 = No Current Alignment
corporates_data = {
    "Kaleida Health": {
        "MedTech": 5, "BioTech": 5, "FinTech": 1, "PropTech": 1, 
        "HRTech": 1, "SalesTech": 1, "SupportTech": 1, "CleanTech": 1, 
        "MaterialsTech": 1, "SupplyChainTech": 1, "FoodTech": 1, "IndustryTech": 1
    },
    "Catholic Health System": {
        "MedTech": 5, "BioTech": 1, "FinTech": 1, "PropTech": 1, 
        "HRTech": 1, "SalesTech": 1, "SupportTech": 1, "CleanTech": 1, 
        "MaterialsTech": 1, "SupplyChainTech": 1, "FoodTech": 1, "IndustryTech": 1
    },
    "Roswell Park": {
        "MedTech": 5, "BioTech": 5, "FinTech": 1, "PropTech": 1, 
        "HRTech": 1, "SalesTech": 1, "SupportTech": 1, "CleanTech": 1, 
        "MaterialsTech": 1, "SupplyChainTech": 1, "FoodTech": 1, "IndustryTech": 1
    },
    "M&T Bank": {
        "MedTech": 1, "BioTech": 1, "FinTech": 5, "PropTech": 5, 
        "HRTech": 1, "SalesTech": 4, "SupportTech": 1, "CleanTech": 1, 
        "MaterialsTech": 1, "SupplyChainTech": 1, "FoodTech": 1, "IndustryTech": 1
    },
    "Citigroup": {
        "MedTech": 1, "BioTech": 1, "FinTech": 5, "PropTech": 1, 
        "HRTech": 1, "SalesTech": 4, "SupportTech": 5, "CleanTech": 1, 
        "MaterialsTech": 1, "SupplyChainTech": 1, "FoodTech": 1, "IndustryTech": 1
    },
    "GEICO": {
        "MedTech": 1, "BioTech": 1, "FinTech": 1, "PropTech": 4, 
        "HRTech": 1, "SalesTech": 4, "SupportTech": 5, "CleanTech": 1, 
        "MaterialsTech": 1, "SupplyChainTech": 1, "FoodTech": 1, "IndustryTech": 1
    },
    "Tops Markets": {
        "MedTech": 1, "BioTech": 1, "FinTech": 1, "PropTech": 1, 
        "HRTech": 4, "SalesTech": 1, "SupportTech": 1, "CleanTech": 4, 
        "MaterialsTech": 1, "SupplyChainTech": 5, "FoodTech": 1, "IndustryTech": 1
    },
    "Wegmans": {
        "MedTech": 1, "BioTech": 1, "FinTech": 1, "PropTech": 1, 
        "HRTech": 4, "SalesTech": 1, "SupportTech": 1, "CleanTech": 1, 
        "MaterialsTech": 1, "SupplyChainTech": 5, "FoodTech": 1, "IndustryTech": 1
    },
    "Delaware North": {
        "MedTech": 1, "BioTech": 1, "FinTech": 1, "PropTech": 1, 
        "HRTech": 5, "SalesTech": 1, "SupportTech": 1, "CleanTech": 1, 
        "MaterialsTech": 1, "SupplyChainTech": 4, "FoodTech": 4, "IndustryTech": 1
    },
    "Moog Inc.": {
        "MedTech": 1, "BioTech": 1, "FinTech": 1, "PropTech": 1, 
        "HRTech": 1, "SalesTech": 1, "SupportTech": 1, "CleanTech": 1, 
        "MaterialsTech": 4, "SupplyChainTech": 1, "FoodTech": 1, "IndustryTech": 5
    },
    "General Motors": {
        "MedTech": 1, "BioTech": 1, "FinTech": 1, "PropTech": 1, 
        "HRTech": 1, "SalesTech": 1, "SupportTech": 1, "CleanTech": 5, 
        "MaterialsTech": 4, "SupplyChainTech": 1, "FoodTech": 1, "IndustryTech": 4
    },
    "Ford Motor Co.": {
        "MedTech": 1, "BioTech": 1, "FinTech": 1, "PropTech": 1, 
        "HRTech": 1, "SalesTech": 1, "SupportTech": 1, "CleanTech": 5, 
        "MaterialsTech": 4, "SupplyChainTech": 1, "FoodTech": 1, "IndustryTech": 4
    },
    "Tesla": {
        "MedTech": 1, "BioTech": 1, "FinTech": 1, "PropTech": 1, 
        "HRTech": 1, "SalesTech": 1, "SupportTech": 1, "CleanTech": 5, 
        "MaterialsTech": 4, "SupplyChainTech": 1, "FoodTech": 1, "IndustryTech": 4
    },
    "Rich Products": {
        "MedTech": 1, "BioTech": 4, "FinTech": 1, "PropTech": 1, 
        "HRTech": 1, "SalesTech": 1, "SupportTech": 1, "CleanTech": 1, 
        "MaterialsTech": 1, "SupplyChainTech": 4, "FoodTech": 5, "IndustryTech": 1
    },
    "Upstate Niagara Cooperative": {
        "MedTech": 1, "BioTech": 1, "FinTech": 1, "PropTech": 1, 
        "HRTech": 1, "SalesTech": 1, "SupportTech": 1, "CleanTech": 1, 
        "MaterialsTech": 1, "SupplyChainTech": 4, "FoodTech": 5, "IndustryTech": 1
    },
    "National Grid": {
        "MedTech": 1, "BioTech": 1, "FinTech": 1, "PropTech": 4, 
        "HRTech": 1, "SalesTech": 1, "SupportTech": 1, "CleanTech": 5, 
        "MaterialsTech": 1, "SupplyChainTech": 1, "FoodTech": 1, "IndustryTech": 4
    },
    "National Fuel Gas Co.": {
        "MedTech": 1, "BioTech": 1, "FinTech": 1, "PropTech": 4, 
        "HRTech": 1, "SalesTech": 1, "SupportTech": 1, "CleanTech": 5, 
        "MaterialsTech": 1, "SupplyChainTech": 1, "FoodTech": 1, "IndustryTech": 1
    }
}
# =========================================================================
# 2. NEW COMPONENT: THE SYSTEMATIC CALCULATION PIPELINE
# =========================================================================
def process_startup_metrics(intake_list):
    processed = []
    for row in intake_list:
        tot_mat = row["compliance_score"] + row["architecture_score"] + row["uptime_score"]
        tech_label = "High" if tot_mat >= 7 else ("Medium" if tot_mat >= 4 else "Low")
        tot_fric = row["data_points"] + row["labor_points"]
        fric_label = "High" if tot_fric >= 7 else ("Medium" if tot_fric >= 3 else "Low")
        
        processed.append({
            "Startup": row["Startup"], "Sector": row["Sector"], "ICP": row["ICP"], 
            "Executive Summary": row["Executive Summary"], 
            "Pilot Ready": row["Pilot Ready"], "Tech Maturity": tech_label, 
            "Integration": fric_label, "Raw Maturity": f"{tot_mat}/9", "Raw Friction": f"{tot_fric}/12"
        })
    return pd.DataFrame(processed)
        

# Execute the engine to create the dynamic DataFrame that feeds the frontend
df_startups = process_startup_metrics(raw_startups_intake)


# =========================================================================
# 3. SIDEBAR CONTROLS (Reads directly from our computed DataFrame)
# =========================================================================
st.sidebar.info("### Filter & Search Capabilities")
# 1. Search by Startup Name
all_company_names = sorted(df_startups["Startup"].unique())
selected_company = st.sidebar.selectbox(
    "Search All Companies (Overrides Filters Below)",
    options=["All Companies"] + all_company_names,
    help="Select a specific startup by name to view their profile immediately, bypassing the category and maturity filters below."
)

# 2. Filter by Corporate Partner 
all_corporate_partners = sorted(list(corporates_data.keys()))
selected_corporate = st.sidebar.selectbox(
    "Filter by Corporate Partner",
    options=["All Corporates"] + all_corporate_partners,
    help="Select a specific corporate partner to isolate their compatibility row in the matrix grid above."
)

st.sidebar.markdown("---")

# 3. Category & Maturity Filters
selected_sector = st.sidebar.multiselect(
    "Filter by Startup Sector", 
    options=df_startups["Sector"].unique(), 
    default=df_startups["Sector"].unique(),
    help="Filter down the active cohort based on their primary operating B2B tech vertical."
)

min_maturity = st.sidebar.selectbox(
    "Minimum Tech Maturity Required", 
    ["Low", "Medium", "High"], 
    index=1,
    help="Technical Maturity evaluates how ready a startup's software or hardware infrastructure is for enterprise deployment. It mathematically scores their cybersecurity compliance (e.g., SOC 2, HIPAA), cloud architecture scalability, and system uptime SLA history to prevent crashes or data vulnerabilities during corporate pilot programs."
)

# --- Consolidated Hierarchical Filter Logic ---
# Map maturity strings to an objective numerical hierarchy so Pandas can filter them correctly
maturity_hierarchy = {"Low": 1, "Medium": 2, "High": 3}
selected_maturity_level = maturity_hierarchy[min_maturity]

# If a specific company is picked, isolate it immediately
if selected_company != "All Companies":
    filtered_startups = df_startups[df_startups["Startup"] == selected_company]
else:
    # Otherwise, apply standard matrix filters using the mapped numerical hierarchy
    filtered_startups = df_startups[
        (df_startups["Sector"].isin(selected_sector)) & 
        (df_startups["Tech Maturity"].map(maturity_hierarchy) >= selected_maturity_level)
    ]


# =========================================================================
# 4. INTERACTIVE HEATMAP MATRIX RESYS
# =========================================================================
st.info("### Corporate Compatibility Matrix")
st.caption("Visualizing objective data alignment between local enterprise priorities and startup readiness.")

matrix_rows = []
for comp, priorities in corporates_data.items():
    # NEW: Skip rows if John is filtering for a specific corporate partner
    if selected_corporate != "All Corporates" and comp != selected_corporate:
        continue
        
    row = {"Corporate Partner": comp}
    for _, startup in filtered_startups.iterrows():
        row[startup["Startup"]] = priorities.get(startup["Sector"], 1)
    matrix_rows.append(row)

if matrix_rows and len(filtered_startups) > 0:
    df_matrix = pd.DataFrame(matrix_rows).set_index("Corporate Partner")
    
    # Create a custom Matplotlib colormap fading from White to 43North Cyan
    cyan_cmap = mcolors.LinearSegmentedColormap.from_list("43NorthCyan", ["#FFFFFF", "#00C2CB"])
    
    # Styled dataframe with custom black borders and cyan gradients
    st.dataframe(
        df_matrix.style.background_gradient(cmap=cyan_cmap, axis=None)
        .set_properties(**{
            'border': '1px solid black',
            'border-color': 'black',
            'color': 'black'
        })
        .format("{:.0f} / 5 Alignment"),
        use_container_width=True
    )
else:
    st.warning("No matches found for the selected filters.")

st.markdown("---")


# =========================================================================
# 5. OBJECTIVE DRILL-DOWN PROFILER
# =========================================================================
st.info("### Profile Directory")

if not filtered_startups.empty:
    selected_startup_name = st.selectbox("Select a startup to view verified profile:", filtered_startups["Startup"].unique())
    profile = filtered_startups[filtered_startups["Startup"] == selected_startup_name].iloc[0]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Left Side: The Narrative Elements
        st.markdown(f"**Executive Summary:**")
        st.write(profile["Executive Summary"])
        
        st.markdown("<br>", unsafe_allow_html=True) # Adds a little breathing room
        
        
    with col2:
        # Right Side: The Objective Metrics Stack
        st.metric(
            label="Target Industry (ICP)", 
            value=profile["ICP"],
            help="Derived via the 3-Variable Filter Token Formula:\n\nICP = [Target Sector Vertical] + [Company Scale Minimum] + [Internal Buyer Persona]."
        )
        st.markdown(f"**Sector Vertical:** {profile['Sector']}")
        
        st.markdown("<hr style='margin: 10px 0; border: none; border-bottom: 1px solid #333;'>", unsafe_allow_html=True)
        
        st.metric(
            label="Audited Tech Maturity", 
            value=profile["Tech Maturity"],
            help="Maturity = Compliance (0-3) + Architecture (0-3) + Uptime (1-3)."
        )
        st.caption(f"Raw Calculation: {profile['Raw Maturity']}")
        
        st.markdown("<hr style='margin: 10px 0; border: none; border-bottom: 1px solid #333;'>", unsafe_allow_html=True)
        
        st.metric(
            label="Calculated Integration Friction", 
            value=profile["Integration"],
            help="Friction = Data Dependencies (0 or 2 or 5) + Labor Points (1 to 7)."
        )
        st.caption(f"Raw Calculation: {profile['Raw Friction']}")   
else:
    st.info("Adjust the sidebar filters to repopulate the directory.")

# =========================================================================
# 6. METHODOLOGY & SCORING GLOSSARY
# =========================================================================
st.markdown("---")

st.info("### Methodology & Scoring Glossary")

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Matrix Alignment Score (X/5)")
    st.markdown("""
The heatmap matrix evaluates the strategic fit between a corporate partner's immediate innovation priorities and a startup's technological sector.

* **5 / 5 (Core Strategic Priority):** Direct alignment with immediate, enterprise-wide objectives. The corporate infrastructure is primed for rapid pilot integration.
* **4 / 5 (High Priority):** Strong secondary alignment. Highly relevant for targeted departmental optimization and positioned for near-term procurement.
* **3 / 5 (Moderate Interest):** Viable exploratory candidate. Addresses emerging operational needs and aligns well with long-term strategic roadmaps.
* **2 / 5 (Low Interest):** Peripheral alignment. The technology is sound but holds minimal immediate relevance to the current enterprise focus.
* **1 / 5 (No Current Alignment):** Outside current scope. The solution does not intersect with active procurement timelines or strategic innovation targets.
""")


with col_b:
    st.subheader("Audited Tech Maturity (Score: 0-9)")
    st.markdown("""
Calculates how ready a startup's infrastructure is for an enterprise deployment to prevent crashes or data vulnerabilities.

* **Formula:** `Compliance (0-3) + Architecture (0-3) + Uptime (1-3)`
* **Low (0-3):** Early-stage or foundational development. Limited to proof-of-concept prototypes or physical materials lacking an established enterprise digital footprint.
* **Medium (4-6):** Standard commercial B2B readiness. Supported by foundational frameworks (e.g., SOC 2 Type I), modular cloud microservices, and 99.9% uptime baselines.
* **High (7-9):** Mission-critical or enterprise-grade readiness. Validated by advanced compliance frameworks (e.g., SOC 2 Type II, HIPAA/FDA clearance) and high-availability infrastructure with 99.99% uptime SLAs.
""")

    st.subheader("Calculated Integration Friction (Score: 1-12)")
    st.markdown("""
Calculates the human labor hours and cybersecurity risks required from the corporate partner's internal IT staff to get a pilot live.

* **Formula:** `Data Dependencies (0-5) + Labor Points (1-7)`
* **Low (0-2):** Minimal deployment friction. Standalone software or localized hardware operating entirely outside the corporate network with zero enterprise data access.
* **Medium (3-6):** Moderate implementation requirements. Relies on secure, read-only API webhooks, standard single sign-on (SSO) configuration, and routine directory mapping.
* **High (7-12):** Complex enterprise integration. Demands extensive read/write permissions into core backend databases (e.g., EHRs, ERPs), rigorous cybersecurity reviews, and multi-department legal sign-off.
""")

# Expandable Sector Definitions Dictionary
with st.expander("View Startup Sector Vertical Definitions"):
    st.markdown("""
    * **MedTech:** Clinical workflow optimization, medical hardware development, diagnostics, and surgical tool engineering.
    * **BioTech:** Therapeutic development, biological preservation solutions, and advanced cellular engineering.
    * **FinTech:** Digital banking infrastructure, transactional processing, secure capital movement, and automated B2B invoicing.
    * **PropTech:** Building efficiency optimization, automated facility maintenance, and commercial real estate asset management.
    * **HRTech:** Talent acquisition systems, high-volume seasonal staffing automation, and workforce shift management software.
    * **SalesTech:** Commercial sales analytics, conversational revenue intelligence, and pipeline execution optimization.
    * **SupportTech:** Customer service automation, omni-channel communication routing, and high-volume ticket queue management.
    * **CleanTech:** Renewable energy integration, electric vehicle development, and sustainable utility grid infrastructure.
    * **MaterialsTech:** Advanced engineering of sustainable eco-materials, structural polymers, and clean chemical applications.
    * **SupplyChainTech:** Logistics optimization, localized supply chain compliance tracking, and circular or reusable vendor packaging management.
    * **FoodTech:** Commercial food processing technology, automated agricultural intelligence, and dairy supply chain monitoring.
    * **IndustryTech:** Industrial hardware automation, advanced 3D printing post-processing, and autonomous drone inspection systems for heavy industry.
    """)