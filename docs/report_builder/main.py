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
    
    # 1. Preliminary Pages (Cover, Acknowledgements, Reviews, TOC, Lists)
    body_elements.extend(build_preliminary())
    
    # 2. Introduction
    body_elements.extend(build_introduction())
    
    # 3. Chapter 1: Overview
    body_elements.extend(build_chapter1())
    
    # 4. Chapter 2: Theory & Core Tech
    body_elements.extend(build_chapter2())
    
    # 5. Chapter 3: Methodology & Design
    body_elements.extend(build_chapter3())
    
    # 6. Chapter 4: Implementation & Operations
    body_elements.extend(build_chapter4())
    
    # 7. Chapter 5: Quantitative Benchmarking & Security Evaluation
    body_elements.extend(build_chapter5())
    
    # 8. Chapter 6 & 7: Conclusion & References
    body_elements.extend(build_chapter6_7())

    # Build OpenXML package
    doc_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:body>'
        + "".join(body_elements) +
        '<w:sectPr>'
        '<w:pgSz w:w="11906" w:h="16838"/>'
        '<w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1417"/>'
        '</w:sectPr>'
        '</w:body>'
        '</w:document>'
    )

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

    print(f"[*] Đang đóng gói tệp tin DOCX tại: {output_path}...")
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as docx:
        docx.writestr('[Content_Types].xml', types_xml)
        docx.writestr('_rels/.rels', rels_xml)
        docx.writestr('word/document.xml', doc_xml)
    print(f"[+] Hoàn tất xuất tệp DOCX: {os.path.getsize(output_path):,} bytes")

if __name__ == "__main__":
    target_docx = "/home/nguyencongduc/mlops-multi-os-pipeline/docs/BAO_CAO_DO_AN_MLOPS_CHINH_THUC.docx"
    generate_full_docx(target_docx)
