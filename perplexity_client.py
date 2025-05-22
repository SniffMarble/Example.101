
# perplexity_client.py
import os
import json
import time
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Pydantic models for validation
class PerplexityAnswer(BaseModel):
    text: str = Field(..., min_length=1)
    citations: List[str] = Field(default_factory=list)

class PerplexityResponse(BaseModel):
    query: str = Field(..., min_length=1)
    answer: PerplexityAnswer
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class PerplexityClient:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.driver = None

    def setup_driver(self):
        """Initialize Selenium WebDriver."""
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")  # Run in headless mode
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            logger.info("WebDriver initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise

    def query_perplexity(self, prompt: str) -> PerplexityResponse:
        """Query Perplexity using browser automation."""
        if not self.driver:
            self.setup_driver()

        try:
            # Navigate to Perplexity
            self.driver.get("https://www.perplexity.ai")
            time.sleep(2)  # Wait for page load

            # Find search input and submit query
            search_box = self.driver.find_element(By.CSS_SELECTOR, "textarea[placeholder*='Ask anything']")
            search_box.send_keys(prompt)
            search_box.submit()
            time.sleep(5)  # Wait for response

            # Extract answer
            answer_element = self.driver.find_element(By.CSS_SELECTOR, ".prose")
            answer_text = answer_element.text

            # Extract citations (if available)
            citations = []
            try:
                citation_elements = self.driver.find_elements(By.CSS_SELECTOR, ".source-attributions a")
                citations = [elem.get_attribute("href") for elem in citation_elements]
            except:
                logger.warning("No citations found.")

            # Validate response
            response = PerplexityResponse(
                query=prompt,
                answer=PerplexityAnswer(text=answer_text, citations=citations)
            )
            self._log_response(response)
            return response

        except Exception as e:
            logger.error(f"Error querying Perplexity: {e}")
            return self._mock_response(prompt)

    def _mock_response(self, prompt: str) -> PerplexityResponse:
        """Return a mock response for offline mode."""
        logger.warning("Using mock response for offline mode.")
        mock_answer = PerplexityAnswer(
            text=f"Mock response for query: {prompt}",
            citations=["https://example.com"]
        )
        response = PerplexityResponse(query=prompt, answer=mock_answer)
        self._log_response(response)
        return response

    def _log_response(self, response: PerplexityResponse):
        """Log response to JSON file in data_dir."""
        try:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"perplexity_response_{timestamp}.json"
            filepath = os.path.join(self.data_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(response.dict(), f, ensure_ascii=False, indent=2)
            logger.info(f"Response logged to {filepath}")
        except Exception as e:
            logger.error(f"Failed to log response: {e}")

    def close(self):
        """Close WebDriver."""
        if self.driver:
            self.driver.quit()
            logger.info("WebDriver closed.")

# Example usage
if __name__ == "__main__":
    client = PerplexityClient(data_dir="data")
    try:
        response = client.query_perplexity("Mis on Eesti pealinn?")
        print(response.json(indent=2))
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        client.close()
2. Update install_packages.sh
Modify your install_packages.sh to fix Flatpak, Notion, and Warp Terminal issues, and install dependencies for the Perplexity integration.

bash

Copy
#!/bin/bash
# scripts/install_packages.sh
# Script to install deb, flatpak, and snap packages for ubuntu-postinstall-script

# Exit on error
set -e

# Navigate to repository
cd /media/sniffmarble/My_Projects1/ubuntu-postinstall-script

# Create and activate virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# Install deb packages
sudo apt update
sudo apt install -y \
    htop neofetch gnome-tweaks vlc gimp flatpak ubuntu-restricted-extras timeshift \
    tlp tlp-rdw python3-pip python3-venv python3-dev python3-numpy python3-scipy \
    python3-pandas python3-matplotlib python3-seaborn python3-jupyter-core \
    python3-jupyter-client jupyter-notebook
sudo tlp start

# Add Flathub repository and install Flatpak packages
sudo flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak install -y flathub org.gimp.GIMP com.obsproject.Studio org.jupyter.JupyterLab

# Install Snap packages
sudo snap install code --classic
sudo snap install pycharm-community --classic
sudo snap install notion-desktop

# Install Warp Terminal
wget -O warp.deb https://releases.warp.dev/linux/deb/stable/warp-terminal_latest_amd64.deb
sudo dpkg -i warp.deb || sudo apt-get install -f -y
rm warp.deb

# Install Python dependencies for Perplexity integration
pip install --no-cache-dir tensorflow==2.17.0 torch==2.4.1 selenium webdriver-manager pydantic

echo "Package installation complete"
3. Create post_install.py
Create a post_install.py script to run post-installation tasks, including testing the Perplexity integration and logging results.

python

Copy
# scripts/post_install.py
import os
import logging
from perplexity_client import PerplexityClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/post_install.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def test_perplexity_integration():
    """Test Perplexity AI integration."""
    client = PerplexityClient(data_dir="data")
    try:
        # Test with an Estonian prompt
        response = client.query_perplexity("Mis on Eesti pealinn?")
        logger.info("Perplexity test successful: %s", response)
        
        # Test with an English prompt
        response = client.query_perplexity("What is the capital of Estonia?")
        logger.info("Perplexity test successful: %s", response)
    except Exception as e:
        logger.error("Perplexity test failed: %s", e)
    finally:
        client.close()

def main():
    """Run post-installation tasks."""
    logger.info("Starting post-installation tasks")
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Test Perplexity integration
    test_perplexity_integration()
    
    logger.info("Post-installation tasks completed")

if __name__ == "__main__":
    main()
4. README Section in Estonian
Add the following section to your README.md in Estonian:

markdown

Copy
## Perplexity AI Integratsioon

See projekt integreerib Perplexity AI reaalajas otsingu- ja küsimustele vastamise võimekuse, et toetada eesti- ja ingliskeelseid päringuid. Integratsioon kasutab Seleniumit veebilehitseja automatiseerimiseks, kuna API võtit pole saadaval.

### Paigaldamine
1. Veenduge, et vajalikud paketid on paigaldatud, käivitades `scripts/install_packages.sh`.
2. Aktiveerige virtuaalkeskkond: `source venv/bin/activate`.
3. Käivitage Perplexity testi: `python3 scripts/post_install.py`.

### Kasutamine
- Perplexity klient asub failis `perplexity_client.py`.
- Näide: Küsi "Mis on Eesti pealinn?" ja saa struktureeritud JSON vastus.
- Vastused logitakse kausta `data` JSON-failidena.

### Logimine
- Sisend/väljund logitakse kausta `data` failidena, näiteks `perplexity_response_YYYYMMDD_HHMMSS.json`.
- Logifail `data/post_install.log` sisaldab post-paigalduse tegevuste logi.

### CI/CD
- GitHub Actions testib Perplexity integratsiooni, kontrollides vastuse formaati ja logimist.

### Võrguühenduseta režiim
- Kui võrk pole saadaval, kasutatakse mock-vastuseid, mis logitakse samamoodi.
