import xml.sax.saxutils as saxutils

def p(text, align="both", bold=False, italic=False, size=26, color="000000",
      space_before=80, space_after=80, line_spacing="360", indent=0):
    b_tag = "<w:b/>" if bold else ""
    i_tag = "<w:i/>" if italic else ""
    jc_val = align if align in ["left", "right", "center"] else "both"
    jc_tag = f'<w:jc w:val="{jc_val}"/>'
    ind_tag = f'<w:ind w:firstLine="{indent}"/>' if indent > 0 else ""
    return (
        f'<w:p>'
        f'<w:pPr>{jc_tag}{ind_tag}<w:spacing w:line="{line_spacing}" w:lineRule="auto" w:before="{space_before}" w:after="{space_after}"/></w:pPr>'
        f'<w:r>'
        f'<w:rPr>{b_tag}{i_tag}<w:sz w:val="{size}"/><w:color w:val="{color}"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>'
        f'<w:t xml:space="preserve">{saxutils.escape(text)}</w:t>'
        f'</w:r>'
        f'</w:p>'
    )

def heading1(text):
    return p(text, align="center", bold=True, size=34, color="002060", space_before=240, space_after=160)

def heading2(text):
    return p(text, align="left", bold=True, size=28, color="002060", space_before=180, space_after=100)

def heading3(text):
    return p(text, align="left", bold=True, size=26, color="000000", space_before=140, space_after=80)

def heading4(text):
    return p(text, align="left", bold=True, italic=True, size=25, color="333333", space_before=100, space_after=60)

def page_break():
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'

def table_grid(headers, rows, col_widths=None):
    xml = ['<w:tbl>',
           '<w:tblPr><w:tblW w:w="9600" w:type="dxa"/><w:jc w:val="center"/>',
           '<w:tblBorders>',
           '<w:top w:val="single" w:sz="8" w:space="0" w:color="002060"/>',
           '<w:left w:val="single" w:sz="6" w:space="0" w:color="D0D7DE"/>',
           '<w:bottom w:val="single" w:sz="8" w:space="0" w:color="002060"/>',
           '<w:right w:val="single" w:sz="6" w:space="0" w:color="D0D7DE"/>',
           '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="D0D7DE"/>',
           '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="D0D7DE"/>',
           '</w:tblBorders></w:tblPr>']
    
    xml.append('<w:tr><w:trPr><w:tblHeader/></w:trPr>')
    for h in headers:
        xml.append(f'<w:tc><w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="F0F4F8"/></w:tcPr>{p(h, align="center", bold=True, size=24, color="002060", space_before=80, space_after=80)}</w:tc>')
    xml.append('</w:tr>')
    
    for r_idx, row in enumerate(rows):
        fill = 'FFFFFF' if r_idx % 2 == 0 else 'F9FAFB'
        xml.append('<w:tr>')
        for cell in row:
            xml.append(f'<w:tc><w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="{fill}"/></w:tcPr>{p(cell, align="left", size=22, space_before=50, space_after=50, line_spacing="280")}</w:tc>')
        xml.append('</w:tr>')
    xml.append('</w:tbl>')
    return "".join(xml)

def code_box(code_lines, title=None):
    xml = []
    if title:
        xml.append(p(f"Listing: {title}", align="left", bold=True, italic=True, size=22, color="555555", space_before=100, space_after=40))
    for line in code_lines:
        xml.append(
            f'<w:p>'
            f'<w:pPr>'
            f'<w:jc w:val="left"/>'
            f'<w:spacing w:line="240" w:lineRule="auto" w:before="15" w:after="15"/>'
            f'<w:shd w:val="clear" w:color="auto" w:fill="F6F8FA"/>'
            f'<w:pBdr><w:left w:val="single" w:sz="18" w:space="10" w:color="0969DA"/></w:pBdr>'
            f'</w:pPr>'
            f'<w:r>'
            f'<w:rPr><w:sz w:val="19"/><w:color w:val="1F2328"/><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/></w:rPr>'
            f'<w:t xml:space="preserve">{saxutils.escape(line)}</w:t>'
            f'</w:r>'
            f'</w:p>'
        )
    xml.append(p("", space_after=80))
    return "".join(xml)

def figure_box(fig_num, fig_title, fig_desc, schematic_lines=None):
    xml = []
    if schematic_lines:
        xml.append(
            f'<w:p>'
            f'<w:pPr><w:jc w:val="center"/><w:spacing w:line="240" w:lineRule="auto" w:before="60" w:after="60"/>'
            f'<w:shd w:val="clear" w:color="auto" w:fill="F8F9FA"/>'
            f'<w:pBdr>'
            f'<w:top w:val="single" w:sz="6" w:space="8" w:color="D0D7DE"/>'
            f'<w:bottom w:val="single" w:sz="6" w:space="8" w:color="D0D7DE"/>'
            f'<w:left w:val="single" w:sz="6" w:space="8" w:color="D0D7DE"/>'
            f'<w:right w:val="single" w:sz="6" w:space="8" w:color="D0D7DE"/>'
            f'</w:pBdr>'
            f'</w:pPr>'
        )
        for s in schematic_lines:
            xml.append(
                f'<w:r><w:rPr><w:sz w:val="18"/><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/><w:color w:val="0969DA"/></w:rPr>'
                f'<w:t xml:space="preserve">{saxutils.escape(s)}</w:t><w:br/></w:r>'
            )
        xml.append('</w:p>')
    
    xml.append(p(f"Hình {fig_num}: {fig_title}", align="center", bold=True, size=24, color="002060", space_before=60, space_after=40))
    xml.append(p(f"Mô tả: Hình {fig_num} {fig_desc}", align="both", italic=True, size=23, color="444444", space_before=20, space_after=120, indent=400))
    return "".join(xml)

def note_box(title, text):
    return (
        f'<w:p>'
        f'<w:pPr>'
        f'<w:jc w:val="both"/>'
        f'<w:spacing w:line="320" w:lineRule="auto" w:before="80" w:after="80"/>'
        f'<w:shd w:val="clear" w:color="auto" w:fill="EDF2F7"/>'
        f'<w:pBdr><w:left w:val="single" w:sz="24" w:space="12" w:color="BA141A"/></w:pBdr>'
        f'</w:pPr>'
        f'<w:r>'
        f'<w:rPr><w:b/><w:sz w:val="24"/><w:color w:val="BA141A"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>'
        f'<w:t xml:space="preserve">{saxutils.escape(title)}: </w:t>'
        f'</w:r>'
        f'<w:r>'
        f'<w:rPr><w:sz w:val="23"/><w:color w:val="2D3748"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>'
        f'<w:t xml:space="preserve">{saxutils.escape(text)}</w:t>'
        f'</w:r>'
        f'</w:p>'
    )





def image_figure(rel_id, fig_num, fig_title, fig_desc, cx=5486400, cy=2286000):
    clean_id = fig_num.replace(".", "")
    xml = [
        "<w:p>",
        "<w:pPr><w:jc w:val=\"center\"/><w:spacing w:line=\"240\" w:lineRule=\"auto\" w:before=\"120\" w:after=\"60\"/></w:pPr>",
        "<w:r>",
        "<w:drawing>",
        "<wp:inline distT=\"0\" distB=\"0\" distL=\"0\" distR=\"0\" xmlns:wp=\"http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing\">",
        f"<wp:extent cx=\"{cx}\" cy=\"{cy}\"/>",
        "<wp:effectExtent l=\"0\" t=\"0\" r=\"0\" b=\"0\"/>",
        f"<wp:docPr id=\"{clean_id}\" name=\"Figure {fig_num}\"/>",
        "<wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a=\"http://schemas.openxmlformats.org/drawingml/2006/main\" noChangeAspect=\"1\"/></wp:cNvGraphicFramePr>",
        "<a:graphic xmlns:a=\"http://schemas.openxmlformats.org/drawingml/2006/main\">",
        "<a:graphicData uri=\"http://schemas.openxmlformats.org/drawingml/2006/picture\">",
        "<pic:pic xmlns:pic=\"http://schemas.openxmlformats.org/drawingml/2006/picture\">",
        f"<pic:nvPicPr><pic:cNvPr id=\"0\" name=\"fig_{fig_num}.png\"/><pic:cNvPicPr/></pic:nvPicPr>",
        "<pic:blipFill>",
        f"<a:blip xmlns:r=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships\" r:embed=\"{rel_id}\"/>",
        "<a:stretch><a:fillRect/></a:stretch>",
        "</pic:blipFill>",
        f"<pic:spPr><a:xfrm><a:off x=\"0\" y=\"0\"/><a:ext cx=\"{cx}\" cy=\"{cy}\"/></a:xfrm><a:prstGeom prst=\"rect\"><a:avLst/></a:prstGeom></pic:spPr>",
        "</pic:pic>",
        "</a:graphicData>",
        "</a:graphic>",
        "</wp:inline>",
        "</w:drawing>",
        "</w:r>",
        "</w:p>"
    ]
    xml.append(p(f"Hình {fig_num}: {fig_title}", align="center", bold=True, size=24, color="002060", space_before=60, space_after=40))
    xml.append(p(f"Mô tả: Hình {fig_num} {fig_desc}", align="both", italic=True, size=23, color="444444", space_before=20, space_after=120, indent=400))
    return "".join(xml)
