from fastapi import APIRouter, HTTPException
from typing import List
from uuid import uuid4
import datetime
import random
import requests
from bs4 import BeautifulSoup
from app.schemas import ScanRequest, ScanResult, Asset

router = APIRouter()

# Mock user agents for "Chrome Ghost" simulation
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
]

def scan_github_zombies(target_url: str) -> List[Asset]:
    """
    Simulates finding abandoned "Zombie" repos related to the target.
    In a real app, this would use GitHub API to find stale forks or dependencies.
    """
    assets = []
    # Mock finding
    if "github" in target_url:
        assets.append(Asset(
            id=str(uuid4()),
            name=f"{target_url.split('/')[-1]}-legacy",
            type="github_zombie",
            url=f"{target_url}/tree/legacy",
            description="Abandoned branch with high value legacy code.",
            detected_at=datetime.datetime.now().isoformat(),
            status="investigate"
        ))
    
    # Always return a random chance zombie
    if random.choice([True, False]):
         assets.append(Asset(
            id=str(uuid4()),
            name="unknown-dependency-v1",
            type="github_zombie",
            url="https://github.com/example/dep-v1",
            description="Deprecated dependency still in use.",
            detected_at=datetime.datetime.now().isoformat()
        ))
    return assets

def scan_chrome_ghosts(target_url: str) -> List[Asset]:
    """
    Simulates finding "Ghost" assets via Chrome simulation (e.g. hidden API endpoints).
    In a real app, this would use Selenium/Playwright or detailed requests analysis.
    """
    assets = []
    try:
        # Simple health check to see if site is up (Real Logic)
        response = requests.get(target_url, headers={"User-Agent": random.choice(USER_AGENTS)}, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string if soup.title else "No Title"
            
            assets.append(Asset(
                id=str(uuid4()),
                name=f"Verified Site: {title}",
                type="chrome_ghost",
                url=target_url,
                description=f"Active endpoint detected. Status: {response.status_code}",
                detected_at=datetime.datetime.now().isoformat()
            ))

            # Mock hidden endpoint
            assets.append(Asset(
                id=str(uuid4()),
                name="Hidden API: /v1/internal",
                type="chrome_ghost",
                url=f"{target_url}/api/v1/internal",
                description="Undocumented internal API endpoint discovered via JS analysis.",
                detected_at=datetime.datetime.now().isoformat(),
                status="high_value"
            ))
    except Exception as e:
        # Fallback mock if request fails
        assets.append(Asset(
            id=str(uuid4()),
            name=f"Inaccessible: {target_url}",
            type="chrome_ghost",
            url=target_url,
            description=f"Could not reach target. Error: {str(e)}",
            detected_at=datetime.datetime.now().isoformat(),
            status="error"
        ))
    return assets

@router.post("/", response_model=ScanResult)
async def trigger_scan(request: ScanRequest):
    found_assets = []
    
    if request.scan_type in ["all", "github"]:
        found_assets.extend(scan_github_zombies(request.target_url))
    
    if request.scan_type in ["all", "chrome"]:
        found_assets.extend(scan_chrome_ghosts(request.target_url))

    return ScanResult(
        assets=found_assets,
        total_found=len(found_assets)
    )
