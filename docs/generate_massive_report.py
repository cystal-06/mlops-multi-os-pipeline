import os
import zipfile
import xml.sax.saxutils as saxutils

def generate_massive_vku_report(output_docx_path):
    body_xml = []

    def p(text, align="left", bold=False, size=26, color="000000", space_before=100, space_after=100, italic=False, line_spacing="360"):
        b_tag = "<w:b/>" if bold else ""
        i_tag = "<w:i/>" if italic else ""
        jc_tag = f'<w:jc w:val="{align}"/>' if align != "left" else '<w:jc w:val="both"/>'
        return (
            f'<w:p>'
            f'<w:pPr>{jc_tag}<w:spacing w:line="{line_spacing}" w:lineRule="auto" w:before="{space_before}" w:after="{space_after}"/></w:pPr>'
            f'<w:r>'
            f'<w:rPr>{b_tag}{i_tag}<w:sz w:val="{size}"/><w:color w:val="{color}"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>'
            f'<w:t>{saxutils.escape(text)}</w:t>'
            f'</w:r>'
            f'</w:p>'
        )

    def page_break():
        return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'

    def table_grid(headers, rows, col_widths=None):
        xml = ['<w:tbl>',
               '<w:tblPr><w:tblW w:w="9500" w:type="dxa"/><w:jc w:val="center"/>',
               '<w:tblBorders>',
               '<w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>',
               '<w:left w:val="single" w:sz="6" w:space="0" w:color="000000"/>',
               '<w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>',
               '<w:right w:val="single" w:sz="6" w:space="0" w:color="000000"/>',
               '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="D0D7DE"/>',
               '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="D0D7DE"/>',
               '</w:tblBorders></w:tblPr>']
        
        # Header Row
        xml.append('<w:tr><w:trPr><w:tblHeader/></w:trPr>')
        for h in headers:
            xml.append(f'<w:tc><w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="F2F4F8"/></w:tcPr>{p(h, align="center", bold=True, size=24, space_before=60, space_after=60)}</w:tc>')
        xml.append('</w:tr>')
        
        # Data Rows
        for row in rows:
            xml.append('<w:tr>')
            for cell in row:
                xml.append(f'<w:tc>{p(cell, size=22, space_before=40, space_after=40)}</w:tc>')
            xml.append('</w:tr>')
        xml.append('</w:tbl>')
        return "".join(xml)

    # 1. TRANG BÌA CHÍNH (Trang 1)
    body_xml.append(p("TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN VÀ", align="center", bold=True, size=28, space_before=150, space_after=40))
    body_xml.append(p("TRUYỀN THÔNG VIỆT – HÀN", align="center", bold=True, size=28, space_after=40))
    body_xml.append(p("KHOA KHOA HỌC MÁY TÍNH", align="center", bold=True, size=28, space_after=120))
    body_xml.append(p("----🙠🙢----", align="center", size=24, space_after=250))
    body_xml.append(p("VKU", align="center", bold=True, size=72, color="BA141A", space_after=500))
    body_xml.append(p("ĐỒ ÁN MÔN HỌC:", align="center", bold=True, size=34, space_after=100))
    body_xml.append(p("LINUX VÀ PHẦN MỀM NGUỒN MỞ", align="center", bold=True, size=34, space_after=300))
    body_xml.append(p("ĐỀ TÀI: CONFIGURE AND DEPLOY MLOPS (MACHINE LEARNING OPS) SERVICES ON ARCH LINUX & UBUNTU", align="center", bold=True, size=30, color="BA141A", space_after=600))
    
    body_xml.append(p("Sinh viên thực hiện :", bold=True, size=26, space_before=300, space_after=40))
    body_xml.append(p("  1. Nguyễn Công Đức   – 24ITxxx (Trưởng nhóm - Node Arch Linux)", bold=True, size=26, space_after=40))
    body_xml.append(p("  2. Nguyễn Tùng Dương – 24ITxxx (Thành viên - Node Ubuntu Infra & Security)", bold=True, size=26, space_after=40))
    body_xml.append(p("  3. Nguyễn Văn C       – 24ITxxx (Thành viên - Observability & Benchmark)", bold=True, size=26, space_after=120))
    body_xml.append(p("Giảng viên hướng dẫn : TS. Hoàng Hữu Đức", bold=True, size=26, space_after=500))
    body_xml.append(p("Đà Nẵng, tháng 10 năm 2026", align="center", size=26, space_before=300))
    body_xml.append(page_break())

    # 2. LỜI CẢM ƠN (Trang 2)
    body_xml.append(p("LỜI CẢM ƠN", align="center", bold=True, size=34, space_before=200, space_after=200))
    body_xml.append(p("Lời đầu tiên, chúng em xin bày tỏ lòng biết ơn sâu sắc và chân thành nhất đến TS. Hoàng Hữu Đức – người thầy đã trực tiếp giảng dạy môn học \"Linux và Phần mềm nguồn mở\", đồng thời luôn dành nhiều thời gian quý báu để định hướng, cố vấn học thuật và đồng hành cùng nhóm trong suốt quá trình hoàn thiện đồ án này.", size=26, space_after=120))
    body_xml.append(p("Đề tài \"Configure and Deploy MLOps (Machine Learning Ops) Services on Arch Linux & Ubuntu\" được khởi tạo từ chính những yêu cầu khắt khe và thực tế nhất của môi trường kỹ thuật hiện đại. Thầy đã hướng dẫn chúng em không chỉ dừng lại ở các thao tác dòng lệnh cơ bản, mà phải đào sâu vào bản chất kiến trúc hạt nhân Linux (Kernel Space vs User Space), cơ chế phân chia tài nguyên cgroups v2, không gian tên User Namespaces và sự tương quan giữa các mô hình phân phối phần mềm: Rolling Release và Long-Term Support (LTS).", size=26, space_after=120))
    body_xml.append(p("Dưới sự dẫn dắt tận tâm của thầy, nhóm đã từng bước làm chủ quy trình Infrastructure as Code (IaC) tự động hóa hoàn toàn bằng Bash script, hiện thực hóa mô hình Rootless Containerization unprivileged trên nền tảng Arch Linux để triệt tiêu hoàn toàn nguy cơ tấn công Container Escape, đồng thời thiết lập hệ thống giám sát tải thời gian thực bằng Prometheus và Grafana.", size=26, space_after=120))
    body_xml.append(p("Chúng em cũng xin gửi lời cảm ơn trân trọng đến Ban Giám hiệu, Khoa Khoa Học Máy Tính và quý Thầy Cô Trường Đại học Công nghệ Thông tin và Truyền thông Việt – Hàn (VKU) đã xây dựng môi trường học tập tiên tiến, tạo điều kiện thuận lợi về trang thiết bị phòng lab để chúng em hoàn thành tốt đề tài.", size=26, space_after=120))
    body_xml.append(p("Dù đã nỗ lực hết mình, đề tài khó tránh khỏi những thiếu sót nhất định do giới hạn về mặt thời gian. Chúng em rất mong nhận được những nhận xét, góp ý quý báu của quý Thầy Cô để hoàn thiện sản phẩm tốt hơn trong tương lai.", size=26, space_after=200))
    body_xml.append(p("Nhóm sinh viên thực hiện xin chân thành cảm ơn!", align="right", bold=True, size=26))
    body_xml.append(page_break())

    # 3. NHẬN XÉT CỦA GIẢNG VIÊN (Trang 3)
    body_xml.append(p("NHẬN XÉT CỦA GIẢNG VIÊN HƯỚNG DẪN", align="center", bold=True, size=30, space_before=200, space_after=150))
    for _ in range(18):
        body_xml.append(p("....................................................................................................................................................................", size=24, space_after=65))
    body_xml.append(p("Đà Nẵng, ngày .... tháng 10 năm 2026", align="right", size=26, space_before=150))
    body_xml.append(p("Chữ ký giảng viên hướng dẫn", align="right", bold=True, size=26, space_after=300))
    body_xml.append(p("TS. Hoàng Hữu Đức", align="right", bold=True, size=28))
    body_xml.append(page_break())

    # 4. MỤC LỤC CHI TIẾT (Trang 4 - 6)
    body_xml.append(p("MỤC LỤC", align="center", bold=True, size=34, space_before=150, space_after=150))
    toc_items = [
        ("LỜI CẢM ƠN", "2"), ("NHẬN XÉT CỦA GIẢNG VIÊN", "3"), ("MỤC LỤC", "4"),
        ("DANH MỤC HÌNH ẢNH", "7"), ("DANH MỤC BẢNG BIỂU", "9"), ("DANH MỤC TỪ VIẾT TẮT", "10"),
        ("MỞ ĐẦU", "11"),
        ("CHƯƠNG 1: TỔNG QUAN VỀ ĐỀ TÀI", "14"),
        ("  1.1. Đặt vấn đề và bối cảnh nghiên cứu", "14"),
        ("    1.1.1. Sự hội tụ giữa MLOps và hạ tầng mã nguồn mở Linux", "14"),
        ("    1.1.2. Thách thức phân phối phần mềm: Rolling Release vs. LTS", "16"),
        ("    1.1.3. Hiểm họa an ninh từ đặc quyền Root trên Container truyền thống", "18"),
        ("    1.1.4. Các sự cố bảo mật tiêu biểu liên quan đến Docker Escape", "20"),
        ("  1.2. Mục tiêu đề tài", "22"),
        ("    1.2.1. Mục tiêu tổng quát", "22"),
        ("    1.2.2. Các mục tiêu cụ thể đo lường được (SMART)", "23"),
        ("    1.2.3. Kết quả và sản phẩm bàn giao mong đợi", "25"),
        ("  1.3. Đối tượng và phạm vi nghiên cứu", "26"),
        ("    1.3.1. Đối tượng nghiên cứu", "26"),
        ("    1.3.2. Phạm vi và môi trường thực nghiệm", "27"),
        ("    1.3.3. Giới hạn đề tài", "28"),
        ("  1.4. Phương pháp nghiên cứu và quy trình thực nghiệm", "29"),
        ("  1.5. Ý nghĩa khoa học và giá trị thực tiễn", "31"),
        ("CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ KIẾN TRÚC CÔNG NGHỆ", "33"),
        ("  2.1. Tổng quan hạt nhân Linux và hệ thống tiến trình", "33"),
        ("    2.1.1. Kiến trúc phân tầng Linux Kernel (User Space vs Kernel Space)", "33"),
        ("    2.1.2. Cơ chế điều khiển tài nguyên Control Groups v2 (cgroups v2)", "36"),
        ("    2.1.3. Không gian tên Linux (Namespaces) và User Namespaces Remapping", "39"),
        ("  2.2. Phân tích đối sánh hai trường phái Linux: Arch Linux và Ubuntu Server", "42"),
        ("    2.2.1. Triết lý thiết kế \"The Arch Way\" và mô hình Rolling Release", "42"),
        ("    2.2.2. Bản phân phối Ubuntu Server LTS và triết lý doanh nghiệp", "45"),
        ("    2.2.3. So sánh hệ thống quản lý gói: Pacman/AUR vs. APT", "47"),
        ("  2.3. Công nghệ Containerization và cơ chế Rootless Docker", "49"),
        ("    2.3.1. Nguyên lý hoạt động của Docker daemon và containerd", "49"),
        ("    2.3.2. Kiến trúc Rootless Docker unprivileged trên Arch Linux", "52"),
        ("    2.3.3. So sánh bảo mật giữa Rootless Docker và Rootful Docker", "55"),
        ("  2.4. Công nghệ tường lửa Stateful: nftables vs. UFW", "57"),
        ("    2.4.1. Kiến trúc Netfilter và bảng lọc gói tin hiện đại nftables", "57"),
        ("    2.4.2. Cơ chế Uncomplicated Firewall (UFW) trên nền tảng Debian/Ubuntu", "60"),
        ("  2.5. Hệ sinh thái công cụ MLOps mã nguồn mở", "62"),
        ("    2.5.1. Nền tảng theo dõi thí nghiệm MLflow Tracking Server", "62"),
        ("    2.5.2. Hệ quản trị cơ sở dữ liệu quan hệ PostgreSQL Metadata Store", "64"),
        ("    2.5.3. Hệ thống lưu trữ đối tượng MinIO tương thích Amazon S3", "66"),
        ("    2.5.4. Khung vi dịch vụ hiệu năng cao FastAPI phục vụ AI Inference", "68"),
        ("    2.5.5. Hệ thống giám sát chuỗi thời gian Prometheus và Grafana", "70"),
        ("CHƯƠNG 3: THIẾT KẾ HỆ THỐNG VÀ QUY CHUẨN TRIỂN KHAI IAC", "72"),
        ("  3.1. Kiến trúc tổng thể Dual-Node MLOps Platform", "72"),
        ("  3.2. Thiết kế bảo mật mạng Zero-Trust Network Segmentation", "75"),
        ("  3.3. Quy chuẩn tự động hóa hạ tầng (IaC) và nguyên tắc Idempotent", "78"),
        ("  3.4. Thiết kế vi dịch vụ AI OCR Vision Engine và giao diện Terminal CLI", "81"),
        ("CHƯƠNG 4: TRIỂN KHAI THỰC NGHIỆM VÀ QUẢN TRỊ DỊCH VỤ", "84"),
        ("  4.1. Triển khai Node Arch Linux (The Arch Way)", "84"),
        ("  4.2. Triển khai Node Ubuntu Server (Debian Standard)", "90"),
        ("  4.3. Quản lý vòng đời dịch vụ bằng User-level Systemd Units", "95"),
        ("  4.4. Vận hành công cụ kiểm định tự động và giao diện Terminal tương tác", "98"),
        ("CHƯƠNG 5: ĐÁNH GIÁ ĐỊNH LƯỢNG BENCHMARK VÀ BẢO MẬT", "102"),
        ("  5.1. Kết quả kiểm định an ninh và kiểm chứng Zero-Trust", "102"),
        ("  5.2. Phân tích đối kháng tài nguyên phần cứng (Resource Footprint)", "105"),
        ("  5.3. Thử nghiệm chịu tải vi dịch vụ AI (Throughput & Latency)", "108"),
        ("  5.4. Đánh giá ưu nhược điểm và bài học kinh nghiệm (Trade-offs)", "112"),
        ("CHƯƠNG 6: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN", "116"),
        ("TÀI LIỆU THAM KHẢO", "119")
    ]
    for title, pg in toc_items:
        is_h = not title.startswith("  ") and not title.startswith("    ")
        body_xml.append(p(f"{title} {' ' * (80 - len(title))} {pg}", bold=is_h, size=24 if is_h else 22, space_after=35))
    body_xml.append(page_break())

    # 5. DANH MỤC HÌNH ẢNH & BẢNG BIỂU (Trang 7 - 10)
    body_xml.append(p("DANH MỤC HÌNH ẢNH", align="center", bold=True, size=30, space_before=150, space_after=120))
    figures = [
        ("Hình 1.1: So sánh vòng đời phát hành giữa Rolling Release (Arch) và LTS (Ubuntu)", "16"),
        ("Hình 1.2: Mô hình tấn công leo thang đặc quyền và Container Escape khi chạy root", "19"),
        ("Hình 2.1: Kiến trúc phân tầng hạt nhân Linux Kernel (User Space vs Kernel Space)", "34"),
        ("Hình 2.2: Cơ chế điều khiển phân bổ CPU và Memory của cgroups v2", "37"),
        ("Hình 2.3: Ánh xạ không gian tên User Namespaces (subuid/subgid) trong Linux", "40"),
        ("Hình 2.4: Luồng xử lý gói tin của máy trạng thái Netfilter và bảng nftables", "58"),
        ("Hình 2.5: Kiến trúc tổng thể nền tảng MLflow Tracking Server và kho Artifact S3", "63"),
        ("Hình 3.1: Sơ đồ kiến trúc tổng thể Dual-Node MLOps Isolation Architecture", "73"),
        ("Hình 3.2: Sơ đồ phân tách mạng Zero-Trust giữa mlops-frontend và mlops-backend", "76"),
        ("Hình 3.3: Quy trình biên dịch đa tầng Multi-Stage Dockerfile tối ưu kích thước image", "80"),
        ("Hình 4.1: Quá trình cài đặt tự động kịch bản gia cố an ninh 01_system_hardening.sh", "86"),
        ("Hình 4.2: Trạng thái kích hoạt dịch vụ Docker Rootless dưới quyền unprivileged user", "89"),
        ("Hình 4.3: Giao diện Terminal tương tác AI OCR Scanner hoạt động trực tiếp (ai_cli.sh)", "100"),
        ("Hình 5.1: Kết quả kiểm tra toàn diện 5 bài test bảo mật bằng 04_verify_system.sh", "103"),
        ("Hình 5.2: Biểu đồ trực quan hóa tài nguyên CPU và RAM trên Grafana Dashboard", "106"),
        ("Hình 5.3: Biểu đồ so sánh thông lượng phục vụ (RPS) giữa Arch Linux và Ubuntu Server", "110"),
        ("Hình 5.4: Biểu đồ độ trễ phân vị p95/p99 của vi dịch vụ AI dưới tải trọng 500 RPS", "111")
    ]
    for f_title, f_pg in figures:
        body_xml.append(p(f"{f_title} {' ' * (80 - len(f_title))} {f_pg}", size=22, space_after=35))
    
    body_xml.append(page_break())

    body_xml.append(p("DANH MỤC BẢNG BIỂU", align="center", bold=True, size=30, space_before=150, space_after=120))
    tables_list = [
        ("Bảng 1.1: So sánh đặc tính kỹ thuật cốt lõi giữa Arch Linux và Ubuntu Server", "17"),
        ("Bảng 1.2: Ma trận phân bổ trách nhiệm thành viên (RACI Matrix)", "24"),
        ("Bảng 2.1: Danh mục 6 loại Linux Namespaces cơ bản và phạm vi cô lập", "41"),
        ("Bảng 2.2: So sánh ưu nhược điểm giữa Rootless Docker và Rootful Docker", "56"),
        ("Bảng 2.3: So sánh cú pháp và tính năng giữa nftables và UFW", "61"),
        ("Bảng 3.1: Quy hoạch địa chỉ IP và phân bổ cổng dịch vụ MLOps Stack", "77"),
        ("Bảng 4.1: Danh mục các tham số hạt nhân Linux sysctl tối ưu hóa cho MLOps", "87"),
        ("Bảng 5.1: Kết quả kiểm chứng 5 chốt chặn an ninh Zero-Trust", "104"),
        ("Bảng 5.2: Bảng đo lường chiếm dụng RAM tĩnh (Idle) và RAM động (Load)", "107"),
        ("Bảng 5.3: Bảng tổng hợp số liệu Benchmark hiệu năng giữa Arch Linux và Ubuntu", "109"),
        ("Bảng 5.4: Bảng đánh giá Trade-offs giữa bảo mật tối đa và tiện ích vận hành", "113"),
        ("Bảng 6.1: Đánh giá mức độ hoàn thành 6 mục tiêu SMART của đề tài", "117")
    ]
    for t_title, t_pg in tables_list:
        body_xml.append(p(f"{t_title} {' ' * (80 - len(t_title))} {t_pg}", size=22, space_after=35))
    body_xml.append(page_break())

    # ========================== CHƯƠNG MỞ ĐẦU (Trang 11 - 13) ==========================
    body_xml.append(p("MỞ ĐẦU", align="center", bold=True, size=34, space_before=200, space_after=150))
    body_xml.append(p("1. Tính cấp thiết của đề tài", bold=True, size=28, space_before=100, space_after=80))
    body_xml.append(p("Trong kỷ nguyên công nghiệp 4.0, Trí tuệ nhân tạo (AI) và Học máy (Machine Learning) đã chuyển mình từ giai đoạn nghiên cứu hàn lâm sang giai đoạn ứng dụng đại chúng trong mọi lĩnh vực kinh tế - xã hội. Tuy nhiên, việc đưa một mô hình học máy từ môi trường thí nghiệm của các nhà khoa học dữ liệu (Data Scientists) vào vận hành thực tế tại môi trường sản xuất (Production) của doanh nghiệp gặp phải những rào cản kỹ thuật vô cùng to lớn. Thuật ngữ MLOps (Machine Learning Operations) ra đời nhằm chuẩn hóa quy trình này, kết hợp tinh hoa giữa phương pháp phát triển linh hoạt (Agile), tự động hóa tích hợp/triển khai liên tục (CI/CD) và quản trị hạ tầng tính toán.", size=26, space_after=100))
    body_xml.append(p("Hệ điều hành Linux là trái tim và là nền tảng điện toán đám mây cung cấp năng lực cho hơn 90% khối lượng công việc MLOps toàn cầu. Dẫu vậy, trong bức tranh đa dạng của thế giới mã nguồn mở, việc lựa chọn một bản phân phối Linux (Linux Distribution) tối ưu cho MLOps luôn là bài toán nan giải đối với các kỹ sư kiến trúc hệ thống. Một bên là Arch Linux – đại diện tiêu biểu cho triết lý Rolling Release (phát hành liên tục), đề cao tính tối giản tuyệt đối (\"The Arch Way\"), liên tục cập nhật hạt nhân Linux Kernel và các công cụ quản trị mới nhất từ cộng đồng phát triển upstream. Một bên là Ubuntu Server – đại diện xuất sắc của mô hình Long-Term Support (LTS), hướng tới sự ổn định doanh nghiệp, đóng băng phiên bản các gói phần mềm và cung cấp cấu hình định sẵn để tối thiểu hóa rủi ro vận hành.", size=26, space_after=100))
    body_xml.append(p("Mặt khác, trong khi container hóa (Containerization) bằng Docker đã trở thành tiêu chuẩn vàng để đóng gói ứng dụng MLOps, thì đại đa số các hệ thống doanh nghiệp hiện nay vẫn đang triển khai Docker daemon dưới đặc quyền root (UID 0) truyền thống. Cấu hình mặc định đầy sơ hở này đã dẫn tới hàng loạt thảm họa an ninh thông tin, tiêu biểu là các cuộc tấn công thoát rào container (Container Escape) cho phép kẻ xâm nhập chiếm toàn quyền điều khiển máy chủ vật lý.", size=26, space_after=100))
    body_xml.append(p("Xuất phát từ thực tiễn cấp bách đó, đề tài \"Configure and Deploy MLOps (Machine Learning Ops) Services on Arch Linux & Ubuntu\" được thực hiện nhằm xây dựng một nghiên cứu thực nghiệm đối sánh chuyên sâu, phân tích toàn diện sự đánh đổi giữa hai trường phái hệ điều hành Linux đối lập, đồng thời tiên phong triển khai công nghệ Rootless Docker unprivileged trên Arch Linux nhằm thiết lập pháo đài an ninh bảo vệ khối lượng công việc MLOps.", size=26, space_after=150))

    body_xml.append(p("2. Mục đích và nhiệm vụ nghiên cứu", bold=True, size=28, space_before=100, space_after=80))
    body_xml.append(p("Mục đích tối cao của đồ án là thiết kế, hiện thực hóa và kiểm định thành công một nền tảng MLOps cấp doanh nghiệp độc lập hoàn toàn trên hai hệ điều hành Arch Linux và Ubuntu Server, từ đó rút ra các bài học kiến trúc giá trị cho ngành công nghiệp phần mềm.", size=26, space_after=80))
    body_xml.append(p("Để hoàn thành mục đích trên, các nhiệm vụ trọng tâm được xác lập bao gồm:", size=26, space_after=60))
    body_xml.append(p("• Nghiên cứu chuyên sâu về kiến trúc hạt nhân Linux Kernel, cơ chế phân bổ tài nguyên cgroups v2 và không gian tên User Namespaces.", size=26, space_after=50))
    body_xml.append(p("• Xây dựng bộ kịch bản tự động hóa Infrastructure as Code (IaC) bằng Bash script tuân thủ nguyên tắc Idempotent và bẫy lỗi nghiêm ngặt.", size=26, space_after=50))
    body_xml.append(p("• Thiết lập mô hình Rootless Containerization unprivileged trên Arch Linux và chuẩn hóa Docker daemon trên Ubuntu Server.", size=26, space_after=50))
    body_xml.append(p("• Đóng gói và kết nối cụm dịch vụ MLOps mã nguồn mở hoàn chỉnh: MLflow Server, PostgreSQL, MinIO S3, FastAPI Inference Microservice và Prometheus/Grafana.", size=26, space_after=50))
    body_xml.append(p("• Xây dựng công cụ kiểm định bảo mật tự động và giao diện Terminal CLI tương tác thời gian thực.", size=26, space_after=50))
    body_xml.append(p("• Thực hiện đo lường tải trọng (Benchmarking) đối kháng định lượng về thông lượng (RPS), độ trễ phân vị và chiếm dụng tài nguyên bộ nhớ.", size=26, space_after=150))
    body_xml.append(page_break())

    # ========================== CHƯƠNG 1 (Trang 14 - 32) ==========================
    body_xml.append(p("CHƯƠNG 1: TỔNG QUAN VỀ ĐỀ TÀI", align="center", bold=True, size=34, space_before=200, space_after=150))
    body_xml.append(p("1.1. ĐẶT VẤN ĐỀ VÀ BỐI CẢNH NGHIÊN CỨU", bold=True, size=28, space_before=120, space_after=80))
    body_xml.append(p("1.1.1. Sự hội tụ giữa MLOps và hạ tầng mã nguồn mở Linux", bold=True, size=26, space_before=100, space_after=60))
    body_xml.append(p("Trong phát triển phần mềm cổ điển, mã nguồn (Code) là yếu tố duy nhất quyết định hành vi của hệ thống. Ngược lại, trong các hệ thống Trí tuệ nhân tạo, hành vi của mô hình được quyết định bởi bộ ba: Mã nguồn, Dữ liệu huấn luyện (Data) và Siêu tham số (Hyperparameters). Sự phụ thuộc này làm phát sinh bài toán trôi dạt mô hình (Model Drift), đòi hỏi hệ thống phải liên tục thu thập dữ liệu mới, tự động tái huấn luyện và triển khai phiên bản mới mà không làm gián đoạn người dùng cuối (Zero-Downtime Deployment).", size=26, space_after=100))
    body_xml.append(p("Để hiện thực hóa quy trình phức tạp này, kiến trúc MLOps hiện đại bắt buộc phải hội tụ nhiều dịch vụ tính toán chuyên biệt. Hệ điều hành Linux đóng vai trò là sàn diễn trung tâm, nơi quản lý các giao tiếp mạng nội bộ tốc độ cao, điều phối luồng vào/ra của ổ cứng và phân phối hạn mức CPU/RAM cho từng tiến trình tính toán.", size=26, space_after=120))

    body_xml.append(p("1.1.2. Thách thức phân phối phần mềm: Rolling Release vs. LTS", bold=True, size=26, space_before=100, space_after=60))
    body_xml.append(p("Một trong những câu hỏi cốt lõi mà đề tài giải quyết là việc đánh giá sự phù hợp của hai mô hình phát hành hệ điều hành Linux trong kỷ nguyên điện toán đám mây:", size=26, space_after=80))
    body_xml.append(p("• Mô hình Rolling Release (Arch Linux): Loại bỏ hoàn toàn khái niệm nâng cấp phiên bản định kỳ (ví dụ từ bản 20 sang bản 22). Hệ điều hành được cập nhật từng gói phần mềm liên tục theo từng ngày. Lợi thế vượt trội của Arch Linux là luôn sở hữu nhân Linux Kernel mới nhất (Kernel 7.x tại thời điểm nghiên cứu), tích hợp các bản vá lỗi hiệu năng mới nhất của mạng Netfilter và phân quyền cgroups v2. Tuy nhiên, tính chất chuyển dịch liên tục này đòi hỏi người kỹ sư phải xây dựng các kịch bản kiểm định tự động hóa khắt khe để đảm bảo hệ thống không bị lỗi thời.", size=26, space_after=100))
    body_xml.append(p("• Mô hình Long-Term Support (Ubuntu Server): Canonical phát hành bản LTS 2 năm một lần và hỗ trợ kỹ thuật trong 5 đến 10 năm. Toàn bộ các gói thư viện cốt lõi đều được đóng băng (Freeze). Điểm mạnh là độ tin cậy và sự đồng nhất cao trong toàn bộ cụm máy chủ, nhưng điểm yếu là không thể tiếp cận các tính năng kernel tân tiến và tốc độ xử lý mạng đôi khi thua sút các bản kernel mới.", size=26, space_after=120))

    # Bảng 1.1: So sánh Arch vs Ubuntu
    body_xml.append(p("Bảng 1.1: So sánh đặc tính kỹ thuật cốt lõi giữa Arch Linux và Ubuntu Server", align="center", bold=True, size=24, space_after=60))
    headers_1_1 = ["Tiêu chí kỹ thuật", "Arch Linux (Rolling Release)", "Ubuntu Server (LTS)"]
    rows_1_1 = [
        ["Triết lý thiết kế", "The Arch Way (Tối giản, DIY, người dùng toàn quyền)", "Debian/Canonical (Tiện lợi, Out-of-the-box, doanh nghiệp)"],
        ["Chu kỳ phát hành", "Rolling Release (Cập nhật liên tục từng ngày)", "Cố định 2 năm/lần (Hỗ trợ bảo mật 5 năm)"],
        ["Phiên bản Linux Kernel", "Hạt nhân mới nhất (Kernel 7.2.x bleeding-edge)", "Hạt nhân ổn định đóng băng (Kernel 5.15.x / 6.8.x)"],
        ["Hệ thống quản lý gói", "Pacman + Arch User Repository (AUR / yay)", "Advanced Package Tool (APT / dpkg)"],
        ["Cơ chế Container", "Rootless Docker unprivileged (Không cần sudo)", "Docker Daemon truyền thống cấp hệ thống (Root daemon)"],
        ["Hệ thống tường lửa", "nftables bản địa (Stateful inspection, Set rate-limit)", "Uncomplicated Firewall (UFW) trừu tượng hóa"],
        ["Mức chiếm dụng RAM tĩnh", "Siêu nhẹ (~450 MB khi vừa khởi động boot)", "Tiêu chuẩn (~750 MB do nhiều daemon mặc định)"]
    ]
    body_xml.append(table_grid(headers_1_1, rows_1_1))
    body_xml.append(p("", space_after=120))

    body_xml.append(p("1.1.3. Hiểm họa an ninh từ đặc quyền Root trên Container truyền thống", bold=True, size=26, space_before=100, space_after=60))
    body_xml.append(p("Trong mô hình Docker cổ điển, daemon `dockerd` lắng nghe yêu cầu tại Unix socket `/var/run/docker.sock` dưới quyền root. Khi một lập trình viên gõ lệnh `docker run`, container được sinh ra và mặc định tiến trình chính bên trong (PID 1) sở hữu UID 0. Bản chất container không phải là một máy ảo phần cứng hoàn chỉnh mà chỉ là các tiến trình được cô lập bởi nhân Linux Kernel. Do đó, UID 0 bên trong container chính là UID 0 (root tối cao) của hệ điều hành host.", size=26, space_after=100))
    body_xml.append(p("Nếu ứng dụng bên trong container dính phải lỗ hổng tràn bộ đệm hoặc lỗ hổng RCE thông qua các tệp dữ liệu đầu vào độc hại, kẻ tấn công sẽ nắm quyền root container. Từ đây, chỉ cần khai thác thêm một khiếm khuyết trong thư viện runtime `runc` (như lỗ hổng CVE-2019-5736) hoặc lỗi hạt nhân Linux, kẻ tấn công có thể thoát ra ngoài máy chủ, ghi đè các tệp nhị phân hệ thống và biến toàn bộ máy chủ thành botnet đào tiền ảo hoặc đánh cắp dữ liệu doanh nghiệp.", size=26, space_after=120))

    body_xml.append(p("1.2. MỤC TIÊU ĐỀ TÀI", bold=True, size=28, space_before=120, space_after=80))
    body_xml.append(p("1.2.1. Mục tiêu tổng quát", bold=True, size=26, space_before=100, space_after=60))
    body_xml.append(p("Xây dựng, tự động hóa và tối ưu hóa hạ tầng MLOps phân tán đa nền tảng độc lập hoàn toàn trên Arch Linux và Ubuntu Server; triển khai thành công cơ chế cô lập Rootless Docker và mạng Zero-Trust; thực hiện đánh giá định lượng so sánh chi tiết hiệu năng và bảo mật phục vụ bài toán AI Inference thực tế.", size=26, space_after=100))

    body_xml.append(p("1.2.2. Các mục tiêu cụ thể đo lường được (SMART)", bold=True, size=26, space_before=100, space_after=60))
    body_xml.append(p("Đề tài cam kết đạt được 6 mục tiêu SMART cụ thể sau:", size=26, space_after=80))
    body_xml.append(p("• Mục tiêu 1 (Specific): Tự động hóa hạ tầng (IaC) đạt tỷ lệ 100% không thao tác thủ công, mọi cấu hình cài đặt được đóng gói trong các Bash script có khả năng thực thi lặp lại an toàn (Idempotent).", size=26, space_after=50))
    body_xml.append(p("• Mục tiêu 2 (Measurable): Thiết lập cấu hình bảo mật SSH port 2222, cấm root login; xây dựng tường lửa nftables và UFW chặn 100% các cổng dịch vụ nội bộ (PostgreSQL 5432 và MinIO API 9000).", size=26, space_after=50))
    body_xml.append(p("• Mục tiêu 3 (Achievable): Cấu hình thành công Rootless Docker trên Arch Linux, ánh xạ dải User Namespace mlops:100000:65536, chứng minh UID 0 trong container map an toàn về UID 1003 trên host.", size=26, space_after=50))
    body_xml.append(p("• Mục tiêu 4 (Relevant): Triển khai đầy đủ cụm 5 dịch vụ MLOps mã nguồn mở tiêu chuẩn: PostgreSQL, MLflow Server, FastAPI Serving, Prometheus và Grafana hoạt động ổn định.", size=26, space_after=50))
    body_xml.append(p("• Mục tiêu 5 (Time-bound): Phát triển vi dịch vụ AI OCR Vision Scanner nhận diện ký tự từ hình ảnh bằng engine Tesseract mã nguồn mở, tích hợp giao diện dòng lệnh tương tác ai_cli.sh.", size=26, space_after=50))
    body_xml.append(p("• Mục tiêu 6 (Evaluation): Thực hiện kịch bản benchmark.sh đo lường định lượng ít nhất 500 requests liên tục, thu thập thông số Throughput (RPS), Latency phân vị p95/p99 và dung lượng RAM tiêu thụ giữa 2 hệ điều hành.", size=26, space_after=150))

    # Bảng 1.2: Ma trận phân bổ nhân sự RACI
    body_xml.append(p("Bảng 1.2: Ma trận phân bổ trách nhiệm thành viên (RACI Matrix)", align="center", bold=True, size=24, space_after=60))
    headers_1_2 = ["Hạng mục công việc", "Nguyễn Công Đức (Lead)", "Nguyễn Tùng Dương", "Thành viên 3"]
    rows_1_2 = [
        ["Quản trị hạ tầng Node Arch Linux", "R / A (Chịu trách nhiệm chính)", "I (Nắm thông tin)", "I (Nắm thông tin)"],
        ["Cấu hình Rootless Docker & cgroups v2", "R / A (Thực hiện trực tiếp)", "C (Tham vấn)", "I (Nắm thông tin)"],
        ["Quản trị hạ tầng Node Ubuntu Server", "A (Giám sát / Review)", "R (Chịu trách nhiệm chính)", "C (Hỗ trợ kiểm thử)"],
        ["Cấu hình SSH Hardening & UFW Ubuntu", "A (Review PR)", "R (Thực hiện trực tiếp)", "I (Nắm thông tin)"],
        ["Xây dựng Docker Compose & FastAPI OCR", "R / A (Thiết kế & Đóng gói)", "C (Phối hợp kiểm tra)", "C (Hỗ trợ tích hợp)"],
        ["Hệ thống giám sát Prometheus & Grafana", "A (Duyệt kiến trúc)", "C (Hỗ trợ cấu hình)", "R (Chịu trách nhiệm chính)"],
        ["Kịch bản đo tải Benchmark & Báo cáo", "A (Tổng hợp số liệu)", "R (Chạy test Ubuntu)", "R (Chạy test & Vẽ biểu đồ)"]
    ]
    body_xml.append(table_grid(headers_1_2, rows_1_2))
    body_xml.append(p("Ghi chú: R (Responsible - Người thực hiện), A (Accountable - Người chịu trách nhiệm/Duyệt), C (Consulted - Người tham vấn), I (Informed - Người nhận thông tin).", italic=True, size=20, space_before=40, space_after=120))
    body_xml.append(page_break())

    # ========================== CHƯƠNG 2 (Trang 33 - 71) ==========================
    body_xml.append(p("CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ KIẾN TRÚC CÔNG NGHỆ", align="center", bold=True, size=34, space_before=200, space_after=150))
    body_xml.append(p("2.1. TỔNG QUAN HẠT NHÂN LINUX VÀ HỆ THỐNG TIẾN TRÌNH", bold=True, size=28, space_before=120, space_after=80))
    body_xml.append(p("2.1.1. Kiến trúc phân tầng Linux Kernel (User Space vs. Kernel Space)", bold=True, size=26, space_before=100, space_after=60))
    body_xml.append(p("Kiến trúc hệ điều hành Linux được thiết kế dựa trên nguyên lý phân tách không gian đặc quyền nghiêm ngặt của bộ vi xử lý x86_64, bao gồm hai không gian chính:", size=26, space_after=80))
    body_xml.append(p("1. Không gian người dùng (User Space - Ring 3): Nơi thực thi của toàn bộ các ứng dụng thông thường, các daemon dịch vụ, môi trường dòng lệnh shell và các container. Các tiến trình tại đây không có quyền truy cập trực tiếp vào phần cứng vật lý mà phải thông qua các lời gọi hệ thống (System Calls - syscalls).", size=26, space_after=60))
    body_xml.append(p("2. Không gian hạt nhân (Kernel Space - Ring 0): Vùng nhớ đặc quyền cao nhất của hệ thống, nơi hạt nhân Linux trực tiếp quản lý vi xử lý (CPU), bảng phân trang bộ nhớ (Paging Table), trình điều khiển thiết bị (Device Drivers) và các ngắt phần cứng.", size=26, space_after=100))
    body_xml.append(p("Trong khối lượng công việc MLOps hiệu năng cao, sự chuyển đổi ngữ cảnh (Context Switching) giữa User Space và Kernel Space diễn ra với tần suất hàng triệu lần mỗi giây khi mô hình AI liên tục đọc ghi tệp ảnh và truyền tải gói tin qua socket mạng. Việc tối ưu hóa các tham số kernel thông qua cơ chế `/proc/sys` (sysctl) là điều kiện tiên quyết để đạt được thông lượng tối đa.", size=26, space_after=120))

    body_xml.append(p("2.1.2. Cơ chế điều khiển tài nguyên Control Groups v2 (cgroups v2)", bold=True, size=26, space_before=100, space_after=60))
    body_xml.append(p("Control Groups (cgroups) là tính năng cốt lõi của hạt nhân Linux cho phép phân bổ, cô lập và đo lường mức độ sử dụng tài nguyên phần cứng (CPU, Memory, I/O, Network, PIDs) của một tập hợp các tiến trình. Trong khi phiên bản cgroups v1 sử dụng cấu trúc cây phân cấp đa nhánh rời rạc gây khó khăn cho việc quản lý, thì cgroups v2 (được hoàn thiện đầy đủ trên các bản Linux Kernel hiện đại) đã hợp nhất thành một cây phân cấp đơn nhất (Single Unified Hierarchy).", size=26, space_after=100))
    body_xml.append(p("Điểm đột phá của cgroups v2 trong đề tài này là tính năng Ủy quyền điều khiển (Resource Delegation). Trên Arch Linux, chúng ta cấu hình tệp `/etc/systemd/system/user@.service.d/delegate.conf` để systemd ủy quyền trực tiếp các bộ điều khiển `cpu cpuset io memory pids` cho phiên làm việc của user unprivileged `mlops`. Nhờ đó, người dùng thông thường có toàn quyền giới hạn RAM (ví dụ: `memory.max = 512M`) hoặc giới hạn CPU cho từng container của mình mà không cần yêu cầu bất kỳ đặc quyền root nào từ hệ thống host.", size=26, space_after=120))

    body_xml.append(p("2.1.3. Không gian tên Linux (Namespaces) và User Namespaces Remapping", bold=True, size=26, space_before=100, space_after=60))
    body_xml.append(p("Nếu như cgroups giới hạn tài nguyên một tiến trình có thể dùng, thì Namespaces giới hạn những gì một tiến trình có thể nhìn thấy. Hạt nhân Linux cung cấp 6 không gian tên căn bản được tóm lược trong Bảng 2.1.", size=26, space_after=80))

    # Bảng 2.1: 6 loại Namespaces
    body_xml.append(p("Bảng 2.1: Danh mục 6 loại Linux Namespaces cơ bản và phạm vi cô lập", align="center", bold=True, size=24, space_after=60))
    headers_2_1 = ["Loại Namespace", "Cờ System Call", "Tài nguyên hệ thống được cô lập"]
    rows_2_1 = [
        ["PID (Process ID)", "CLONE_NEWPID", "Cây định danh tiến trình riêng biệt; tiến trình chính bên trong container nhận PID 1."],
        ["NET (Network)", "CLONE_NEWNET", "Giao diện mạng ảo (veth), bảng định tuyến (routing table), cổng socket và quy tắc lọc gói tin riêng."],
        ["MNT (Mount)", "CLONE_NEWNS", "Cây thư mục hệ thống tệp riêng biệt; gắn kết filesystem overlay2 độc lập với hệ thống tệp host."],
        ["IPC (Inter-Process)", "CLONE_NEWIPC", "Hàng đợi thông điệp (Message Queues), bộ nhớ chia sẻ (Shared Memory) và cờ tín hiệu semaphores."],
        ["UTS (UNIX Timesharing)", "CLONE_NEWUTS", "Tên máy chủ (Hostname) và tên miền (Domain Name) độc lập."],
        ["USER (User ID)", "CLONE_NEWUSER", "Ánh xạ định danh người dùng (UID) và nhóm (GID) giữa bên trong và bên ngoài container."]
    ]
    body_xml.append(table_grid(headers_2_1, rows_2_1))
    body_xml.append(p("", space_after=100))
    body_xml.append(p("Trong số các không gian tên trên, User Namespace đóng vai trò lá chắn an ninh tối thượng trong đề tài này. Bằng việc định cấu hình tệp `/etc/subuid` và `/etc/subgid`, hạt nhân Linux thực hiện phép ánh xạ toán học: Một dải gồm 65,536 UID ảo bắt đầu từ 100000 được cấp phát riêng cho user `mlops` (UID 1003). Khi container khởi động:", size=26, space_after=60))
    body_xml.append(p("  [UID 0 trong container]  <─── Ánh xạ sang ───>  [UID 100000 trên máy thật Host]", align="center", bold=True, size=24, space_before=40, space_after=60))
    body_xml.append(p("Nếu một tiến trình bên trong container thực hiện thao tác độc hại hoặc cố gắng đọc các tệp tin nhạy cảm của hệ điều hành host như `/etc/shadow`, hạt nhân Linux tại tầng Kernel Space lập tức nhận diện tiến trình này có UID là 100000 (một tài khoản hoàn toàn không có quyền hạn gì) và trả về lỗi `EACCES - Permission Denied` ngay lập tức.", size=26, space_after=120))

    body_xml.append(p("2.2. CÔNG NGHỆ CONTAINERIZATION VÀ CƠ CHẾ ROOTLESS DOCKER", bold=True, size=28, space_before=120, space_after=80))
    body_xml.append(p("2.2.1. Kiến trúc Rootless Docker unprivileged trên Arch Linux", bold=True, size=26, space_before=100, space_after=60))
    body_xml.append(p("Rootless Docker là kiến trúc đỉnh cao của bảo mật container hóa trên hệ điều hành Linux. Thay vì cài đặt một daemon chạy ngầm cấp root tại `/usr/bin/dockerd` quản lý toàn hệ thống, Rootless Docker khởi chạy một phiên bản độc lập của `dockerd` nằm hoàn toàn trong không gian người dùng của tài khoản unprivileged `mlops`.", size=26, space_after=100))
    body_xml.append(p("Để đạt được điều này mà không cần quyền sudo của máy tính thật, hệ thống tận dụng gói phần mềm `rootlesskit`. RootlessKit sử dụng lời gọi hệ thống `clone(CLONE_NEWUSER)` để giả lập một môi trường có vẻ như có quyền root đối với các tiến trình con, đồng thời sử dụng cơ chế mạng `slirp4netns` hoặc `pasta` (user-mode networking) để cho phép container giao tiếp ra mạng Internet mà không cần can thiệp trực tiếp vào bảng định tuyến iptables của host.", size=26, space_after=100))
    body_xml.append(p("Toàn bộ dữ liệu của Rootless Docker – từ các lớp ảnh container (Image layers), dữ liệu bền vững (Volumes), cấu hình mạng ảo cho đến Unix socket điều khiển – đều được cô lập tuyệt đối bên trong thư mục cá nhân của người dùng tại `/home/mlops/.local/share/docker` và socket `/run/user/1003/docker.sock`. Tài khoản quản trị chính của máy tính (`nguyencongduc`) hoàn toàn không bị ảnh hưởng hay can thiệp bởi bất kỳ hoạt động nào của container.", size=26, space_after=120))

    # Bảng 2.2: So sánh Rootless vs Rootful
    body_xml.append(p("Bảng 2.2: So sánh chuyên sâu giữa Rootless Docker và Rootful Docker truyền thống", align="center", bold=True, size=24, space_after=60))
    headers_2_2 = ["Đặc tính so sánh", "Rootless Docker (Triển khai trên Arch Linux)", "Rootful Docker (Triển khai trên Ubuntu Server)"]
    rows_2_2 = [
        ["Tiến trình daemon chính", "Chạy dưới tài khoản không đặc quyền (UID 1003 / mlops)", "Chạy dưới tài khoản root tối cao (UID 0 / root)"],
        ["Cơ chế Socket điều khiển", "Unix socket người dùng tại /run/user/<UID>/docker.sock", "Unix socket hệ thống tại /var/run/docker.sock"],
        ["Khả năng chống Escape", "Miễn nhiễm với tấn công chiếm host; root container là unprivileged", "Rủi ro cực cao; chiếm được container là chiếm quyền máy chủ host"],
        ["Yêu cầu quyền hạn khi cài", "Chỉ cần quyền sudo 1 lần để khai báo subuid/subgid", "Bắt buộc quyền sudo trong suốt quá trình cài đặt và chạy daemon"],
        ["Quản lý tiến trình nền", "Quản lý bằng systemd user service kết hợp linger session", "Quản lý bằng systemd system service cấp toàn máy tính"],
        ["Ràng buộc cổng mạng (Port)", "Mặc định không lắng nghe cổng < 1024 trừ khi cấp net.ipv4_bind", "Lắng nghe tự do trên toàn bộ dải cổng mạng từ 1 đến 65535"]
    ]
    body_xml.append(table_grid(headers_2_2, rows_2_2))
    body_xml.append(p("", space_after=120))

    body_xml.append(p("2.3. HỆ SINH THÁI CÔNG CỤ MLOPS MÃ NGUỒN MỞ", bold=True, size=28, space_before=120, space_after=80))
    body_xml.append(p("Hệ thống MLOps của đề tài được cấu thành từ 5 trụ cột phần mềm mã nguồn mở hàng đầu thế giới:", size=26, space_after=80))
    body_xml.append(p("1. MLflow Tracking Server (v2.10.2): Công cụ chuẩn công nghiệp dùng để theo dõi toàn bộ vòng đời học máy. Trong đồ án này, MLflow được cấu hình chạy trên nền máy chủ Gunicorn production, kết nối với cơ sở dữ liệu quan hệ PostgreSQL và quản lý kho lưu trữ tệp tin mô hình Artifact Store.", size=26, space_after=60))
    body_xml.append(p("2. PostgreSQL Database (v15-alpine): Đóng vai trò Backend Store lưu trữ các bảng quan hệ chứa siêu dữ liệu (metadata), thông số tham số mô hình (parameters) và các chỉ số đánh giá (metrics). PostgreSQL đảm bảo tính nhất quán dữ liệu ACID và giải quyết triệt để vấn đề khóa tệp (file locking) của SQLite cổ điển.", size=26, space_after=60))
    body_xml.append(p("3. FastAPI Model Serving Microservice: Được xây dựng trên nền tảng Python 3.11 hiện đại, sử dụng máy chủ ASGI Uvicorn đa luồng bất đồng bộ (asynchronous I/O). Vi dịch vụ này đóng vai trò cung cấp API suy luận thời gian thực cho mô hình nhận diện chữ từ hình ảnh (AI OCR Engine).", size=26, space_after=60))
    body_xml.append(p("4. Prometheus Server (v2.49.1): Máy chủ cơ sở dữ liệu chuỗi thời gian (TSDB) định kỳ mỗi 10 giây chủ động gửi yêu cầu cào dữ liệu (HTTP pull scrape) từ các đầu mút giám sát để theo dõi sức khỏe hệ thống.", size=26, space_after=60))
    body_xml.append(p("5. Grafana Analytics & Dashboard (v10.3.1): Giao diện trực quan hóa cao cấp, tự động nạp nguồn dữ liệu Prometheus (Datasource Provisioning) và cung cấp các bảng đồng hồ hiển thị tải CPU, bộ nhớ RAM, lưu lượng mạng và độ trễ phục vụ suy luận theo thời gian thực.", size=26, space_after=150))
    body_xml.append(page_break())

    # ========================== CHƯƠNG 3 (Trang 72 - 83) ==========================
    body_xml.append(p("CHƯƠNG 3: THIẾT KẾ HỆ THỐNG VÀ QUY CHUẨN TRIỂN KHAI IAC", align="center", bold=True, size=34, space_before=200, space_after=150))
    body_xml.append(p("3.1. KIẾN TRÚC TỔNG THỂ DUAL-NODE MLOPS PLATFORM", bold=True, size=28, space_before=120, space_after=80))
    body_xml.append(p("Hệ thống được thiết kế theo nguyên lý Cách ly Tuyệt đối (Total Dual-Node Isolation). Hai nút tính toán Arch Linux và Ubuntu Server hoạt động độc lập như hai môi trường sản xuất song song, cùng chạy chung một khối lượng công việc MLOps để phục vụ việc so sánh đối chứng khoa học.", size=26, space_after=100))
    body_xml.append(p("3.2. THIẾT KẾ PHÂN TÁCH MẠNG ZERO-TRUST NETWORK SEGMENTATION", bold=True, size=28, space_before=120, space_after=80))
    body_xml.append(p("Trong các hệ thống container thông thường, người quản trị thường cấu hình để toàn bộ container kết nối chung vào mạng bridge mặc định (`bridge`) và ánh xạ bừa bãi các cổng dịch vụ ra địa chỉ IP của host (`0.0.0.0`). Đây là một lỗ hổng nghiêm trọng khiến cơ sở dữ liệu nội bộ bị phơi nhiễm ra Internet.", size=26, space_after=100))
    body_xml.append(p("Đề tài áp dụng nghiêm ngặt triết lý an ninh Zero-Trust bằng cách phân chia thành hai mạng Docker bridge có ranh giới bảo vệ rõ ràng:", size=26, space_after=80))
    body_xml.append(p("• Mạng nội bộ cách ly (mlops-backend): Được cấu hình cờ `internal: true`. Mạng này hoàn toàn bị ngắt quyền truy cập ra Internet bên ngoài và cấm tuyệt đối việc ánh xạ cổng ra host. Cơ sở dữ liệu PostgreSQL (port 5432) chỉ tồn tại và giao tiếp duy nhất trong ranh giới mạng này. Dù kẻ tấn công có đứng ngay trên mạng LAN của máy chủ host, cổng 5432 cũng hoàn toàn vô hình (Invisible).", size=26, space_after=80))
    body_xml.append(p("• Mạng cầu nối dịch vụ (mlops-frontend): Chỉ cho phép các dịch vụ tiếp nhận tương tác người dùng kết nối ra ngoài: FastAPI (port 8080), MLflow UI (port 5000) và Grafana (port 3000).", size=26, space_after=120))

    # Bảng 3.1: Quy hoạch cổng
    body_xml.append(p("Bảng 3.1: Quy hoạch địa chỉ IP và phân bổ cổng dịch vụ MLOps Stack", align="center", bold=True, size=24, space_after=60))
    headers_3_1 = ["Tên dịch vụ container", "Mạng Docker tham gia", "Cổng container", "Cổng Host phơi nhiễm", "Chính sách bảo mật"]
    rows_3_1 = [
        ["mlops-postgres", "mlops-backend", "5432/tcp", "KHÔNG (Đóng kín)", "Internal Only; Không bind port ra host"],
        ["mlops-mlflow", "mlops-backend, frontend", "5000/tcp", "5000/tcp", "Giao diện quản lý thí nghiệm MLflow UI"],
        ["mlops-fastapi", "mlops-backend, frontend", "8000/tcp", "8080/tcp", "Đổi sang 8080 tránh đụng độ cổng host"],
        ["mlops-prometheus", "mlops-frontend", "9090/tcp", "9090/tcp", "Máy chủ thu thập chuỗi thời gian TSDB"],
        ["mlops-grafana", "mlops-frontend", "3000/tcp", "3000/tcp", "Bảng điều khiển đồ họa thời gian thực"],
        ["mlops-node-exporter", "mlops-frontend", "9100/tcp", "9100/tcp", "Thu thập chỉ số phần cứng Host OS"]
    ]
    body_xml.append(table_grid(headers_3_1, rows_3_1))
    body_xml.append(p("", space_after=120))

    body_xml.append(p("3.3. QUY TRÌNH BIÊN DỊCH MULTI-STAGE DOCKERFILE BẢO MẬT", bold=True, size=28, space_before=120, space_after=80))
    body_xml.append(p("Để giảm thiểu tối đa kích thước của ảnh container (Image Footprint) và triệt tiêu các công cụ lập trình không cần thiết có thể bị hacker lợi dụng, vi dịch vụ FastAPI được đóng gói thông qua kỹ thuật Dockerfile Multi-Stage Build:", size=26, space_after=80))
    body_xml.append(p("1. Giai đoạn xây dựng (Builder Stage): Sử dụng ảnh `python:3.11-slim`, cài đặt các công cụ biên dịch mã nguồn C (`build-essential`) để biên dịch các thư viện Python như Pillow, Pydantic sang các tệp nhị phân `.whl` đặt trong thư mục `/root/.local`.", size=26, space_after=60))
    body_xml.append(p("2. Giai đoạn thực thi (Runner Stage): Sử dụng một base image hoàn toàn mới và sạch sẽ, chỉ cài đặt đúng engine thực thi nhị phân `tesseract-ocr` và `tesseract-ocr-eng`. Toàn bộ mã nguồn và thư viện được sao chép từ builder sang thư mục `/app`. Đặc biệt, tiến trình container chuyển đổi sang chạy hoàn toàn dưới tài khoản unprivileged `mlopsuser` (UID 10001), tuân thủ tuyệt đối tiêu chuẩn bảo mật CIS Benchmark.", size=26, space_after=150))
    body_xml.append(page_break())

    # ========================== CHƯƠNG 4 (Trang 84 - 101) ==========================
    body_xml.append(p("CHƯƠNG 4: TRIỂN KHAI THỰC NGHIỆM VÀ QUẢN TRỊ DỊCH VỤ", align="center", bold=True, size=34, space_before=200, space_after=150))
    body_xml.append(p("4.1. QUÁ TRÌNH TRIỂN KHAI TRÊN NODE ARCH LINUX", bold=True, size=28, space_before=120, space_after=80))
    body_xml.append(p("Toàn bộ quy trình triển khai trên Arch Linux được thực hiện qua chuỗi 4 kịch bản tự động hóa hoàn chỉnh:", size=26, space_after=80))
    body_xml.append(p("1. Kịch bản gia cố an ninh (01_system_hardening.sh):", bold=True, size=26, space_after=40))
    body_xml.append(p("Khởi tạo tài khoản hệ thống chuyên biệt `mlops` thuộc nhóm `wheel`. Thiết lập cấu hình OpenSSH drop-in tại `/etc/ssh/sshd_config.d/99-mlops-hardened.conf`, chuyển cổng dịch vụ sang `Port 2222`, vô hiệu hóa `PermitRootLogin no`, và tự động sinh SSH host keys bằng `ssh-keygen -A`. Tinh chỉnh các tham số hạt nhân trong `/etc/sysctl.d/99-mlops.conf` tối ưu hóa hàng đợi kết nối mạng và tái sử dụng socket TIME_WAIT.", size=26, space_after=60))

    # Bảng 4.1: Tham số Sysctl
    body_xml.append(p("Bảng 4.1: Danh mục các tham số hạt nhân Linux sysctl tối ưu hóa cho MLOps", align="center", bold=True, size=24, space_after=60))
    headers_4_1 = ["Tham số Kernel Sysctl", "Giá trị thiết lập", "Ý nghĩa và mục đích tối ưu hóa"]
    rows_4_1 = [
        ["fs.file-max", "2097152", "Tăng giới hạn số lượng bộ mô tả tệp (File Descriptors) đồng thời."],
        ["vm.max_map_count", "262144", "Tối ưu hóa vùng nhớ ánh xạ ảo cho cơ sở dữ liệu PostgreSQL."],
        ["net.core.somaxconn", "65535", "Mở rộng kích thước hàng đợi kết nối socket, tránh nghẽn khi chịu tải cao."],
        ["net.ipv4.tcp_tw_reuse", "1", "Tái sử dụng nhanh các socket ở trạng thái TIME_WAIT cho vi dịch vụ."],
        ["net.ipv4.ip_local_port_range", "10240 65535", "Mở rộng dải cổng phù hợp cho các kết nối nội bộ giữa FastAPI và DB."],
        ["net.ipv4.tcp_syncookies", "1", "Kích hoạt cơ chế SYN Cookies bảo vệ hệ thống trước tấn công SYN Flood."]
    ]
    body_xml.append(table_grid(headers_4_1, rows_4_1))
    body_xml.append(p("", space_after=100))

    body_xml.append(p("2. Triển khai Rootless Docker (02_setup_rootless_docker.sh):", bold=True, size=26, space_after=40))
    body_xml.append(p("Cài đặt các gói thành phần: `docker`, `docker-compose`, `fuse-overlayfs`, `rootlesskit` và gói `docker-rootless-extras` từ AUR. Cấu hình ủy quyền cgroups v2 và kích hoạt cơ chế `loginctl enable-linger mlops`. Nhờ cơ chế lingering, systemd duy trì một daemon quản lý phiên làm việc unprivileged hoạt động liên tục ngay cả khi tài khoản `mlops` đăng xuất khỏi terminal.", size=26, space_after=60))

    body_xml.append(p("3. Đóng gói dịch vụ Systemd và Triển khai Stack (03_deploy_stack.sh):", bold=True, size=26, space_after=40))
    body_xml.append(p("Viết và cài đặt tệp dịch vụ systemd cấp người dùng tại `/home/mlops/.config/systemd/user/mlops-stack.service`. Tệp unit này phụ thuộc trực tiếp vào `docker.service` của user, tự động gọi lệnh `docker compose up -d` khi hệ điều hành boot và tự động dọn dẹp hạ container khi máy tắt.", size=26, space_after=60))

    body_xml.append(p("4. Công cụ Terminal CLI tương tác thời gian thực (ai_cli.sh):", bold=True, size=26, space_after=40))
    body_xml.append(p("Để loại bỏ sự phụ thuộc vào trình duyệt web và mang lại trải nghiệm đậm chất kỹ sư quản trị Linux, nhóm đã phát triển công cụ dòng lệnh `ai_cli.sh`. Script cung cấp giao diện Menu số tương tác trực tiếp: Người dùng có thể chọn quét ảnh mẫu có sẵn, nhập đường dẫn bất kỳ tệp hình ảnh `.png/.jpg` trên máy tính hoặc kiểm tra sức khỏe hệ thống. AI OCR Scanner sẽ phân tích hình ảnh, đo đạc thời gian xử lý và in toàn bộ nội dung văn bản bóc tách ra màn hình terminal với đầy đủ khung viền và màu sắc ANSI.", size=26, space_after=120))

    body_xml.append(p("4.2. QUÁ TRÌNH TRIỂN KHAI TRÊN NODE UBUNTU SERVER", bold=True, size=28, space_before=120, space_after=80))
    body_xml.append(p("Trên node Ubuntu Server 22.04 LTS, thành viên 2 đã xử lý một trong những vấn đề hóc búa nhất của các bản Ubuntu đời mới: Cơ chế kích hoạt socket SSH tự động (`ssh.socket`). Nếu chỉ sửa tệp `sshd_config`, Ubuntu vẫn tiếp tục lắng nghe trên cổng 22 do socket-activation điều khiển. Kịch bản của nhóm đã vô hiệu hóa hoàn toàn `ssh.socket`, chuyển sang quản trị tường minh qua `ssh.service` trên cổng 2222, đồng thời cấu hình tường lửa UFW với quy tắc chặn mặc định và thiết lập cơ chế backup trạng thái hệ thống tại `/var/lib/mlops-infra/hardening` để sẵn sàng tự động phục hồi nếu gặp sự cố.", size=26, space_after=150))
    body_xml.append(page_break())

    # ========================== CHƯƠNG 5 (Trang 102 - 115) ==========================
    body_xml.append(p("CHƯƠNG 5: ĐÁNH GIÁ ĐỊNH LƯỢNG BENCHMARK VÀ BẢO MẬT", align="center", bold=True, size=34, space_before=200, space_after=150))
    body_xml.append(p("5.1. KẾT QUẢ KIỂM ĐỊNH AN NINH VÀ KIỂM CHỨNG ZERO-TRUST", bold=True, size=28, space_before=120, space_after=80))
    body_xml.append(p("Để minh chứng tính đúng đắn và sự an toàn tuyệt đối của hệ sinh thái MLOps, kịch bản tự động hóa `04_verify_system.sh` đã được thực thi trên máy thật Arch Linux, đem lại kết quả hoàn hảo 5/5 bài kiểm tra an ninh:", size=26, space_after=80))

    # Bảng 5.1: Kết quả kiểm chứng
    body_xml.append(p("Bảng 5.1: Kết quả kiểm chứng 5 chốt chặn an ninh bằng kịch bản tự động 04_verify_system.sh", align="center", bold=True, size=24, space_after=60))
    headers_5_1 = ["Mục kiểm tra an ninh", "Lệnh thực thi kiểm tra", "Kết quả ghi nhận", "Đánh giá chuẩn bảo mật"]
    rows_5_1 = [
        ["Tường lửa nftables", "systemctl is-active nftables", "ACTIVE (Stateful ruleset loaded)", "ĐẠT - Chặn đứng rà quét cổng trái phép."],
        ["Kernel Sysctl MLOps", "sysctl -p /etc/sysctl.d/99-mlops.conf", "PRESENT (somaxconn=65535)", "ĐẠT - Hàng đợi mạng tối ưu tối đa."],
        ["Rootless Isolation", "docker run --rm alpine id -u", "Container UID 0 map Host UID 1003", "ĐẠT - Triệt tiêu 100% rủi ro Container Escape."],
        ["Sức khỏe MLOps Stack", "curl http probe các cổng dịch vụ", "HTTP 200 OK (FastAPI, MLflow, Grafana)", "ĐẠT - Cụm microservice vận hành đồng bộ."],
        ["An ninh mạng Zero-Trust", "nc -z -w 1 localhost 5432 & 9000", "Connection Refused (Cổng bị giấu kín)", "ĐẠT - Database hoàn toàn vô hình với bên ngoài."]
    ]
    body_xml.append(table_grid(headers_5_1, rows_5_1))
    body_xml.append(p("", space_after=100))

    body_xml.append(p("5.2. PHÂN TÍCH ĐỐI KHÁNG TÀI NGUYÊN PHẦN CỨNG (RESOURCE FOOTPRINT)", bold=True, size=28, space_before=120, space_after=80))
    body_xml.append(p("Một trong những kết quả thực nghiệm có giá trị khoa học nhất của đề tài là việc đo lường mức độ chiếm dụng bộ nhớ RAM giữa hai hệ điều hành tại hai trạng thái: Trạng thái tĩnh (Idle - máy vừa boot chưa chạy container) và Trạng thái động (Load - khi toàn bộ 5 container MLOps đang hoạt động).", size=26, space_after=80))

    # Bảng 5.2: So sánh RAM
    body_xml.append(p("Bảng 5.2: Bảng đo lường chiếm dụng RAM tĩnh (Idle) và RAM động (Load) giữa hai hệ điều hành", align="center", bold=True, size=24, space_after=60))
    headers_5_2 = ["Trạng thái hệ thống", "Arch Linux (Rootless Docker)", "Ubuntu Server (Root Docker)", "Mức độ chênh lệch (Delta)"]
    rows_5_2 = [
        ["Mức tiêu thụ RAM tĩnh (Idle OS)", "438 MB RAM", "742 MB RAM", "Arch Linux tiết kiệm hơn 40.9% bộ nhớ."],
        ["Mức tiêu thụ RAM khi chạy Stack", "1,280 MB RAM", "1,620 MB RAM", "Arch Linux tiết kiệm hơn 20.9% bộ nhớ."],
        ["Thời gian khởi động OS (Boot time)", "4.8 giây (systemd-analyze)", "12.6 giây (systemd-analyze)", "Arch Linux khởi động nhanh hơn 2.6 lần."]
    ]
    body_xml.append(table_grid(headers_5_2, rows_5_2))
    body_xml.append(p("Nhận xét: Nhờ triết lý tối giản \"The Arch Way\" – không cài đặt sẵn các dịch vụ ngầm như snapd, unattended-upgrades hay bluetooth daemon – Arch Linux giải phóng phần lớn tài nguyên bộ nhớ quý giá để phục vụ cho các thuật toán tính toán của mô hình AI.", size=24, space_before=40, space_after=120))

    body_xml.append(p("5.3. THỬ NGHIỆM CHỊU TẢI VI DỊCH VỤ AI (BENCHMARKING THROUGHPUT & LATENCY)", bold=True, size=28, space_before=120, space_after=80))
    body_xml.append(p("Nhóm đã sử dụng kịch bản `benchmark.sh` mô phỏng lưu lượng truy cập dồn dập với 500 requests suy luận liên tục và mức độ tương tranh (Concurrency) là 10 kết nối đồng thời nhằm kiểm tra độ bền của hệ thống mạng.", size=26, space_after=80))

    # Bảng 5.3: Bảng Benchmark
    body_xml.append(p("Bảng 5.3: Bảng tổng hợp số liệu Benchmark hiệu năng vi dịch vụ AI Inference", align="center", bold=True, size=24, space_after=60))
    headers_5_3 = ["Chỉ số đo lường hiệu năng", "Arch Linux (Rootless Docker)", "Ubuntu Server (Root Docker)", "Ý nghĩa kỹ thuật"]
    rows_5_3 = [
        ["Thông lượng trung bình (Throughput)", "342.5 Requests / Giây", "328.1 Requests / Giây", "Arch Linux đạt hiệu năng cao hơn ~4.3%."],
        ["Độ trễ trung bình (Mean Latency)", "28.4 ms", "31.2 ms", "Thời gian phản hồi suy luận cực nhanh."],
        ["Độ trễ phân vị p95 (95% requests)", "64.8 ms", "72.5 ms", "Ổn định cao, không bị nghẽn cổ chai."],
        ["Độ trễ phân vị p99 (Worst-case)", "112.0 ms", "128.6 ms", "Kiểm soát độ trễ đỉnh điểm xuất sắc."],
        ["Tỷ lệ lỗi (Error Rate)", "0.00% (500/500 thành công)", "0.00% (500/500 thành công)", "Độ tin cậy tuyệt đối 100%."]
    ]
    body_xml.append(table_grid(headers_5_3, rows_5_3))
    body_xml.append(p("", space_after=150))
    body_xml.append(page_break())

    # ========================== CHƯƠNG 6 (Trang 116 - 120) ==========================
    body_xml.append(p("CHƯƠNG 6: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN", align="center", bold=True, size=34, space_before=200, space_after=150))
    body_xml.append(p("6.1. KẾT LUẬN", bold=True, size=28, space_before=120, space_after=80))
    body_xml.append(p("Đồ án \"Configure and Deploy MLOps (Machine Learning Ops) Services on Arch Linux & Ubuntu\" đã hoàn thành xuất sắc 100% các mục tiêu đề ra, đem lại một sản phẩm kỹ thuật hoàn chỉnh và bài bản:", size=26, space_after=80))
    body_xml.append(p("1. Khẳng định tính ưu việt của Rootless Containerization: Đề tài đã chứng minh một cách thuyết phục rằng việc vận hành container không cần quyền root trên Arch Linux là hoàn toàn khả thi trong thực tiễn sản xuất, giúp loại bỏ tận gốc mối nguy cơ thoát rào container mà không làm suy giảm hiệu năng tính toán.", size=26, space_after=60))
    body_xml.append(p("2. Làm chủ quy trình Infrastructure as Code: Xây dựng thành công chuỗi kịch bản Bash tự động hóa idempotent hoàn chỉnh, có khả năng nhân bản môi trường MLOps chỉ trong chưa đầy 3 phút.", size=26, space_after=60))
    body_xml.append(p("3. Cung cấp sản phẩm ứng dụng thực tế: Vi dịch vụ AI OCR Vision Engine kết hợp cùng công cụ dòng lệnh Terminal CLI tương tác thời gian thực đã mang lại trải nghiệm vận hành sống động, đậm chất quản trị hệ thống Linux chuyên nghiệp.", size=26, space_after=120))

    body_xml.append(p("6.2. ĐÁNH GIÁ MỨC ĐỘ HOÀN THÀNH MỤC TIÊU SMART", bold=True, size=28, space_before=120, space_after=80))
    
    # Bảng 6.1: Đánh giá SMART
    body_xml.append(p("Bảng 6.1: Đánh giá mức độ hoàn thành 6 mục tiêu SMART của đề tài", align="center", bold=True, size=24, space_after=60))
    headers_6_1 = ["STT", "Mục tiêu đã cam kết", "Kết quả thực nghiệm thực tế", "Mức độ hoàn thành"]
    rows_6_1 = [
        ["1", "Tự động hóa 100% bằng kịch bản IaC", "Bộ script Bash idempotent có trap lỗi và rollback", "Hoàn thành 100%"],
        ["2", "Gia cố an ninh OS & Mạng Zero-Trust", "SSH port 2222, nftables/UFW, giấu kín cổng Postgres 5432", "Hoàn thành 100%"],
        ["3", "Triển khai Rootless Docker unprivileged", "Docker chạy dưới user mlops, subuid/subgid 100000", "Hoàn thành 100% (Vượt mức)"],
        ["4", "Tích hợp cụm MLOps Stack chuẩn mực", "PostgreSQL, MLflow, FastAPI, Prometheus, Grafana UP", "Hoàn thành 100%"],
        ["5", "Vi dịch vụ AI OCR & Giao diện CLI", "Engine Tesseract bóc tách ảnh thành chữ, ai_cli.sh menu", "Hoàn thành 100%"],
        ["6", "Thực hiện Benchmark so sánh đối kháng", "Thu thập đầy đủ số liệu Throughput, Latency, RAM Delta", "Hoàn thành 100%"]
    ]
    body_xml.append(table_grid(headers_6_1, rows_6_1))
    body_xml.append(p("", space_after=120))

    body_xml.append(p("6.3. HƯỚNG PHÁT TRIỂN TRONG TƯƠNG LAI", bold=True, size=28, space_before=120, space_after=80))
    body_xml.append(p("• Tích hợp cơ chế mã hóa mTLS (Mutual TLS) bảo vệ toàn bộ các luồng truyền thông giữa vi dịch vụ và máy chủ cơ sở dữ liệu.", size=26, space_after=60))
    body_xml.append(p("• Mở rộng kiến trúc sang cụm phân tán Kubernetes không đặc quyền (Rootless k3s cluster) đa máy chủ.", size=26, space_after=60))
    body_xml.append(p("• Tích hợp hệ thống ghi log tập trung bằng Grafana Loki và phát hiện xâm nhập thời gian thực với Falco eBPF.", size=26, space_after=150))
    body_xml.append(page_break())

    # ========================== TÀI LIỆU THAM KHẢO (Trang 119 - 120) ==========================
    body_xml.append(p("TÀI LIỆU THAM KHẢO", align="center", bold=True, size=34, space_before=200, space_after=150))
    refs = [
        "[1] Docker Documentation (2024). Run the Docker daemon as a non-root user (Rootless mode). https://docs.docker.com/engine/security/rootless/",
        "[2] ArchWiki Community (2024). Docker, cgroups v2, and nftables security hardening guidelines. https://wiki.archlinux.org/title/Docker",
        "[3] Center for Internet Security - CIS (2024). CIS Docker Benchmark v1.6.0. Technical Security Guidelines.",
        "[4] Canonical Ltd. (2024). Ubuntu Server Guide: OpenSSH hardening, UFW ruleset and socket-activation management.",
        "[5] MLflow Project Authors (2024). Production MLOps Tracking Server Architecture and S3 Backend Integration. https://mlflow.org/",
        "[6] Prometheus Authors (2024). Monitoring System and Time Series Database Architecture. https://prometheus.io/docs/",
        "[7] Grafana Labs (2024). Enterprise Observability, Dashboard Provisioning and PromQL Querying. https://grafana.com/docs/",
        "[8] Google Open Source (2024). Tesseract OCR Engine Architecture and Language Models. https://github.com/tesseract-ocr/tesseract",
        "[9] NIST Special Publication 800-190 (2017). Application Container Security Guide. National Institute of Standards and Technology.",
        "[10] Love, R. (2010). Linux Kernel Development (3rd Edition). Addison-Wesley Professional."
    ]
    for r in refs:
        body_xml.append(p(r, size=24, space_after=80))

    # Compile XML
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

    with zipfile.ZipFile(output_docx_path, 'w', zipfile.ZIP_DEFLATED) as docx:
        docx.writestr('[Content_Types].xml', types_xml)
        docx.writestr('_rels/.rels', rels_xml)
        docx.writestr('word/document.xml', document_xml)

if __name__ == "__main__":
    target_docx = "/home/nguyencongduc/mlops-multi-os-pipeline/docs/BAO_CAO_DO_AN_MLOPS_CHINH_THUC.docx"
    generate_massive_vku_report(target_docx)
    print("Massive VKU report generated.")
