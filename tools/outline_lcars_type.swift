// Render the terminal's technical lettering as original artwork paths.
// Requires macOS CoreText and its licensed system DIN Condensed Bold font.
// Fonts are not copied into the repository. Technical captions need no viewer-installed font.
import Foundation
import CoreText
import CoreGraphics

let fm = FileManager.default
let root = URL(fileURLWithPath: #filePath).deletingLastPathComponent().deletingLastPathComponent()
let assets = root.appendingPathComponent("assets")
let textRE = try! NSRegularExpression(pattern: "<text\\b([^>]*)>(.*?)</text>", options: [.dotMatchesLineSeparators])
let attrRE = try! NSRegularExpression(pattern: "([\\w-]+)=\"([^\"]*)\"")
func decode(_ s: String) -> String {
    s.replacingOccurrences(of: "&lt;", with: "<").replacingOccurrences(of: "&gt;", with: ">").replacingOccurrences(of: "&quot;", with: "\"").replacingOccurrences(of: "&#x27;", with: "'").replacingOccurrences(of: "&apos;", with: "'").replacingOccurrences(of: "&amp;", with: "&")
}
func fmt(_ x: CGFloat) -> String {
    let s=String(format: "%.2f", Double(x))
    return s.replacingOccurrences(of: #"\.?0+$"#, with: "", options: .regularExpression)
}
var total=0
for url in (try! fm.contentsOfDirectory(at: assets, includingPropertiesForKeys: nil)).filter({ url in
    url.pathExtension == "svg" && ["lcars-starship", "lcars-logbook", "lcars-aqvionis-link"].contains { url.lastPathComponent.hasPrefix($0) }
}) {
    var svg=try! String(contentsOf: url, encoding: .utf8)
    let matches=textRE.matches(in: svg, range: NSRange(svg.startIndex..., in: svg))
    var count=0
    for match in matches.reversed() {
        let raw=String(svg[Range(match.range(at: 2), in: svg)!])
        let text=decode(raw)
        // Personal prose remains readable sans. Technical captions use a
        // consistent condensed outline, independent of a viewer's fonts.
        if text != text.uppercased() || text.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty { continue }
        let attributes=String(svg[Range(match.range(at: 1), in: svg)!])
        var attrs=[String:String]()
        for a in attrRE.matches(in: attributes, range: NSRange(attributes.startIndex..., in: attributes)) {
            attrs[String(attributes[Range(a.range(at: 1), in: attributes)!])] = String(attributes[Range(a.range(at: 2), in: attributes)!])
        }
        if attrs["transform"] != nil { continue } // preserve the ship's tiny hull registry
        guard let size=Double(attrs["font-size"] ?? ""),let x=Double(attrs["x"] ?? ""),let y=Double(attrs["y"] ?? "") else {continue}
        let font=CTFontCreateWithName("DINCondensed-Bold" as CFString, size, nil)
        let chars=Array(text.utf16)
        var glyphs=[CGGlyph](repeating: 0,count: chars.count)
        _=CTFontGetGlyphsForCharacters(font,chars,&glyphs,chars.count)
        var advances=[CGSize](repeating: .zero,count: chars.count)
        _=CTFontGetAdvancesForGlyphs(font,.horizontal,glyphs,&advances,glyphs.count)
        let spacing=Double(attrs["letter-spacing"] ?? "0") ?? 0
        let width=advances.reduce(0){$0+$1.width}+CGFloat(spacing)*CGFloat(max(0,chars.count-1))
        let xscale:CGFloat=0.86
        var origin=CGFloat(x)
        if attrs["text-anchor"] == "end" {origin-=width*xscale}
        if attrs["text-anchor"] == "middle" {origin-=width*xscale/2}
        let path=CGMutablePath()
        var cursor:CGFloat=0
        for (i,glyph) in glyphs.enumerated() {
            if let p=CTFontCreatePathForGlyph(font,glyph,nil) {
                path.addPath(p,transform:CGAffineTransform(translationX:cursor,y:0))
            }
            cursor += advances[i].width+CGFloat(spacing)
        }
        var d=""
        path.applyWithBlock { ptr in
            let e=ptr.pointee
            switch e.type {
            case .moveToPoint:d+="M"+fmt(e.points[0].x)+" "+fmt(e.points[0].y)
            case .addLineToPoint:d+="L"+fmt(e.points[0].x)+" "+fmt(e.points[0].y)
            case .addQuadCurveToPoint:d+="Q"+fmt(e.points[0].x)+" "+fmt(e.points[0].y)+" "+fmt(e.points[1].x)+" "+fmt(e.points[1].y)
            case .addCurveToPoint:d+="C"+fmt(e.points[0].x)+" "+fmt(e.points[0].y)+" "+fmt(e.points[1].x)+" "+fmt(e.points[1].y)+" "+fmt(e.points[2].x)+" "+fmt(e.points[2].y)
            case .closeSubpath:d+="Z"
            @unknown default:break
            }
        }
        let fill=attrs["fill"].map { " fill=\""+$0+"\"" } ?? ""
        let replacement="<g aria-label=\""+raw+"\""+fill+" transform=\"translate("+fmt(origin)+" "+fmt(CGFloat(y))+") scale(.86 -1)\"><title>"+raw+"</title><path d=\""+d+"\"/></g>"
        svg.replaceSubrange(Range(match.range, in: svg)!,with:replacement)
        count+=1
    }
    try! svg.write(to:url,atomically:true,encoding:.utf8)
    total+=count
    print("\(url.lastPathComponent): \(count) condensed captions")
}
print("Outlined \(total) technical captions. Technical captions have no installed-font dependency.")
