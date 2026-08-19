# Ponytail cleanup audit

> **Scope:** Complete CampusConnect repository and remote GitHub tree
> **Audit mode:** Whole-repository over-engineering review
> **Important boundary:** This report is advisory; correctness, security, and performance review remain separate validation passes.

## Executive conclusion

CampusConnect is already a relatively small Spring Boot website. The audit found **a limited amount of safe cleanup**, not a justification for a broad rewrite. The largest confirmed issue is documentation drift in the legacy remediation folder. The Maven dependency-analysis report also emitted broad “unused declared dependency” warnings, but those warnings are not reliable for Spring Boot starters, annotation-driven auto-configuration, Actuator, Flyway, Thymeleaf, test slices, or runtime JDBC drivers; no dependency is removed on that basis alone.

> **Ponytail result:** Remove stale duplicate remediation notes, preserve runtime and DBSE&DBD evidence, and defer ambiguous developer conveniences until a project-owner policy is established.

## Baseline evidence

| Check | Result |
| --- | --- |
| Baseline commit | `6bceb7c` before the documentation-only working-tree edits |
| Tracked files | Full Java application, templates, static assets, migrations, tests, CI, Docker/Compose, scripts, and documentation present |
| Test command | `./mvnw -B test` executed |
| Test result | 63 tests discovered; 28 application-context errors because the local environment supplied no MySQL credentials and Flyway attempted `ubuntu@localhost` with no password |
| Passing test groups | Unit-oriented configuration, rate limiting, event service, recommendation service, session service, user service, and model tests passed |
| Environment limitation | Runtime-backed tests require MySQL configuration; this is not a cleanup regression |
| Ignored output | `target/` is generated and ignored; it is not part of the proposed GitHub cleanup |
| Ponytail source | Official `ponytail-audit` instructions were reviewed; the workflow explicitly produces findings and applies no fixes |

## Candidate register

| Tag | Candidate | Evidence | Disposition | Reason |
| --- | --- | --- | --- | --- |
| `delete` | `docs/remediation/completion_report.md` | Claims Spring Boot 3.4.2-era state, includes stale “enterprise-grade” language, and duplicates current security, operations, testing, and showcase documents | **REMOVE** | Superseded by current documentation and contains inaccurate version/verification claims |
| `delete` | `docs/remediation/remediation_roadmap.md` | References old dependency versions and unfinished tasks that are now either implemented or represented elsewhere | **REMOVE** | Historical working notes are not authoritative evidence; current docs preserve the final controls and remaining gaps |
| `delete` | `docs/remediation/security_design.md` | Contains machine-local `file:///d:/...` links and a proposal-only README plan | **REMOVE** | Obsolete planning note with no unique security evidence |
| `yagni` | `run_app.ps1`, `stop_app.ps1` | Only referenced by `PROJECT_STRUCTURE.md`; they support Windows local development and are not runtime code | **DEFER** | Useful developer convenience; removal would reduce supported local workflows without a documented replacement |
| `yagni` | `.vscode/settings.json` | Only contains Java language-server settings; no runtime consumer | **DEFER** | Small, harmless contributor convenience; retain unless repository policy requires editor-neutral trees |
| `delete` | `.agents/rules/coderabbit-pro-autofix.md` | Contains a local Windows/WSL path, obsolete “13 comments/74 files” context, and an instruction to invoke a non-repository CLI | **REMOVE** | Stale machine-specific automation rule; it is not a reliable repository governance control |
| `native` | Maven dependencies | `dependency:analyze` reports starters as unused because usage is annotation/configuration/auto-configuration driven | **KEEP** | Removing them would break runtime or tests; verify by application context and package-level usage instead |
| `delete` | `target/` | Build output is ignored by `.gitignore` and absent from `git ls-files` | **KEEP-IGNORED** | No GitHub deletion required; clean locally when needed |
| `defer` | `images/hero.png`, `images/student_view.png` | Reference search did not establish that they are required by runtime; they may support a visual showcase | **DEFER** | Keep until visual inspection and documentation asset policy are completed |
| `defer` | `docs/StudentDashboard_QA_TestPlan.md` | Standalone QA plan may provide evidence not duplicated elsewhere | **KEEP** | Preserve as a testing artifact unless a content comparison proves complete duplication |

## Framework reachability checks

The following categories were explicitly treated as reachable even when textual reference counts are low:

| Category | Why it is protected |
| --- | --- |
| `@Configuration`, `@Service`, `@Controller`, `@Repository` classes | Spring component scanning discovers them at runtime |
| Thymeleaf templates and static assets | View names and browser URLs resolve them indirectly |
| Flyway migrations | Versioned filenames are discovered by Flyway and are part of database history |
| `application*.properties` keys | Spring binding and auto-configuration consume them without direct Java references |
| CI workflows and shell scripts | They are external operational entry points and handout evidence |
| Security and test classes | They encode controls and verification even when not part of the production call graph |

## Adopted cleanup principles

The audit adopts the following practices from the supplied references without introducing their unrelated runtime stacks:

1. **Ponytail:** rank cuts by evidence and favor deletion over speculative abstraction, but keep the audit one-shot and separate from correctness/security review. [1]
2. **Agent governance:** apply least privilege, explicit policy, clean execution boundaries, and auditable decisions to automation and CI guidance. [2]
3. **Code intelligence:** use reference-aware search and framework reachability checks before declaring a symbol dead. [3]
4. **No-mistakes Git:** require clean-tree checks, expected diff inspection, validation before push, and no history rewrite. [4]
5. **UI/UX review:** keep screenshots and visual assets only when they improve product comprehension, accessibility review, or evaluator evidence. [5] [6]
6. **Rust/ImGui/open-design boundaries:** retain a focused Java website rather than adding native, desktop, or alternate-language infrastructure without a concrete requirement. [7] [8] [9]

## Planned implementation

The only high-confidence deletions from this audit are the three stale remediation notes and the machine-specific CodeRabbit rule. The PowerShell helpers, editor settings, screenshots, QA plan, migrations, tests, CI, and all runtime dependencies remain until a later evidence-based review proves otherwise.

## References

[1]: https://github.com/DietrichGebert/ponytail/blob/main/skills/ponytail-audit/SKILL.md "Ponytail whole-repository audit"
[2]: https://github.com/microsoft/agent-governance-toolkit "Microsoft Agent Governance Toolkit"
[3]: https://github.com/DeusData/codebase-memory-mcp "Codebase Memory MCP"
[4]: https://github.com/kunchenguid/no-mistakes "No Mistakes"
[5]: https://github.com/nexu-io/open-design "Open Design"
[6]: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill "UI/UX Pro Max Skill"
[7]: https://github.com/rust-lang/rust "Rust"
[8]: https://github.com/ocornut/imgui "Dear ImGui"
[9]: https://github.com/DietrichGebert/ponytail "Ponytail repository"
