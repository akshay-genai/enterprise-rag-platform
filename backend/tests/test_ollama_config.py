import importlib

from app.core import config as config_module


def test_llm_model_can_be_overridden_by_env(monkeypatch):
    monkeypatch.setenv("OLLAMA_MODEL", "llama3.1:8b")
    reloaded = importlib.reload(config_module)

    assert reloaded.settings.llm_model == "llama3.1:8b"
