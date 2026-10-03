QUIT_COMMANDS = {"q", "quit", "exit"}


def parse_skill_selection(user_input, available_skills):
    cleaned_input = user_input.strip()
    if not cleaned_input:
        return [], "Please select some skills."
    if cleaned_input.casefold() in QUIT_COMMANDS:
        return None, None
    selected_skills = []
    invalid_entries = []
    for entry in cleaned_input.split():
        if not entry.isdigit():
            invalid_entries.append(entry)
            continue
        index = int(entry) - 1
        if not 0 <= index < len(available_skills):
            invalid_entries.append(entry)
            continue
        skill = available_skills[index]
        if skill not in selected_skills:
            selected_skills.append(skill)
    if invalid_entries:
        return [], "Please enter valid skill numbers."
    if len(selected_skills) < 3:
        return [], "Please select at least 3 different skills."
    return selected_skills, None
