from fastapi import FastAPI, UploadFile, File, Form, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, SessionLocal
from .models import Base, Project, File as DBFile, Report

from .services import (
    static_engine,
    security_engine,
    plagiarism_engine,
    scoring_engine,
    report_generator,
    execution_engine,
    test_engine,
    llm_engine
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CodeInspector API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# ---------------- DB Dependency ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- ANALYZE ENDPOINT ----------------
@app.post("/analyze/")
async def analyze_code(
    project_name: str = Form(...),
    language: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    content = (await file.read()).decode("utf-8")

    # Create Project
    project = Project(name=project_name)
    db.add(project)
    db.commit()
    db.refresh(project)

    # Save File
    db_file = DBFile(
        project_id=project.id,
        filename=file.filename,
        language=language,
        content=content
    )
    db.add(db_file)
    db.commit()

    # -------- STATIC ANALYSIS --------
    static_output = static_engine.analyze(content, language)

    # -------- SECURITY --------
    security_result = security_engine.analyze_security(content)

    # -------- PLAGIARISM --------
    existing_files = db.query(DBFile).all()
    existing_contents = [f.content for f in existing_files if f.id != db_file.id]

    plagiarism_result = plagiarism_engine.analyze_plagiarism(
        content,
        existing_contents
    )

    # -------- EXECUTION TEST --------
    execution_result = {}
    if language.lower() == "python":
        execution_result = execution_engine.execute_python_code(content)

    # -------- TEST ENGINE --------
    test_result = test_engine.run_tests(content)

    # -------- SCORING --------
    quality_score = scoring_engine.calculate_quality_score(static_output)
    security_score = security_result["security_score"]
    scalability_score = scoring_engine.calculate_scalability_score(content)
    plagiarism_score = plagiarism_result["plagiarism_score"]

    final_score = scoring_engine.calculate_final_score(
        quality_score,
        security_score,
        scalability_score,
        plagiarism_score
    )

    scores = {
        "quality": quality_score,
        "security": security_score,
        "scalability": scalability_score,
        "plagiarism": plagiarism_score,
        "final": final_score
    }

    # -------- PDF REPORT --------
    pdf_path = report_generator.generate_pdf_report(project_name, scores)

    report = Report(
        project_id=project.id,
        quality_score=quality_score,
        security_score=security_score,
        scalability_score=scalability_score,
        plagiarism_score=plagiarism_score,
        final_score=final_score,
        pdf_path=pdf_path
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    # -------- LLM REVIEW --------
    llm_review = llm_engine.analyze_with_llm(content)

    return {
        "project_id": project.id,
        "report_id": report.id,
        "scores": scores,
        "security_issues": security_result["issues"],
        "plagiarism_similarity": plagiarism_result["similarity_percentage"],
        "execution_result": execution_result,
        "test_result": test_result,
        "llm_review": llm_review,
        "pdf_report": pdf_path
    }


# ---------------- DOWNLOAD REPORT ----------------
@app.get("/report/{report_id}")
def download_report(report_id: int):
    db = SessionLocal()
    report = db.query(Report).filter(Report.id == report_id).first()

    if not report:
        return {"error": "Report not found"}

    return FileResponse(
        report.pdf_path,
        filename=f"CodeInspector_Report_{report_id}.pdf",
        media_type="application/pdf"
    )


# ---------------- ROOT ----------------
@app.get("/")
def root():
    return {"message": "CodeInspector Backend Running"}
