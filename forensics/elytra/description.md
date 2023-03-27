# elytra

So... this was _intended_ to be a simple stego challenge. (Maybe it didn't
end up that way). The challenge consists of the End Poem from Minecraft, but
the line endings encode a message. Linux and Windows utilize two different line
endings: `\n` for Linux and `CRLF` for Windows. In this file, we'll mix and
match those to encode either `0` (`\n`) or `1` (`CRLF`).
