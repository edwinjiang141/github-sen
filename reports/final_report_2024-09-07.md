# LangChain 项目进展

## 时间周期：2024-09-07

## 新增功能
- 添加了会话过期重试机制，支持 Neo4j 图数据库。
- 为 BoxRetriever 添加了搜索选项，并提供作为代理工具的文档支持。
- 向 ChatOctoAI 添加了 bind_tools 功能支持。
- 增加了对 HuggingFacePipeline 中 model_id 参数的支持。
- 集成了 PiecesOS LLM。

## 主要改进
- 更新了 RAG 教程的依赖项，以保持工具的现代性。
- 更新了文档中的函数注释，提升可读性。
- 提高了 RedisVectorStore 的 API 文档质量。
- 修复了 AzureChatOpenAI 的 json_schema 模式相关问题。

## 修复问题
- 解决了 Azure Cosmos DB 中出现的键错误问题。
- 修复了 ScrapflyLoader 文档中的拼写错误。
- 修复了在新版本的 ClickHouse 中的嵌入问题。
- 修复了 Databricks Vector Search 的调用参数问题。