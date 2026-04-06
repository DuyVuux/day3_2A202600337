import os
import sys
from datetime import datetime, timezone

# Thêm đường dẫn gốc để Python tìm thấy module src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.tools.ats_validator import validate_ats
from src.tools._session import session
from src.schemas.cv_tailoring import (
    JobDescription, JobRequirement, RequirementCategory, 
    RequirementPriority, ExtractionMetadata, SourceType
)

def setup_mock_session():
    """Giả lập dữ liệu JD trong session để validator có thể truy cập"""
    
    # Tạo Metadata giả
    meta = ExtractionMetadata(
        source_type=SourceType.PDF,
        extractor_name="Test_Extractor",
        extracted_at=datetime.now(timezone.utc)
    )

    # Tạo các yêu cầu công việc (Requirements) mẫu
    reqs = [
        JobRequirement(
            requirement_id="req1",
            category=RequirementCategory.HARD_SKILL,
            text="Python",
            priority=RequirementPriority.MUST
        ),
        JobRequirement(
            requirement_id="req2",
            category=RequirementCategory.HARD_SKILL,
            text="AWS",
            priority=RequirementPriority.MUST
        ),
        JobRequirement(
            requirement_id="req3",
            category=RequirementCategory.HARD_SKILL,
            text="Docker",
            priority=RequirementPriority.SHOULD
        ),
        JobRequirement(
            requirement_id="req4",
            category=RequirementCategory.SOFT_SKILL,
            text="Teamwork",
            priority=RequirementPriority.NICE_TO_HAVE
        )
    ]

    # Lưu vào session giả lập
    session.jd_data = JobDescription(
        metadata=meta,
        title="Senior Backend Engineer",
        requirements=reqs
    )

def run_test_cases():
    print("🚀 BẮT ĐẦU TEST ATS VALIDATOR (DETERMINISTIC)")
    print("-" * 50)
    
    setup_mock_session()

    # Case 1: CV hoàn hảo (Có đủ MUST, đầy đủ section)
    print("\n[CASE 1: CV HOÀN HẢO]")
    perfect_cv = """
    SUMMARY: Senior Engineer with Python and AWS expertise.
    EXPERIENCE: 5 years working with cloud technologies.
    SKILLS: Python, AWS, Docker, Teamwork.
    EDUCATION: Bachelor of Computer Science.
    PROJECTS: Built a microservices app.
    """
    result1 = validate_ats(perfect_cv)
    print(result1)

    # Case 2: Thiếu từ khóa MUST (Thiếu AWS)
    print("\n[CASE 2: THIẾU TỪ KHÓA BẮT BUỘC (MUST)]")
    missing_must_cv = """
    SUMMARY: Python Developer.
    EXPERIENCE: Professional coder.
    SKILLS: Python, Docker.
    EDUCATION: University.
    PROJECTS: None.
    """
    result2 = validate_ats(missing_must_cv)
    print(result2)

    # Case 3: Vi phạm định dạng (Dùng bảng |...|)
    print("\n[CASE 3: VI PHẠM ĐỊNH DẠNG (TABLE)]")
    bad_format_cv = """
    SUMMARY: Senior Engineer.
    | Skills | Level |
    | Python | Expert |
    EXPERIENCE: Worked at XYZ.
    EDUCATION: MIT.
    SKILLS: AWS.
    PROJECTS: Project A.
    """
    result3 = validate_ats(bad_format_cv)
    print(result3)

if __name__ == "__main__":
    try:
        run_test_cases()
    except Exception as e:
        print(f"❌ Lỗi thực thi test: {e}")
        import traceback
        traceback.print_exc()