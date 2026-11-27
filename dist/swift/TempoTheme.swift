// tempo-theme: tokens.json에서 generate.py가 만든다. 고치지 말 것
import AppKit

enum TempoTheme {
    struct Palette {
        let void: NSColor
        let archive: NSColor
        let drawer: NSColor
        let seam: NSColor
        let paper: NSColor
        let dust: NSColor
        let ash: NSColor
        let brass: NSColor
        let thread: NSColor
        let signal: NSColor
        let branch: NSColor
    }

    static let ember = Palette(
        void: rgb(0x0f0c09),
        archive: rgb(0x1a1510),
        drawer: rgb(0x241d16),
        seam: rgb(0x3a3026),
        paper: rgb(0xefe3cf),
        dust: rgb(0xa8977f),
        ash: rgb(0x9a8a73),
        brass: rgb(0xd79a45),
        thread: rgb(0x46f0a0),
        signal: rgb(0xf5c84b),
        branch: rgb(0xff6a45)
    )

    static let thread = Palette(
        void: rgb(0x050b0b),
        archive: rgb(0x0b1615),
        drawer: rgb(0x12211f),
        seam: rgb(0x1f3530),
        paper: rgb(0xdcf3e7),
        dust: rgb(0x86ab9c),
        ash: rgb(0x7b9d90),
        brass: rgb(0xe8a33d),
        thread: rgb(0x46f0a0),
        signal: rgb(0xf2c14a),
        branch: rgb(0xff5d3a)
    )

    private static func rgb(_ hex: UInt32) -> NSColor {
        NSColor(srgbRed: CGFloat((hex >> 16) & 0xff) / 255, green: CGFloat((hex >> 8) & 0xff) / 255,
                blue: CGFloat(hex & 0xff) / 255, alpha: 1)
    }
}
