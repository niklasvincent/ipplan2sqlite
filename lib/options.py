def enum(**enums):
    return type('Enum', (), enums)


Address = enum(IPv4 = 4, IPv6 = 6)
