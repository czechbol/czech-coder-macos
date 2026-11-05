#!/usr/bin/env python3
# Generate a macOS .keylayout replicating Linux xkb cz(coder).
# Base = US ANSI. Option = AltGr (level3), Shift+Option = level4.
# Option layer keeps all normal letters (overrides only diacritic keys),
# so you can hold Option for a whole sentence and still type plain text.


# code: (lower, upper) for US ANSI printable + space/tab/return + keypad
BASE = {
    0:("a","A"),1:("s","S"),2:("d","D"),3:("f","F"),4:("h","H"),5:("g","G"),
    # ISO key below Esc (also what some boards send for Esc-as-backtick); matches cz(coder)
    10:("`","~"),
    6:("z","Z"),7:("x","X"),8:("c","C"),9:("v","V"),11:("b","B"),12:("q","Q"),
    13:("w","W"),14:("e","E"),15:("r","R"),16:("y","Y"),17:("t","T"),
    18:("1","!"),19:("2","@"),20:("3","#"),21:("4","$"),22:("6","^"),23:("5","%"),
    24:("=","+"),25:("9","("),26:("7","&"),27:("-","_"),28:("8","*"),29:("0",")"),
    30:("]","}"),31:("o","O"),32:("u","U"),33:("[","{"),34:("i","I"),35:("p","P"),
    37:("l","L"),38:("j","J"),39:("'","\""),40:("k","K"),41:(";",":"),42:("\\","|"),
    43:(",","<"),44:("/","?"),45:("n","N"),46:("m","M"),47:(".",">"),50:("`","~"),
    49:(" "," "),48:("\t","\t"),36:("\r","\r"),
    # Backspace (macOS virtual key code 51)
    51:("\b","\b"),
    # keypad
    65:(".","."),67:("*","*"),69:("+","+"),75:("/","/"),78:("-","-"),81:("=","="),
    76:("\r","\r"),82:("0","0"),83:("1","1"),84:("2","2"),85:("3","3"),86:("4","4"),
    87:("5","5"),88:("6","6"),89:("7","7"),91:("8","8"),92:("9","9"),
}

# accent maps: plain -> accented (lowercase keys; uppercase derived)
ACUTE = {"a":"á","e":"é","i":"í","o":"ó","u":"ú","y":"ý"}
CARON = {"c":"č","s":"š","z":"ž","r":"ř","e":"ě","d":"ď","t":"ť","n":"ň","l":"ľ"}
RING  = {"u":"ů","a":"å"}
DIA   = {"a":"ä","e":"ë","i":"ï","o":"ö","u":"ü","y":"ÿ"}
STATES = {"acute":ACUTE,"caron":CARON,"ring":RING,"dia":DIA}
TERM = {"acute":"´","caron":"ˇ","ring":"˚","dia":"¨"}

# letters that combine with at least one dead key -> need an <action>
accentable = set()
for m in STATES.values():
    accentable |= set(m.keys())

# Option-layer overrides (keyMap 2). code -> literal output
OPT = {
    50:";", 10:";", 19:"ě",20:"š",21:"č",23:"ř",22:"ž",26:"ý",28:"á",25:"í",29:"é",
    33:"ú",41:"ů",39:"§",
}
OPT_ACTION = {24:"deadAcute", 42:"deadDia"}   # = and \

# Shift+Option-layer overrides (keyMap 3)
SOPT = {
    19:"Ě",20:"Š",21:"Č",23:"Ř",22:"Ž",26:"Ý",28:"Á",25:"Í",29:"É",
    14:"€",33:"Ú",41:"Ů",39:"\"",42:"'",
}
SOPT_ACTION = {24:"deadCaron", 50:"deadRing", 10:"deadRing"}  # = and ` (and ISO key)

def o(ch):
    # XML 1.0 cannot contain C0 controls literally, but keylayout uses their
    # numeric character references for editing keys such as Backspace.
    # Use numeric references, not named entities (&lt; &gt; &quot;): macOS's
    # keylayout parser drops the named forms, so <, > and " never type.
    refs = {"\b": "&#x0008;", "<": "&#x003C;", ">": "&#x003E;", "&": "&#x0026;", '"': "&#x0022;"}
    return refs.get(ch, ch)

def char_for(code, upper):
    lo,up = BASE[code]
    return up if upper else lo

def key_line(code, upper, overrides, override_actions):
    """Produce a <key> line for keyMap 2/3 given overrides."""
    if code in override_actions:
        return f'      <key code="{code}" action="{override_actions[code]}"/>'
    if code in overrides:
        return f'      <key code="{code}" output="{o(overrides[code])}"/>'
    # otherwise mirror base; accentable letters reference shared action
    ch = char_for(code, upper)
    if ch in accentable:
        aid = ch  # action id = the plain char (case-sensitive)
        return f'      <key code="{code}" action="{aid}"/>'
    return f'      <key code="{code}" output="{o(ch)}"/>'

def base_key_line(code, upper):
    ch = char_for(code, upper)
    if ch in accentable:
        return f'      <key code="{code}" action="{ch}"/>'
    return f'      <key code="{code}" output="{o(ch)}"/>'

codes = sorted(BASE.keys())

# --- actions ---
actions = []
# dead triggers
for name,st in [("deadAcute","acute"),("deadCaron","caron"),("deadRing","ring"),("deadDia","dia")]:
    actions.append(f'    <action id="{name}">\n      <when state="none" next="{st}"/>\n    </action>')
# letter actions (lower + upper)
def letter_action(ch, upper):
    plain = ch.upper() if upper else ch
    aid = plain
    whens = [f'      <when state="none" output="{o(plain)}"/>']
    for st,m in STATES.items():
        if ch in m:
            res = m[ch].upper() if upper else m[ch]
            whens.append(f'      <when state="{st}" output="{o(res)}"/>')
    return f'    <action id="{aid}">\n' + "\n".join(whens) + "\n    </action>"

for ch in sorted(accentable):
    actions.append(letter_action(ch, False))
    actions.append(letter_action(ch, True))

# --- keymaps ---
def keymap(index, upper, overrides=None, override_actions=None):
    lines = [f'    <keyMap index="{index}">']
    for c in codes:
        if overrides is None:
            lines.append(base_key_line(c, upper))
        else:
            lines.append(key_line(c, upper, overrides, override_actions))
    lines.append('    </keyMap>')
    return "\n".join(lines)

km0 = keymap(0, False)                         # base lower
km1 = keymap(1, True)                           # base upper
km2 = keymap(2, False, OPT,  OPT_ACTION)        # option
km3 = keymap(3, True,  SOPT, SOPT_ACTION)       # shift+option

terms = "\n".join(f'    <when state="{st}" output="{o(t)}"/>' for st,t in TERM.items())

xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE keyboard SYSTEM "file://localhost/System/Library/DTDs/KeyboardLayout.dtd">
<keyboard group="126" id="-9412" name="Czech Coder" maxout="1">
  <layouts>
    <layout first="0" last="255" mapSet="ANSI" modifiers="mods"/>
  </layouts>
  <modifierMap id="mods" defaultIndex="0">
    <keyMapSelect mapIndex="0">
      <modifier keys=""/>
      <modifier keys="command"/>
    </keyMapSelect>
    <keyMapSelect mapIndex="1">
      <modifier keys="anyShift"/>
      <modifier keys="caps"/>
      <modifier keys="anyShift caps"/>
      <modifier keys="anyShift command"/>
    </keyMapSelect>
    <keyMapSelect mapIndex="2">
      <modifier keys="anyOption"/>
      <modifier keys="anyOption command"/>
      <modifier keys="caps anyOption"/>
    </keyMapSelect>
    <keyMapSelect mapIndex="3">
      <modifier keys="anyShift anyOption"/>
      <modifier keys="anyShift caps anyOption"/>
      <modifier keys="anyShift anyOption command"/>
    </keyMapSelect>
  </modifierMap>
  <keyMapSet id="ANSI">
{km0}
{km1}
{km2}
{km3}
  </keyMapSet>
  <actions>
{chr(10).join(actions)}
  </actions>
  <terminators>
{terms}
  </terminators>
</keyboard>
'''

import sys
out = sys.argv[1] if len(sys.argv) > 1 else "Czech Coder.keylayout"
open(out, "w", encoding="utf-8").write(xml)
print(f"wrote {out} ({len(xml)} bytes)")
