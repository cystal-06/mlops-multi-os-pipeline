#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import zipfile
import subprocess
import xml.sax.saxutils as saxutils

def generate_slides_docx(output_path):
    body = []

    def p(text, align="left", bold=False, italic=False, size=24, color="1E293B",
          space_before=60, space_after=60, line_spacing="280", indent=0):
        b_tag = "<w:b/>" if bold else ""
        i_tag = "<w:i/>" if italic else ""
        jc_val = align if align in ["left", "right", "center"] else "left"
        jc_tag = f'<w:jc w:val="{jc_val}"/>'
        ind_tag = f'<w:ind w:left="{indent}"/>' if indent > 0 else ""
        return (
            f'<w:p>'
            f'<w:pPr>{jc_tag}{ind_tag}<w:spacing w:line="{line_spacing}" w:lineRule="auto" w:before="{space_before}" w:after="{space_after}"/></w:pPr>'
            f'<w:r>'
            f'<w:rPr>{b_tag}{i_tag}<w:sz w:val="{size}"/><w:color w:val="{color}"/><w:rFonts w:ascii="Segoe UI" w:hAnsi="Segoe UI"/></w:rPr>'
            f'<w:t xml:space="preserve">{saxutils.escape(text)}</w:t>'
            f'</w:r>'
            f'</w:p>'
        )

    def slide_header(title, subtitle=None, tag="VKU MLOPS"):
        xml = []
        xml.append(
            f'<w:p>'
            f'<w:pPr>'
            f'<w:jc w:val="left"/>'
            f'<w:spacing w:line="300" w:lineRule="auto" w:before="120" w:after="40"/>'
            f'<w:pBdr><w:bottom w:val="single" w:sz="14" w:space="8" w:color="0284C7"/></w:pBdr>'
            f'</w:pPr>'
            f'<w:r><w:rPr><w:b/><w:sz w:val="40"/><w:color w:val="002060"/><w:rFonts w:ascii="Segoe UI" w:hAnsi="Segoe UI"/></w:rPr>'
            f'<w:t xml:space="preserve">{saxutils.escape(title)}  </w:t></w:r>'
            f'<w:r><w:rPr><w:b/><w:sz w:val="20"/><w:color w:val="BA141A"/><w:rFonts w:ascii="Segoe UI" w:hAnsi="Segoe UI"/></w:rPr>'
            f'<w:t xml:space="preserve">[{saxutils.escape(tag)}]</w:t></w:r>'
            f'</w:p>'
        )
        if subtitle:
            xml.append(p(subtitle, size=22, color="64748B", space_before=20, space_after=120, italic=True))
        return "".join(xml)

    def slide_break():
        return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'

    def table_grid(headers, rows):
        xml = ['<w:tbl>',
               '<w:tblPr><w:tblW w:w="15000" w:type="dxa"/><w:jc w:val="center"/>',
               '<w:tblBorders>',
               '<w:top w:val="single" w:sz="8" w:space="0" w:color="002060"/>',
               '<w:left w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>',
               '<w:bottom w:val="single" w:sz="8" w:space="0" w:color="002060"/>',
               '<w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>',
               '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>',
               '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>',
               '</w:tblBorders></w:tblPr>']
        
        xml.append('<w:tr><w:trPr><w:tblHeader/></w:trPr>')
        for h in headers:
            xml.append(f'<w:tc><w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="002060"/></w:tcPr>{p(h, align="center", bold=True, size=22, color="FFFFFF", space_before=60, space_after=60)}</w:tc>')
        xml.append('</w:tr>')
        
        for r_idx, row in enumerate(rows):
            fill = 'FFFFFF' if r_idx % 2 == 0 else 'F8FAFC'
            xml.append('<w:tr>')
            for cell in row:
                xml.append(f'<w:tc><w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="{fill}"/></w:tcPr>{p(cell, align="left", size=20, color="1E293B", space_before=40, space_after=40, line_spacing="240")}</w:tc>')
            xml.append('</w:tr>')
        xml.append('</w:tbl>')
        return "".join(xml)

    def code_box(lines):
        xml = []
        for l in lines:
            xml.append(
                f'<w:p>'
                f'<w:pPr><w:jc w:val="left"/><w:spacing w:line="220" w:lineRule="auto" w:before="10" w:after="10"/>'
                f'<w:shd w:val="clear" w:color="auto" w:fill="0F172A"/>'
                f'<w:pBdr><w:left w:val="single" w:sz="18" w:space="8" w:color="0284C7"/></w:pBdr>'
                f'</w:pPr>'
                f'<w:r><w:rPr><w:sz w:val="18"/><w:color w:val="38BDF8"/><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/></w:rPr>'
                f'<w:t xml:space="preserve">{saxutils.escape(l)}</w:t></w:r>'
                f'</w:p>'
            )
        xml.append(p("", space_after=40))
        return "".join(xml)

    def bullet(text, bold_prefix="", indent=300):
        return (
            f'<w:p>'
            f'<w:pPr><w:ind w:left="{indent}"/><w:spacing w:line="280" w:lineRule="auto" w:before="40" w:after="40"/></w:pPr>'
            f'<w:r><w:rPr><w:b/><w:sz w:val="22"/><w:color w:val="0284C7"/><w:rFonts w:ascii="Segoe UI" w:hAnsi="Segoe UI"/></w:rPr><w:t>• </w:t></w:r>'
            f'<w:r><w:rPr><w:b/><w:sz w:val="22"/><w:color w:val="002060"/><w:rFonts w:ascii="Segoe UI" w:hAnsi="Segoe UI"/></w:rPr><w:t xml:space="preserve">{saxutils.escape(bold_prefix)} </w:t></w:r>'
            f'<w:r><w:rPr><w:sz w:val="22"/><w:color w:val="334155"/><w:rFonts w:ascii="Segoe UI" w:hAnsi="Segoe UI"/></w:rPr><w:t xml:space="preserve">{saxutils.escape(text)}</w:t></w:r>'
            f'</w:p>'
        )

    # ========================== SLIDE 1 ==========================
    body.append(p("TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN VÀ TRUYỀN THÔNG VIỆT – HÀN (VKU)", align="center", bold=True, size=24, color="BA141A", space_before=500, space_after=100))
    body.append(p("KHOA KHOA HỌC MÁY TÍNH - BỘ MÔN HỆ THỐNG THÔNG TIN & MẠNG", align="center", size=20, color="64748B", space_after=400))
    body.append(p("BÁO CÁO TIẾN ĐỘ ĐỒ ÁN MÔN HỌC", align="center", bold=True, size=32, color="002060", space_after=100))
    body.append(p("CONFIGURE AND DEPLOY MLOPS SERVICES ON ARCH LINUX & UBUNTU", align="center", bold=True, size=40, color="BA141A", space_after=300))
    body.append(p("Nghiên cứu đối kháng, xây dựng hạ tầng Rootless Containerization và Zero-Trust Network", align="center", italic=True, size=24, color="334155", space_after=600))
    
    body.append(p("Giảng viên hướng dẫn: TS. Hoàng Hữu Đức", align="center", bold=True, size=24, color="002060", space_after=100))
    body.append(p("Nhóm sinh viên thực hiện: Nguyễn Công Đức (Lead - Arch Linux) | Nguyễn Tùng Dương (Ubuntu Infra) | Nguyễn Văn C (Monitor & Benchmark)", align="center", size=22, color="1E293B", space_after=200))
    body.append(slide_break())

    # ========================== SLIDE 2 ==========================
    body.append(slide_header("1. TỔNG QUAN & BỐI CẢNH ĐỀ TÀI", "Thách thức phân phối phần mềm Linux và rủi ro an ninh Container", "OVERVIEW"))
    body.append(p("Bối cảnh thực tiễn và tính cấp thiết của đề tài:", bold=True, size=24, color="002060", space_after=80))
    body.append(bullet("Arch Linux (Rolling Release, Kernel mới nhất 6.x/7.x, tối giản ~400MB RAM) vs. Ubuntu Server (LTS 5 năm ổn định nhưng nặng nề ~750MB RAM).", "1. Hai thái cực phân phối Linux:"))
    body.append(bullet("Docker mặc định chạy daemon bằng quyền root (UID 0); nếu vi dịch vụ bị RCE, hacker có thể leo thang Container Escape chiếm trọn máy chủ vật lý (CVE-2019-5736).", "2. Rủi ro an ninh Container:"))
    body.append(bullet("Mở cổng cơ sở dữ liệu (5432) ra host IP (0.0.0.0) tạo điều kiện cho botnet quét mạng và đánh cắp dữ liệu mô hình học máy.", "3. Thiếu phân đoạn mạng Zero-Trust:"))
    body.append(bullet("Triển khai Rootless Docker unprivileged (không dùng root) kết hợp mạng nội bộ Zero-Trust và tự động hóa 100% bằng Bash script.", "4. Giải pháp đột phá của nhóm:"))
    body.append(slide_break())

    # ========================== SLIDE 3 ==========================
    body.append(slide_header("2. MỤC TIÊU NGHIÊN CỨU (SMART GOALS)", "6 mục tiêu kỹ thuật then chốt cam kết hoàn thành trong đồ án", "OBJECTIVES"))
    headers_s3 = ["Mục tiêu kỹ thuật SMART", "Giải pháp kiến trúc", "Chỉ số nghiệm thu cam kết"]
    rows_s3 = [
        ["1. Tự động hóa hạ tầng (IaC)", "Bộ Bash script chuẩn hóa tính Idempotent.", "100% tự động; có script Rollback an toàn."],
        ["2. Hardening Host OS", "Đổi SSH 2222, cấm root, tường lửa stateful.", "nftables rate limit 4/phút; drop invalid."],
        ["3. Rootless Container Engine", "User Namespaces subuid 100000:65536.", "dockerd chạy dưới user mlops (UID 1003)."],
        ["4. Mạng Zero-Trust Network", "Mạng Docker compose internal: true.", "CSDL PostgreSQL 5432 vô hình với mạng ngoài."],
        ["5. Vi dịch vụ AI & CLI", "FastAPI + Tesseract OCR Non-root 10001.", "Suy luận siêu nhẹ 200ms; menu ANSI ai_cli.sh."],
        ["6. Benchmark đối kháng", "Load test đo RPS, độ trễ và dung lượng RAM.", "Số liệu thực nghiệm so sánh Arch vs. Ubuntu."]
    ]
    body.append(table_grid(headers_s3, rows_s3))
    body.append(slide_break())

    # ========================== SLIDE 4 ==========================
    body.append(slide_header("3. KIẾN TRÚC PHÂN TẦNG DUAL-NODE MLOPS", "Mô hình tổng thể phân tách an ninh đa tầng trên Arch Linux và Ubuntu", "ARCHITECTURE"))
    body.append(p("Sơ đồ luồng phân tầng xử lý và cô lập an ninh:", bold=True, size=24, color="002060", space_after=80))
    code_s4 = [
        "[INTERNET ACCESS]  --->  SSH: 2222  |  FastAPI API: 8080  |  MLflow UI: 5000  |  Grafana: 3000",
        "                                  |",
        "                                  v",
        "[TẦNG TƯỜNG LỬA HOST]  nftables (Arch Linux) / UFW (Ubuntu Server) -> Stateful Meter (4/phút)",
        "                                  |",
        "                                  v",
        "[TẦNG HỆ ĐIỀU HÀNH]    Kernel Sysctl Tuning (somaxconn=65535, tcp_tw_reuse=1, file-max=2M)",
        "                                  |",
        "                                  v",
        "[TẦNG ROOTLESS ENGINE] User Namespace: mlops (UID 1003) -> subuid 100000:65536 (Non-Root)",
        "                                  |",
        "                                  v",
        "[MẠNG DOCKER ZERO-TRUST]  mlops-frontend (Bridge: 8080, 5000, 3000)  <-->  mlops-backend (Internal: true)",
        "                                                                            |",
        "                                                  [PostgreSQL: 5432 & MinIO S3 API: 9000 HIDDEN!]"
    ]
    body.append(code_box(code_s4))
    body.append(bullet("Mỗi tầng đóng vai trò là một chốt chặn độc lập (Defense in Depth), ngăn chặn xâm nhập lan rộng.", "Ý nghĩa kiến trúc:"))
    body.append(slide_break())

    # ========================== SLIDE 5 ==========================
    body.append(slide_header("4. ĐỘT PHÁ AN NINH: ROOTLESS DOCKER ENGINE", "Vận hành toàn bộ container dưới quyền tài khoản unprivileged (Non-Root)", "SECURITY"))
    body.append(p("Nguyên lý hoạt động và kiểm chứng thực nghiệm Container Escape:", bold=True, size=24, color="002060", space_after=80))
    body.append(bullet("Tiến trình trong container tưởng mình là UID 0 (root ảo), nhưng nhân Linux máy chủ chỉ gán UID 1003 / 110000.", "1. User Namespaces Mapping:"))
    body.append(bullet("Cho phép phiên làm việc của user unprivileged tự điều phối hạn mức CPU/RAM mà không cần gõ sudo.", "2. cgroups v2 Delegation:"))
    body.append(bullet("Kích hoạt loginctl enable-linger mlops giúp các container duy trì chạy nền liên tục 24/7 sau khi logout.", "3. Systemd Lingering:"))
    
    code_s5 = [
        "[KIỂM CHỨNG TẤN CÔNG CONTAINER ESCAPE KHI CHẠY ROOTLESS DOCKER TRÊN ARCH LINUX]:",
        "$ docker run --rm -v /:/host alpine touch /host/etc/exploit_test",
        "-> touch: /host/etc/exploit_test: Permission denied",
        "==> KẾT QUẢ: Hạt nhân Linux chặn đứng 100% ý đồ phá hoại hệ thống tệp của máy chủ host!"
    ]
    body.append(code_box(code_s5))
    body.append(slide_break())

    # ========================== SLIDE 6 ==========================
    body.append(slide_header("5. PHÂN ĐOẠN MẠNG ZERO-TRUST NETWORK", "Bảo vệ tuyệt đối cơ sở dữ liệu PostgreSQL và kho Artifacts MinIO", "ZERO-TRUST"))
    body.append(p("Cơ chế phân tách 2 mạng Docker trong docker-compose.yml:", bold=True, size=24, color="002060", space_after=80))
    body.append(bullet("Chỉ mở các cổng giao tiếp API và Web UI cần thiết ra host (8080, 5000, 3000, 9090).", "1. Mạng mlops-frontend (Bridge):"))
    body.append(bullet("Cấu hình internal: true. Ngắt hoàn toàn cổng Gateway ra ngoài; PostgreSQL 15 (5432) và MinIO API (9000) không bind IP ra máy chủ.", "2. Mạng mlops-backend (Internal):"))
    body.append(bullet("Container MLflow tham gia cả 2 mạng, đóng vai trò cầu nối an toàn ghi dữ liệu vào CSDL qua DNS nội bộ postgres:5432.", "3. Cầu nối an toàn:"))

    code_s6 = [
        "[KIỂM CHỨNG TRUY CẬP TRÁI PHÉP TỪ BÊN NGOÀI BẰNG NETCAT]:",
        "$ nc -z -v -w 1 localhost 5432  -> Connection refused (CƠ SỞ DỮ LIỆU HOÀN TOÀN VÔ HÌNH!)",
        "$ nc -z -v -w 1 localhost 9000  -> Connection refused (MINIO S3 API HOÀN TOÀN VÔ HÌNH!)"
    ]
    body.append(code_box(code_s6))
    body.append(slide_break())

    # ========================== SLIDE 7 ==========================
    body.append(slide_header("6. GIA CỐ HOST OS & TƯỜNG LỬA STATEFUL NFTABLES", "Thiết lập pháo đài bảo vệ tầng hệ điều hành và tối ưu hóa hàng đợi mạng", "HARDENING"))
    headers_s7 = ["Hạng mục gia cố", "Cấu hình kỹ thuật triển khai", "Hiệu quả an ninh & vận hành"]
    rows_s7 = [
        ["OpenSSH Hardening", "Port 2222, PermitRootLogin no, MaxAuthTries 3.", "Loại bỏ 99% botnet quét cổng 22; triệt tiêu brute-force."],
        ["Tường lửa nftables", "Default drop INPUT, meter ssh-meter { limit 4/m }.", "Chặn đứng quét cổng; tự động drop IP gõ sai SSH >4 lần."],
        ["Kernel Sysctl Tuning", "net.core.somaxconn=65535, net.ipv4.tcp_tw_reuse=1.", "Chống nghẽn socket queue khi tải cao; tái sử dụng socket."],
        ["SYN Flood Protection", "net.ipv4.tcp_syncookies = 1, file-max = 2097152.", "Bảo vệ máy chủ trước các đợt tấn công từ chối dịch vụ."],
        ["Kịch bản Rollback", "01_rollback_hardening.sh tự động hoàn nguyên.", "Khôi phục nguyên trạng OS chỉ trong 3 giây nếu có lỗi."]
    ]
    body.append(table_grid(headers_s7, rows_s7))
    body.append(slide_break())

    # ========================== SLIDE 8 ==========================
    body.append(slide_header("7. VI DỊCH VỤ AI OCR SERVING TỐI ƯU", "Đóng gói Dockerfile Multi-stage build và thực thi dưới quyền UID 10001", "MICROSERVICE"))
    body.append(p("Quy chuẩn đóng gói và vận hành vi dịch vụ AI nhận dạng chữ:", bold=True, size=24, color="002060", space_after=80))
    body.append(bullet("Tách riêng Stage 1 (Builder cài gcc/dev build wheel) và Stage 2 (Runtime sạch), loại bỏ compiler để giảm dung lượng và bề mặt tấn công.", "1. Dockerfile Multi-Stage:"))
    body.append(bullet("Chỉ thị USER 10001 (tài khoản mlopsuser). Ứng dụng không bao giờ chạy quyền root ngay cả bên trong container.", "2. Thực thi Non-root User:"))
    body.append(bullet("Tesseract-OCR (mạng nơ-ron hồi quy LSTM) siêu nhẹ, tiêu thụ ~60MB RAM, không phụ thuộc GPU/CUDA cồng kềnh.", "3. Động cơ nhận dạng chữ:"))
    body.append(bullet("Tốc độ suy luận chỉ mất ~200 - 300 ms/ảnh; bóc tách chính xác toàn bộ văn bản tiếng Việt và tiếng Anh.", "4. Hiệu năng phục vụ:"))
    body.append(slide_break())

    # ========================== SLIDE 9 ==========================
    body.append(slide_header("8. HỆ THỐNG QUAN SÁT & TERMINAL CLI", "Giám sát thời gian thực với Prometheus/Grafana và công cụ dòng lệnh", "OBSERVABILITY"))
    body.append(p("Hệ sinh thái công cụ hỗ trợ người quản trị và nhà phát triển:", bold=True, size=24, color="002060", space_after=80))
    body.append(bullet("Tự động cào chỉ số chuỗi thời gian mỗi 5s từ FastAPI (/metrics) và máy chủ host (Node Exporter 9100).", "1. Prometheus Server (Port 9090):"))
    body.append(bullet("Trực quan hóa tức thời thông lượng yêu cầu (RPS), độ trễ p50/p95/p99 và % sử dụng CPU/RAM.", "2. Grafana Dashboard (Port 3000):"))
    body.append(bullet("Quản lý vòng đời mô hình học máy, lưu vết siêu tham số và kết nối cơ sở dữ liệu PostgreSQL bền vững.", "3. MLflow Tracking UI (Port 5000):"))
    body.append(bullet("Giao diện menu ANSI Color ai_cli.sh cho phép quét ảnh trực tiếp trên màn hình dòng lệnh chuẩn Linux.", "4. Terminal Interactive CLI:"))
    body.append(slide_break())

    # ========================== SLIDE 10 ==========================
    body.append(slide_header("9. KẾT QUẢ ĐỐI SÁNH THỰC NGHIỆM ĐỊNH LƯỢNG", "Bảng so sánh số liệu đo lường trực tiếp giữa Arch Linux và Ubuntu Server", "BENCHMARK"))
    headers_s10 = ["Chỉ số đo lường hiệu năng", "Arch Linux (Rootless Docker)", "Ubuntu Server (Rootful Docker)", "Chênh lệch / Đánh giá"]
    rows_s10 = [
        ["Chiếm dụng RAM tĩnh (Idle OS)", "438 MB RAM", "742 MB RAM", "Arch Linux tiết kiệm 40.9% bộ nhớ."],
        ["Chiếm dụng RAM động (Stack Active)", "1,280 MB RAM", "1,620 MB RAM", "Arch Linux tiết kiệm 20.9% bộ nhớ."],
        ["Thời gian khởi động OS (Boot Time)", "4.8 giây (systemd-analyze)", "12.6 giây (systemd-analyze)", "Arch Linux khởi động nhanh hơn 2.6 lần."],
        ["Thông lượng xử lý AI (Throughput)", "342.5 Requests / Giây", "328.1 Requests / Giây", "Arch Linux đạt hiệu năng cao hơn 4.3%."],
        ["Độ trễ phân vị p95 (95% requests)", "64.8 ms", "72.5 ms", "Arch Linux duy trì độ trễ ổn định hơn."],
        ["Tỷ lệ lỗi (Error Rate)", "0.00% (500/500 thành công)", "0.00% (500/500 thành công)", "Độ tin cậy tuyệt đối 100%."],
        ["Kiểm định an ninh 04_verify", "5/5 Bài Test PASS", "5/5 Bài Test PASS", "Đạt chuẩn an ninh Enterprise cao nhất."]
    ]
    body.append(table_grid(headers_s10, rows_s10))
    body.append(slide_break())

    # ========================== SLIDE 11 ==========================
    body.append(slide_header("10. ĐÁNH GIÁ TIẾN ĐỘ & SẢN PHẨM BÀN GIAO", "Tổng kết kết quả thực hiện đề tài và các sản phẩm khoa học hoàn thành", "DELIVERABLES"))
    body.append(p("Các sản phẩm kỹ thuật và tài liệu đã bàn giao:", bold=True, size=24, color="002060", space_after=80))
    body.append(bullet("Đã cam kết và hoàn thành 100% cả 6 mục tiêu SMART đã đề ra ban đầu.", "1. Mức độ hoàn thành mục tiêu:"))
    body.append(bullet("Bộ kịch bản IaC Bash script đầy đủ: 01_system_hardening.sh, 01_rollback_hardening.sh, 02_setup_rootless_docker.sh, 03_deploy_stack.sh, 04_verify_system.sh, ai_cli.sh, scan_image.sh.", "2. Mã nguồn tự động hóa hạ tầng:"))
    body.append(bullet("Đã đồng bộ nhánh arch-mlops trên GitHub của nhóm.", "3. Kho lưu trữ Git chuẩn mực:"))
    body.append(bullet("Đã biên soạn hoàn chỉnh 7 chương, dày 82 trang chuẩn mẫu học thuật VKU (định dạng DOCX và PDF).", "4. Báo cáo đồ án chính thức:"))
    body.append(bullet("Cả 2 máy chủ ảo hoạt động ổn định và sẵn sàng cho buổi bảo vệ chính thức.", "5. Hệ sinh thái thực nghiệm:"))
    body.append(slide_break())

    # ========================== SLIDE 12 ==========================
    body.append(slide_header("11. HƯỚNG PHÁT TRIỂN & KẾT LUẬN", "Định hướng mở rộng kiến trúc trong tương lai và lời cảm ơn", "CONCLUSION"))
    body.append(p("Định hướng nâng cấp hệ thống trong các giai đoạn tiếp theo:", bold=True, size=24, color="002060", space_after=80))
    body.append(bullet("Nâng cấp kiến trúc từ máy chủ đơn lên cụm phân tán đa máy chủ sử dụng bản phân phối k3s unprivileged.", "1. Rootless k3s Cluster:"))
    body.append(bullet("Tích hợp Service Mesh Linkerd mã hóa toàn bộ lưu lượng giữa các vi dịch vụ bằng chứng chỉ số tự động xoay vòng.", "2. Mutual TLS (mTLS):"))
    body.append(bullet("Khai thác công nghệ eBPF để giám sát các lời gọi hệ thống (Syscalls) ở tầng kernel, phát hiện xâm nhập tức thì.", "3. Runtime Security với Falco:"))
    body.append(bullet("Tích hợp công cụ quét Trivy vào GitHub Actions để tự động kiểm định CVE trước khi đóng gói image.", "4. DevSecOps CI/CD Pipeline:"))
    
    body.append(p("LỜI CẢM ƠN", align="center", bold=True, size=28, color="BA141A", space_before=200, space_after=80))
    body.append(p("Nhóm tác giả xin chân thành cảm ơn TS. Hoàng Hữu Đức và quý Thầy Cô Hội đồng Khoa học máy tính VKU!", align="center", italic=True, size=22, color="1E293B", space_after=100))
    body.append(p("Q & A: KÍNH MỜI THẦY CÔ VÀ HỘI ĐỒNG ĐẶT CÂU HỎI CHẤT VẤN!", align="center", bold=True, size=24, color="002060", space_after=100))

    # Compile document XML
    doc_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:body>'
        + "".join(body) +
        '<w:sectPr>'
        '<w:pgSz w:w="16838" w:h="9500" w:orient="landscape"/>'
        '<w:pgMar w:top="720" w:right="720" w:bottom="720" w:left="720"/>'
        '</w:sectPr>'
        '</w:body>'
        '</w:document>'
    )

    types_xml = '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>'
    rels_xml = '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>'

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as docx:
        docx.writestr('[Content_Types].xml', types_xml)
        docx.writestr('_rels/.rels', rels_xml)
        docx.writestr('word/document.xml', doc_xml)
    print(f"[+] Đã tạo tệp slide DOCX tại: {output_path}")

if __name__ == "__main__":
    target = "/home/nguyencongduc/mlops-multi-os-pipeline/docs/SLIDE_BAO_CAO_TIEN_DO.docx"
    generate_slides_docx(target)
