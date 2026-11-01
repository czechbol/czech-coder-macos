# Czech Coder

A macOS port of the Linux [`cz(coder)`](https://github.com/michalkahle/czech-coder-xkb)
xkb layout. It's a normal US keyboard with Czech diacritics on the **Option (⌥)** layer,
so you can write code on US and type Czech without switching input sources. Option works
like AltGr here: hold it down for a whole sentence and the regular letters still type as
themselves.

## How it works

- The base layer is stock US ANSI. Symbols, brackets and shortcuts stay where you expect.
- Option is the Czech layer. The diacritics live on the number row and a few punctuation
  keys, so the letter keys keep their normal letters. That's what lets you hold Option the
  whole time and type mixed text.
- Option+Shift gives the uppercase accents and `€`.
- Dead keys cover the accents that aren't on a direct key.

It matches the Linux layout key for key. Unlike
[mariancerny/us-czech-keyboard-layout](https://github.com/mariancerny/us-czech-keyboard-layout),
it leaves the letter keys alone. The only letter that changes on the Option layer is
**⌥⇧E**, which gives `€`.

## Key map

Hold **⌥** for the first column, **⌥⇧** for the second.

| Key | ⌥ | ⌥⇧ |
|-----|---|----|
| `2` to `0` | ě š č ř ž ý á í é | Ě Š Č Ř Ž Ý Á Í É |
| `[` | ú | Ú |
| `;` | ů | Ů |
| `'` | § | " |
| `` ` `` | `;` | ˚ dead ring |
| `=` | ´ dead acute | ˇ dead caron |
| `\` | ¨ dead diaeresis | `'` |
| `E` | e | € |

Dead keys work like this: press the combo, then the letter. Press space after a dead key
to get the accent on its own.

| Dead key | Trigger | Covers |
|----------|---------|--------|
| acute ´ | ⌥`=` | á é í ó ú ý |
| caron ˇ | ⌥⇧`=` | č š ž ř ě ď ť ň ľ |
| ring ˚ | ⌥⇧`` ` `` | ů å |
| diaeresis ¨ | ⌥`\` | ä ë ï ö ü ÿ |

Uppercase works too.

## Install (macOS)

Open **Terminal** and paste one of these.

With git:

```sh
git clone https://github.com/czechbol/czech-coder-macos.git
cd czech-coder-macos
./install.sh
```

Without git (download and unpack):

```sh
curl -L https://github.com/czechbol/czech-coder-macos/archive/refs/heads/main.tar.gz | tar xz
cd czech-coder-macos-main
./install.sh
```

The installer copies `Czech Coder.bundle` into `~/Library/Keyboard Layouts/`. After that:

1. Log out and back in (or restart) so macOS notices the new layout.
2. Open System Settings > Keyboard > Input Sources, click `+`, pick Czech, and add Czech Coder.
3. Switch to it from the input menu in the menu bar (or with `⌃Space` / `⌘Space`).

To remove it, run `rm -rf ~/Library/Keyboard\ Layouts/Czech\ Coder.bundle` and delete it
from Input Sources.

## Build

It ships as a `.bundle` for two reasons. A bare `.keylayout` always ends up under "Others",
and its icon doesn't show reliably. The bundle's `Info.plist` sets `TISIntendedLanguage=cs`
so it lists under **Czech**, and `TISIconIsTemplate` so the monochrome icon inverts in dark
mode.

The `.keylayout` is generated from a single key table in `src/gen_keylayout.py`. The icon
is a `CZ` text badge packed into a real `.icns`. You only need `python3` and `Pillow`.

```sh
make                 # build Czech Coder.bundle
make BADGE=čš        # use different badge text
```

## Credits

- Layout design: [czech-coder-xkb](https://github.com/michalkahle/czech-coder-xkb) by michalkahle (MIT).
- Earlier macOS version: [us-czech-keyboard-layout](https://github.com/mariancerny/us-czech-keyboard-layout).
- File format: Apple [TN2056](https://developer.apple.com/library/mac/technotes/tn2056/_index.html).

MIT, see [LICENSE](LICENSE).
