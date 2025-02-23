# -*- coding: utf-8 -*-
"""Unit test for prompt engineering strategies in format function."""
import unittest
from unittest.mock import MagicMock, patch

from agentscope.message import Msg
from agentscope.models import (
    OpenAIChatWrapper,
    OllamaChatWrapper,
    OllamaGenerationWrapper,
    GeminiChatWrapper,
    ZhipuAIChatWrapper,
    DashScopeChatWrapper,
    DashScopeMultiModalWrapper,
)


class ExampleTest(unittest.TestCase):
    """
    ExampleTest for a unit test.
    """

    def setUp(self) -> None:
        """Init for ExampleTest."""
        self.inputs = [
            Msg("system", "You are a helpful assistant", role="system"),
            [
                Msg("user", "What is the weather today?", role="user"),
                Msg("assistant", "It is sunny today", role="assistant"),
            ],
        ]

        self.wrong_inputs = [
            Msg("system", "You are a helpful assistant", role="system"),
            [
                "What is the weather today?",
                Msg("assistant", "It is sunny today", role="assistant"),
            ],
        ]

    @patch("openai.OpenAI")
    def test_openai_chat(self, mock_client: MagicMock) -> None:
        """Unit test for the format function in openai chat api wrapper."""
        # Prepare the mock client
        mock_client.return_value = "client_dummy"

        model = OpenAIChatWrapper(
            config_name="",
            model_name="gpt-4",
        )

        # correct format
        ground_truth = [
            {
                "role": "system",
                "content": "You are a helpful assistant",
                "name": "system",
            },
            {
                "role": "user",
                "content": "What is the weather today?",
                "name": "user",
            },
            {
                "role": "assistant",
                "content": "It is sunny today",
                "name": "assistant",
            },
        ]

        prompt = model.format(*self.inputs)  # type: ignore[arg-type]
        self.assertListEqual(prompt, ground_truth)

        # wrong format
        with self.assertRaises(TypeError):
            model.format(*self.wrong_inputs)  # type: ignore[arg-type]

    def test_ollama_chat(self) -> None:
        """Unit test for the format function in ollama chat api wrapper."""
        model = OllamaChatWrapper(
            config_name="",
            model_name="llama2",
        )

        # correct format
        ground_truth = [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "What is the weather today?"},
            {"role": "assistant", "content": "It is sunny today"},
        ]
        prompt = model.format(*self.inputs)  # type: ignore[arg-type]
        self.assertEqual(prompt, ground_truth)

        # wrong format
        with self.assertRaises(TypeError):
            model.format(*self.wrong_inputs)  # type: ignore[arg-type]

    def test_ollama_generation(self) -> None:
        """Unit test for the generation function in ollama chat api wrapper."""
        model = OllamaGenerationWrapper(
            config_name="",
            model_name="llama2",
        )

        # correct format
        ground_truth = (
            "You are a helpful assistant\n\n## Dialogue History\nuser: "
            "What is the weather today?\nassistant: It is sunny today"
        )
        prompt = model.format(*self.inputs)  # type: ignore[arg-type]
        self.assertEqual(prompt, ground_truth)

        # wrong format
        with self.assertRaises(TypeError):
            model.format(*self.wrong_inputs)  # type: ignore[arg-type]

    @patch("google.generativeai.configure")
    def test_gemini_chat(self, mock_configure: MagicMock) -> None:
        """Unit test for the format function in gemini chat api wrapper."""
        mock_configure.return_value = "client_dummy"

        model = GeminiChatWrapper(
            config_name="",
            model_name="gemini-pro",
            api_key="xxx",
        )

        # correct format
        ground_truth = [
            {
                "role": "user",
                "parts": [
                    "You are a helpful assistant\n\n## Dialogue History\n"
                    "user: What is the weather today?\nassistant: It is "
                    "sunny today",
                ],
            },
        ]

        prompt = model.format(*self.inputs)  # type: ignore[arg-type]
        self.assertListEqual(prompt, ground_truth)

        # wrong format
        with self.assertRaises(TypeError):
            model.format(*self.wrong_inputs)  # type: ignore[arg-type]

    def test_dashscope_chat(self) -> None:
        """Unit test for the format function in dashscope chat api wrapper."""
        model = DashScopeChatWrapper(
            config_name="",
            model_name="qwen-max",
            api_key="xxx",
        )

        ground_truth = [
            {
                "content": "You are a helpful assistant",
                "role": "system",
            },
            {
                "content": (
                    "## Dialogue History\n"
                    "user: What is the weather today?\n"
                    "assistant: It is sunny today"
                ),
                "role": "user",
            },
        ]

        prompt = model.format(*self.inputs)
        self.assertListEqual(prompt, ground_truth)

        # wrong format
        with self.assertRaises(TypeError):
            model.format(*self.wrong_inputs)  # type: ignore[arg-type]

    def test_zhipuai_chat(self) -> None:
        """Unit test for the format function in zhipu chat api wrapper."""
        model = ZhipuAIChatWrapper(
            config_name="",
            model_name="glm-4",
            api_key="xxx",
        )

        ground_truth = [
            {
                "content": "You are a helpful assistant",
                "role": "system",
            },
            {
                "content": (
                    "## Dialogue History\n"
                    "user: What is the weather today?\n"
                    "assistant: It is sunny today"
                ),
                "role": "user",
            },
        ]

        prompt = model.format(*self.inputs)
        self.assertListEqual(prompt, ground_truth)

        # wrong format
        with self.assertRaises(TypeError):
            model.format(*self.wrong_inputs)  # type: ignore[arg-type]

    def test_dashscope_multimodal_image(self) -> None:
        """Unit test for the format function in dashscope multimodal
        conversation api wrapper for image."""
        model = DashScopeMultiModalWrapper(
            config_name="",
            model_name="qwen-vl-plus",
            api_key="xxx",
        )

        multimodal_input = [
            Msg(
                "system",
                "You are a helpful assistant",
                role="system",
                url="url1.png",
            ),
            [
                Msg(
                    "user",
                    "What is the weather today?",
                    role="user",
                    url="url2.png",
                ),
                Msg(
                    "assistant",
                    "It is sunny today",
                    role="assistant",
                    url="url3.png",
                ),
            ],
        ]

        ground_truth = [
            {
                "role": "system",
                "content": [
                    {"image": "url1.png"},
                    {"text": "You are a helpful assistant"},
                ],
            },
            {
                "role": "user",
                "content": [
                    {"image": "url2.png"},
                    {"image": "url3.png"},
                    {
                        "text": (
                            "## Dialogue History\n"
                            "user: What is the weather today?\n"
                            "assistant: It is sunny today"
                        ),
                    },
                ],
            },
        ]

        prompt = model.format(*multimodal_input)
        self.assertListEqual(prompt, ground_truth)

        # wrong format
        with self.assertRaises(TypeError):
            model.format(*self.wrong_inputs)

    def test_dashscope_multimodal_audio(self) -> None:
        """Unit test for the format function in dashscope multimodal
        conversation api wrapper for audio."""
        model = DashScopeMultiModalWrapper(
            config_name="",
            model_name="qwen-audio-turbo",
            api_key="xxx",
        )

        multimodal_input = [
            Msg(
                "system",
                "You are a helpful assistant",
                role="system",
                url="url1.mp3",
            ),
            [
                Msg(
                    "user",
                    "What is the weather today?",
                    role="user",
                    url="url2.mp3",
                ),
                Msg(
                    "assistant",
                    "It is sunny today",
                    role="assistant",
                    url="url3.mp3",
                ),
            ],
        ]

        ground_truth = [
            {
                "role": "system",
                "content": [
                    {"audio": "url1.mp3"},
                    {"text": "You are a helpful assistant"},
                ],
            },
            {
                "role": "user",
                "content": [
                    {"audio": "url2.mp3"},
                    {"audio": "url3.mp3"},
                    {
                        "text": (
                            "## Dialogue History\n"
                            "user: What is the weather today?\n"
                            "assistant: It is sunny today"
                        ),
                    },
                ],
            },
        ]

        prompt = model.format(*multimodal_input)
        self.assertListEqual(prompt, ground_truth)

        # wrong format
        with self.assertRaises(TypeError):
            model.format(*self.wrong_inputs)


if __name__ == "__main__":
    unittest.main()
