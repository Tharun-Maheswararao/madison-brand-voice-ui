# app.py

import streamlit as st
import pandas as pd

from brand_voice_backend import generate_brand_voice, BrandVoiceBackendError

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Madison Brand Voice Generator",
    page_icon="🎙️",
    layout="wide",
)

# ---------- CUSTOM GRADIENT BACKGROUND ----------
gradient_css = """
<style>
/* Main app background: deep blue gradient matching portfolio site */
.stApp {
    background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 25%, #3b82f6 50%, #2563eb 75%, #1d4ed8 100%);
}

/* Make the main content container transparent so gradient shows through */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    background-color: transparent;
}

/* Sidebar with glass effect */
[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-right: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
}

/* Optional: remove any inner white cards that Streamlit might add */
[data-testid="stHeader"] {
    background-color: rgba(0, 0, 0, 0);
}

/* Form container with glass effect */
.stForm {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    padding: 2rem;
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
}

/* White input boxes with black text and grey placeholder */
.stTextInput input,
.stTextArea textarea {
    background-color: white !important;
    color: #000000 !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    border-radius: 8px !important;
    caret-color: #000000 !important;
}

/* Grey placeholder text */
.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #9ca3af !important;
    opacity: 1 !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #3b82f6 !important;
    outline: none !important;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
}

/* Generate Brand Voice button with glass effect */
.stForm button[type="submit"] {
    background: rgba(59, 130, 246, 0.8);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    color: white;
    font-weight: 600;
    padding: 0.75rem 2rem;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.3);
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    transition: all 0.3s ease;
}

.stForm button[type="submit"]:hover {
    background: rgba(59, 130, 246, 0.9);
    transform: translateY(-2px);
    box-shadow: 0 12px 40px 0 rgba(59, 130, 246, 0.4);
}

/* Glass effect for results sections */
.element-container:has(> .stMarkdown) {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    padding: 1.5rem;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    margin-bottom: 1rem;
}

/* Glass effect for success message */
.stSuccess {
    background: rgba(34, 197, 94, 0.15) !important;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(34, 197, 94, 0.3) !important;
    border-radius: 10px;
}

/* Glass effect for info message */
.stInfo {
    background: rgba(59, 130, 246, 0.15) !important;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(59, 130, 246, 0.3) !important;
    border-radius: 10px;
}

/* Glass effect for expanders */
.streamlit-expanderHeader {
    background: rgba(255, 255, 255, 0.1) !important;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Glass effect for expander content */
.streamlit-expanderContent {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 0 0 10px 10px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-top: none;
}

/* Glass effect for text areas in results (editable outputs) */
div[data-baseweb="textarea"] {
    background: rgba(255, 255, 255, 0.1) !important;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Text color for results */
.stMarkdown {
    color: white;
}

/* Subheaders styling */
h2, h3 {
    color: white !important;
}
</style>
"""

st.markdown(gradient_css, unsafe_allow_html=True)


# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("### Madison Brand Voice Generator")
    st.markdown(
        """
This tool takes your brand description and audience
and generates:

- A **brand voice profile**
- Website hero copy
- A newsletter email
- A voice script for sales calls

It uses:
- Your **n8n workflow** (Brand Voice Generator v2)  
- The **Madison** multi-step AI process under the hood.

**How to use it:**
1. Fill in brand, audience, and offer  
2. Click **Generate Brand Voice**  
3. Review the voice profile and generated content
        """
    )
    st.markdown("---")
    st.caption("Built by Tharun Maheswararao · Madison + n8n · INFO7375 Branding & AI.")

# ---------- HEADER ----------
st.markdown("#### Tharun Maheswararao • Branding, AI & DevOps")
st.title("Dynamic Brand Voice Adaptation System")
st.caption("Front-end UI for your n8n Madison Brand Voice Generator workflow.")

# ---------- INPUT FORM ----------
with st.form("brand_voice_form"):
    col1, col2 = st.columns(2)

    with col1:
        brand_name = st.text_input(
            "Brand / Company Name",
            placeholder="e.g., CloudBridge DevOps Studio",
        )

        audience = st.text_area(
            "Who is your target audience?",
            placeholder="e.g., Cloud-native SaaS founders, early-stage startups, DevOps leads at mid-sized companies, etc.",
            height=100,
        )

    with col2:
        offer = st.text_area(
            "What are you offering?",
            placeholder="e.g., production-ready DevOps pipelines, done-for-you observability, subscription skincare routine, etc.",
            height=100,
        )

    brand_info = st.text_area(
        "Describe your brand in 3–5 sentences (how you talk about yourself today)",
        placeholder=(
            "Example: We help early-stage SaaS teams ship reliably with production-grade CI/CD, "
            "observability, and security guardrails. Our tone is friendly expert: we keep things "
            "simple but grounded in real engineering practice."
        ),
        height=160,
    )

    submitted = st.form_submit_button("Generate Brand Voice 🎯")

# ---------- HANDLE SUBMIT ----------
if submitted:
    if not brand_name or not brand_info or not audience or not offer:
        st.error("Please fill in Brand name, Brand description, Audience, and Offer.")
    else:
        with st.spinner("Calling n8n + Madison to generate your brand voice and assets..."):
            try:
                result = generate_brand_voice(
                    brand_name=brand_name,
                    brand_info=brand_info,
                    audience=audience,
                    offer=offer,
                )
            except BrandVoiceBackendError as e:
                st.error(f"Something went wrong talking to the backend: {e}")
                st.stop()

        st.success("Brand voice and assets generated.")

        # ---------- DISPLAY RESULTS ----------
        st.subheader("1. Brand Voice Profile")

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"**Brand name:** {result.get('brandName', brand_name)}")
            st.markdown(f"**Audience:** {result.get('audience', audience)}")
            st.markdown(f"**Offer:** {result.get('offer', offer)}")
            st.markdown(f"**Tone label:** `{result.get('tone', 'unknown')}`")

        with col_b:
            st.markdown("**Voice description:**")
            st.markdown(result.get("voice_description", "No description returned."))

        st.markdown("**Emotional angle:**")
        st.markdown(result.get("emotional_angle", "Not specified."))

        keywords = result.get("keywords_to_use", [])
        avoid = result.get("phrases_to_avoid", [])
        selling_points = result.get("selling_points", [])

        col_k, col_p = st.columns(2)
        with col_k:
            st.markdown("**Keywords to use:**")
            if isinstance(keywords, list):
                st.markdown("- " + "\n- ".join([str(k) for k in keywords]) if keywords else "_none_")
            else:
                st.markdown(str(keywords))

        with col_p:
            st.markdown("**Phrases to avoid:**")
            if isinstance(avoid, list):
                st.markdown("- " + "\n- ".join([str(a) for a in avoid]) if avoid else "_none_")
            else:
                st.markdown(str(avoid))

        st.markdown("**Core selling points:**")
        if isinstance(selling_points, list):
            st.markdown("- " + "\n- ".join([str(s) for s in selling_points]) if selling_points else "_none_")
        else:
            st.markdown(str(selling_points))

        st.markdown("---")
        st.subheader("2. Website Hero Copy")

        website_headline = result.get("website_headline", "")
        website_subheadline = result.get("website_subheadline", "")
        website_bullets = result.get("website_bullets", [])

        st.markdown(f"### {website_headline or '[headline missing]'}")
        st.markdown(website_subheadline or "_No subheadline returned._")

        if isinstance(website_bullets, list) and website_bullets:
            st.markdown("**Key value props:**")
            st.markdown("- " + "\n- ".join([str(b) for b in website_bullets]))

        st.markdown("---")
        st.subheader("3. Newsletter Email")

        newsletter_email = result.get("newsletter_email", "")
        if newsletter_email:
            st.text_area(
                "Generated newsletter (editable):",
                value=newsletter_email,
                height=220,
            )
        else:
            st.info("No newsletter email returned from backend.")

        st.markdown("---")
        st.subheader("4. Voice Script for Sales Calls / Voice Agent")

        voice_script = result.get("voice_script_for_sales_calls", "")
        if voice_script:
            st.text_area(
                "Generated voice script (editable):",
                value=voice_script,
                height=260,
            )
        else:
            st.info("No voice script returned from backend.")

        with st.expander("5. Raw JSON (for technical reviewers)"):
            st.json(result)

        with st.expander("How this maps to Madison & n8n (for your assignment write-up)"):
            st.markdown(
                """
**Madison-style flow:**
- Input is normalized in n8n.
- **Brand Voice Profiler** analyzes the founder’s description and creates a structured brand voice profile.
- **Generate Deliverables** uses that profile to create website copy, email, and a voice script.
- **Code in JavaScript** combines everything into a single JSON object.
- This UI calls the workflow via HTTP and renders the result for non-technical users.
                """
            )
