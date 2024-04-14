#!/usr/bin/env python

from hid_rgb import Moonlander, ColorMode
from pynput import keyboard
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from collections import deque

CONTEXT_CHARS = 25
PRED_LEN = 5
LIGHT_HORIZON_CHARS = 5
MODEL_NAME = "TinyLlama/TinyLlama-1.1B-intermediate-step-1195k-token-2.5T"

# Buffer to keep track of the last CONTEXT characters
char_buffer = []
special_chars_map = {
    keyboard.Key.space: " ",
    keyboard.Key.enter: "\n",
    # Add more mappings as needed
}

class LLMBlinky:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.model = AutoModelForCausalLM.from_pretrained(MODEL_NAME).cuda()
        self.text_generation = pipeline(
            "text-generation", model=self.model, tokenizer=self.tokenizer, device=0
        )

        self.board = Moonlander()
        self.board.clear_all()

        self.board.color_mode(ColorMode.COLOR_MODE_ROLLING)

        # rolling context
        self.input_chars = deque(maxlen=CONTEXT_CHARS)

        self.last_prediction = ""

    def record_keypress(self, key):
        try:
            # Directly add the character if it's a regular key press
            char = key.char
        except AttributeError:
            # For special keys, look up their mapping
            char = special_chars_map.get(key, "")

        regenerate_prediction = False
        # Add the character to the buffer
        self.input_chars.append(char)
        if len(self.last_prediction) > 0 and self.last_prediction[0] == char:
            print("Removing first character from prediction.")
            self.last_prediction = self.last_prediction[1:]
            self.update_backlight()
        else:
            regenerate_prediction = True

        extend_horizon = len(self.last_prediction) < LIGHT_HORIZON_CHARS

        # need to fetch further tokens!
        if regenerate_prediction or extend_horizon:
            print(f"{regenerate_prediction=} / {extend_horizon=}")
            if extend_horizon:
                pass  # TODO: special case since we have to keep last_prediction
                input_text = "".join(self.input_chars) + "".join(self.last_prediction)
            else:
                input_text = "".join(self.input_chars)

            print(f"Current input: {input_text}")

            # Tokenize the input and find the number of tokens
            input_tokens = self.tokenizer.encode(
                input_text, add_special_tokens=True
            )  # add_special_tokens=True includes tokens like [CLS], [SEP]
            num_input_tokens = len(input_tokens)

            # Calculate desired max_length (input length + 2 tokens)
            desired_max_length = num_input_tokens + PRED_LEN

            prediction = self.text_generation(
                input_text,
                max_length=desired_max_length,
                num_return_sequences=1,
                temperature=0,
                return_full_text=False,
            )[0]["generated_text"]

            if extend_horizon:
                self.last_prediction += prediction
            else:
                self.last_prediction = prediction

            print(f"Prediction: {self.last_prediction}")
            self.update_backlight()

    def update_backlight(self):
        self.board.clear_all()
        for i, c in enumerate(self.last_prediction[:LIGHT_HORIZON_CHARS]):
            # break if c is non-ascii
            if ord(c) > 127 or c in self.last_prediction[:i]:
                continue
            input_int = ord(c)

            # brightness is overwritten by firmware in COLOR_MODE_ROLLING
            brightness = max(
                0, int(255 / LIGHT_HORIZON_CHARS * (LIGHT_HORIZON_CHARS - i))
            )
            if brightness <= 0:
                break
            self.board.led_rgb(input_int, brightness, brightness, brightness)


if __name__ == "__main__":
    lb = LLMBlinky()
    # Listen for keyboard input
    with keyboard.Listener(on_press=lambda x: lb.record_keypress(x)) as listener:
        listener.join()
