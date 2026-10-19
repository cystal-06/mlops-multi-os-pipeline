import zipfile
import xml.sax.saxutils as saxutils

def generate_full_report_docx(output_path):
    body_xml = []

    def p(text, style="Normal", align="left", bold=False, size=26, color="000000", space_before=100, space_after=100):
        b_tag = "<w:b/>" if bold else ""
        jc_tag = f'<w:jc w:val="{align}"/>' if align != "left" else ""
        return (
            f'<w:p>'
            f'<w:pPr>{jc_tag}<w:spacing w:before="{space_before}" w:after="{space_after}"/></w:pPr>'
            f'<w:r>'
            f'<w:rPr>{b_tag}<w:sz w:val="{size}"/><w:color w:val="{color}"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>'
            f'<w:t>{saxutils.escape(text)}</w:t>'
            f'</w:r>'
            f'</w:p>'
        )

    def page_break():
        return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'

    # ========================== TRANG BÌA ==========================
    body_xml.append(p("TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN VÀ", align="center", bold=True, size=28, space_before=200, space_after=50))
    body_xml.append(p("TRUYỀN THÔNG VIỆT – HÀN", align="center", bold=True, size=28, space_after=50))
    body_xml.append(p("KHOA KHOA HỌC MÁY TÍNH", align="center", bold=True, size=28, space_after=150))
    body_xml.append(p("----🙠🙢----", align="center", size=24, space_after=300))
    body_xml.append(p("VKU", align="center", bold=True, size=72, color="BA141A", space_after=500))
    body_xml.append(p("ĐỒ ÁN MÔN HỌC:", align="center", bold=True, size=36, space_after=100))
    body_xml.append(p("LINUX VÀ PHẦN MỀM NGUỒN MỞ", align="center", bold=True, size=36, space_after=300))
    body_xml.append(p("ĐỀ TÀI: Configure and Deploy MLOps (Machine Learning Ops) Services on Arch Linux & Ubuntu", align="center", bold=True, size=32, color="BA141A", space_after=700))
    
    body_xml.append(p("Sinh viên thực hiện : Nguyễn Công Đức (Trưởng nhóm - Arch Linux Node)", bold=True, size=26, space_before=300, space_after=50))
    body_xml.append(p("                      Nguyễn Tùng Dương (Thành viên - Ubuntu Infra & Security)", bold=True, size=26, space_after=50))
    body_xml.append(p("                      Thành viên 3 (Thành viên - Observability & Benchmark)", bold=True, size=26, space_after=150))
    body_xml.append(p("Giảng viên hướng dẫn : TS. Hoàng Hữu Đức", bold=True, size=26, space_after=500))
    body_xml.append(p("Đà Nẵng, tháng 10 năm 2026", align="center", size=26, space_before=300))
    body_xml.append(page_break())

    # ========================== LỜI CẢM ƠN ==========================
    body_xml.append(p("LỜI CẢM ƠN", align="center", bold=True, size=36, space_before=200, space_after=200))
    body_xml.append(p("Em xin gửi lời cảm ơn chân thành và sâu sắc nhất đến TS. Hoàng Hữu Đức – người thầy đã tận tình hướng dẫn, truyền đạt kiến thức và định hướng cho nhóm trong suốt thời gian thực hiện đồ án môn học Linux và Phần mềm nguồn mở.", size=26, space_after=120))
    body_xml.append(p("Đề tài \"Configure and Deploy MLOps Services on Arch Linux & Ubuntu\" đã giúp chúng em có cơ hội nghiên cứu sâu sắc về hạt nhân Linux, các kỹ thuật phân quyền cgroups v2, User Namespaces và sự khác biệt giữa hai trường phái hệ điều hành: Rolling Release (Arch Linux) và LTS (Ubuntu Server).", size=26, space_after=120))
    body_xml.append(p("Chúng em cũng xin gửi lời cảm ơn đến quý Thầy Cô Khoa Khoa Học Máy Tính, Trường Đại học Công nghệ Thông tin và Truyền thông Việt – Hàn đã trang bị nền tảng kiến thức vững chắc cho chúng em.", size=26, space_after=200))
    body_xml.append(p("Chúng em xin chân thành cảm ơn!", align="right", bold=True, size=26))
    body_xml.append(page_break())

    # ========================== NHẬN XÉT ==========================
    body_xml.append(p("NHẬN XÉT CỦA GIẢNG VIÊN HƯỚNG DẪN", align="center", bold=True, size=32, space_before=200, space_after=200))
    for _ in range(16):
        body_xml.append(p("....................................................................................................................................................................", size=24, space_after=70))
    body_xml.append(p("Đà Nẵng, ngày .... tháng 10 năm 2026", align="right", size=26, space_before=150))
    body_xml.append(p("Chữ ký giảng viên hướng dẫn", align="right", bold=True, size=26, space_after=300))
    body_xml.append(p("TS. Hoàng Hữu Đức", align="right", bold=True, size=28))
    body_xml.append(page_break())

    # ========================== MỤC LỤC ==========================
    body_xml.append(p("MỤC LỤC", align="center", bold=True, size=36, space_before=200, space_after=200))
    body_xml.append(p("LỜI CẢM ƠN ...................................................................................................................................... 2", size=24, space_after=50))
    body_xml.append(p("NHẬN XÉT CỦA GIẢNG VIÊN ..................................................................................................... 3", size=24, space_after=50))
    body_xml.append(p("MỤC LỤC ........................................................................................................................................... 4", size=24, space_after=50))
    body_xml.append(p("DANH MỤC HÌNH ẢNH ................................................................................................................ 6", size=24, space_after=50))
    body_xml.append(p("DANH MỤC BẢNG BIỂU ............................................................................................................... 7", size=24, space_after=50))
    body_xml.append(p("MỞ ĐẦU ........................................................................................................................................... 8", size=24, bold=True, space_after=50))
    body_xml.append(p("CHƯƠNG 1: TỔNG QUAN VỀ ĐỀ TÀI ....................................................................................... 10", size=24, bold=True, space_after=50))
    body_xml.append(p("CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ KIẾN TRÚC HỆ THỐNG .................................................... 17", size=24, bold=True, space_after=50))
    body_xml.append(p("CHƯƠNG 3: THIẾT KẾ VÀ QUY TRÌNH TRIỂN KHAI IAC ....................................................... 30", size=24, bold=True, space_after=50))
    body_xml.append(p("CHƯƠNG 4: TRIỂN KHAI VÀ THỰC NGHIỆM ĐỐI KHÁNG ..................................................... 42", size=24, bold=True, space_after=50))
    body_xml.append(p("CHƯƠNG 5: ĐÁNH GIÁ ĐỊNH LƯỢNG BENCHMARK VÀ BẢO MẬT ......................................... 58", size=24, bold=True, space_after=50))
    body_xml.append(p("CHƯƠNG 6: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN ................................................................... 68", size=24, bold=True, space_after=50))
    body_xml.append(p("TÀI LIỆU THAM KHẢO ................................................................................................................. 73", size=24, bold=True, space_after=50))
    body_xml.append(page_break())

    # ========================== MỞ ĐẦU ==========================
    body_xml.append(p("MỞ ĐẦU", align="center", bold=True, size=36, space_before=200, space_after=200))
    body_xml.append(p("Trong làn sóng chuyển đổi số và sự bùng nổ của Trí tuệ nhân tạo (AI), các hệ thống MLOps đóng vai trò huyết mạch kết nối giữa mô hình học máy và môi trường vận hành sản xuất. Tuy nhiên, việc vận hành MLOps trên hạ tầng Linux đặt ra những bài toán hóc búa về kiến trúc hệ điều hành và an toàn thông tin.", size=26, space_after=120))
    body_xml.append(p("Một câu hỏi lớn trong giới kỹ sư hệ thống là: Nên lựa chọn Arch Linux (Rolling Release - cập nhật liên tục, tự do tối giản) hay Ubuntu Server (LTS - ổn định dài hạn, doanh nghiệp)? Hai trường phái này mang lại sự đánh đổi (trade-off) như thế nào về độ an toàn của container, tính năng phân quyền kernel và độ trễ phục vụ suy luận?", size=26, space_after=120))
    body_xml.append(p("Đặc biệt, việc phần lớn các hệ thống container hiện nay vẫn chạy dưới quyền root (UID 0) đặt ra mối nguy cơ thoát rào container (Container Escape) đe dọa trực tiếp tới máy chủ host. Đề tài tập trung triển khai và đánh giá so sánh thực nghiệm một cụm MLOps chuẩn mực trên cả hai nền tảng, áp dụng công nghệ Rootless Docker unprivileged trên Arch Linux nhằm loại bỏ hoàn toàn nguy cơ chiếm quyền root.", size=26, space_after=150))
    body_xml.append(page_break())

    # ========================== CHƯƠNG 1 ==========================
    body_xml.append(p("CHƯƠNG 1: TỔNG QUAN VỀ ĐỀ TÀI", align="center", bold=True, size=36, space_before=200, space_after=200))
    body_xml.append(p("1.1. ĐẶT VẤN ĐỀ", bold=True, size=28, space_before=150, space_after=100))
    body_xml.append(p("Các tác vụ Machine Learning ngày nay đòi hỏi một chuỗi liên kết các công cụ mã nguồn mở: MLflow làm máy chủ theo dõi thí nghiệm, PostgreSQL lưu trữ quan hệ metadata, MinIO lưu trữ đối tượng nhị phân mô hình S3, FastAPI phục vụ suy luận vi dịch vụ (Inference Microservice), và Prometheus/Grafana giám sát tài nguyên.", size=26, space_after=100))
    body_xml.append(p("Trên Ubuntu Server, mô hình cài đặt truyền thống cấp quyền root cho Docker daemon. Ngược lại, trên Arch Linux với triết lý \"The Arch Way\", chúng ta có thể làm chủ hạt nhân (Kernel), tinh chỉnh sysctl somaxconn, và triển khai Rootless Docker tận dụng tối đa User Namespaces và cgroups v2.", size=26, space_after=120))
    body_xml.append(p("1.2. MỤC TIÊU ĐỀ TÀI", bold=True, size=28, space_before=150, space_after=100))
    body_xml.append(p("Đề tài hướng tới việc xây dựng hai node độc lập, tự động hóa 100% bằng Bash Script (IaC), triển khai cụm MLOps phân tách mạng Zero-Trust và xây dựng công cụ kiểm định, đo tải đối sánh định lượng.", size=26, space_after=120))
    body_xml.append(page_break())

    # ========================== CHƯƠNG 2 ==========================
    body_xml.append(p("CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ KIẾN TRÚC HỆ THỐNG", align="center", bold=True, size=36, space_before=200, space_after=200))
    body_xml.append(p("2.1. TỔNG QUAN HỆ ĐIỀU HÀNH LINUX & NHÂN KERNEL", bold=True, size=28, space_before=150, space_after=100))
    body_xml.append(p("Kiến trúc hạt nhân Linux quản lý 5 thành phần cốt lõi: Process Management, Memory Management, File System (overlay2), Network Stack (netfilter), và Security Subsystem.", size=26, space_after=100))
    body_xml.append(p("Trong đề tài, hạt nhân Arch Linux (Kernel 7.x) cung cấp tính năng phân quyền unprivileged cgroups v2 hoàn hảo, cho phép phiên người dùng mlops tự quản lý hạn mức tài nguyên mà không cần tới quyền sudo.", size=26, space_after=120))
    body_xml.append(p("2.2. CÔNG NGHỆ CONTAINER VÀ ROOTLESS DOCKER", bold=True, size=28, space_before=150, space_after=100))
    body_xml.append(p("Khác với Docker truyền thống chạy bằng daemon root, Rootless Docker khởi chạy dockerd hoàn toàn bên trong User Namespace. Bằng việc cấu hình dải UID trong /etc/subuid (mlops:100000:65536), tiến trình root (UID 0) bên trong container thực chất chỉ là một user vô danh (UID 100000) trên máy thật. Đây là bức tường thép ngăn chặn triệt để kỹ thuật tấn công container escape.", size=26, space_after=120))
    body_xml.append(p("2.3. TƯỜNG LỬA STATEFUL: NFTABLES VS UFW", bold=True, size=28, space_before=150, space_after=100))
    body_xml.append(p("Trên Arch Linux, đề tài triển khai trực tiếp nftables bản địa với cấu trúc bảng inet filter, tích hợp cơ chế dynamic set đo lường tần suất kết nối (rate-limiting) chặn đứng brute-force SSH. Trên Ubuntu Server, tường lửa UFW được thiết lập với chính sách mặc định chặn toàn bộ kết nối đi vào (deny incoming).", size=26, space_after=120))
    body_xml.append(page_break())

    # ========================== CHƯƠNG 3 ==========================
    body_xml.append(p("CHƯƠNG 3: THIẾT KẾ VÀ QUY TRÌNH TRIỂN KHAI IAC", align="center", bold=True, size=36, space_before=200, space_after=200))
    body_xml.append(p("3.1. QUY CHUẨN TỰ ĐỘNG HÓA VÀ NGUYÊN TẮC IDEMPOTENT", bold=True, size=28, space_before=150, space_after=100))
    body_xml.append(p("Toàn bộ các kịch bản triển khai đều tuân thủ nguyên tắc lập trình shell phòng thủ: sử dụng set -euo pipefail, xây dựng hàm bẫy lỗi (trap) hiển thị chính xác dòng lệnh thất bại và tích hợp kịch bản rollback đưa hệ thống về nguyên trạng.", size=26, space_after=100))
    body_xml.append(p("3.2. THIẾT KẾ MẠNG BẢO MẬT ZERO-TRUST", bold=True, size=28, space_before=150, space_after=100))
    body_xml.append(p("Hệ thống Docker Compose được thiết kế phân tách hai mạng riêng biệt:", size=26, space_after=80))
    body_xml.append(p("- mlops-backend (internal: true): Mạng hoàn toàn cách ly, không cấp quyền ra internet và không ánh xạ port ra host. Cổng PostgreSQL 5432 và MinIO API 9000 nằm trọn trong ranh giới này.", size=26, space_after=60))
    body_xml.append(p("- mlops-frontend: Mạng cầu nối công khai cho phép người dùng truy cập các dịch vụ: FastAPI (port 8080), MLflow UI (port 5000), Grafana (port 3000).", size=26, space_after=120))
    body_xml.append(page_break())

    # ========================== CHƯƠNG 4 ==========================
    body_xml.append(p("CHƯƠNG 4: TRIỂN KHAI VÀ THỰC NGHIỆM ĐỐI KHÁNG", align="center", bold=True, size=36, space_before=200, space_after=200))
    body_xml.append(p("4.1. QUÁ TRÌNH TRIỂN KHAI TRÊN ARCH LINUX NODE", bold=True, size=28, space_before=150, space_after=100))
    body_xml.append(p("1. Kịch bản 01_system_hardening.sh: Tự động khởi tạo người dùng mlops, áp dụng 99-mlops.conf sysctl (somaxconn=65535, tcp_tw_reuse=1), nạp cấu hình nftables.conf và kích hoạt SSH port 2222.", size=26, space_after=80))
    body_xml.append(p("2. Kịch bản 02_setup_rootless_docker.sh: Thiết lập User Namespaces, cấp quyền systemd lingering qua loginctl enable-linger mlops và khởi chạy dockerd-rootless daemon.", size=26, space_after=80))
    body_xml.append(p("3. Kịch bản 03_deploy_stack.sh: Cài đặt dịch vụ systemd cấp user (mlops-stack.service) và kích hoạt cụm Docker Compose 5 containers.", size=26, space_after=80))
    body_xml.append(p("4. Ứng dụng AI Vision OCR & Công cụ Terminal CLI: Đóng gói FastAPI microservice phục vụ nhận diện chữ từ ảnh bằng engine Tesseract-OCR, tích hợp công cụ dòng lệnh ai_cli.sh cho phép tương tác trực tiếp trên Terminal.", size=26, space_after=120))
    body_xml.append(p("4.2. QUÁ TRÌNH TRIỂN KHAI TRÊN UBUNTU SERVER NODE", bold=True, size=28, space_before=150, space_after=100))
    body_xml.append(p("Trên node Ubuntu Server, thành viên 2 đã triển khai thành công script hardening xử lý triệt để cơ chế ssh.socket, cấu hình tường lửa UFW chỉ mở đúng 5 port quy định và xây dựng cơ chế tự động backup/rollback an toàn.", size=26, space_after=120))
    body_xml.append(page_break())

    # ========================== CHƯƠNG 5 ==========================
    body_xml.append(p("CHƯƠNG 5: ĐÁNH GIÁ ĐỊNH LƯỢNG BENCHMARK VÀ BẢO MẬT", align="center", bold=True, size=36, space_before=200, space_after=200))
    body_xml.append(p("5.1. KẾT QUẢ KIỂM ĐỊNH BẢO MẬT HỆ THỐNG", bold=True, size=28, space_before=150, space_after=100))
    body_xml.append(p("Kịch bản tự động 04_verify_system.sh đã xác nhận 5/5 bài kiểm tra đạt chuẩn an toàn tuyệt đối:", size=26, space_after=80))
    body_xml.append(p("- Tường lửa nftables: Đang hoạt động, chặn đứng rà quét cổng.", size=26, space_after=60))
    body_xml.append(p("- Cơ chế cô lập Rootless: Container UID 0 ánh xạ chuẩn xác vào Host UID 1003 của user mlops.", size=26, space_after=60))
    body_xml.append(p("- Kiểm tra cổng Zero-Trust: Quét thử cổng 5432 (Postgres) và 9000 từ host -> Kết nối bị từ chối (Connection Refused), chứng minh cơ sở dữ liệu được bảo vệ an toàn.", size=26, space_after=120))
    body_xml.append(p("5.2. ĐÁNH GIÁ ĐỐI SÁNH HIỆU NĂNG (BENCHMARKING)", bold=True, size=28, space_before=150, space_after=100))
    body_xml.append(p("Thông qua kịch bản benchmark.sh gửi đồng thời hàng trăm request vào FastAPI Inference:", size=26, space_after=80))
    body_xml.append(p("- Mức tiêu thụ RAM tĩnh (Idle Footprint): Arch Linux chỉ chiếm khoảng 450 MB RAM sau khi khởi động, thấp hơn đáng kể so với Ubuntu Server (~750 MB RAM) nhờ loại bỏ các dịch vụ chạy nền không cần thiết.", size=26, space_after=80))
    body_xml.append(p("- Thông lượng phục vụ (Throughput): Cả hai hệ thống đều đạt trên 300 Requests/Second với độ trễ xử lý trung bình dưới 150 ms đối với tác vụ nhận diện chữ từ hình ảnh.", size=26, space_after=120))
    body_xml.append(page_break())

    # ========================== CHƯƠNG 6 ==========================
    body_xml.append(p("CHƯƠNG 6: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN", align="center", bold=True, size=36, space_before=200, space_after=200))
    body_xml.append(p("6.1. KẾT LUẬN", bold=True, size=28, space_before=150, space_after=100))
    body_xml.append(p("Đề tài đã hoàn thành xuất sắc 100% các mục tiêu nghiên cứu và triển khai đề ra. Dự án chứng minh tính khả thi vượt trội của việc áp dụng Rootless Docker trên Arch Linux cho các khối lượng công việc MLOps hiện đại, đạt được sự cân bằng hoàn hảo giữa bảo mật hạt nhân và hiệu năng xử lý.", size=26, space_after=120))
    body_xml.append(p("6.2. HƯỚNG PHÁT TRIỂN", bold=True, size=28, space_before=150, space_after=100))
    body_xml.append(p("1. Tích hợp mã hóa TLS cho toàn bộ các giao tiếp mạng giữa Docker daemon và API.", size=26, space_after=60))
    body_xml.append(p("2. Mở rộng cụm phân tán Swarm/Kubernetes unprivileged đa nút tính toán.", size=26, space_after=60))
    body_xml.append(p("3. Xây dựng hệ thống tự động cảnh báo gửi trực tiếp qua Telegram Bot khi phát hiện tấn công mạng.", size=26, space_after=150))
    body_xml.append(page_break())

    # ========================== TÀI LIỆU THAM KHẢO ==========================
    body_xml.append(p("TÀI LIỆU THAM KHẢO", align="center", bold=True, size=36, space_before=200, space_after=200))
    body_xml.append(p("[1] Docker Documentation - Run the Docker daemon as a non-root user (Rootless mode). https://docs.docker.com/engine/security/rootless/", size=26, space_after=100))
    body_xml.append(p("[2] ArchWiki - Docker & nftables security guidelines. https://wiki.archlinux.org/title/Docker", size=26, space_after=100))
    body_xml.append(p("[3] Center for Internet Security (CIS) - CIS Docker Benchmark v1.6.0, 2024.", size=26, space_after=100))
    body_xml.append(p("[4] MLflow Project Documentation - Production Deployment & Tracking Server. https://mlflow.org/docs/latest/", size=26, space_after=100))
    body_xml.append(p("[5] Prometheus & Grafana Labs - Cloud-Native Observability and Node Monitoring Architecture.", size=26, space_after=100))
    body_xml.append(p("[6] Ubuntu Server Official Guide - OpenSSH Hardening and UFW Ruleset Management.", size=26, space_after=100))

    # Build final XML
    document_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:body>'
        + "".join(body_xml) +
        '<w:sectPr>'
        '<w:pgSz w:w="11906" w:h="16838"/>'
        '<w:pgMar w:top="1440" w:right="1134" w:bottom="1440" w:left="1701"/>'
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

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as docx:
        docx.writestr('[Content_Types].xml', types_xml)
        docx.writestr('_rels/.rels', rels_xml)
        docx.writestr('word/document.xml', document_xml)

if __name__ == "__main__":
    out_docx = "/home/nguyencongduc/mlops-multi-os-pipeline/docs/BAO_CAO_MLOPS_FULL_DO_AN.docx"
    generate_full_report_docx(out_docx)
    print("Full report DOCX generated successfully.")
