#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import zipfile
import subprocess

from report_builder.preliminary import build_preliminary
from report_builder.introduction import build_introduction
from report_builder.chapter1 import build_chapter1
from report_builder.chapter2 import build_chapter2
from report_builder.chapter3 import build_chapter3
from report_builder.chapter4 import build_chapter4
from report_builder.chapter5 import build_chapter5
from report_builder.chapter6_7 import build_chapter6_7

def generate_full_docx(output_path):
    print("[*] Bắt đầu tổng hợp nội dung báo cáo đồ án VKU...")
    body_elements = []
    
    body_elements.extend(build_preliminary())
    body_elements.extend(build_introduction())
    body_elements.extend(build_chapter1())
    body_elements.extend(build_chapter2())
    body_elements.extend(build_chapter3())
    body_elements.extend(build_chapter4())
    body_elements.extend(build_chapter5())
    body_elements.extend(build_chapter6_7())

    doc_xml = (
        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>"
        "<w:document xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\" "
        "xmlns:r=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships\" "
        "xmlns:wp=\"http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing\" "
        "xmlns:a=\"http://schemas.openxmlformats.org/drawingml/2006/main\" "
        "xmlns:pic=\"http://schemas.openxmlformats.org/drawingml/2006/picture\">"
        "<w:body>"
        + "".join(body_elements) +
        "<w:sectPr>"
        "<w:pgSz w:w=\"11906\" w:h=\"16838\"/>"
        "<w:pgMar w:top=\"1134\" w:right=\"1134\" w:bottom=\"1134\" w:left=\"1417\"/>"
        "</w:sectPr>"
        "</w:body>"
        "</w:document>"
    )

    types_xml = (
        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>"
        "<Types xmlns=\"http://schemas.openxmlformats.org/package/2006/content-types\">"
        "<Default Extension=\"rels\" ContentType=\"application/vnd.openxmlformats-package.relationships+xml\"/>"
        "<Default Extension=\"xml\" ContentType=\"application/xml\"/>"
        "<Default Extension=\"png\" ContentType=\"image/png\"/>"
        "<Override PartName=\"/word/document.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml\"/>"
        "</Types>"
    )

    rels_root = (
        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>"
        "<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\">"
        "<Relationship Id=\"rId1\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument\" Target=\"word/document.xml\"/>"
        "</Relationships>"
    )

    rels_doc = (
        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>"
        "<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\">"
        "<Relationship Id=\"rIdImg1_2\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/image\" Target=\"media/hinh_1_2.png\"/>"
        "</Relationships>"
    )

    print(f"[*] Đang đóng gói tệp tin DOCX tại: {output_path}...")
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as docx:
        docx.writestr("[Content_Types].xml", types_xml)
        docx.writestr("_rels/.rels", rels_root)
        docx.writestr("word/_rels/document.xml.rels", rels_doc)
        docx.writestr("word/document.xml", doc_xml)
        
        # Thêm ảnh đồ họa
        img_1_2_path = "/home/nguyencongduc/mlops-multi-os-pipeline/docs/figures/hinh_1_2_mlops_lifecycle.png"
        if os.path.exists(img_1_2_path):
            with open(img_1_2_path, "rb") as img_f:
                docx.writestr("word/media/hinh_1_2.png", img_f.read())
                
    print(f"[+] Hoàn tất xuất tệp DOCX: {os.path.getsize(output_path):,} bytes")

if __name__ == "__main__":
    target_docx = "/home/nguyencongduc/mlops-multi-os-pipeline/docs/BAO_CAO_DO_AN_MLOPS_CHINH_THUC.docx"
    generate_full_docx(target_docx)
