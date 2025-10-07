const std = @import("std");

const encoded_flag = [_]u16{ 65, 87, 108, 106, 100, 130, 95, 55, 66, 84, 141, 71, 64, 121, 176, 66, 44, 48, 58, 58, 112, 108, 47, 105, 161, 156, 119, 167, 164, 156, 194, 120, 175, 173, 186, 101, 188, 111, 136 };

const key = [_]u8{ 13, 7, 29, 42, 3, 9, 11 };

fn transform(i: usize, v: u16) u16 {
    const k = key[(i * 7) % key.len];
    const step1 = v ^ (@intCast(u16, (i << 1) + 5));
    const step2 = step1 - (@intCast(u16, k ^ @intCast(u16, i)));
    return step2;
}

pub fn main() !void {
    const stdout = std.io.getStdOut().writer();
    var sum: u32 = 0;
    for (encoded_flag, 0..) |v, i| {
        const x = transform(i, v);
        sum += @intCast(u32, x);
    }
    try stdout.print("Checksum: {x}\n", .{sum});
}
