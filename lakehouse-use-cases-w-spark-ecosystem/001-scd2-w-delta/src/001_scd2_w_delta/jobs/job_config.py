#!/usr/bin/env python

import argparse
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yaml

try:
    from cloudpathlib import AnyPath
except ImportError:
    AnyPath = None


def _merge_dicts(base: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
    merged: dict[str, Any] = dict(base)
    for key, value in overlay.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _merge_dicts(merged[key], value)
        else:
            merged[key] = value
    return merged


class ConfigLoader:
    """Load YAML config files from base/env directories with shallow deep-merge."""

    def __init__(self, confs_dir: str | Path, env: str = "local", base_env: str = "base") -> None:
        self.confs_dir = self._build_root_path(confs_dir)
        self.env = env
        self.base_env = base_env

    def get(self, file_name: str) -> dict[str, Any]:
        base_file = self.confs_dir / self.base_env / file_name
        env_file = self.confs_dir / self.env / file_name

        if not base_file.exists() and not env_file.exists():
            raise FileNotFoundError(
                f"Neither {base_file} nor {env_file} exists for config '{file_name}'."
            )

        base_conf = self._read_yaml(base_file) if base_file.exists() else {}
        env_conf = self._read_yaml(env_file) if env_file.exists() else {}
        return _merge_dicts(base_conf, env_conf)

    @staticmethod
    def _build_root_path(confs_dir: str | Path):
        confs_dir_str = str(confs_dir)
        parsed = urlparse(confs_dir_str)
        has_uri_scheme = bool(parsed.scheme and parsed.scheme != "file")

        if has_uri_scheme:
            if AnyPath is None:
                raise ImportError(
                    "URI config paths require cloudpathlib. "
                    "Install it to use non-local --confs-dir values (e.g. s3://...)."
                )
            return AnyPath(confs_dir_str)

        if AnyPath is not None:
            return AnyPath(confs_dir_str)

        return Path(confs_dir_str)

    @staticmethod
    def _read_yaml(file_path: Path) -> dict[str, Any]:
        loaded = yaml.safe_load(file_path.read_text())
        return loaded or {}


@dataclass
class JobArgs:
    confs_dir: str = "confs"
    env: str = "local"
    log_level: str = "INFO"

    @classmethod
    def parse_common_args(cls, argv: list[str] | None = None) -> "JobArgs":
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--confs-dir",
            type=str,
            default="confs",
            dest="confs_dir",
            help=(
                "Path or URI to root config directory containing env subdirs "
                "(e.g. base/, local/)."
            ),
        )
        parser.add_argument(
            "--env",
            type=str,
            default="local",
            help="Environment config subdirectory name under --confs-dir.",
        )
        parser.add_argument(
            "--log-level",
            type=str,
            default="INFO",
            dest="log_level",
            help=(
                "Python/Spark log level. One of ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN."
            ),
        )
        args = parser.parse_args(argv)
        return cls(confs_dir=args.confs_dir, env=args.env, log_level=args.log_level.upper())

    def as_logging_level(self) -> int:
        mapping = {
            "CRITICAL": logging.CRITICAL,
            "FATAL": logging.FATAL,
            "ERROR": logging.ERROR,
            "WARN": logging.WARNING,
            "WARNING": logging.WARNING,
            "INFO": logging.INFO,
            "DEBUG": logging.DEBUG,
            "NOTSET": logging.NOTSET,
        }
        return mapping.get(self.log_level, logging.INFO)
