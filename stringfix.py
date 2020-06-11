def fix_text(txt):
  short_txt = txt
  if len(short_txt) > 250:
    short_txt = short_txt[:250]
    if '.' in short_txt:
      short_txt = short_txt[: -short_txt[::-1].find('.')]
  fixed_txt = ''
  for newline in short_txt:
    if not (newline.isdecimal()):
      fixed_txt = fixed_txt + newline
  return(fixed_txt)