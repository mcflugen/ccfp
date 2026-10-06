from __future__ import annotations

import os

import nox

ROOT = os.path.dirname(os.path.abspath(__file__))
WILO_PROJECT_URL = "git+https://github.com/mcflugen/wilo.git"
WILO_VERSION = "v0.1.0"

nox.options.sessions = ("update-score", "update-ratings")


@nox.session
def init(session: nox.Session) -> None:
    config_file = os.path.join(ROOT, "wilo.toml")

    _install_wilo(session, tag=WILO_VERSION)
    session.run("wilo", f"--config={config_file}", "init")


@nox.session(name="update-score")
def update_score(session: nox.Session) -> None:
    _install_wilo(session, tag=WILO_VERSION)
    session.run("wilo", "season", "--download", "--update")


@nox.session
def standings(session: nox.Session) -> None:
    _install_wilo(session, extras=("tables",), tag=WILO_VERSION)
    session.run("wilo", "standings", "--table")


@nox.session(name="update-ratings")
def update_ratings(session: nox.Session) -> None:
    _install_wilo(session, tag=WILO_VERSION)
    session.run("wilo", "ratings", "--download", "--update")


@nox.session
def optimize(session: nox.Session) -> None:
    _install_wilo(session, extras=("tables", "optimize"), tag=WILO_VERSION)
    session.run("wilo", "optimize", "--player=Eric", "--table")


@nox.session
def lint(session: nox.Session) -> None:
    """Run all configured pre-commit checks."""
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files")


def _install_wilo(session: nox.Session, extras=None, tag=None) -> None:
    tag = "main" if tag is None else tag
    extras = "" if extras is None else f"[{','.join(sorted(extras))}]"

    session.install(f"wilo{extras} @ {WILO_PROJECT_URL}@{tag}")
