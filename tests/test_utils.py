from unittest.mock import MagicMock

from utils import clear_tags, attach_file


class TestClearTags:
    """Tests for the clear_tags utility function."""

    def test_removes_markdown_link_tags(self):
        """Test removal of markdown-style link tags."""
        message = "Hello [@user](http://example.com) world"
        result = clear_tags(message)
        assert result == "Hello world"

    def test_removes_citation_tags(self):
        """Test removal of citation-style tags."""
        message = "Some text [source](http://link.com) more text"
        result = clear_tags(message)
        assert result == "Some text more text"

    def test_removes_curly_braces(self):
        """Test removal of curly braces."""
        message = "Hello {world}"
        result = clear_tags(message)
        assert result == "Hello world"

    def test_removes_dash_prefix_tags(self):
        """Test removal of tags with dash prefix."""
        message = "Text - [ref](http://url.com) end"
        result = clear_tags(message)
        assert result == "Text  end"

    def test_empty_string(self):
        """Test with empty string input."""
        assert clear_tags("") == ""

    def test_no_tags(self):
        """Test string without any tags passes through."""
        message = "Plain text without tags"
        assert clear_tags(message) == "Plain text without tags"

    def test_multiple_tags(self):
        """Test removal of multiple tags preserves text between them."""
        message = "[a](b) text [c](d)"
        result = clear_tags(message)
        assert result == "text"


class TestAttachFile:
    """Tests for the attach_file utility function."""

    def test_creates_attachment_dict(self):
        """Test attach_file creates correct attachment structure."""
        mock_file = MagicMock()
        mock_file.id = "file-abc123"

        result = attach_file(mock_file)

        assert result == {
            "file_id": "file-abc123",
            "tools": [{"type": "file_search"}],
        }

    def test_uses_file_id(self):
        """Test attach_file extracts the file id correctly."""
        mock_file = MagicMock()
        mock_file.id = "file-xyz789"

        result = attach_file(mock_file)

        assert result["file_id"] == "file-xyz789"
