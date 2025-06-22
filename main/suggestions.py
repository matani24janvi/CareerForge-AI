# keyword_matching.py

import json
from Variables import (
    ds_keyword, ds_course,
    web_keyword, web_course,
    android_keyword, android_course,
    ios_keyword, ios_course,
    uiux_keyword, uiux_course
)

def find_missing_keywords(all_keywords, tokens):
    tokens_lower = set([t.lower() for t in tokens])
    missing = [k for k in all_keywords if k.lower() not in tokens_lower]
    return missing

def match_courses_from_keywords(missing_keywords, course_list):
    matched_courses = []
    for title, url in course_list:
        for keyword in missing_keywords:
            if keyword.lower() in title.lower() and [title, url] not in matched_courses:
                matched_courses.append([title, url])
                break
        if len(matched_courses) >= 10:
            break
    return matched_courses or course_list[:2]  # fallback if no matches

def get_course_recommendations(tokens):
    roles = {
        "Data Science": (ds_keyword, ds_course),
        "Web Development": (web_keyword, web_course),
        "Android Development": (android_keyword, android_course),
        "iOS Development": (ios_keyword, ios_course),
        "UI/UX Design": (uiux_keyword, uiux_course)
    }

    recommendations = []

    for role, (keywords, courses) in roles.items():
        matched = [k for k in keywords if k.lower() in [t.lower() for t in tokens]]
        missing = [k for k in keywords if k not in matched]

        if matched:
            suggested_courses = match_courses_from_keywords(missing, courses)
            course_data = [{"title": c[0], "url": c[1]} for c in suggested_courses]
            recommendations.append({
                "role": role,
                "fit": round((len(matched) / len(keywords)) * 100, 2),
                "missing_skills": missing[:5],  # show top 5 gaps
                "courses": course_data
            })

    # Sort by fit descending
    return sorted(recommendations, key=lambda x: x['fit'], reverse=True)

# 🧪 Example test
if __name__ == "__main__":
    
    with open("./uploads/resume.json", 'r', encoding='utf-8') as file:
        data = json.load(file)
        text = data.get('extracted_text', '')
        tokens = data.get('tokens', [])
    for role_data in get_course_recommendations(tokens):
        print(f"\n🎯 Role: {role_data['role']} (Fit: {role_data['fit']}%)")
        print("🔻 Missing Keywords:", ', '.join(role_data['missing_skills']))
        print("📚 Suggested Courses:")
        for c in role_data['courses']:
            print(f" - {c['title']}: {c['url']}")