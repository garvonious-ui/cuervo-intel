"""
Client Context Manager
=======================
Loads per-client configuration and provides helpers to access the active
client's config from any page via get_client().
"""

import importlib
import os
import tempfile

import streamlit as st

from clients._schema import ClientConfig

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


def list_available_clients() -> list[str]:
    """Scan the clients/ directory for valid client modules."""
    clients_dir = os.path.join(PROJECT_ROOT, "clients")
    available = []
    for name in sorted(os.listdir(clients_dir)):
        client_dir = os.path.join(clients_dir, name)
        if os.path.isdir(client_dir) and not name.startswith("_"):
            client_file = os.path.join(client_dir, "client.py")
            if os.path.isfile(client_file):
                available.append(name)
    return available


def load_client_config(client_id: str) -> ClientConfig:
    """Dynamically import clients/{client_id}/client.py and call get_config()."""
    module_path = f"clients.{client_id}.client"
    try:
        mod = importlib.import_module(module_path)
    except ModuleNotFoundError:
        raise ValueError(f"Client '{client_id}' not found. Expected module at clients/{client_id}/client.py")

    if not hasattr(mod, "get_config"):
        raise ValueError(f"Client module '{module_path}' must export a get_config() function")

    cfg = mod.get_config()

    # Resolve data paths
    cfg.data_dir = os.path.join(PROJECT_ROOT, "data", cfg.client_id)
    cfg.sprout_dir = os.path.join(cfg.data_dir, "sprout")
    cfg.autostrat_dir = os.path.join(cfg.data_dir, "autostrat")
    cfg.sprout_output_dir = os.path.join(tempfile.gettempdir(), f"{cfg.client_id}_sprout_imported")

    # Resolve asset paths (relative to client directory)
    client_assets = os.path.join(PROJECT_ROOT, "clients", cfg.client_id, "assets")
    if cfg.logo_path and not os.path.isabs(cfg.logo_path):
        cfg.logo_path = os.path.join(client_assets, cfg.logo_path)
    if cfg.favicon_path and not os.path.isabs(cfg.favicon_path):
        cfg.favicon_path = os.path.join(client_assets, cfg.favicon_path)
    if cfg.app_logo_path and not os.path.isabs(cfg.app_logo_path):
        cfg.app_logo_path = os.path.join(client_assets, cfg.app_logo_path)

    return cfg


def set_active_client(cfg: ClientConfig) -> None:
    """Store the active client config in Streamlit session state."""
    st.session_state["client_config"] = cfg


def get_client() -> ClientConfig:
    """Retrieve the active client config from session state.
    Call this from any page to access client-specific configuration."""
    cfg = st.session_state.get("client_config")
    if cfg is None:
        raise RuntimeError(
            "No client config loaded. Ensure app.py has called set_active_client() "
            "before any page code runs."
        )
    return cfg
