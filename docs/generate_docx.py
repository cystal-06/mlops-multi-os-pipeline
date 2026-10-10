import zipfile
import xml.sax.saxutils as saxutils

def create_docx(md_path, docx_path):
    with open(md_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    title = "QUY ƯỚC LÀM VIỆC NHÓM & PHÂN CÔNG ĐỒ ÁN"
    content_xml_parts = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">',
        '<w:body>',
        f'<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="36"/><w:color w:val="0969DA"/></w:rPr><w:t>{saxutils.escape(title)}</w:t></w:r></w:p>'
    ]

    for para in lines:
        if para.startswith("# QUY ƯỚC"):
            continue
        elif para.startswith("## "):
            text = para[3:]
            content_xml_parts.append(
                f'<w:p><w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="28"/><w:color w:val="1F2328"/></w:rPr><w:t>{saxutils.escape(text)}</w:t></w:r></w:p>'
            )
        elif para.startswith("### "):
            text = para[4:]
            content_xml_parts.append(
                f'<w:p><w:pPr><w:spacing w:before="180" w:after="80"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="24"/><w:color w:val="0969DA"/></w:rPr><w:t>{saxutils.escape(text)}</w:t></w:r></w:p>'
            )
        elif para.startswith("* ") or para.startswith("- "):
            text = para[2:]
            content_xml_parts.append(
                f'<w:p><w:pPr><w:ind w:left="360"/><w:spacing w:after="60"/></w:pPr><w:r><w:t>• {saxutils.escape(text)}</w:t></w:r></w:p>'
            )
        else:
            content_xml_parts.append(
                f'<w:p><w:pPr><w:spacing w:after="100"/></w:pPr><w:r><w:t>{saxutils.escape(para)}</w:t></w:r></w:p>'
            )

    content_xml_parts.append('<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr>')
    content_xml_parts.append('</w:body></w:document>')
    document_xml = "".join(content_xml_parts)

    types_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        '</Types>'
    )

    rels_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        '</Relationships>'
    )

    with zipfile.ZipFile(docx_path, 'w', zipfile.ZIP_DEFLATED) as docx:
        docx.writestr('[Content_Types].xml', types_xml)
        docx.writestr('_rels/.rels', rels_xml)
        docx.writestr('word/document.xml', document_xml)

if __name__ == "__main__":
    create_docx(
        "/home/nguyencongduc/mlops-multi-os-pipeline/docs/QUY_UOC_LAM_VIEC.md",
        "/home/nguyencongduc/mlops-multi-os-pipeline/docs/QUY_UOC_LAM_VIEC.docx"
    )
    print("DOCX generated successfully.")
