import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "build" / "config.json"
FALLBACK_CONFIG_PATH = ROOT / "build" / "config.example.json"
STATIC_DIR = ROOT / "static"
DEFAULT_EXTENSIONS = [".flac", ".mp3", ".wav", ".m4a", ".ogg"]


def slugify(value: str) -> str:
    text = value.lower().strip()
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"[^\w\-]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return text or "track"


def load_config() -> dict:
    path = CONFIG_PATH if CONFIG_PATH.exists() else FALLBACK_CONFIG_PATH
    with path.open("r", encoding="utf-8") as f:
        cfg = json.load(f)

    source_dir = (ROOT / cfg.get("sourceDir", ".")).resolve()
    output_dir = (ROOT / cfg.get("outputDir", "dist")).resolve()
    audio_subdir = cfg.get("audioOutputSubdir", "audio")
    extensions = [x.lower() for x in cfg.get("audioExtensions", DEFAULT_EXTENSIONS)]

    return {
        "source_dir": source_dir,
        "output_dir": output_dir,
        "audio_subdir": audio_subdir,
        "extensions": extensions,
    }


def ensure_clean_output(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    if STATIC_DIR.exists():
        for item in STATIC_DIR.iterdir():
            target = output_dir / item.name
            if item.is_dir():
                shutil.copytree(item, target, dirs_exist_ok=True)
            else:
                shutil.copy2(item, target)


def collect_audio_files(source_dir: Path, output_dir: Path, extensions: list[str]) -> list[Path]:
    files: list[Path] = []
    excluded = {
        output_dir.resolve(),
        (ROOT / ".git").resolve(),
        (ROOT / ".cursor").resolve(),
        (ROOT / ".specify").resolve(),
        (ROOT / "specs").resolve(),
        (ROOT / "build").resolve(),
        (ROOT / "static").resolve(),
    }

    for file in source_dir.rglob("*"):
        if not file.is_file():
            continue
        if file.suffix.lower() not in extensions:
            continue
        if any(parent.resolve() in excluded for parent in [file.parent, *file.parents]):
            continue
        files.append(file)
    return sorted(files)


def build_manifest(audio_files: list[Path], output_dir: Path, audio_subdir: str) -> dict:
    audio_target = output_dir / audio_subdir
    audio_target.mkdir(parents=True, exist_ok=True)

    used_names: set[str] = set()
    items: list[dict] = []

    for index, src in enumerate(audio_files, start=1):
        stem = src.stem
        ext = src.suffix
        base_name = src.name
        target_name = base_name
        counter = 1
        while target_name.lower() in used_names:
            target_name = f"{stem}-{counter}{ext}"
            counter += 1
        used_names.add(target_name.lower())

        dest = audio_target / target_name
        shutil.copy2(src, dest)

        item_id = slugify(stem)
        if any(existing["id"] == item_id for existing in items):
            item_id = f"{item_id}-{index}"

        items.append(
            {
                "id": item_id,
                "label": stem,
                "url": f"{audio_subdir}/{target_name}".replace("\\", "/"),
                "filename": src.name,
            }
        )

    return {
        "items": items,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
    }


def main() -> int:
    cfg = load_config()
    source_dir = cfg["source_dir"]
    output_dir = cfg["output_dir"]
    audio_subdir = cfg["audio_subdir"]
    extensions = cfg["extensions"]

    if not source_dir.exists():
        raise SystemExit(f"Source directory does not exist: {source_dir}")

    ensure_clean_output(output_dir)
    audio_files = collect_audio_files(source_dir, output_dir, extensions)

    if not audio_files:
        print("WARNING: No audio files found. Writing empty manifest.")

    manifest = build_manifest(audio_files, output_dir, audio_subdir)
    manifest_path = output_dir / "manifest.json"
    with manifest_path.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Build completed: {manifest_path}")
    print(f"Tracks: {len(manifest['items'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
