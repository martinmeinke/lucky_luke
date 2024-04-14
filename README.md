# Lucky Luke - Saving the Keyboard in the age of LLM's
Do you feel like your keyboard became obsolete since the advent of LLM's?  
Are you tired of just copy-pasting LLM-generated content from ChatGPT?  
...or accepting changes proposed by Copilot after prompting it with your voice?

This project aims at taking the human into the loop again!
It reads your keyboard input as you type and uses the huggingface [transformers](https://huggingface.co/docs/transformers/index) API to complete what you are writing.
It implements a USB HID protocol to communicate with [QMK](https://docs.qmk.fm/#/) keyboards and illuminates the backlight of your keys according to the LLM predictions.

Of course, latency being a major concern - on my meager `RTX2070-mobile` I can not run models much bigger than a `TinyLlama-1.1B` and have to use a small context window for things to feel "immediate".


_Highlighting only the respective next key._

https://github.com/martinmeinke/lucky_luke/assets/1669917/6fd78da8-f267-44b9-869c-3028bd0308d8


_Highlighting the next 5 Keys - rolling animation - white to red_

https://github.com/martinmeinke/lucky_luke/assets/1669917/569b85bd-88cf-4953-bdd6-b4336c2701f6


Of course this is completely useless, but it's surprisingly satisfying to type on a keyboard with wildly flashing keys...

## Details
For the sake of energy-efficiency, the LLM is not queried on every keystroke, but only if the input diverges from the previously predicted text.

Compare [my qmk fork](https://github.com/martinmeinke/zsa_qmk_firmware) for the receiving end of the rgb protocol.
