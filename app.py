import streamlit as st
import pandas as pd
import json

# --- 1. CONFIG & DEFINITIONS ---
st.set_page_config(
    page_title="Faraday Operando Sample Environment Library",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Technique Glossary 
TECHNIQUE_DEFINITIONS = {
    "Neutron Diffraction": "Sensitive to light elements (Li, O) and isotopes. Used to determine long-range crystal structure and phase evolution.",
    "Muon spectroscopy": "A sensitive local probe (μ+SR) used to quantify ion diffusion rates (Li+, Na+) and pathways at the atomic scale.",
    "Muon Elemental Analysis": "Uses negative muons (μ-SR/μXES) to probe elemental composition far below the surface without destruction.",
    "SANS": "Small Angle Neutron Scattering. Probes nanoscale structures (1–100 nm), such as porosity, SEI formation, and particle morphology.",
    "XPDF": "X-ray Pair Distribution Function. Probes local structure in disordered/amorphous materials (e.g., electrolytes).",
    "XAS": "X-ray Absorption Spectroscopy. Probes oxidation states, bond lengths, and local coordination geometry.",
    "XRS": "X-ray Raman Scattering. Provides electronic structure information using hard X-rays; suitable for bulk measurements.",
    "Soft XPS": "X-ray Photoelectron Spectroscopy. Surface-sensitive (<10 nm) analysis of elemental composition and SEI chemistry.",
    "AP-XPS": "Ambient Pressure XPS. Allows surface analysis at realistic pressures (solid-gas/solid-liquid interfaces), bridging the pressure gap.",
    "NEXAFS": "Near-Edge X-ray Absorption Fine Structure. Probes electronic structure of light elements at surfaces.",
    "Nano-focus XRF": "X-ray Fluorescence microscopy. Maps elemental distribution with nanoscale resolution.",
    "XANES": "X-ray Absorption Near Edge Structure. Determines oxidation state and local symmetry.",
    "Imaging": "Visualises macroscopic features like dendrites, gas evolution, and particle cracking (2D/3D).",
    "XRD": "X-ray Diffraction. Determines crystal structure, lattice parameters, strain, and phase evolution during cycling.",
    "XRD-CT": "X-ray Diffraction Computed Tomography. Combines diffraction contrast with tomography to map phase distributions and strain fields in 3D.",
    "DFXM": "Dark Field X-ray Microscopy. Allows high-resolution mapping of crystal orientation and strain within individual grains.",
    "EXAFS": "Extended X-ray Absorption Fine Structure. Analyzes average local structure and coordination numbers in materials lacking long-range order.",
    "RIXS": "Resonant Inelastic X-ray Scattering. Probes orbital states and charge transfer dynamics.",
    "Neutron Total Scattering": "Characterises non-crystalline/disordered materials (e.g., liquids) using H/D isotopic substitution.",
    "QENS": "Quasi-Elastic Neutron Scattering. Probes slow diffusional processes like Li-ion hopping.",
    "INS": "Inelastic Neutron Scattering. Probes vibrational modes to investigate material dynamics.",
    "Bragg Edge Imaging": "Maps crystal texture, phase distribution, and lattice strain in real space.",
    "Ptychography": "High-resolution phase-contrast imaging for nanoscale morphology.",
    "Neutron Reflectometry": "Measures thin films and buried interfaces."
}

# --- 2. LOAD DATA ---
@st.cache_data
def load_registry():
    try:
        with open('operando_cell_registry.json', 'r') as f:
            data = json.load(f)
        df = pd.json_normalize(data)
        return df, data
    except FileNotFoundError:
        st.error("Registry file not found. Ensure 'operando_cell_registry.json' is in the directory.")
        st.stop()

df, raw_json = load_registry()

# --- 3. SIDEBAR FILTERS ---
st.sidebar.header("Filter Registry")

# A. Technique Filter
all_techniques = sorted(list(set([item for sublist in df['compatibility.techniques'] for item in sublist])))
selected_techniques = st.sidebar.multiselect("Technique", all_techniques, placeholder="e.g. Neutron Diffraction")

# B. Instrument Filter
all_instruments = sorted(list(set([item for sublist in df['compatibility.instruments'] for item in sublist])))
selected_instruments = st.sidebar.multiselect("Instrument", all_instruments, placeholder="e.g. POLARIS")

# C. Smart Capabilities
st.sidebar.markdown("---")
st.sidebar.subheader("Capabilities")
digital_twin_only = st.sidebar.checkbox("Digital Twin Ready (CAD)")
high_temp_only = st.sidebar.checkbox("High Temperature (>100°C)")
pressure_control = st.sidebar.checkbox("Pressure Control")

# D. Glossary (Kept as secondary reference)
st.sidebar.markdown("---")
with st.sidebar.expander("Technique Dictionary"):
    term = st.selectbox("Select a term:", sorted(TECHNIQUE_DEFINITIONS.keys()))
    st.info(TECHNIQUE_DEFINITIONS[term])

# --- 4. FILTER LOGIC ---
filtered_df = df.copy()

if selected_techniques:
    filtered_df = filtered_df[filtered_df['compatibility.techniques'].apply(lambda x: any(i in selected_techniques for i in x))]

if selected_instruments:
    filtered_df = filtered_df[filtered_df['compatibility.instruments'].apply(lambda x: any(i in selected_instruments for i in x))]

if digital_twin_only:
    filtered_df = filtered_df[filtered_df['digital_twin.cad_available'] == True]

if pressure_control:
    filtered_df = filtered_df[filtered_df['specifications.operating_limits.pressure_control'] == True]

if high_temp_only:
    filtered_df = filtered_df[filtered_df['specifications.operating_limits.max_temp_c'].fillna(25) >= 100]

# --- 5. DASHBOARD HEADER ---
st.title("Operando Sample Environment Library")
st.markdown(
    """
    **The open-access hardware registry for the UK battery community.** A machine-readable database of the Rutherford Appleton Laboratory's sample environments, designed to standardise metadata for multi-modal experiments.  
    *See the framework: [arXiv:2601.00851](https://arxiv.org/abs/2601.00851)*
    """
)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Cells Found", len(filtered_df))
m2.metric("Digital Twin Ready", len(filtered_df[filtered_df['digital_twin.cad_available']==True]))
m3.metric("High Temp Capable", len(filtered_df[filtered_df['specifications.operating_limits.max_temp_c'].fillna(25) >= 100]))
m4.metric("Avg. TRL", "Research")

st.markdown("---")

# --- 6. MAIN TABLE ---
st.subheader("Hardware Registry")

st.dataframe(
    filtered_df[[
        'name', 'type', 'digital_twin.cad_available', 
        'compatibility.techniques', 'specifications.operating_limits.max_temp_c',
        'contact_info.primary_email'  # <--- Added this
    ]],
    use_container_width=True,
    column_config={
        'name': "Cell Name",
        'type': "Geometry",
        'digital_twin.cad_available': st.column_config.CheckboxColumn("Digital Twin", default=False),
        'compatibility.techniques': st.column_config.ListColumn("Techniques"),
        'specifications.operating_limits.max_temp_c': st.column_config.NumberColumn("Max Temp", format="%.0f°C"),
        'contact_info.primary_email': st.column_config.LinkColumn("Point of Contact") # <--- Formatted as link
    },
    hide_index=True,
    height=300
)

# --- 7. COMPARISON & DEEP DIVE ---
st.markdown("---")
st.subheader("Cell Comparison & Deep Dive")

selected_cell_names = st.multiselect(
    "Select cells to compare (Max 3):", 
    filtered_df['name'].unique(),
    max_selections=3,
    default=[filtered_df['name'].iloc[0]] if not filtered_df.empty else None
)

if selected_cell_names:
    cols = st.columns(len(selected_cell_names))
    
    for idx, cell_name in enumerate(selected_cell_names):
        cell_data = next(item for item in raw_json if item["name"] == cell_name)
        limits = cell_data['specifications']['operating_limits']
        r3 = cell_data.get('limitations_3r', {})

        with cols[idx]:
            st.markdown(f"### {cell_data['name']}")
            st.caption(f"Type: {cell_data['type']}")
            
            # --- CONTACT BUTTON ---
            email = cell_data.get('contact_info', {}).get('primary_email', 'N/A')
            st.link_button(f"📧 Contact Support", f"mailto:{email}", use_container_width=True)

            with st.container(border=True):
                st.write("**Key Specifications**")
                st.write(f"Max Temp: {limits.get('max_temp_c', 25)}°C")
                st.write(f"Pressure Control: {'Yes' if limits.get('pressure_control') else 'No'}")
                st.write(f"CAD Available: {'Yes' if cell_data['digital_twin']['cad_available'] else 'No'}")

            # --- NEW: Integrated Glossary ---
            with st.expander("Supported Techniques (Definitions)", expanded=False):
                for tech in cell_data['compatibility']['techniques']:
                    # Find partial match
                    desc = "Definition unavailable."
                    for key, val in TECHNIQUE_DEFINITIONS.items():
                        if key.lower() in tech.lower():
                            desc = val
                            break
                    st.markdown(f"**{tech}**")
                    st.caption(desc)

            st.markdown("#### The 3Rs Profile")
            st.error("Reliability")
            for i in r3.get('reliability', []): st.markdown(f"- {i}")
            
            st.warning("Representativeness")
            for i in r3.get('representativeness', []): st.markdown(f"- {i}")
            
            st.info("Reproducibility")
            for i in r3.get('reproducibility', []): st.markdown(f"- {i}")

# --- 8. COMPATIBILITY MATRIX ---
st.markdown("---")
st.subheader("Technique Compatibility Matrix")

technique_matrix = []
for entry in raw_json:
    if entry['name'] in filtered_df['name'].values:
        row = {"Cell": entry['name']}
        for tech in all_techniques:
            row[tech] = tech in entry['compatibility']['techniques']
        technique_matrix.append(row)

if technique_matrix:
    df_matrix = pd.DataFrame(technique_matrix).set_index("Cell")
    column_config = {col: st.column_config.CheckboxColumn(col) for col in df_matrix.columns}
    st.dataframe(
        df_matrix,
        use_container_width=True,
        column_config=column_config
    )

# --- 9. FOOTER & DOWNLOAD ---
st.markdown("---")
c_left, c_right = st.columns([3, 1])

with c_left:
    st.caption("**Maintained by James Le Houx (STFC/Faraday Institution).**")
    st.caption("Reference: [Autonomous battery research: Principles of heuristic operando experimentation (arXiv:2601.00851)](https://arxiv.org/abs/2601.00851)")

with c_right:
    # Filter the download data to match what the user is currently seeing
    visible_ids = filtered_df['id'].tolist()
    filtered_json_download = [entry for entry in raw_json if entry['id'] in visible_ids]

    st.download_button(
        label="📥 Download JSON",
        data=json.dumps(filtered_json_download, indent=2),
        file_name="filtered_cell_registry.json",
        mime="application/json",
        use_container_width=True

    )
