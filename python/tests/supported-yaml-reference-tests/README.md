# Tests status
c-byte-order-mark.invalid.input does not seem invalid.
Opened an [issue](https://github.com/orenbenkiki/yamlreference/issues/7) against the reference implementation.
For now it's renamed to be excluded.

Looks like a repeating pattern, same problem with b-break.invalid.


## b-break symbol in yeast:
    --  [@b@] Contains separation line break
    --  [@L@] Contains line break normalized to content line feed
    --  [@l@] Contains line break folded to content space
    
Actually expecting a '-':

    --  [@-@] Unparsed text following error point.
    
Either the comment is wrong or, more likely - something is still missing.