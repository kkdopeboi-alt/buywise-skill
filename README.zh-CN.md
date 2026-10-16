# BuyWise — 关键信息必问，减少无效沟通

[English](README.md) · [v0.3 改进](docs/V03-CHANGES.md)

Research-first shopping skill for personal agents. Compare exact products or select up to three useful alternatives, with seller evidence, comparable cost, delivery and clear buying boundaries.

**v0.3：可安装的指令与规则包，附关键问题检查器、离线报价计算器和可复跑沙盘。不是购物平台、价格数据库或自动支付服务。**

## 能做什么

- 使用宿主 Bot 已有搜索/浏览能力查商品，区分产品、变体、卖家报价。
- 比较到手成本、优惠资格、配送、退货、保修和兼容性。
- 尺码、尺码体系、地区和兼容性等会影响决策的关键问题必须问；明确适用的上下文/记忆已有时不重复问。给礼物不能套用本人的尺码与地址。关键项未解决时不冒充精准推荐。
- 对明确授权且工具支持的购买提供执行流程；遇到访问限制或支付不明时准确交接。

不能保证所有网站访问、正品、库存或到货时间；Markdown 不能提供支付层幂等、权限强制或注入免疫。无自动抓价后台、API密钥、联盟链接、联网遥测或隐藏收费。

## 安装

实际 Skill 目录是 `skills/buywise/`，其中包含必需 `SKILL.md`、按需引用和可选脚本。

**Codex：** 将整个 `skills/buywise` 文件夹复制到自己的技能目录（通常 `~/.codex/skills/buywise`），按客户端要求重新加载。调用 `$buywise`。

**其他支持 SKILL.md 的 Agent：** 把同一文件夹放到该产品文档规定的技能目录。宿主须支持相对引用；若执行脚本需 Python 3.10+。搜索/浏览是实际比价所需能力，支付是可选且单独授权的能力。无浏览能力时仅能整理用户提供的材料，不能声称已核验实时信息。

未验证 Grok Bot、Muse 或其他宿主的安装兼容性；不要把“能读 Markdown”当作已适配。

## 使用示例

```text
用 $buywise 给我找100美元内适合视频会议的耳机。
我用Windows电脑，寄到美国10001；优先新机，不需要会员价。
```

```text
比较这个准确型号在品牌官网和Amazon的报价，核对卖家、版本、
税费运费和退货，不要购买。资料不全就标明。
```

```text
按我已给的设备型号配录音套装，总预算200美元包含必需线材。
先研究，最多给三个完整方案。
```

## 项目布局

- `skills/buywise/SKILL.md`：宿主加载的入口，英文规则便于跨环境复用；回复语言跟随用户。
- `skills/buywise/references/`：需求、比价履约、支付恢复和报价格式。
- `skills/buywise/scripts/quote_check.py`：Python标准库离线计算器，无网络或购买能力。
- `skills/buywise/scripts/decision_gate.py`：核验声明的关键字段及记忆适用性，缺项生成合并问题；不替代Agent识别关键字段。
- `docs/RESEARCH.md`：研究依据、问题映射和边界。
- `docs/EVALUATION.md`：20个行为验收场景。
- `examples/quote.json`：虚构算术样例；不是真实商品。
- `tests/`：未知费用、估算、金额精度与输入验证测试。
- `tests/run_sandbox.py`：26个可复跑关键问题沙盘；不是浏览器/模型端到端基准。
- `docs/PROBLEM-SOLUTION.md`：用户问题与方案、验证范围映射。

```sh
python skills/buywise/scripts/quote_check.py examples/quote.json
python skills/buywise/scripts/decision_gate.py examples/intake.json
python skills/buywise/scripts/compare_offers.py examples/offers.json
python -m unittest discover -s tests -v
python tests/run_sandbox.py --output docs/sandbox-results.json
```

## 版本与贡献

v0.2 增强强制关键澄清、收件人记忆核验及可复跑沙盘，但尚无真实商家端到端付款测试。优先贡献可复现错误、品类兼容证据和宿主适配记录。请提供脱敏需求、来源时间、预期/实际行为；不要提交账号、地址、支付资料或抓取到的受限数据。新增商家接入须说明权限、缓存规则、限流和失败处理。

代码与原创文档使用 MIT；引用页面及第三方数据保留原权利。没有已运行的全类目数据库、星数、节省金额或成功率声明。

## v0.3 新增

关键字段按场景补全；无效值/收件人不符会阻断；无邮编地区可用配送区域。新增离线同款报价比较器，只对同型号、同数量、同目的地的完整已观测报价排序，过期/估算/缺费保持待核验。所有工具依赖调用方提供真实证据，不能自行验证实时库存或正品。
