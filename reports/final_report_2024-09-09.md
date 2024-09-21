# edwinjiang141/github-sen 项目进展

## 时间周期：2024-09-06至2024-09-08

## Issues:
- 暂无更新。

## Pull Requests:
- 暂无更新。

---

# LangChain 项目进展

## 时间周期：2024-09-06至2024-09-08

## 新增功能
- 为 BoxRetriever 添加搜索选项，并提供相应的文档支持。
- 加入对 PiecesOS LLM 的集成，扩展了模型的适用性。
- 在 AzureChatOpenAI 中添加了结构化输出方法的工具支持，增强了功能。
- 文档中增加了 ai21 工具调用的示例，帮助用户更好地理解使用方式。

## 主要改进
- 更新了 HuggingFacePipeline，添加了 model_id 参数的支持，提升了灵活性。
- 递归地为结构化输出添加了附加属性，以增强输出数据的完整性和实用性。
- 修复了 Pydantic 的警告，改善了代码的兼容性，提升了开发者体验。

## 修复问题
- 修复了 AzureChatOpenAI 的 json_schema 模式问题，确保了功能的正常运行。
- 解决了使用 create_xml_agent 时与无参数函数相关的崩溃问题，提升了系统稳定性。
- 处理了在新版本 ClickHouse 中的嵌入问题，确保兼容性与性能。