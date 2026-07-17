from app.embeddings.embedding_service import EmbeddingService


def test_embedding_service_is_singleton() -> None:
    service_one = EmbeddingService.get_instance()
    service_two = EmbeddingService.get_instance()

    assert service_one is service_two
