import fastapi

from job_match_application.config import create_app

app = create_app()
app.add_api_route()

@app.refresh_priority
def refresh_candidate_priority():
    return {'operation successfully'}