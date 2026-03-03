"""Configuration models for PageIndex."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PageIndexConfig(BaseSettings):
    """Configuration for PageIndex processing."""

    model_config = SettingsConfigDict(
        env_prefix="PAGEINDEX_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Vertex AI settings
    project_id: str = Field(
        default="",
        description="Google Cloud project ID for Vertex AI",
    )
    location: str = Field(
        default="us-central1",
        description="Vertex AI location/region",
    )
    model: str = Field(
        default="gemini-1.5-flash",
        description="Gemini model to use for reasoning",
    )

    # Processing settings
    toc_check_page_num: int = Field(
        default=20,
        description="Number of pages to check for table of contents",
    )
    max_page_num_each_node: int = Field(
        default=10,
        description="Maximum number of pages per node before splitting",
    )
    max_token_num_each_node: int = Field(
        default=20000,
        description="Maximum number of tokens per node before splitting",
    )

    # Output settings
    if_add_node_id: Literal["yes", "no"] = Field(
        default="yes",
        description="Whether to add node IDs to the tree",
    )
    if_add_node_summary: Literal["yes", "no"] = Field(
        default="yes",
        description="Whether to generate summaries for nodes",
    )
    if_add_doc_description: Literal["yes", "no"] = Field(
        default="no",
        description="Whether to generate document description",
    )
    if_add_node_text: Literal["yes", "no"] = Field(
        default="no",
        description="Whether to include full text in nodes",
    )

    # Docling serve settings
    docling_serve_url: str | None = Field(
        default=None,
        description="URL of docling-serve API (e.g., http://localhost:5001). If set, uses remote server for document conversion instead of local docling.",
    )
    docling_serve_timeout: int = Field(
        default=300,
        description="Timeout in seconds for docling-serve API calls",
    )


class MarkdownConfig(BaseModel):
    """Configuration specific to Markdown processing."""

    if_thinning: bool = Field(
        default=False,
        description="Whether to apply tree thinning",
    )
    thinning_threshold: int = Field(
        default=5000,
        description="Minimum token threshold for thinning",
    )
    summary_token_threshold: int = Field(
        default=200,
        description="Token threshold for generating summaries",
    )


class ConfigLoader:
    """Load configuration from YAML files and merge with user options."""

    def __init__(self, default_path: Path | None = None):
        if default_path is None:
            default_path = Path(__file__).parent / "config.yaml"
        self._default_dict = self._load_yaml(default_path) if default_path.exists() else {}

    @staticmethod
    def _load_yaml(path: Path) -> dict:
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def load(self, user_opt: dict | None = None) -> PageIndexConfig:
        """Load configuration, merging user options with defaults."""
        if user_opt is None:
            user_dict = {}
        elif isinstance(user_opt, PageIndexConfig):
            user_dict = user_opt.model_dump()
        elif isinstance(user_opt, dict):
            user_dict = user_opt
        else:
            raise TypeError("user_opt must be dict, PageIndexConfig, or None")

        merged = {**self._default_dict, **user_dict}
        return PageIndexConfig(**merged)
