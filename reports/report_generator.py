# reports/report_generator.py

import os
import datetime
from core.llm import LLM
from core.logger import LOG
class ReportGenerator:
    def __init__(self,llm):
        self.llm = llm  # 初始化时接受一个LLM实例，用于后续生成报告

    def generate_final_report(self):
        report_files = [f for f in os.listdir("reports") if f.endswith(".md")]
        combined_content = ""

        for file in report_files:
            with open(os.path.join("reports", file), "r",encoding='utf-8',errors='ignore') as f:
                combined_content += f.read() + "\n\n"

        # 使用 GPT API 生成总结
        final_report = self.llm.generate_summary(combined_content)

        if final_report:
            # 保存最终报告
            final_filename = f"final_report_{datetime.datetime.now().strftime('%Y-%m-%d')}.md"
            with open(os.path.join("reports", final_filename), "w",encoding='utf-8',errors='ignore') as file:
                file.write(final_report)
            print(f"Final report saved as {final_filename}")
        else:
            print("Failed to generate final report.")

    def generate_github_report(self, markdown_file_path):
        """
        生成 GitHub 项目的报告，并保存为 {original_filename}_report.md。
        """
        with open(markdown_file_path, 'r') as file:
            markdown_content = file.read()

        report = self.llm.generate_summary(markdown_content)
        
        report_file_path = os.path.splitext(markdown_file_path)[0] + "_report.md"
        with open(report_file_path, 'w+') as report_file:
            report_file.write(report)

        LOG.info(f"GitHub 项目报告已保存到 {report_file_path}")
        return report, report_file_path

