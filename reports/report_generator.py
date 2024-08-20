# reports/report_generator.py

def generate_report(updates):
    report = "GitHub Releases Report\n\n"
    for update in updates:
        report += f"Repository: {update['name']}\n"
        report += f"Tag: {update['tag_name']}\n"
        report += f"Published at: {update['published_at']}\n"
        report += f"Release notes:\n{update['body']}\n\n"
    return report
