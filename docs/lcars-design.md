# LCARS profile design notes

The profile is conceived as a personal log opened on an Enterprise-D console. The ship display, Personal Log, Mission Log, Science Log, Off-Duty Log and Captain’s Log share one visual language. AQVIONIS remains the principal research mission; the personal prose retains its curious, lightly humorous British English voice.

## Research and interpretation

- [Michael and Denise Okuda’s 1999 Q&A](https://trektoday.com/interviews/okuda_qa.shtml) explains the original goal: clear organisation of complicated information. It also describes the original lettering and illustration processes. The profile therefore gives prose a clear reading order and treats small instrument details as secondary information.
- [The Art Directors Guild’s Enterprise-D production reference](https://assets.adg.org/media/submissions/2023-09-30_21-38-05/ADG_PICARD.pdf) records Michael Okuda’s recreation of his 1987 console graphics for *Star Trek: Picard*. Its panels informed the black negative space, warm colour blocks, curved elbows and restrained technical labelling.
- [Andrew Probert’s Enterprise-D design account and concept art](https://forgottentrek.com/the-next-generation/designing-the-next-generation-enterprise/) describes the dominant saucer and the compressed oval shapes that unify the ship. These principles guide the illustration’s proportions, swept supports and organic secondary hull.
- [Ubisoft’s Enterprise-D announcement](https://news.ubisoft.com/en-us/article/O9FIK2Y8t3e0X31u5TNxR/star-trek-bridge-crew-enterprised-romulans-borg-and-more-arrive-in-new-expansion) provides a licensed game depiction useful for checking the recognisable silhouette and relationship of hull, deflector and engines.

The artwork is an original, procedurally drawn three-quarter SVG illustration, rather than traced reference imagery or embedded raster art. References establish visual principles; they are not repository image dependencies. The warm orange and lavender palette is an interpretation of TNG displays, rather than a claim that the production used one immutable digital palette.

## Shared display system

Black backgrounds, orange and lavender rails, rounded panel ends and consistent gutters connect every display. Uppercase technical headings establish the console character; larger, less compressed prose supports reading. Blue is reserved principally for propulsion and scientific display elements. The ship remains the central visual focus, with window bands, surface seams and subdued metallic shading providing scale and depth.

SVG titles and descriptions provide meaningful image alternatives. Narrow-layout assets give the log content room to breathe on smaller screens. All display resources live in this repository; the published profile requires no JavaScript or runtime dependencies.

Starship sensor, navigation and propulsion readings are fictional console scenery. They are not measured project statistics. No invented research outcomes or project performance metrics are presented. AQVIONIS is private and remains a research mission in the log. The public project button links to the M3 repository.

## Regeneration

From the repository root, run:

```sh
python3 tools/build_starship.py
python3 tools/build_logbook.py
swift tools/outline_lcars_type.swift
```

The content and illustration generators use the Python standard library only. The optional final lettering pass uses macOS CoreText and its system DIN Condensed Bold font, compressed slightly to suit the terminal. It renders technical captions as paths; no font file is distributed or required by the published profile. Personal prose retains a readable sans serif. Keep the generated SVGs alongside the sources, inspect wide and narrow layouts after changing copy or geometry, and check the rendered GitHub profile before publishing subsequent revisions.

The README pins image URLs to a verified artwork commit. This prevents GitHub’s raw-image cache from mixing old and new displays. After regenerating artwork, commit it first, update the image commit in the README, and check the public rendering.
