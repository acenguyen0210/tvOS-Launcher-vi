<<<<<<< HEAD
# Contributing

Thanks for helping more TVs lose their ads. Three kinds of contributions are especially welcome.

Working with a coding agent? Point it at [`AGENTS.md`](AGENTS.md): the same rules, written for agents.

The reasons a pull request most often came back for changes or was closed, one example for each, are
in [`docs/DOS-AND-DONTS.md`](docs/DOS-AND-DONTS.md). It is the short list of mistakes to skip, and it
does not replace the sections below.

## Where does my idea go?

The launcher stays small on purpose, so pick the smallest home that fits:

| Your idea | Where it goes |
|---|---|
| A TV model, a fix, a translation, a small switch that is off by default | A pull request here (sections 1 to 3 below); a new switch with a screenshot in [`docs/switches.md`](docs/switches.md) |
| A new look: colours, wallpaper, dock, columns | [`themes/`](themes/README.md), with a screenshot from a real TV |
| A widget or tile that can be its own small app | [`addons/`](addons/README.md), as a module card with a screenshot from a real TV; it never touches `launcher/` |
| A whole new launcher, a heavy restyle, a port to another platform | Your own repo, plus one row in [`SHOWCASE.md`](SHOWCASE.md) (section 4) |

Everything merged into `themes/` and `addons/` shows up on [cleanyour.tv/addons](https://cleanyour.tv/addons).

## 1. Add your TV model

Every brand ships different bloat. If you ran the prompt (or did it by hand) on a TV that isn't in
`examples/`, add it. The same steps for a coding agent are in
[`docs/workflows/tv-list.md`](docs/workflows/tv-list.md).

1. Create `examples/<brand>-<model>/debloat.txt`. Copy the format from
   `examples/xiaomi-mi-tv-4a/debloat.txt`: one package per line, grouped with a comment that says
   what the group is, and a trailing comment on anything non-obvious ("re-enable for firmware
   updates", "needed for HDMI-CEC", etc.).
2. Put the exact model name, Android version and firmware build in the header so people can tell
   whether it matches theirs. `tools/tv.py --probe` prints all three.
3. Only list packages you have actually disabled and lived with for a few days. Note anything that
   broke and what you re-enabled.
4. Add `examples/<brand>-<model>/tv.json`, the row the TV tables show for your list. Copy
   `examples/xiaomi-mi-tv-4a/tv.json`: `tv` (the model as the tables name it), `os`, `brand` (spelled as
   in the README's brand grid; a new brand is fine) and `notes` (one line: what the list disables and
   keeps). One optional key, `readme_os`, is the OS cell of the short table in `README.nl.md` when it should
   read shorter than `os` does in `examples/README.md`. Change nothing outside your folder: the TV table in
   `examples/README.md`, the brand grid in the READMEs and the counts are generated from every folder's
   `tv.json` after merging, so a PR that edits them only collides with the other open lists.
5. If your TV's Live TV app or stock launcher has a different package name, say so in the header. Where
   a script needs the stock launcher, `tools/restore.sh` takes it as its second argument
   (`tools/restore.sh <list> <package>`) and `launcher/build-and-install.sh` takes it in the
   environment, as `STOCK_LAUNCHER=<package>` (`-StockLauncher` on the PowerShell twin, and `none`
   keeps it enabled) - not as an argument. The launcher shows your Live TV app in its Inputs menu from
   `live_tv_package`, in `config.xml` or a theme.

Never list packages to *uninstall*. Everything in this repo disables with `pm disable-user`, which
is reversible from the TV's own settings if the tools are gone.

Android's own packages are not bloat either. Never list the permission controller, the package
installer, ext services or ext shared, module metadata, a `com.google.android.overlay.modules*`
overlay, systemui, shell, phone, settings, tv.settings, `android`, or a `com.android.providers.*`
package other than calendar, contacts, user dictionary and blocked numbers. A TV that loses one of
them may never boot again ([#884](https://github.com/Gathin23/cleanyourtv/issues/884), and
[what to do if it already happened](docs/TROUBLESHOOTING.md#working-on-the-tv)), so
`tools/disable.sh`, `disable.ps1` and `check.py --fix` refuse such a list outright, with no switch to
override it, and a pull request that names them comes back for a rework.

## 2. Improve the launcher

The launcher lives in `launcher/` and is deliberately small: plain Java, AndroidX RecyclerView and
DynamicAnimation, no Kotlin, no Compose, no network. It targets TVs with 1 GB of RAM. A new switch follows
[`docs/workflows/launcher-switch.md`](docs/workflows/launcher-switch.md), a new language
[`docs/workflows/translation.md`](docs/workflows/translation.md), and a speed-up or slow-down is measured with
[`docs/workflows/perf-ab.md`](docs/workflows/perf-ab.md). In every change:

- No blur, no video backgrounds, no polling, no background services.
- Anything that depends on a specific TV goes in `app/src/main/res/values/config.xml`, not in code.
- Keep D-pad navigation deterministic. Test Up/Down/Left/Right from every edge.
- Verify on a real TV, not only the emulator. The easiest way is remote key injection plus a
  screenshot: `tools/tv.py --screenshot shots/after.png DPAD_DOWN` presses the key, waits a second
  (`--wait` changes that), captures on the TV and pulls the PNG, creating the folder if it is missing.
  Include a screenshot in your pull request.
- Long presses (hold OK on Settings or on a tile) can't always be injected: `input keyevent --longpress`
  arrives as a short press on some firmware (Android TV 8.0 on a Philips opens the app instead). Writing
  to the remote's own input device works, because Android then repeats the held key itself. Find the
  device and the OK key with `tools/tv.py 'getevent -pl'` (a remote that lists `KEY_OK` is scancode 352),
  then hold it for a second:
  `tools/tv.py 'e=/dev/input/event1; sendevent $e 1 352 1; sendevent $e 0 0 0; sleep 1.2; sendevent $e 1 352 0; sendevent $e 0 0 0'`.
  This needs the shell user in the `input` group (`tools/tv.py id`).
  SELinux can refuse it even then: on a TCL 55C728 (Google TV 11, enforcing) the shell is in `input`,
  yet `sendevent` fails with `Permission denied` and `logcat` shows
  `avc: denied { write } ... scontext=u:r:shell:s0 tcontext=u:object_r:input_device:s0`, while
  `--longpress` arrives as a short press too. On a set like that, test long presses with the remote.

### Automated navigation and lifecycle checks

- Use D-pad key events throughout focus tests, including entering and leaving Reorder.
  Injected touch input can enter Android's system-wide [touch mode](https://developer.android.com/develop/ui/views/touch-and-input/input-events#TouchMode),
  where ordinary buttons may not take focus. If a test uses touch, send a directional key
  and verify the focused tile before continuing with D-pad assertions.
- After Home, an app transition or a reboot, wait with a timeout for the launcher UI and
  focused window before sending navigation or capturing a hierarchy. A fixed sleep or
  a boot-completion property alone does not establish that Home is ready. Android's
  [UI Automator guidance](https://developer.android.com/training/testing/other-components/ui-automator-legacy#wait)
  demonstrates waiting for the launcher and for specific UI conditions.
- For synthetic memory checks, record the process state, requested trim level and command
  result. ActivityManager [can reject background trim levels for foreground processes](https://android.googlesource.com/platform/frameworks/base/+/master/services/core/java/com/android/server/am/ActivityManagerService.java).
  To exercise hidden Home, put an opaque app in front and verify Home's process state;
  use a trim level supported by the target Android version. Treat a rejected command as
  a test setup failure. A delivered trim callback tests recovery behavior, not performance
  under real memory pressure.

Build with `TV_HOST=<ip> launcher/build-and-install.sh` (JDK 17, Android SDK platform 34 and
build-tools 34.0.0; on macOS `brew install openjdk@17 android-commandlinetools` then
`sdkmanager "platforms;android-34" "build-tools;34.0.0"`; with the newer command-line tools the form is
`android sdk install platforms/android-34 build-tools/34.0.0`).

No TV on the network, or an APK for someone else to install? Build it on its own: from `launcher/`,
`./gradlew --no-daemon assembleRelease` leaves it at
`launcher/app/build/outputs/apk/release/app-release.apk`, which has to stay under 589,824 B (576 KB);
CI builds with the same command and refuses a bigger one. Gradle also has to find the SDK, and this is
where a hand build stops: `launcher/build-and-install.sh` writes the gitignored
`launcher/local.properties` for you, so by hand either run
`ANDROID_HOME=~/Android/Sdk ./gradlew --no-daemon assembleRelease` or put `sdk.dir=<sdk>` in that file;
without one or the other Gradle stops at `SDK location not found`. The JDK has to be a full 17 - a JRE
answers `java -version` as a 17 but has no `jlink`, which the Android Gradle plugin needs (#1255) - and
Homebrew's `openjdk@17` is keg-only, so point `JAVA_HOME` at it
(`export JAVA_HOME=$(brew --prefix openjdk@17)`).

With neither a JDK nor an SDK on this computer, build it in a container that has both:
`tools/docker-build.sh launcher` (Docker only; `addons/<name>` builds an add-on, and the Gradle task
defaults to `assembleRelease`). It writes the APK to the same place, so
`SKIP_BUILD=1 TV_HOST=<ip> launcher/build-and-install.sh` installs it. Its debug key lives in the
`cleanyourtv-gradle` volume rather than `~/.android`, so installing over an APK built here fails with
`INSTALL_FAILED_UPDATE_INCOMPATIBLE` unless both use the same key (`HOST_KEY_DIR=~/.android`), and
[`tools/docker-build.md`](tools/docker-build.md) has the rest.

Ideas that fit the direction: an idle screensaver with clock and ambient colour, per-TV icon packs
for apps without banners, a settings screen to edit the dock from the TV, localisation.
Ideas that don't: recommendation rows, content feeds, ads, telemetry.

A new theme goes in `themes/<name>/` with its `config.json` and a required `screenshot.jpg` of Home on a
real TV with that theme; see [Adding a theme](themes/README.md#adding-a-theme).

## 3. Improve the prompt and tools

`PROMPT.md` is what most people will actually use. If your assistant got stuck somewhere, the fix
usually belongs in the prompt as one extra sentence, not in a script. Keep it brand-neutral; put
brand-specific knowledge in `examples/`.

`tools/tv.py` and `tools/b64push.py` exist because the stock `adb` is blocked on recent macOS. If
you find a cleaner workaround, open an issue first.

## 4. Show what you built

Built your own launcher, a port to another platform, or an add-on that is too big or too personal
for the shared launcher? Put it in its own repository and add one row to
[`SHOWCASE.md`](SHOWCASE.md). That page is the place for alternative launchers, forks with a
different look, and tools around the launcher; this repo keeps one small reference launcher and
points at everything else. The rules for a row are on that page.

Things that stay in this repo: debloat lists, fixes and small, opt-in features for the reference
launcher, prompt and tool improvements. A feature that can be its own small app goes in [`addons/`](addons/README.md)
as a module card. Things that go in the showcase: a second launcher, a
restyle, a platform port, anything with its own background services or network access.

## Pull requests

- One topic per PR. Small is fine.
- Read [`docs/DOS-AND-DONTS.md`](docs/DOS-AND-DONTS.md) before you open one: it is why most PRs come
  back for a change, with an example for each reason.
- Say which TV you tested on.
- No new dependencies in the launcher without discussing it in an issue.
- Be kind in reviews. Most contributors here are doing this for their parents.

By contributing you agree your work is released under the repo's MIT licence.
=======
# Contributing to tvOS Launcher

Thanks for helping. tvOS Launcher is a tvOS 26–style home screen for Android TV: plain Java, no
Gradle, no third-party runtime libraries, built to stay smooth on low-end TV boxes. This guide
covers how to work on it; to set up your machine first, see
**[docs/getting-started.md](docs/getting-started.md)**.

## Contents

1. [Project in one page](#1-project-in-one-page)
2. [Workflow](#2-workflow)
3. [Code style](#3-code-style)
4. [Design rules](#4-design-rules)
5. [Performance rules](#5-performance-rules)
6. [Permissions and privacy rules](#6-permissions-and-privacy-rules)
7. [Testing a change](#7-testing-a-change)
8. [Pull requests](#8-pull-requests)
9. [Good first areas](#9-good-first-areas)
10. [Licensing](#10-licensing)

## 1. Project in one page

```
AndroidManifest.xml      package com.techgenius.tvoslauncher, activities/services/receivers
build.sh                 the whole build (aapt2 → javac → d8 → zipalign → apksigner)
src/com/techgenius/tvoslauncher/   the launcher (≈9,400 lines of Java)
src/com/techgenius/tvoslauncher/present/   Presentation mode: HTTP server, player, storage
src/io/nayuki/qrcodegen/ vendored QR encoder (MIT)
res/                     manifest resources: icons, device-admin and accessibility XML, strings
assets/fonts/            Inter (OFL)
assets/present/          the browser admin app for Presentation (HTML/CSS/JS)
docs/                    user and developer documentation, screenshots
```

Key files (full map in **[docs/architecture.md](docs/architecture.md)**):

| File | What lives there |
|---|---|
| `MainActivity.java` | Home: dock/grid, focus, carousel, status row, Control Center, profiles UI, Liquid Glass, idle mode |
| `SettingsActivity.java` | Settings pages |
| `SetupActivity.java` | First-time setup pages |
| `Suggestions.java`, `News.java` | Carousel content (JustWatch/TMDB/Stremio recommendations, Indian news RSS) |
| `Search.java`, `SearchPanel.java` | Search: titles on every service with Open / Get, apps and settings; the search screen |
| `MediaWatchService.java` | Continue Watching from media sessions |
| `Weather*.java` | Weather data, pill and forecast panel, icons |
| `Perms.java`, `PowerService.java` | On-screen permission flows; accessibility service for Power Off / Clean |
| `AirPlayGuard.java`, `Inputs.java`, `Clicks.java`, `Profiles.java` | AirPlay watchdog, TV inputs, sounds, profiles |
| `Ui.java`, `Glyphs.java` | Sizing (960×540 design grid), fonts, glyphs drawn in code |

Features are described in **[docs/features.md](docs/features.md)**.

## 2. Workflow

- `main` is protected: **never push to it**. Work on a branch and open a pull request; one approval
  is required to merge.
- Branch names: `feature/<short-name>`, `fix/<short-name>`, `docs/<short-name>`.
- Keep pull requests focused on one thing; several small ones beat one huge one.
- Commit messages: a short imperative summary line (≤ 72 chars), a blank line, then *what* and
  *why* in a few bullets. Mention what you tested and on which device.

```
Weather: retry the next source when one times out

- Open-Meteo timeouts left the pill empty until the next 15-minute tick.
- Tested on Mi Box (Android 12): pulled the network for 30 s, pill recovered.
```

- Bump the version only in release builds (`VERSION_CODE`/`VERSION_NAME` on the `build.sh` command
  line), not in source.

## 3. Code style

Match the code around you; consistency matters more than any rule here.

- **Java 11 language level**, Android API 24+ (`minSdk 24`, `targetSdk 34`). Guard newer APIs with
  `Build.VERSION.SDK_INT` checks.
- **No new runtime libraries.** The APK is ~1 MB and has no dependencies; keep it that way. Small,
  permissively licensed code may be vendored under `src/` with its licence (like Nayuki QR).
- **Views in code**, no XML layouts. Follow the existing patterns (`row(...)`, `ccTile(...)`,
  `option(...)`, `LiquidGlass`).
- **Sizes in design units**: always `dp(x)` / `Ui.px(ctx, x)`, never raw pixels, so 720p, 1080p and 4K
  keep their proportions. Text with `Ui.textSize`.
- **Fonts**: `Ui.font(ctx, "regular" | "medium" | "semibold" | "display")` (Inter).
- **ASCII-only source files.** Write non-ASCII characters as `\uXXXX` escapes (e.g. `"°"` for °).
- **Comments**: a short Javadoc on each class and non-obvious method saying *why*, matching the
  density of the surrounding code. No commented-out code.
- **Threads**: network, disk and bitmap decoding off the UI thread (`io` executor or a `Thread`);
  post results back with `handler`.
- **Strings**: user-facing text in sentence case for rows, Title Case for buttons/titles, as Apple
  does; keep it short and plain.

## 4. Design rules

tvOS Launcher's whole point is to look and feel like Apple tvOS 26. Before building UI:

- **Measure Apple's real UI first** (Apple's tvOS screenshots and the Human Interface Guidelines),
  then implement and state the measured numbers in the code or PR. Don't improvise the look.
- Liquid Glass is for **controls and panels** (dock, buttons, Control Center, pills). App cards stay
  opaque.
- Focus: lift/scale (cards 1.2×, controls ~1.06–1.12×), white focused state for buttons/tiles, never
  a coloured outline. Make sure focused items have room to grow (no clipping by parents).
- Text must stay legible over any artwork: use the existing scrims/shades, minimum text size 11.5
  design units (≈ Apple's 23 pt tvOS minimum).
- Everything must work with a 5-key remote (arrows, OK, Back, Home): every focusable item reachable,
  focus never lost, Home always returns to the first dock app.

## 5. Performance rules

The target is a Mi Box 4 (Mali-450 MP GPU, GLES 2.0, fill-rate bound). Home navigation should stay
near a 16 ms median frame time.

- **No perpetual animations.** Idle Home draws ~0 frames per second.
- **Nothing rendered in software on the UI thread during transitions.** Bake expensive things
  (blurs, gradients, glass backdrops) into bitmaps once.
- Avoid hidden full-screen layers and overdraw; prefer one baked image to several stacked ones.
- Cache network results and images on disk; never block startup on the network.

Measure before and after any visual change:

```sh
adb shell dumpsys gfxinfo com.techgenius.tvoslauncher reset
# …press Right/Left along the dock a few times…
adb shell dumpsys gfxinfo com.techgenius.tvoslauncher | grep -E "Janky|50th|90th"
```

Include the numbers in your PR. `--es perf <layer>` (see getting-started) helps find costly layers.

## 6. Permissions and privacy rules

- **adb is the last resort.** Every permission must have an on-screen path where the TV allows it
  (runtime prompt, the system's own settings screen, accessibility switch, role request), and must
  degrade gracefully with a clear message where the TV can't do it. Add new flows to `Perms.java`.
- Detect what the device supports before offering a feature (e.g. low-RAM TVs can't grant
  notification access; some TVs have no device-admin feature).
- The accessibility service (`PowerService`) does only what the user asked from tvOS Launcher (sleep, close
  apps). Don't extend it to read screen content.
- No analytics, no tracking, no accounts. Network calls go only to the content sources a feature
  needs (weather, news, recommendations, search, IP location) and never send personal data.
  Search queries go only to JustWatch (and Stremio's Cinemeta when Stremio/Nuvio is installed);
  recent searches stay on the TV.
- The microphone is used only while the user is dictating in Search (after Android's own prompt);
  tvOS Launcher never records or stores audio itself.
- Never commit secrets (API tokens, passwords) — TMDB keys are entered by the user at runtime.

## 7. Testing a change

There is no automated test suite yet; changes are verified on devices. For every change:

1. `./build.sh` succeeds with no new warnings you introduced.
2. Install and exercise the change with the remote (or `adb shell input keyevent …`), including
   Back and Home from every new screen.
3. Take screenshots (`adb exec-out screencap -p > shot.png`) of new or changed screens; attach them
   to the PR.
4. If it touches the Home screen, record frame times (see §5).
5. If it touches permissions, network or storage, test on both an Android 12 device and an
   **Android 9 / 1 GB RAM** device, and with the network off.
6. Check `adb logcat -s TvHome AndroidRuntime` for errors and crashes.

Checklist for UI changes: legible over bright and dark artwork · nothing clipped when focused ·
reachable with arrows · Home returns to the dock · 720p and 1080p both look right.

## 8. Pull requests

Open the PR against `main` with:

- **What and why** (link the issue if there is one).
- **Screenshots** of every changed screen.
- **How you tested**: device(s), Android version, steps.
- **Frame-time numbers** for Home changes.
- Docs updated if behaviour changed (`docs/features.md`, and `docs/architecture.md` for new files).

Reviewers check: matches tvOS design, no performance regression, works with a remote, permissions
follow §6, code follows §3.

## 9. Good first areas

- New weather icons (`WeatherIcons.java`) or connector icons (`Glyphs.java`).
- More Indian city news feeds (`News.java`, `TOI_CITIES` and the city slugs).
- More streaming services for recommendations (`Suggestions.java`, `PROVIDERS`).
- Translations of setup and Settings text (no i18n yet — a good larger project).
- Automated checks: a script that builds and lints, or JVM tests for the parsers (weather, news,
  playlist model).
- Accessibility: TalkBack labels on custom views.

## 10. Licensing

tvOS Launcher is licensed under the **[Apache License 2.0](LICENSE)**. By submitting a pull request
you agree that your contribution is licensed under the same terms (Apache-2.0, section 5). Keep the
[NOTICE](NOTICE) file accurate: add an entry for any third-party code or asset you bring in, and only
bring in code under a licence compatible with Apache-2.0 (MIT, BSD, Apache, OFL for fonts — not GPL).

Third-party code and assets already here: **Inter** font (SIL Open Font License,
`assets/fonts/Inter-LICENSE.txt`) and **Nayuki QR Code generator** (MIT, `src/io/nayuki/qrcodegen`).

### Signing

Development builds are signed with a local `debug.keystore` that `build.sh` creates on first use; it
is ignored by git. **Release builds are signed by maintainers only**, with the private key kept in
a separate private repository (never in this one):

```sh
RELEASE_KEYSTORE=/path/to/tvos-release.jks RELEASE_KEYSTORE_PASS=... VERSION_CODE=.. VERSION_NAME=.. ./build.sh
```

A debug build can't update a release install (different key): uninstall first.
>>>>>>> d9c9b2d05631118b07d2e84dce3b278f8eec4880
