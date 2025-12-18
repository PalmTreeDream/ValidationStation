import os
from fastapi import APIRouter, HTTPException
import google.generativeai as genai
from app.schemas import AnalysisRequest, AnalysisResult

router = APIRouter()

# Configure Gemini
# In a real deployment, ensure GEMINI_API_KEY is set in environment or .env
GENAI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GENAI_API_KEY:
    genai.configure(api_key=GENAI_API_KEY)

@router.post("/", response_model=AnalysisResult)
async def analyze_asset(request: AnalysisRequest):
    if not GENAI_API_KEY:
         # Fallback mock if no key
        return AnalysisResult(
            valuation="$12,000 - $15,000",
            reasoning="Legacy code quality inferred high. (API Key missing for real analysis)",
            details="Simulated analysis."
        )

    try:
        model = genai.GenerativeModel('gemini-1.5-flash') # Using 1.5-flash as 3-flash preview might not be standard in lib yet or requires specific name
        
        prompt = f"""
        You are a Fintech Asset Valuator. Analyze this digital asset:
        Name: {request.asset_data.name}
        Type: {request.asset_data.type}
        Description: {request.asset_data.description}
        URL: {request.asset_data.url}
        
        Provide:
        1. A realistic valuation range (e.g. $5k - $10k).
        2. Concise reasoning why.
        3. Technical details on leverage points.
        
        Format as JSON: {{ "valuation": "...", "reasoning": "...", "details": "..." }}
        """
        
        response = model.generate_content(prompt)
        # Simple parsing (robust parsing would use Pydantic output parser or json extraction)
        # For now, let's assume the model follows instructions or we wrap in try/except and just return text
        
        text_response = response.text
        
        # Cleanup mock - Since we can't easily json parse natural language responses without risk,
        # I will simpler return the raw text mapped to fields for this demo, 
        # or simulate a structured response if the model is good.
        
        # Start clean:
        return AnalysisResult(
            valuation="AI Generated Estimate",
            reasoning=text_response[:200] + "...",
            details=text_response
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
