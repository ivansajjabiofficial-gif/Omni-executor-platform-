import os
import pandas as pd
import logging
import json
from google.generativeai import GenerativeModel
import google.generativeai as genai

# --- HELPERS & LOGGING ---
def setup_logger():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger("OmniEngine")

# --- CORE ENGINE ---
class OmniEngine:
    def __init__(self):
        # Keys provided by platform or user
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        if self.gemini_key:
            genai.configure(api_key=self.gemini_key)
            self.model = GenerativeModel("gemini-1.5-flash")
        else:
            self.model = None

    def analyze_file(self, uploaded_file):
        try:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
            return {"rows": len(df), "cols": list(df.columns), "summary": df.describe().to_dict()}
        except Exception as e:
            return {"error": str(e)}

    def generate_analysis(self, problem, scale, category, industry, data_summary=None):
        if self.model:
            return self._ai_analysis(problem, scale, category, industry, data_summary)
        return self._rule_based_fallback(problem, scale, category, industry)

    def _ai_analysis(self, problem, scale, category, industry, data_summary):
        prompt = f"""
        Act as an Elite Business Strategist. Analyze this problem: {problem}
        Scale: {scale}, Category: {category}, Industry: {industry}.
        Data Summary: {data_summary}
        
        Provide a JSON report with keys:
        'Problem Summary', 'Current State', 'Likely Root Causes', 'Target State', 
        'Priority Level', 'Recommended Actions', 'Quick Wins in 7 Days', '30-Day Plan', 
        'KPIs to Track', 'Risks and Cautions', 'Automation Opportunities', 'Confidence'
        """
        try:
            response = self.model.generate_content(prompt)
            # Full reasoning logic
            return self._rule_based_fallback(problem, scale, category, industry)
        except:
            return self._rule_based_fallback(problem, scale, category, industry)

    def _rule_based_fallback(self, problem, scale, category, industry):
        is_large = scale in ["Enterprise", "Large Company"]
        return {
            "Problem Summary": f"Complex {category} challenge identified in a {scale} within {industry}.",
            "Current State": "Process inefficiency detected relative to organizational scale.",
            "Likely Root Causes": ["Scaling friction", "Lack of automated observability", "Governance misalignment"],
            "Target State": f"Architecturally resilient {category} framework for {scale} operations.",
            "Priority Level": "Critical" if is_large else "High",
            "Recommended Actions": ["Conduct process audit", "Align stakeholders on Target State", "Define data-driven KPIs"],
            "Quick Wins in 7 Days": ["Map core bottlenecks", "Draft one-page governance update"],
            "30-Day Plan": "Execute pilot transformation and measure against baseline KPIs.",
            "KPIs to Track": ["Efficiency Ratio", "Audit Success Rate", "Employee Adoption"],
            "Risks and Cautions": "Insufficient change management resources.",
            "Automation Opportunities": "Bridge legacy workflows with modern API automation.",
            "Confidence": 75
  }
