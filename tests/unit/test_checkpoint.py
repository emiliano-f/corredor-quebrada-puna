import json
from pathlib import Path

from corredor.sources.checkpoint import Checkpoint


def test_statuses_and_persistence(tmp_path: Path) -> None:
    path = tmp_path / "ckpt" / "fuente.json"
    ckpt = Checkpoint(path)
    ckpt.mark("2024-01", "ok", urls=10)
    ckpt.mark("2024-02", "empty", urls=0)
    ckpt.mark("2024-03", "missing", http_status=404)
    ckpt.mark("2024-04", "error", error="timeout")
    assert all(ckpt.is_done(m) for m in ("2024-01", "2024-02", "2024-03"))
    assert not ckpt.is_done("2024-04")  # an error month is retried
    assert not ckpt.is_done("2024-05")
    reloaded = Checkpoint(path)
    assert reloaded.get("2024-02") is not None
    assert reloaded.units()["2024-02"]["status"] == "empty"
    assert reloaded.units()["2024-04"]["status"] == "error"
    assert json.loads(path.read_text())["units"]["2024-01"]["urls"] == 10
    assert not list(path.parent.glob("*.tmp"))


def test_in_memory(tmp_path: Path) -> None:
    ckpt = Checkpoint(None)
    ckpt.mark("2020", "ok")
    assert ckpt.is_done("2020")
    assert not list(tmp_path.iterdir())
