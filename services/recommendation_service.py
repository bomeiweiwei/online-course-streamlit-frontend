from enums.sys_preference import SysPreference

def calculate_recommend_score(course: dict, filters: dict) -> float:
    score = 0

    rating = course.get("rating", 0)
    students = course.get("students", 0)
    price = course.get("price", 0)

    budget = filters.get("budget", 0)
    preferences = filters.get("preferences", [])

    # 基礎分：評價，最核心權重
    # 4.8 星 → +48 分
    # 4.2 星 → +42 分
    score += float(rating) * 10

    # 報名人數分，很多人買有一定品質
    if students >= 1000:
        score += 20
    elif students >= 500:
        score += 15
    elif students >= 100:
        score += 10

    # 預算分，價格符合度
    if budget and price <= budget:
        score += 20
    elif budget and price <= budget * 1.2:
        score += 10
    
    # 偏好加權
    if SysPreference.VIDEO_SHORT.code in preferences:
        if SysPreference.VIDEO_SHORT.code in course.get("preferences", []):
            score += 5

    if SysPreference.QUESTION_MORE.code in preferences:
        if SysPreference.QUESTION_MORE.code in course.get("preferences", []):
            score += 5

    if SysPreference.TEACHER_GOOD.code in preferences:
        if SysPreference.TEACHER_GOOD.code in course.get("preferences", []):
            score += 5

    return round(score, 1)


def build_recommend_reason(course: dict, filters: dict) -> list[str]:
    reasons = []

    rating = course.get("rating", 0)
    students = course.get("students", 0)
    price = course.get("price", 0)
    budget = filters.get("budget", 0)

    if rating >= 4.5:
        reasons.append("評價表現良好")

    if students >= 1000:
        reasons.append("報名人數多，課程受歡迎")
    elif students >= 500:
        reasons.append("已有一定報名人數")

    if budget and price <= budget:
        reasons.append("價格符合預算")
    elif budget and price <= budget * 1.2:
        reasons.append("價格略高於預算，但仍可考慮")

    if not reasons:
        reasons.append("符合目前基本篩選條件")

    return reasons


def get_ranked_courses(courses: list[dict], filters: dict) -> list[dict]:
    ranked_courses = []

    for course in courses:
        course_copy = course.copy()

        course_copy["recommend_score"] = calculate_recommend_score(
            course_copy,
            filters
        )

        course_copy["recommend_reasons"] = build_recommend_reason(
            course_copy,
            filters
        )

        ranked_courses.append(course_copy)

    ranked_courses = sorted(
        ranked_courses,
        key=lambda item: item["recommend_score"],
        reverse=True
    )

    limit = filters.get("limit", 3)

    return ranked_courses[:limit]