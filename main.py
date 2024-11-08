from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging
import os
import re
import asyncio

# Setup logging config
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Pydantic model for input
class ImageURL(BaseModel):
    url: str

@app.post("/extract_and_map_tests_url/")
async def extract_and_map_tests(image_url: ImageURL):
    """
    This endpoint extracts test names from an image given via an HTTP/HTTPS or local file path URL
    and maps them to test codes. The response is delayed by 3 seconds to simulate processing time.
    """
    try:
        # Log the start of the request
        logger.info(f"Received request for image processing from URL: {image_url.url}")

        local_path = None
        # Check if the URL is a local path (starts with localhost)
        local_path_pattern = r'http://127\.0\.0\.1(:\d+)?/["\']?(.*)["\']?'
        if re.match(local_path_pattern, image_url.url):
            local_path_match = re.match(local_path_pattern, image_url.url)
            if local_path_match:
                local_path = local_path_match.group(2)
                local_path = os.path.normpath(local_path)  # Normalize path for OS compatibility
                logger.info(f"Interpreted local file path: {local_path}")

                # Check if the file exists before proceeding
                if not os.path.exists(local_path):
                    logger.error(f"File not found at path: {local_path}")
                    raise HTTPException(status_code=404, detail=f"File not found: {local_path}")
            else:
                raise HTTPException(status_code=400, detail="Invalid local path URL format.")
        else:
            # Log that this is an external URL
            logger.info("Processing an external URL.")

        # Simulate processing delay of 3 seconds
        await asyncio.sleep(3)
        
        # Mock response for demonstration
        mock_response = {
            "extracted_data": {
                "patient_title": "Mr",
                "patient_name": "Kumar",
                "patient_name_reg": "Kumar",
                "patient_age": 62,
                "patient_age_period": "Y",
                "patient_sex": "M",
                "patient_address": "Chennai",
                "patient_contact": "948865128",
                "date": "2023-06-30",
                "ID": "DA99",
                "referrer_type": "H",
                "referrer_name": "Arun Vijaya Hospitals Pvt. Ltd.",
                "referrer_name_reg": "NA",
                "prescribed_test": ["Complete Blood Count"],
                "remark": "NA",
                "matched_ref_name": "Ram",
                "matched_ref_code": "0001",
                "matched_ref_type": "D"
            },
            "mapped_tests": [
                {
                    "input_test_name": "Complete Blood Count",
                    "matched_test_name": "Complete Blood Count",
                    "matched_test_code": "CBC001"
                },
                {
                    "input_test_name": "LFT",
                    "matched_test_name": "LFT",
                    "matched_test_code": "LFT001"
                },
                {
                    "input_test_name": "HbA1c",
                    "matched_test_name": "HbA1c",
                    "matched_test_code": "HbA1c001"
                }
            ]
        }

        return JSONResponse(content=mock_response)

    except Exception as e:
        logger.error(f"Error during processing: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error during processing: {e}")
