import pytest
from unittest.mock import MagicMock, patch, AsyncMock

from alkemio_virtual_contributor_engine.events.response import Response


@pytest.fixture
def mock_input():
    """Create a mock Input object for testing."""
    inp = MagicMock()
    inp.display_name = "Test VC"
    inp.message = "What is Alkemio?"
    inp.external_config.api_key = "test-api-key"
    inp.external_config.assistant_id = "asst-test-123"
    inp.external_metadata = None
    return inp


@pytest.fixture
def mock_input_with_thread(mock_input):
    """Create a mock Input with existing thread_id."""
    mock_input.external_metadata = MagicMock()
    mock_input.external_metadata.thread_id = "thread-existing-123"
    return mock_input


@pytest.fixture
def mock_openai_client():
    """Create a fully mocked AsyncOpenAI client."""
    client = MagicMock()

    # Mock thread
    mock_thread = MagicMock()
    mock_thread.id = "thread-test-123"
    client.beta.threads.create = AsyncMock(return_value=mock_thread)
    client.beta.threads.retrieve = AsyncMock(return_value=mock_thread)

    # Mock run - completed immediately
    mock_run = MagicMock()
    mock_run.status = "completed"
    mock_run.id = "run-test-123"
    client.beta.threads.runs.create = AsyncMock(return_value=mock_run)
    client.beta.threads.runs.retrieve = AsyncMock(return_value=mock_run)

    # Mock messages with TextContentBlock
    mock_text = MagicMock()
    mock_text.value = "This is the answer."
    mock_text.annotations = []

    mock_content = MagicMock()
    mock_content.text = mock_text
    # Make isinstance check work for TextContentBlock
    mock_content.__class__ = MagicMock()

    mock_message = MagicMock()
    mock_message.content = [mock_content]

    mock_messages = MagicMock()
    mock_messages.data = [mock_message]
    client.beta.threads.messages.list = AsyncMock(
        return_value=mock_messages
    )

    # Mock files
    client.files.list = AsyncMock(return_value=[])

    return client


class TestInvoke:
    """Tests for the invoke() function."""

    @pytest.mark.asyncio
    async def test_invoke_returns_response_on_error(self, mock_input):
        """Test invoke returns error response when query_chain fails."""
        with patch("ai_adapter.query_chain", new_callable=AsyncMock) as mock_qc:
            mock_qc.side_effect = Exception("API Error")

            from ai_adapter import invoke
            result = await invoke(mock_input)

            assert isinstance(result, Response)
            assert "currently unavailable" in result.result
            assert "Test VC" in result.result

    @pytest.mark.asyncio
    async def test_invoke_returns_query_chain_result(self, mock_input):
        """Test invoke returns the result from query_chain on success."""
        expected = Response(result="answer", thread_id="t-123")
        with patch("ai_adapter.query_chain", new_callable=AsyncMock) as mock_qc:
            mock_qc.return_value = expected

            from ai_adapter import invoke
            result = await invoke(mock_input)

            assert result == expected


class TestQueryChain:
    """Tests for the query_chain() function."""

    @pytest.mark.asyncio
    async def test_creates_new_thread_without_metadata(
        self, mock_input, mock_openai_client
    ):
        """Test that a new thread is created when no thread_id exists."""
        with patch("ai_adapter.AsyncOpenAI", return_value=mock_openai_client):
            with patch("ai_adapter.isinstance", return_value=True):
                from ai_adapter import query_chain
                result = await query_chain(mock_input)

            mock_openai_client.beta.threads.create.assert_called_once()
            assert result.thread_id == "thread-test-123"

    @pytest.mark.asyncio
    async def test_retrieves_existing_thread_with_metadata(
        self, mock_input_with_thread, mock_openai_client
    ):
        """Test that an existing thread is retrieved when thread_id exists."""
        with patch("ai_adapter.AsyncOpenAI", return_value=mock_openai_client):
            with patch("ai_adapter.isinstance", return_value=True):
                from ai_adapter import query_chain
                await query_chain(mock_input_with_thread)

            mock_openai_client.beta.threads.retrieve.assert_called_once_with(
                "thread-existing-123"
            )

    @pytest.mark.asyncio
    async def test_run_failure_raises_error(self, mock_input, mock_openai_client):
        """Test that a failed run raises RuntimeError."""
        mock_run = MagicMock()
        mock_run.status = "failed"
        mock_run.id = "run-fail"
        mock_run.last_error = MagicMock()
        mock_run.last_error.message = "Something went wrong"
        mock_openai_client.beta.threads.runs.create.return_value = mock_run

        with patch("ai_adapter.AsyncOpenAI", return_value=mock_openai_client):
            from ai_adapter import query_chain
            with pytest.raises(RuntimeError, match="OpenAI run failed"):
                await query_chain(mock_input)

    @pytest.mark.asyncio
    async def test_citation_removal(self, mock_input, mock_openai_client):
        """Test that citations are removed from the response."""
        mock_annotation = MagicMock()
        mock_annotation.text = "【4:0†source】"

        mock_text = MagicMock()
        mock_text.value = "Answer text【4:0†source】"
        mock_text.annotations = [mock_annotation]

        mock_content = MagicMock()
        mock_content.text = mock_text

        mock_message = MagicMock()
        mock_message.content = [mock_content]

        mock_messages = MagicMock()
        mock_messages.data = [mock_message]
        mock_openai_client.beta.threads.messages.list.return_value = mock_messages

        with patch("ai_adapter.AsyncOpenAI", return_value=mock_openai_client):
            with patch("ai_adapter.isinstance", return_value=True):
                from ai_adapter import query_chain
                result = await query_chain(mock_input)

            assert "【4:0†source】" not in result.result
            assert "Answer text" in result.result

    @pytest.mark.asyncio
    async def test_creates_run_with_correct_ids(
        self, mock_input, mock_openai_client
    ):
        """Test that run is created with correct thread and assistant IDs."""
        with patch("ai_adapter.AsyncOpenAI", return_value=mock_openai_client):
            with patch("ai_adapter.isinstance", return_value=True):
                from ai_adapter import query_chain
                await query_chain(mock_input)

            mock_openai_client.beta.threads.runs.create.assert_called_once_with(
                thread_id="thread-test-123",
                assistant_id="asst-test-123",
            )

    @pytest.mark.asyncio
    async def test_incomplete_run_raises_error(
        self, mock_input, mock_openai_client
    ):
        """Test that an incomplete run raises RuntimeError."""
        mock_run = MagicMock()
        mock_run.status = "incomplete"
        mock_run.id = "run-incomplete"
        mock_run.last_error = None
        mock_openai_client.beta.threads.runs.create = AsyncMock(
            return_value=mock_run
        )

        with patch("ai_adapter.AsyncOpenAI", return_value=mock_openai_client):
            from ai_adapter import query_chain
            with pytest.raises(RuntimeError, match="OpenAI run incomplete"):
                await query_chain(mock_input)

    @pytest.mark.asyncio
    async def test_requires_action_run_raises_error(
        self, mock_input, mock_openai_client
    ):
        """Test that a requires_action run raises RuntimeError."""
        mock_run = MagicMock()
        mock_run.status = "requires_action"
        mock_run.id = "run-action"
        mock_run.last_error = None
        mock_openai_client.beta.threads.runs.create = AsyncMock(
            return_value=mock_run
        )

        with patch("ai_adapter.AsyncOpenAI", return_value=mock_openai_client):
            from ai_adapter import query_chain
            with pytest.raises(
                RuntimeError, match="OpenAI run requires_action"
            ):
                await query_chain(mock_input)
