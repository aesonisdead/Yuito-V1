from libs import BaseCommand, MessageClass
import requests
import base64

# Your OpenAI API key
OPENAI_API_KEY = "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"  # <-- Replace with your new valid key

# Track usage per bot session
FREE_IMAGE_QUOTA = 50
used_images = 0

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "imagine",
                "aliases": ["gen"],
                "category": "ai",
                "description": {"content": "Generate an image from a prompt using OpenAI DALL·E"},
                "exp": 1,
            },
        )

    def exec(self, M: MessageClass, _):
        global used_images

        prompt = (
            M.content.replace(f"{self.client.config.prefix}imagine", "")
            .replace(f"{self.client.config.prefix}gen", "")
            .strip()
        )

        if not prompt:
            return self.client.reply_message(
                f"⚠️ Please provide a prompt.\n\nExample: `{self.client.config.prefix}imagine a flying car`",
                M,
            )

        if used_images >= FREE_IMAGE_QUOTA:
            return self.client.reply_message(
                "⚠️ You’ve reached the free OpenAI image generation quota. Please wait until you get more credits.",
                M,
            )

        self.client.reply_message("🎨 Generating image...", M)

        try:
            url = "https://api.openai.com/v1/images/generations"
            headers = {
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            }
            json_data = {
                "prompt": prompt,
                "n": 1,
                "size": "512x512"
            }

            response = requests.post(url, headers=headers, json=json_data, timeout=30)

            if response.status_code == 401:
                return self.client.reply_message(
                    "❌ OpenAI API key is invalid, expired, or unauthorized. Please check your key.",
                    M
                )
            elif response.status_code == 429:
                return self.client.reply_message(
                    "⚠️ You have reached your OpenAI free credits limit. Please wait or add payment info.",
                    M
                )
            elif response.status_code >= 400:
                return self.client.reply_message(
                    f"❌ HTTP error {response.status_code}: {response.text}",
                    M
                )

            data = response.json()
            if "data" not in data or len(data["data"]) == 0:
                return self.client.reply_message("❌ Failed to generate image. No data returned.", M)

            img_base64 = data["data"][0]["b64_json"]
            img_bytes = base64.b64decode(img_base64)

            self.client.send_message(
                M.gcjid,
                {
                    "image": img_bytes,
                    "caption": f"🖼️ {prompt}"
                },
            )

            used_images += 1

        except requests.RequestException as e:
            self.client.reply_message(f"❌ Request failed: {str(e)}", M)
        except Exception as e:
            self.client.log.error(f"[ImagineOpenAIError] {e}")
            self.client.reply_message("❌ Failed to generate image. Please try again later.", M)
