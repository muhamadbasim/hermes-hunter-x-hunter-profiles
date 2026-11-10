# Hunter x Hunter Profiles for Hermes Agent

A collection of comprehensive, installable Hermes Agent personas inspired by characters from **Hunter x Hunter**, mapped across Nen categories and Hunter Association disciplines:

- **Specialist (Tokushitsu)**: Ging Freecss, Chrollo Lucilfer, Pakunoda
- **Conjurer (Gugenka)**: Kurapika, Kite, Shizuku Murasaki
- **Manipulator (Sōsa)**: Morel Mackernasey, Shalnark, Mizaistom Nana, Illumi Zoldyck
- **Transmuter (Henka)**: Killua Zoldyck, Biscuit Krueger, Machi Komacine, Hisoka Morow
- **Enhancer (Kyōka)**: Isaac Netero, Gon Freecss, Wing
- **Emitter (Hōshutsu)**: Leorio Paradinight, Knuckle Bine, Razor
- **Hunter Association & Operations**: Beans, Cheadle Yorkshire, Satotz

Each character is a separate Hermes [profile distribution](https://hermes-agent.nousresearch.com/docs/user-guide/profile-distributions). The profile changes how Hermes reasons, communicates, disagrees, handles pressure, and collaborates. It does not turn Hermes into a shallow quote generator or remove its normal tools and factual standards.

---

## What each profile contains

- A substantial `SOUL.md` covering identity, voice, worldview, operating method, strengths, blind spots, pressure behavior, disagreement style, safeguards, and task affinities
- A character-branded terminal skin with custom Nen-inspired palettes
- A provider-neutral `config.yaml`
- A standard `distribution.yaml`

No profile ships credentials, memories, sessions, conversation history, a model choice, cron jobs, or MCP servers. Your provider setup remains yours.

---

## Browse the collection

```bash
python3 manage.py list
python3 manage.py list --nen Specialist
python3 manage.py list --nen Manipulator
```

The generated catalog lives in [`catalog.json`](./catalog.json), and every installable distribution is under [`profiles/`](./profiles). The human-readable [roster](./ROSTER.md) shows the full collection and the engineering work each persona suits.

---

## Install

Clone once, then install any combination:

```bash
git clone https://github.com/muhamadbasim/hermes-hunter-x-hunter-profiles.git
cd hermes-hunter-x-hunter-profiles

# One profile
python3 manage.py install ging-freecss --alias

# A whole Nen category
python3 manage.py install --nen Specialist --alias

# The complete collection
python3 manage.py install --all --alias
```

### One-line bootstrap on Linux/macOS:

```bash
curl -fsSL https://raw.githubusercontent.com/muhamadbasim/hermes-hunter-x-hunter-profiles/main/install.sh | sh -s -- ging-freecss --alias
```

The one-liner follows mutable `main`; inspect it before use. For a reproducible install, clone a tagged release or commit SHA, review the checkout, then run `python3 manage.py install ...`. The manager prints a SHA-256 of every selected profile payload before installation.

### PowerShell:

```powershell
$script = irm https://raw.githubusercontent.com/muhamadbasim/hermes-hunter-x-hunter-profiles/main/install.ps1
& ([scriptblock]::Create($script)) ging-freecss --alias
```

Start the installed profile with either form:

```bash
ging-freecss chat
# or
hermes -p ging-freecss chat
```

Profile identity is loaded when a session starts. Start a new session after installing or updating.

---

## Why the collection has an installer

Hermes accepts a local directory containing `distribution.yaml`, while a remote Git install expects that manifest at the repository root. This repository contains many distributions, so `manage.py` selects the requested character directories and hands each one to Hermes' native installer. It adds no alternate profile format and writes no profile state itself.

---

## Update

```bash
cd hermes-hunter-x-hunter-profiles

# Review and fast-forward the collection, then update selected profiles
git pull --ff-only
python3 manage.py update ging-freecss killua-zoldyck

# Update every installed profile from this collection
python3 manage.py update --all
```

Hermes' distribution updater replaces `SOUL.md` and the skin while preserving local memories, sessions, credentials, and `config.yaml`. Pass `--force-config` if you also want to restore the distribution's skin selection. `manage.py update --pull ...` is a convenience for explicitly opting into the fast-forward before updating.

Keep the collection checkout if you want native `hermes profile update` to keep working: current Hermes records a local absolute source path for monorepo-selected distributions. Moving the checkout requires reinstalling the affected profiles from the new location. `manage.py install --force` also replaces `config.yaml`; it preserves memories and sessions, not local config overrides.

---

## Design principles

1. **Behavior over cosplay.** A persona changes how the agent approaches work, reason, and solve problems, not sprinkle anime dialogue references over generic answers.
2. **Useful asymmetry.** Ging, Kurapika, Morel, Killua, Chrollo, Bisky, Beans, and Netero solve the same problem with completely different cognitive biases and technical approaches.
3. **Character limits survive.** Blind spots are modeled, then bounded so they add texture without making the agent worse or unsafe.
4. **User agency stays intact.** Rank, authority, intimacy, loyalty, and fictional history are never imposed on the user. The user is always the commander and collaborator.
5. **Original wording only.** The profiles use no scripts, copied dialogue, character art, logos, manga/anime text, or catchphrases.
6. **Provider neutral.** The collection does not assume a particular model or API key.

---

## Development

Persona source data is in `source/*.json`. Generated distributions are deterministic.

```bash
python3 tools/build_collection.py
python3 tools/build_collection.py --check
python3 tools/validate_collection.py
python3 tools/e2e_collection.py       # requires an installed `hermes`
```

When adding a character, stop if there is not enough stable behavioral signal to justify a distinct agent. Depth beats roster inflation.

---

## Rights and attribution

This is an unofficial, non-commercial fan-made collection for Hermes Agent. Hunter x Hunter, its characters, and related concepts are trademarks or copyrighted properties of Yoshihiro Togashi, Shueisha, and their respective rights holders. This repository is not affiliated with, endorsed by, or sponsored by Yoshihiro Togashi, Shueisha, or any rights holders.

The repository contains behavioral descriptions written in original language. It includes no franchise logos, promotional art, character likenesses, scripts, manga panels, anime transcripts, audio, video, or copied dialogue.

Code and original profile text are released under the MIT License, subject to all third-party rights in the underlying fictional characters and setting.
