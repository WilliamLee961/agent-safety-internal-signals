# 文献与综述筛选

最后核查记录：2026-09-23。下列为研究入口，不自动代表会议录用或高引用。

## 仍需完成的主读综述选择

候选：[A Survey on Trustworthy LLM Agents: Threats and Countermeasures](https://arxiv.org/abs/2503.09648)。

- 已核实 arXiv 页面存在，首次提交为 2025-03-12，当前已查看页面显示 v1。
- 摘要提出 TrustAgent 框架，将可信性按内部模块（brain、memory、tool）与外部关系（user、agent、environment）整理，覆盖威胁、防御、评测与多智能体。
- 它适合建立概念地图，但 2025 年版本可能无法覆盖我们讨论的 2026 年方法。
- **尚未确认正式发表渠道、可靠引用量、全文文献截止时间，以及相较其他综述的影响力。未正式选定。**

后续检索线索：[LLM agents security duality: a comprehensive survey of self-security and empowered cybersecurity](https://arxiv.org/abs/2606.28450)。此前检索摘要出现过，尚未完成全文和发表信息核查，不能将更近日期等同于高影响力。

筛选标准：与 Agent 自身安全而非仅“用 Agent 做网络安全”相关；覆盖间接提示注入、工具执行、误防御及评测；能核实版本/发表信息；有可追溯的独立影响力依据；实际文献覆盖时间足够新。无法核实引用量时不要填数字，GitHub stars 也不等价于学术影响力。

检索环境记录：本会话尝试的 arXiv 搜索接口返回过 406，OpenAlex / Semantic Scholar 搜索返回过 429；单篇 arXiv 页面和 GitHub API 可用。不要把一次接口失败解释为论文不存在。未经检查的普通搜索结果有不相关内容，未采用为证据。

## 核心路线

| 论文 | 作用 | 当前状态 |
| --- | --- | --- |
| [ReAct](https://arxiv.org/abs/2210.03629) | 理解推理、动作、观察交替 | 已核对原文，不是防御论文 |
| [AgentDojo](https://arxiv.org/abs/2406.13352) | 可执行安全评测 | 已核对；主基准候选 |
| [CaMeL](https://arxiv.org/abs/2503.18813) | 控制与数据流隔离 | 已核对；结构防御基础 |
| [AgentDyn v3](https://arxiv.org/html/2602.03117v3) | 动态任务、效用与安全 | 表格与公开日志已核查；首个复现对象 |
| [AttriGuard v2](https://arxiv.org/abs/2603.10749v2) | 动作反事实归因 | 方法和局限已核对；近邻强基线候选 |
| [AgentSentry](https://arxiv.org/abs/2602.22724) | 时间诊断、净化、安全续跑 | 方法和配置局限已核对；近邻基线候选 |
| [PACT](https://arxiv.org/abs/2605.11039) | 参数来源与授权 | 核查理想来源和实际推断的区别 |
| [PIPES](https://arxiv.org/abs/2608.12789) | 观察单元与状态误导防御 | 原文与限制已核对 |
| [StepGuard](https://arxiv.org/abs/2608.24777) | 步骤监督、安全效用平衡 | 原文与限制已核对 |
| [EvoSafeHarness](https://arxiv.org/abs/2609.05903) | 运行时搜索与领域适配 | 方法与重叠范围已梳理 |

“已核对”指助手核查相关原文部分，不表示用户已精读、项目已独立复现、代码均可直接运行或结论获独立确认。

## 备选方向

- [MINJA](https://arxiv.org/abs/2503.03704)：通过查询交互写入恶意记忆。
- [Dependency-Guided Rollback Repair](https://arxiv.org/abs/2608.10502)：已诊断错误记忆与运行时依赖下的局部恢复。
- [MCPTox](https://arxiv.org/abs/2508.14925)：工具元数据污染评测。
- [ProjGuard](https://arxiv.org/abs/2605.13631)：**v2 已撤回，仅作引用更正记录。**

## 阅读产物

每篇记录：威胁模型、一个实际例子、检查发生的位置、必须获得的信息、评测和成本、作者局限、自己推测、可能否定该推测的实验。不要只保存摘要，也不要把预印本存在本身视为已验证的技术结论。
