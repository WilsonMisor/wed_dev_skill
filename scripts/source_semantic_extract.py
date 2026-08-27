#!/usr/bin/env python3
"""Safe deterministic semantic candidate extraction for Blueprint source intake.

This module never executes supplied project material and never grants authority.
It extracts candidate requirements plus observed/declared architecture and stack
facts from supported text/document/project metadata. Human/governed decisions
remain the only route to APPROVED architecture/stack or authoritative source
status.
"""
from __future__ import annotations

import io
import json
from pathlib import Path, PurePosixPath
import re
import stat
import zipfile
import xml.etree.ElementTree as ET

TEXT_EXTENSIONS = {
    ".md", ".markdown", ".txt", ".rst", ".adoc", ".json", ".jsonl",
    ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf", ".env.example",
    ".php", ".js", ".jsx", ".ts", ".tsx", ".py", ".java", ".kt", ".kts",
    ".swift", ".dart", ".go", ".rs", ".rb", ".cs", ".cpp", ".cc", ".c",
    ".sql", ".sh", ".ps1", ".html", ".htm", ".css", ".scss", ".xml",
    ".gradle", ".properties", ".vue", ".svelte",
}
MAX_TEXT_BYTES = 4 * 1024 * 1024
MAX_ARCHIVE_MEMBER_BYTES = 8 * 1024 * 1024

REQUIREMENT_RE = re.compile(
    r"(?:\b(?:must|shall|required to|is required to|will need to|needs to)\b|"
    r"^\s*(?:REQ[-_ ]?\d+|FR[-_ ]?\d+|NFR[-_ ]?\d+)\s*[:.-])",
    re.IGNORECASE,
)
LIST_PREFIX_RE = re.compile(r"^\s*(?:[-*+]\s+|\d+[.)]\s+|[A-Za-z][.)]\s+)")
ARCH_DECL_RE = re.compile(
    r"\b(?:architecture|architectural|frontend|front-end|backend|back-end|database|data store|"
    r"api gateway|REST API|GraphQL|microservice|micro-service|monolith|modular monolith|"
    r"event[- ]driven|client[- ]server|three[- ]tier|layered architecture|serverless|queue|"
    r"message broker|cache|CDN|load balancer|worker|background job)\b",
    re.IGNORECASE,
)
STACK_DECL_RE = re.compile(
    r"\b(?:built with|implemented (?:with|in)|uses?|using|technology stack|tech stack|stack is|"
    r"framework|runtime|database|language)\b",
    re.IGNORECASE,
)

MANIFEST_NAMES = {
    "package.json", "pyproject.toml", "requirements.txt", "poetry.lock", "pipfile",
    "composer.json", "gemfile", "go.mod", "cargo.toml", "pubspec.yaml",
    "build.gradle", "build.gradle.kts", "pom.xml", "global.json", "package-lock.json",
    "pnpm-lock.yaml", "yarn.lock", "dockerfile", "docker-compose.yml", "compose.yml",
}

FRAMEWORK_MARKERS = {
    "react": "React", "next": "Next.js", "nextjs": "Next.js", "vue": "Vue",
    "nuxt": "Nuxt", "svelte": "Svelte", "angular": "Angular", "express": "Express",
    "nestjs": "NestJS", "fastify": "Fastify", "django": "Django", "flask": "Flask",
    "fastapi": "FastAPI", "laravel": "Laravel", "symfony": "Symfony",
    "wordpress": "WordPress", "flutter": "Flutter", "rails": "Ruby on Rails",
    "spring": "Spring", "spring-boot": "Spring Boot", "prisma": "Prisma",
    "sequelize": "Sequelize", "typeorm": "TypeORM", "supabase": "Supabase",
}

DB_MARKERS = {
    "postgres": "PostgreSQL", "postgresql": "PostgreSQL", "pg": "PostgreSQL",
    "mysql": "MySQL", "mariadb": "MariaDB", "sqlite": "SQLite", "mongodb": "MongoDB",
    "redis": "Redis", "sqlserver": "SQL Server", "mssql": "SQL Server",
    "dynamodb": "DynamoDB", "firestore": "Firestore",
}

LANGUAGE_BY_EXT = {
    ".py": "Python", ".php": "PHP", ".js": "JavaScript", ".jsx": "JavaScript",
    ".ts": "TypeScript", ".tsx": "TypeScript", ".java": "Java", ".kt": "Kotlin",
    ".kts": "Kotlin", ".swift": "Swift", ".dart": "Dart", ".go": "Go",
    ".rs": "Rust", ".rb": "Ruby", ".cs": "C#", ".cpp": "C++", ".cc": "C++",
    ".c": "C", ".vue": "Vue SFC", ".svelte": "Svelte", ".sql": "SQL",
}


def _safe_archive_name(name: str) -> PurePosixPath:
    normalized = name.replace("\\", "/")
    if normalized.startswith("/") or re.match(r"^[A-Za-z]:", normalized):
        raise ValueError(f"unsafe absolute archive path: {name}")
    p = PurePosixPath(normalized)
    if any(part in {"", ".."} for part in p.parts):
        raise ValueError(f"unsafe archive traversal path: {name}")
    return p


def _archive_symlink(info: zipfile.ZipInfo) -> bool:
    return stat.S_ISLNK((info.external_attr >> 16) & 0xFFFF)


def _decode_text(data: bytes) -> str | None:
    if b"\x00" in data[:4096]:
        return None
    for encoding in ("utf-8", "utf-8-sig", "utf-16", "cp1252"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return None


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _paragraph_lines(root: ET.Element) -> list[str]:
    """Return one logical OOXML paragraph per line, preserving document boundaries."""
    lines: list[str] = []
    for paragraph in root.iter():
        if _local_name(paragraph.tag) != "p":
            continue
        pieces: list[str] = []
        for node in paragraph.iter():
            if _local_name(node.tag) == "t" and node.text:
                pieces.append(node.text)
        text = "".join(pieces).strip()
        if text:
            lines.append(text)
    return lines


def _office_xml_text(data: bytes, kind: str) -> str:
    """Extract DOCX/PPTX text without collapsing paragraphs into one line.

    Each Word paragraph becomes one line. Each PowerPoint paragraph becomes one
    line in deterministic slide order. This gives downstream extraction stable
    paragraph-level wording and a deterministic line/paragraph location.
    """
    lines: list[str] = []
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        if kind == ".docx":
            names = ["word/document.xml"] if "word/document.xml" in zf.namelist() else []
        elif kind == ".pptx":
            names = sorted(
                (n for n in zf.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)),
                key=lambda n: int(re.search(r"slide(\d+)\.xml$", n).group(1)),
            )
        else:
            names = []
        for name in names:
            root = ET.fromstring(zf.read(name))
            lines.extend(_paragraph_lines(root))
    return "\n".join(lines)


def _read_path_text(path: Path) -> str | None:
    try:
        size = path.stat().st_size
    except OSError:
        return None
    suffix = path.suffix.lower()
    if size > MAX_TEXT_BYTES and suffix not in {".docx", ".pptx"}:
        return None
    if suffix in {".docx", ".pptx"}:
        if size > MAX_ARCHIVE_MEMBER_BYTES:
            return None
        try:
            return _office_xml_text(path.read_bytes(), suffix)
        except (OSError, zipfile.BadZipFile, ET.ParseError, KeyError):
            return None
    if suffix not in TEXT_EXTENSIONS and path.name.lower() not in MANIFEST_NAMES:
        return None
    try:
        return _decode_text(path.read_bytes())
    except OSError:
        return None


def _read_zip_member(zf: zipfile.ZipFile, info: zipfile.ZipInfo) -> str | None:
    if info.is_dir() or _archive_symlink(info):
        return None
    _safe_archive_name(info.filename)
    if info.file_size > MAX_ARCHIVE_MEMBER_BYTES:
        return None
    suffix = Path(info.filename).suffix.lower()
    name = Path(info.filename).name.lower()
    data = zf.read(info)
    if suffix in {".docx", ".pptx"}:
        try:
            return _office_xml_text(data, suffix)
        except (zipfile.BadZipFile, ET.ParseError, KeyError):
            return None
    if suffix not in TEXT_EXTENSIONS and name not in MANIFEST_NAMES:
        return None
    return _decode_text(data)


def source_text_map(source: Path, records: list[dict]) -> tuple[dict[str, str], list[str]]:
    """Return record-path -> safely decoded text without executing source material."""
    wanted = {str(r.get("path")): r for r in records}
    texts: dict[str, str] = {}
    warnings: list[str] = []
    if source.is_dir():
        for rel in sorted(wanted):
            p = source / rel
            if p.is_symlink():
                continue
            text = _read_path_text(p)
            if text is not None:
                texts[rel] = text
    elif source.is_file() and zipfile.is_zipfile(source):
        try:
            with zipfile.ZipFile(source) as zf:
                by_name = {i.filename.replace("\\", "/"): i for i in zf.infolist()}
                for rel in sorted(wanted):
                    info = by_name.get(rel)
                    if info is None:
                        continue
                    text = _read_zip_member(zf, info)
                    if text is not None:
                        texts[rel] = text
        except zipfile.BadZipFile:
            warnings.append("semantic extraction skipped: invalid ZIP")
    elif source.is_file():
        text = _read_path_text(source)
        if text is not None and records:
            texts[str(records[0].get("path"))] = text
    return texts, warnings


def _clean_statement(line: str) -> str:
    value = LIST_PREFIX_RE.sub("", line.strip())
    value = re.sub(r"^#+\s*", "", value)
    return re.sub(r"\s+", " ", value).strip()


def _requirement_category(text: str) -> str:
    low = text.lower()
    if any(k in low for k in ("security", "encrypt", "authentication", "authorization", "permission", "nonce")):
        return "SECURITY"
    if any(k in low for k in ("performance", "latency", "throughput", "response time", "capacity")):
        return "PERFORMANCE"
    if any(k in low for k in ("privacy", "personal data", "retention", "gdpr", "consent")):
        return "PRIVACY"
    if any(k in low for k in ("accessibility", "wcag", "screen reader", "keyboard")):
        return "ACCESSIBILITY"
    if any(k in low for k in ("availability", "recover", "backup", "rollback", "reliab")):
        return "RELIABILITY"
    return "FUNCTIONAL_OR_GENERAL"


def extract_requirements(texts: dict[str, str], records: list[dict]) -> list[dict]:
    by_path = {str(r.get("path")): r for r in records}
    found: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for path in sorted(texts):
        record = by_path[path]
        in_requirement_section = False
        for line_no, raw in enumerate(texts[path].splitlines(), 1):
            stripped = raw.strip()
            if not stripped:
                continue
            heading = re.sub(r"^#+\s*", "", stripped).strip().lower().rstrip(":")
            if heading in {
                "requirements", "functional requirements", "non-functional requirements",
                "acceptance criteria", "constraints", "business rules",
            }:
                in_requirement_section = True
                continue
            if stripped.startswith("#") and in_requirement_section:
                in_requirement_section = False
            statement = _clean_statement(raw)
            if len(statement) < 8 or len(statement) > 1500:
                continue
            candidate = bool(REQUIREMENT_RE.search(statement)) or (
                in_requirement_section and bool(LIST_PREFIX_RE.match(raw))
            )
            if not candidate:
                continue
            key = (str(record["source_id"]), statement.casefold())
            if key in seen:
                continue
            seen.add(key)
            # source_id is the canonical source reference. The corresponding
            # path remains losslessly available in SOURCE-INTAKE.sources. Not
            # duplicating source_path here prevents path-vs-ID merge keys from
            # creating duplicate governed/extracted requirements.
            found.append({
                "source_id": record["source_id"],
                "source_location": f"line {line_no}",
                "original_wording": statement,
                "normalized_interpretation": statement,
                "category": _requirement_category(statement),
                "authority": record.get("authority", "UNCLASSIFIED"),
                "confidence": "HIGH" if REQUIREMENT_RE.search(statement) else "MEDIUM",
                "conflict_state": "NONE",
                "extraction_method": "DETERMINISTIC_TEXT_CANDIDATE",
                "requires_governed_review": True,
            })
    return found


def _package_json_stack(text: str) -> tuple[set[str], set[str]]:
    frameworks: set[str] = set()
    databases: set[str] = set()
    try:
        obj = json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return frameworks, databases
    deps: dict = {}
    if isinstance(obj, dict):
        for key in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
            if isinstance(obj.get(key), dict):
                deps.update(obj[key])
    for dep in deps:
        normalized = dep.lower().replace("@", "").split("/")[-1]
        for marker, label in FRAMEWORK_MARKERS.items():
            if marker in normalized:
                frameworks.add(label)
        for marker, label in DB_MARKERS.items():
            if marker == normalized or marker in normalized:
                databases.add(label)
    return frameworks, databases


def _implementation_evidence_path(path: str) -> bool:
    p = Path(path)
    return p.name.lower() in MANIFEST_NAMES or p.suffix.lower() in LANGUAGE_BY_EXT


def _scan_markers(text: str, markers: dict[str, str]) -> set[str]:
    low = text.lower()
    found: set[str] = set()
    for marker, label in markers.items():
        if re.search(rf"(?:^|[^a-z0-9]){re.escape(marker)}(?:[^a-z0-9]|$)", low):
            found.add(label)
    return found


def extract_observed_stack(texts: dict[str, str], records: list[dict]) -> dict:
    """Infer *observed* stack only from implementation files and manifests.

    Documentary prose is intentionally excluded here; technology mentioned in a
    plan, legacy note, rejected option, or requirements document belongs in the
    declared stack channel, never observed implementation evidence.
    """
    languages: set[str] = set()
    frameworks: set[str] = set()
    databases: set[str] = set()
    package_managers: set[str] = set()
    infrastructure: set[str] = set()
    evidence: list[dict] = []
    for r in records:
        path = str(r.get("path"))
        p = Path(path)
        suffix = p.suffix.lower()
        name = p.name.lower()
        implementation = _implementation_evidence_path(path)
        if suffix in LANGUAGE_BY_EXT:
            languages.add(LANGUAGE_BY_EXT[suffix])
        if not implementation:
            continue

        text = texts.get(path, "")
        if name == "package.json":
            package_managers.add("npm-compatible")
            fws, dbs = _package_json_stack(text)
            frameworks |= fws
            databases |= dbs
        elif name in {"pyproject.toml", "requirements.txt", "pipfile", "poetry.lock"}:
            package_managers.add("Python packaging")
        elif name == "composer.json":
            package_managers.add("Composer")
        elif name == "gemfile":
            package_managers.add("Bundler")
        elif name == "go.mod":
            package_managers.add("Go modules")
        elif name == "cargo.toml":
            package_managers.add("Cargo")
        elif name == "pubspec.yaml":
            package_managers.add("Dart/Flutter pub")
        if name in {"dockerfile", "docker-compose.yml", "compose.yml"}:
            infrastructure.add("Docker")

        normalized_path = path.replace("\\", "/").lower()
        if "wp-content/" in normalized_path:
            frameworks.add("WordPress")
        frameworks |= _scan_markers(text, FRAMEWORK_MARKERS)
        databases |= _scan_markers(text, DB_MARKERS)
        evidence.append({"source_id": r["source_id"], "path": path})

    return {
        "languages": sorted(languages),
        "frameworks": sorted(frameworks),
        "databases": sorted(databases),
        "package_managers": sorted(package_managers),
        "infrastructure": sorted(infrastructure),
        "evidence": evidence,
        "provenance": "OBSERVED_FROM_IMPLEMENTATION_FILES_AND_PROJECT_METADATA",
        "requires_governed_review": True,
    }


def extract_declared_facts(texts: dict[str, str], records: list[dict]) -> tuple[dict, dict]:
    by_path = {str(r.get("path")): r for r in records}
    arch: list[dict] = []
    stack: list[dict] = []
    arch_seen: set[tuple[str, str]] = set()
    stack_seen: set[tuple[str, str]] = set()
    stack_tokens = [
        *FRAMEWORK_MARKERS.keys(), *DB_MARKERS.keys(), "python", "php", "javascript",
        "typescript", "java", "kotlin", "swift", "dart", "golang", "rust", "ruby",
        "c#", "docker", "wordpress",
    ]
    for path in sorted(texts):
        for line_no, raw in enumerate(texts[path].splitlines(), 1):
            statement = _clean_statement(raw)
            if len(statement) < 8 or len(statement) > 1200:
                continue
            if ARCH_DECL_RE.search(statement):
                key = (path, statement.casefold())
                if key not in arch_seen:
                    arch_seen.add(key)
                    arch.append({
                        "source_id": by_path[path]["source_id"],
                        "path": path,
                        "location": f"line {line_no}",
                        "statement": statement,
                        "confidence": "MEDIUM",
                        "requires_governed_review": True,
                    })
            if STACK_DECL_RE.search(statement) and any(token in statement.lower() for token in stack_tokens):
                key = (path, statement.casefold())
                if key not in stack_seen:
                    stack_seen.add(key)
                    stack.append({
                        "source_id": by_path[path]["source_id"],
                        "path": path,
                        "location": f"line {line_no}",
                        "statement": statement,
                        "confidence": "MEDIUM",
                        "requires_governed_review": True,
                    })
    return (
        {"statements": arch, "provenance": "DECLARED_IN_SOURCE_TEXT", "requires_governed_review": True},
        {"statements": stack, "provenance": "DECLARED_IN_SOURCE_TEXT", "requires_governed_review": True},
    )


def extract_observed_architecture(records: list[dict], observed_stack: dict) -> dict:
    paths = [str(r.get("path", "")).replace("\\", "/").lower() for r in records]
    components: set[str] = set()
    signals: list[str] = []
    if any("/api/" in f"/{p}/" or p.startswith("api/") for p in paths):
        components.add("API")
        signals.append("api directory")
    if any(any(seg in p for seg in ("frontend/", "client/", "src/components/", "templates/")) for p in paths):
        components.add("Frontend")
        signals.append("frontend/client/UI source layout")
    if any(any(seg in p for seg in ("backend/", "server/", "controllers/", "routes/")) for p in paths):
        components.add("Backend")
        signals.append("backend/server source layout")
    if observed_stack.get("databases") or any(any(x in p for x in ("migrations/", "schema.sql", "models/")) for p in paths):
        components.add("Data persistence")
        signals.append("database dependency/schema/model layout")
    if any("wp-content/themes/" in p for p in paths):
        components.add("WordPress classic/theme layer")
        signals.append("wp-content/themes")
    if any("wp-content/plugins/" in p for p in paths):
        components.add("WordPress plugin layer")
        signals.append("wp-content/plugins")
    if any("docker" in Path(p).name for p in paths):
        components.add("Containerized runtime")
        signals.append("Docker metadata")
    shape = "UNKNOWN"
    if "WordPress classic/theme layer" in components or "WordPress plugin layer" in components:
        shape = "WORDPRESS_APPLICATION"
    elif {"Frontend", "Backend", "Data persistence"}.issubset(components):
        shape = "MULTI_TIER_APPLICATION"
    elif "Backend" in components and "Data persistence" in components:
        shape = "SERVER_APPLICATION_WITH_PERSISTENCE"
    elif components:
        shape = "PARTIALLY_OBSERVED_APPLICATION"
    return {
        "shape": shape,
        "components": sorted(components),
        "signals": sorted(signals),
        "provenance": "OBSERVED_FROM_REPOSITORY_STRUCTURE",
        "requires_governed_review": True,
    }


def merge_fact_objects(auto: dict, governed: dict) -> dict:
    """Preserve both extraction and governed input without silently overwriting either."""
    if not governed:
        return auto
    return {
        "extracted": auto,
        "governed": governed,
        "precedence": "GOVERNED_INPUT_DOES_NOT_ERASE_EXTRACTED_EVIDENCE",
    }


def semantic_extract(source: Path, records: list[dict]) -> dict:
    texts, warnings = source_text_map(source, records)
    requirements = extract_requirements(texts, records)
    observed_stack = extract_observed_stack(texts, records)
    declared_architecture, declared_stack = extract_declared_facts(texts, records)
    observed_architecture = extract_observed_architecture(records, observed_stack)
    return {
        "source_requirements": requirements,
        "observed_architecture": observed_architecture,
        "declared_architecture": declared_architecture,
        "observed_stack": observed_stack,
        "declared_stack": declared_stack,
        "warnings": warnings,
        "documents_examined": sorted(texts),
        "semantic_extraction_version": "1.1",
        "authority_boundary": "CANDIDATES_ONLY_HUMAN_OR_GOVERNED_DECISION_REQUIRED_FOR_APPROVAL",
    }
