def apply_frontend_filters(courses, filters):

    filtered_courses = courses

    version_id = filters.get("version_id")
    
    degree_id = filters.get("degree_id")
    goal_id = filters.get("goal_id")

    if version_id:
        filtered_courses = [
            course for course in filtered_courses
            if course.get("version_id") == version_id
        ]

    if degree_id:
        filtered_courses = [
            course for course in filtered_courses
            if course.get("degree_id") == degree_id
        ]

    if goal_id:
        filtered_courses = [
            course for course in filtered_courses
            if course.get("goal_id") == goal_id
        ]

    return filtered_courses