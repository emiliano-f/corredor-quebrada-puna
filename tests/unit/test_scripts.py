from datetime import date

import pytest

import check_docs
import check_identity
import release


class TestCheckDocs:
    def test_sources_need_scraping_or_fuentes(self) -> None:
        errs = check_docs.check(["src/corredor/sources/generic.py", "CHANGELOG.md"])
        assert len(errs) == 1
        assert errs[0].startswith("sources")
        assert (
            check_docs.check(["src/corredor/sources/generic.py", "docs/FUENTES.md", "CHANGELOG.md"])
            == []
        )

    def test_models_and_storage_need_datos(self) -> None:
        for path in ("src/corredor/models.py", "src/corredor/storage/repository.py"):
            assert check_docs.check([path, "CHANGELOG.md"])[0].startswith("data model")
            assert check_docs.check([path, "docs/DATOS.md", "CHANGELOG.md"]) == []

    def test_changelog_always_required(self) -> None:
        assert check_docs.check(["README.md"]) == [
            'CHANGELOG.md: add a line under "## [Unreleased]"'
        ]
        assert check_docs.check([]) == []

    def test_prefix_does_not_overmatch(self) -> None:
        assert check_docs.check(["src/corredor/models_extra.py", "CHANGELOG.md"]) == []
        assert check_docs.check(["src/corredor/sourcesx.py", "CHANGELOG.md"]) == []

    def test_skip_label(self) -> None:
        assert check_docs.has_skip_label("bug, no-docs")
        assert not check_docs.has_skip_label("docs")
        assert not check_docs.has_skip_label(None)


class TestIdentity:
    @pytest.mark.parametrize(
        "ident",
        [
            "Emiliano Flores <1+emiliano-f@users.noreply.github.com> 1 +0000",
            "Devin AI <2+devin-ai-integration[bot]@users.noreply.github.com> 1 +0000",
        ],
    )
    def test_noreply_ok(self, ident: str) -> None:
        assert check_identity.check_ident("author", ident) is None

    @pytest.mark.parametrize(
        "ident",
        [
            "Someone <someone@example.com> 1 +0000",
            "Someone <x@users.noreply.github.com.evil.com> 1 +0000",
            "garbage",
        ],
    )
    def test_rejected(self, ident: str) -> None:
        assert check_identity.check_ident("committer", ident) is not None


CHANGELOG = """# Changelog

## [Unreleased]

### Added
- Thing.

## [0.0.1] - 2026-01-01

### Added
- Old.
"""


class TestRelease:
    def test_roll_changelog(self) -> None:
        out = release.roll_changelog(CHANGELOG, "0.1.0", date(2026, 11, 20))
        assert "## [Unreleased]\n\n## [0.1.0] - 2026-11-20\n\n### Added\n- Thing.\n" in out
        assert release.changelog_section(out, "0.1.0") == "### Added\n- Thing.\n"
        assert release.changelog_section(out, "0.0.1") == "### Added\n- Old.\n"

    def test_empty_unreleased_fails(self) -> None:
        text = "# Changelog\n\n## [Unreleased]\n\n## [0.0.1] - 2026-01-01\n"
        with pytest.raises(release.ReleaseError):
            release.roll_changelog(text, "0.1.0", date(2026, 11, 20))

    @pytest.mark.parametrize(
        ("version", "final"),
        [("0.1.0", True), ("1.20.3", True), ("0.1.0.dev0", False), ("0.2.0rc1", False)],
    )
    def test_is_final(self, version: str, final: bool) -> None:
        assert release.is_final(version) is final

    def test_bump_arg_finalizes_dev(self) -> None:
        assert release.bump_arg("0.1.0.dev0", "minor") == "stable"
        assert release.bump_arg("0.1.0", "minor") == "minor"

    def test_missing_section_fails(self) -> None:
        with pytest.raises(release.ReleaseError):
            release.changelog_section(CHANGELOG, "9.9.9")
