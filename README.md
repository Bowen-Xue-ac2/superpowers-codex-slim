# Superpowers Codex Slim

给 Codex 用的个人特化 Superpowers：保留组合式技能，把启动权、任务范围和验收标准交还给用户。

基于 [obra/superpowers](https://github.com/obra/superpowers) **v7.0.0**。这是独立维护的 Codex 适配版，不代表上游默认工作流，也不是上游官方发行。

## 目录

- [它如何工作](#它如何工作)
- [这个版本改变了什么](#这个版本改变了什么)
- [安装](#安装)
- [基本工作方式](#基本工作方式)
- [里面有什么](#里面有什么)
- [个人信息与配置隔离](#个人信息与配置隔离)
- [验证与边界](#验证与边界)
- [更新与贡献](#更新与贡献)
- [许可证](#许可证)

## 它如何工作

普通开发直接做。你提出修复、设计、调试或验证请求，不会因此自动进入 Superpowers。

需要一套流程时，说“启用 Superpowers”。只需要某个方法时，说“使用 systematic-debugging”或点名单项技能。技能按当前任务工作；引用示例、历史记录、审阅或编辑技能文本都不构成启用。

已经有效的证据继续有效。换阶段、换 Agent、恢复上下文或准备交付，不是重新跑测试、计算文件哈希或再加一层审查的理由。相关代码、输入、环境或验收要求变了，就补受影响的验证。

完成、取消或关闭后退出。下一项任务不会继承一串已经过期的待办。

## 这个版本改变了什么

这些调整来自个人使用中出现的重复施工、范围膨胀和方法错配。它们收窄的是工作规则，不取消必要的工程检查。

| 使用中的问题 | Slim 的处理 |
|---|---|
| 普通请求、低门槛匹配或“1% 相关”就启动整套流程 | 显式准入；15 项技能均声明 `allow_implicit_invocation: false`，入口另行约束引用、历史与编辑场景 |
| 点名一个技能，却连带规划、TDD、多 Agent 和多轮 review | 单技能只授权该项；`REQUIRED SUB-SKILL` 与交接建议不能自行扩链；正常读取、修改和局部验证继续执行 |
| 到了下一阶段就重跑同一套测试、哈希和检查 | 统一有效证据规则；同状态复用，相关变化或具体缺口才补验 |
| 完成脚本把已经通过的测试再跑一遍 | `task-done --reuse` 绑定任务、计划、命令、验收目标和 Git 状态，不重复执行或追加完成记录 |
| 上下文恢复后重建计划、复活已取消任务、多写者互相覆盖 | 复用现有任务记录，保留目标、下一步、完成证据、移交/取消事项、唯一写者及最新指令 |
| 结果成功，却没完成用户指定的方法 | 结果验收与方法验收分开；关键未知方法先在最小副本验证，查询不能冒充写入 |
| 审查把风格、假设中的兼容性和顺手重构升级成需求 | 阻塞项须关联当前验收、支持范围内的可达缺陷或必要保障；复审聚焦原问题及修复风险 |
| 防御和备份无限加层，交付还没结束就报完成 | 在负责层与独立信任边界保留必要防护；检查点先明确恢复目标；等待原操作终态，unknown 先核对原状态 |

真实可达缺陷、明确验证要求、宿主强制检查和安全边界仍然有效。没有发生过生产事故，不代表风险可以忽略；已有证据也不能替失败或未完成的方法要求背书。

“Slim”指流程与范围的收敛。没有经过统计对照，不宣称更快、更省 token 或能够消除所有模型偏差。

## 安装

面向支持原生 plugin marketplace 的 Codex CLI。先确认你安装的宿主支持这些命令。

```powershell
codex plugin marketplace add Bowen-Xue-ac2/superpowers-codex-slim --ref v7.0.0-slim.1
codex plugin add superpowers@superpowers-codex-slim
```

安装后新建任务或按宿主支持的方式重新加载。若已有其他 Superpowers 发行版，核对并关闭重复的 SP 插件入口，保留其他插件与账户指令。不要整份覆盖 `AGENTS.md`，也不要把插件缓存作为维护源。

Codex Desktop 可以使用共享插件配置，但本版没有完成 Desktop UI 的独立重新加载验收；安装成功不等于当前旧会话已切换到新内容。

如果账户/项目还保留自动启用 SP 的旧条款，只替换冲突的 SP 条款。可参考 [最小指令片段](docs/config-example.md)，不要把示例当成完整账户配置。

此包的 Codex manifest 没有注册启动 Hook；也不安装 STS Guard、Governance、网络服务或凭据。

## 基本工作方式

普通任务：

```text
修复这个计算错误，并运行必要的局部测试。
```

启用当前任务需要的流程：

```text
启用 Superpowers：为这个已经确定的需求安排必要的实现步骤。
```

只用一个技能：

```text
使用 systematic-debugging，定位这个已复现的问题。
```

退出当前任务的 SP 工作流：

```text
关闭 Superpowers，继续完成当前已授权的普通工程工作。
```

必要验证不因关闭流程而消失。授权范围、明确方法和宿主审批也不因启用技能而扩大。

### 复用完成证据

从插件内的 `skills/executing-plans/` 使用已有 helper：

```bash
bash scripts/task-done PLAN N BASE --acceptance "current task acceptance" -- COMMAND ARGS...
bash scripts/task-done PLAN N BASE --reuse --acceptance "current task acceptance" -- COMMAND ARGS...
```

第二行对照相同任务、计划、精确 argv、验收目标、BASE/HEAD 和干净状态，复用之前的成功结果，不重新执行命令。环境、输入、配置和已知缺陷仍需由调用者判断；身份相同不等于所有语义条件都满足。

已有有效外部回执也可以直接引用。不要仅为补齐 helper 的新格式而重跑无变化检查，更不能伪造一份新回执。完整规则见 [evidence-policy.md](skills/verification-before-completion/evidence-policy.md)。

## 里面有什么

保留 15 项技能及其必要脚本和支持材料：

- 需求与计划：`brainstorming`、`writing-plans`。
- 实现与协作：`executing-plans`、`subagent-driven-development`、`dispatching-parallel-agents`、`using-git-worktrees`。
- 调试与验证：`systematic-debugging`、`test-driven-development`、`verification-before-completion`。
- 审查与收尾：`requesting-code-review`、`receiving-code-review`、`finishing-a-development-branch`。
- 入口与技能维护：`using-superpowers`、`diagnosing-superpowers`、`writing-skills`。

公开包只保留 Codex 清单、技能、必要资源和定向测试。不捆绑其他宿主的自动启动入口、上游完整 Git 历史、个人账户配置或本机运维档案。

STS 是独立组件。本版的证据与审查规则可与其软指导协同，但本仓库不捆绑、不安装也不默认启动 STS Guard。

## 个人信息与配置隔离

**公开规则，私有配置。** 个性化的是工作边界，不是把个人工作台复制到 GitHub。

- 公开：可复用技能、通用示例、定向测试、上游归属和脱敏验证摘要。
- 留在本地：账户/项目完整指令、绝对路径、业务资料、会话与原始回执、备份、环境变量、认证和私钥。
- 提交使用 GitHub noreply 身份和 GPG 签名；仓库不包含密钥文件，也不携带本机旧 Git 历史。
- 个人约束留在宿主支持的账户/项目配置中，按条款合并；本仓库不自动扫描、上传或改写这些文件。

`.gitignore` 只是降低误提交概率，不是秘密检测器或访问控制。这一隔离说明针对发布内容和配置归属，不承诺运行时 DLP、沙箱或通用权限治理。详见 [个人配置边界](docs/personalization.md)。

## 验证与边界

规则基线在 Windows、Codex CLI `0.165.0` 的新会话中完成定向验证：普通请求不触发、显式启用有效、单技能不扩链、同状态证据复用、相关变化后补验。helper 的 12 项隔离 Git 夹具测试通过。

这些结果来自发布前的同内容安装副本；本次公开仓库做了清单、文档和发布材料隔离，没有把安装路径变更说成新一轮行为测试。原始私人回执不进入仓库，公开范围见 [验证说明](docs/validation.md)。

没有验证 Desktop UI、实际平台 compaction 或跨宿主普适效果。`allow_implicit_invocation: false` 是宿主元数据与指令配合的一部分，不是权限中间件。

## 更新与贡献

按具体版本或提交更新，核对原生安装副本并新建任务。不要通过整份覆盖账户指令或反复修改缓存来升级。

贡献请说明当前问题、受影响路径、必要改动和实际验证。保持一次修改的范围；不要为一条文案改动自动引入新框架、模型服务或全量审计。个人特化不自动适合上游，本仓库不会把这些规则冒充上游默认行为。

## 许可证

[MIT](LICENSE)。保留 Jesse Vincent 与上游 Superpowers 的归属；本版由 Bowen-Xue-ac2 独立维护。基线与差异范围见 [UPSTREAM.md](UPSTREAM.md)。
