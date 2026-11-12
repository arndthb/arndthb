# LCARS profile design notes

The profile is conceived as a personal exploration log on a dark science-fiction console. The shuttle display, Personal Log, Mission Log, Science Log, Off-Duty Log and Captain’s Log share one visual language. AQVIONIS remains the principal research mission; the personal prose retains its curious, lightly humorous British English voice.

## Research and interpretation

- [Michael and Denise Okuda’s 1999 Q&A](https://trektoday.com/interviews/okuda_qa.shtml) explains the original goal: clear organisation of complicated information. It also describes the original lettering and illustration processes. The profile therefore gives prose a clear reading order and treats small instrument details as secondary information.
- [The Art Directors Guild’s Enterprise-D production reference](https://assets.adg.org/media/submissions/2023-09-30_21-38-05/ADG_PICARD.pdf) records Michael Okuda’s recreation of his 1987 console graphics for *Star Trek: Picard*. Its panels informed the black negative space, warm colour blocks, curved elbows and restrained technical labelling.

The AR04 survey shuttle is a procedurally drawn three-quarter SVG illustration with original vector geometry and deliberate TNG design inspiration. The final silhouette deliberately draws on classic TNG shuttle proportions: a compact ivory cabin, a long dark windshield, large angular side windows, raised roof shoulders and short low engine pods with orange collars. The large tail fin is removed. Recessed drive channels, a service hatch, AR04 identification stencils and manoeuvring jets provide technical detail. The artwork retains its own designation and carries no franchise insignia. It is not presented as licensed or affiliated artwork. No reference image is traced or embedded. References establish visual principles; they are not repository image dependencies. The warm orange and lavender palette is an interpretation of TNG displays, rather than a claim that the production used one immutable digital palette.

The [official Star Trek shuttlecraft article](https://www.startrek.com/news/eaglemoss-adds-four-shuttlecraft-to-starships-collection) identifies the Type 6 as an Enterprise-D shuttle and provides the visual reference for this final design direction. The illustration is drawn anew rather than traced from those photographs.

## Shared display system

Black backgrounds, orange and lavender rails, rounded panel ends and consistent gutters connect every display. Uppercase technical headings establish the console character; larger, less compressed prose supports reading. Blue is reserved principally for propulsion and scientific display elements. The shuttle remains the central visual focus, with cockpit reflections, service panels, surface seams and subdued metallic shading providing scale and depth.

SVG titles and descriptions provide meaningful image alternatives. Narrow-layout assets give the log content room to breathe on smaller screens. All display resources live in this repository; the published profile requires no JavaScript or runtime dependencies.

Shuttle sensor, navigation and propulsion readings are fictional console scenery. They are not measured project statistics. No invented research outcomes or project performance metrics are presented. AQVIONIS is private and remains a research mission in the log. The public project button links to the M3 repository.

## Regeneration

From the repository root, run:

```sh
python3 tools/build_starship.py
python3 tools/build_logbook.py
swift tools/outline_lcars_type.swift
```

The content and illustration generators use the Python standard library only. The optional final lettering pass uses macOS CoreText and its system DIN Condensed Bold font, compressed slightly to suit the terminal. It renders technical captions as paths; no font file is distributed or required by the published profile. Personal prose retains a readable sans serif. Keep the generated SVGs alongside the sources, inspect wide and narrow layouts after changing copy or geometry, and check the rendered GitHub profile before publishing subsequent revisions.

The README pins image URLs to a verified artwork commit. This prevents GitHub’s raw-image cache from mixing old and new displays. After regenerating artwork, commit it first, update the image commit in the README, and check the public rendering.

## Motion and scope

Seven small status beacons pulse slowly across the craft, propulsion, sensor and navigation displays using SVG CSS animation. Their cycle is 3.8 seconds. A visible star field sits behind the craft in both layouts, with a few stars twinkling over 7.2 seconds. No JavaScript is used. A `prefers-reduced-motion: reduce` media query keeps all beacons and stars steady. The entire display remains readable as a static image.

The console draws inspiration from LCARS. The independent shuttle design is not a legal clearance of the overall presentation. German copyright law distinguishes protected creative work and adaptations, including the need for sufficient distance from another work; see [UrhG section 2](https://www.gesetze-im-internet.de/urhg/__2.html) and [UrhG section 23](https://www.gesetze-im-internet.de/urhg/__23.html).

## Interactive inspection

The profile image links to the GitHub Pages inspection view. The model data is exported from the same procedural geometry before SVG view culling. The inspection view adds the otherwise unseen port-side details and rear hatch. A dependency-free Canvas renderer projects and shades the three-dimensional surfaces. Pointer capture provides drag rotation; the wheel and two-pointer pinch adjust distance. Keyboard arrows, plus/minus and Home provide equivalent controls. Motion preferences stop automatic rotation and status animations. All application code, model data and display assets are stored in this repository.

### Cabin cutaway
The interior toggle sections the upper hull at deck level and reveals two flight seats, sloped LCARS consoles, a passenger bench, equipment lockers, a small workstation and the aft double hatch. The lower exterior and propulsion pods retain the original silhouette. Geometry is generated by `tools/build_interior.py` from the shared mesh; no external models or libraries are used. The toggle exposes its state to assistive technology and preserves manual orbit and zoom controls.
