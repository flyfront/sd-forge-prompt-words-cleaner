# sd-forge-prompt-words-cleaner

A small extension for [Stable Diffusion WebUI Forge Neo](https://github.com/Haoming02/sd-webui-forge-classic/tree/neo). It replaces the `[prompt_words]` filename / directory pattern so that names are built from the words of the prompt, not from its syntax.

- JSON prompts (MOSS-Image, Krea 2, ...): uses the values of `caption` / `prompt` instead of the key names
- Removes `<lora:...>` and other `<...>` extra-network tags
- Resolves prompt editing / alternation (`[a:b:0.5]`, `[a|b]`) to the state at the last step
- Strips emphasis syntax (`(a:1.2)`, `((a))`, `[a]`) and keeps only the text

Example (`directories_max_prompt_words` = 8):

| Prompt | Forge Neo default | With this extension |
|---|---|---|
| `<lora:moss_lora_r2:1> 1girl, solo, (maid:1.2), [cat ears:cat tail:0.5], smile` | `lora moss lora r2 1 1girl solo maid` | `1girl solo maid cat tail smile` |
| `{"caption": "1girl, solo, maid, cat ears", "style": "anime illustration"}` | `caption 1girl solo maid cat ears style anime` | `1girl solo maid cat ears` |

## Install

Extensions > Install from URL: `https://github.com/flyfront/sd-forge-prompt-words-cleaner`

No settings. It changes only what `[prompt_words]` expands to, which is used by "Save images to a subdirectory" (the default directory name pattern) and by any filename / directory pattern that contains `[prompt_words]`.

## How it works

At startup it overwrites `FilenameGenerator.replacements["prompt_words"]` in `modules/images.py`. Forge Neo's own code is not modified, and disabling the extension restores the default behavior.

It relies on Forge Neo internals (`modules.prompt_parser`, `backend.text_processing.parsing`), so a Forge Neo update may break it. Tested with Forge Neo 2.31.

Made for personal use, written with AI assistance.

## 日本語

Forge Neo 用の小さな拡張。保存先サブディレクトリ名などに使う `[prompt_words]` パターンを差し替え、プロンプトの構文要素を除いた単語で名前を作る。

- JSON プロンプト(MOSS-Image、Krea 2 など)はキー名ではなく `caption` / `prompt` の値を使う
- `<lora:...>` などの `<...>` タグを除去
- Prompt Editing / 交互(`[a:b:0.5]`、`[a|b]`)は最終ステップの状態に解決
- 強調構文(`(a:1.2)`、`((a))`、`[a]`)は括弧と重みを取り除く

導入は Extensions > Install from URL に `https://github.com/flyfront/sd-forge-prompt-words-cleaner`。設定項目は無い。

`modules/images.py` の `FilenameGenerator.replacements["prompt_words"]` を起動時に上書きしているだけで、本体コードは変更しない。Forge Neo の内部モジュールに依存するので、本体の更新で動かなくなることがある(2.31 で確認)。

## License

MIT
