"""Read-only MCP tools for inspecting TaskFlow's SDD artifacts."""

from pathlib import Path

from mcp.server.fastmcp import FastMCP

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = {
    "specification": "docs/SPEC.md",
    "plan": "docs/PLAN.md",
    "tasks": "docs/TASKS.md",
    "decisions": "docs/DECISIONS.md",
}

mcp = FastMCP("taskflow-docs")


@mcp.tool()
def get_sdd_status() -> dict[str, object]:
    """Return project name, SDD artifact presence, and outstanding checklist items."""
    files = {name: (PROJECT_ROOT / path).is_file() for name, path in ARTIFACTS.items()}
    task_file = PROJECT_ROOT / ARTIFACTS["tasks"]
    pending = []
    if task_file.is_file():
        pending = [
            line.removeprefix("- [ ] ").strip()
            for line in task_file.read_text(encoding="utf-8").splitlines()
            if line.startswith("- [ ] ")
        ]
    return {
        "project": "TaskFlow",
        "workflow": "Specification -> Plan -> Tasks -> Implementation -> Verification",
        "artifacts": files,
        "pending_count": len(pending),
        "pending": pending,
    }


@mcp.tool()
def read_sdd_artifact(name: str) -> str:
    """Read one project document: specification, plan, tasks, or decisions."""
    relative_path = ARTIFACTS.get(name)
    if relative_path is None:
        return "Unknown artifact. Choose: " + ", ".join(ARTIFACTS)
    path = (PROJECT_ROOT / relative_path).resolve()
    if PROJECT_ROOT.resolve() not in path.parents:
        return "Path is outside the project root."
    return path.read_text(encoding="utf-8")


if __name__ == "__main__":
    mcp.run()
