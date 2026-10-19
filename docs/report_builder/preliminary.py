from .styles import p, heading1, heading2, heading3, page_break, table_grid

def build_preliminary():
    body = []

    # TRANG BÌA 1 (Trang bìa chính)
    body.append(p("TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN VÀ", align="center", bold=True, size=28, space_before=150, space_after=40))
    body.append(p("TRUYỀN THÔNG VIỆT – HÀN", align="center", bold=True, size=28, space_after=40))
    body.append(p("KHOA KHOA HỌC MÁY TÍNH", align="center", bold=True, size=28, space_after=120))
    body.append(p("----🙠🙢----", align="center", size=24, space_after=250))
    body.append(p("VKU", align="center", bold=True, size=72, color="BA141A", space_after=500))
    body.append(p("ĐỒ ÁN MÔN HỌC:", align="center", bold=True, size=34, space_after=100))
    body.append(p("LINUX VÀ PHẦN MỀM NGUỒN MỞ", align="center", bold=True, size=34, space_after=300))
    body.append(p("ĐỀ TÀI: CONFIGURE AND DEPLOY MLOPS (MACHINE LEARNING OPS) SERVICES ON ARCH LINUX & UBUNTU", align="center", bold=True, size=30, color="BA141A", space_after=600))
    body.append(p("Sinh viên thực hiện :", bold=True, size=26, space_before=300, space_after=40))
    body.append(p("  1. Nguyễn Công Đức   – 24IT277 (Trưởng nhóm - Node Arch Linux)", bold=True, size=26, space_after=40))
    body.append(p("  2. Nguyễn Tùng Dương – 24IT260 (Thành viên - Node Ubuntu Infra & Security)", bold=True, size=26, space_after=40))
    body.append(p("  3. Nguyễn Văn C       – 24NS061 (Thành viên - Observability & Benchmark)", bold=True, size=26, space_after=120))
    body.append(p("Giảng viên hướng dẫn : TS. Hoàng Hữu Đức", bold=True, size=26, space_after=500))
    body.append(p("Đà Nẵng, tháng 10 năm 2026", align="center", size=26, space_before=300))
    body.append(page_break())

    # TRANG BÌA 2 (Trang phụ bìa)
    body.append(p("TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN VÀ", align="center", bold=True, size=28, space_before=150, space_after=40))
    body.append(p("TRUYỀN THÔNG VIỆT – HÀN", align="center", bold=True, size=28, space_after=40))
    body.append(p("KHOA KHOA HỌC MÁY TÍNH", align="center", bold=True, size=28, space_after=120))
    body.append(p("----🙠🙢----", align="center", size=24, space_after=250))
    body.append(p("BÁO CÁO KẾT QUẢ NGHIÊN CỨU THỰC NGHIỆM", align="center", bold=True, size=30, space_after=200))
    body.append(p("ĐỀ TÀI:", align="center", bold=True, size=28, space_after=100))
    body.append(p("NGHIÊN CỨU, CẤU HÌNH VÀ TRIỂN KHAI HỆ SINH THÁI MLOPS KHÔNG ĐẶC QUYỀN TRÊN NỀN TẢNG ARCH LINUX VÀ ĐỐI SÁNH UBUNTU SERVER", align="center", bold=True, size=28, color="002060", space_after=400))
    body.append(p("Chuyên ngành: Kỹ thuật phần mềm & Mạng máy tính", align="center", italic=True, size=26, space_after=500))
    body.append(p("Cán bộ hướng dẫn : TS. Hoàng Hữu Đức", bold=True, size=26, space_after=80))
    body.append(p("Cán bộ phản biện : Ban Giám khảo Hội đồng Khoa học máy tính", bold=True, size=26, space_after=600))
    body.append(p("Đà Nẵng, tháng 10 năm 2026", align="center", size=26, space_before=300))
    body.append(page_break())

    # LỜI CẢM ƠN
    body.append(heading1("LỜI CẢM ƠN"))
    body.append(p("Lời đầu tiên, nhóm tác giả xin bày tỏ lòng biết ơn sâu sắc và chân thành nhất đến TS. Hoàng Hữu Đức – người thầy đã trực tiếp giảng dạy học phần \"Linux và Phần mềm nguồn mở\", đồng thời luôn dành nhiều thời gian quý báu để định hướng, cố vấn học thuật và đồng hành cùng nhóm trong suốt quá trình triển khai đề tài nghiên cứu này.", indent=400))
    body.append(p("Đề tài \"Configure and Deploy MLOps (Machine Learning Ops) Services on Arch Linux & Ubuntu\" được khởi tạo từ chính những thách thức kỹ thuật nóng bỏng nhất của ngành công nghệ thông tin hiện đại: Làm thế nào để vận hành một cụm dịch vụ học máy phức tạp, đòi hỏi thông lượng xử lý cao nhưng vẫn đảm bảo tính an toàn tuyệt đối trước các nguy cơ tấn công leo thang đặc quyền hạt nhân Linux. Thầy Hoàng Hữu Đức đã hướng dẫn chúng em không chỉ dừng lại ở các thao tác dòng lệnh cơ bản, mà phải đào sâu vào bản chất kiến trúc hệ điều hành: Sự tương tác giữa User Space và Kernel Space, cơ chế điều phối tài nguyên theo phân cấp của cgroups v2, sự cô lập không gian tên User Namespaces và việc hiện thực hóa mô hình mạng Zero-Trust bằng tường lửa hiện đại nftables.", indent=400))
    body.append(p("Dưới sự dẫn dắt tận tâm của thầy, nhóm đã từng bước làm chủ quy trình Infrastructure as Code (IaC) tự động hóa hoàn toàn bằng Bash script, hiện thực hóa mô hình Rootless Containerization unprivileged trên nền tảng Arch Linux để triệt tiêu hoàn toàn nguy cơ tấn công Container Escape, đồng thời thiết lập hệ thống đo lường benchmark đối kháng định lượng với Ubuntu Server.", indent=400))
    body.append(p("Chúng em cũng xin gửi lời cảm ơn trân trọng đến Ban Giám hiệu Trường Đại học Công nghệ Thông tin và Truyền thông Việt – Hàn (VKU), Ban Chủ nhiệm Khoa Khoa Học Máy Tính cùng toàn thể quý Thầy Cô đã xây dựng chương trình đào tạo chuẩn quốc tế, tạo điều kiện thuận lợi nhất về cơ sở vật chất phòng lab để chúng em hoàn thành tốt đồ án môn học này.", indent=400))
    body.append(p("Dù đã nỗ lực hết mình và làm việc nghiêm túc với tinh thần trách nhiệm cao nhất, đồ án chắc chắn khó tránh khỏi những thiếu sót nhất định do giới hạn về mặt thời gian và kinh nghiệm thực tiễn. Nhóm sinh viên kính mong nhận được những nhận xét, góp ý quý báu của quý Thầy Cô và Hội đồng phản biện để tiếp tục hoàn thiện đề tài trong tương lai.", indent=400))
    body.append(p("Đà Nẵng, ngày 19 tháng 10 năm 2026", align="right", italic=True, size=24, space_before=200))
    body.append(p("Đại diện nhóm sinh viên thực hiện", align="right", bold=True, size=26))
    body.append(p("Nguyễn Công Đức (Trưởng nhóm)", align="right", bold=True, size=26, space_after=100))
    body.append(page_break())

    # NHẬN XÉT CỦA GIẢNG VIÊN HƯỚNG DẪN
    body.append(heading1("NHẬN XÉT CỦA GIẢNG VIÊN HƯỚNG DẪN"))
    body.append(p("(Dành cho TS. Hoàng Hữu Đức đánh giá kết quả và thái độ thực hiện đề tài)", align="center", italic=True, size=24, space_after=150))
    body.append(p("1. Đánh giá về tinh thần, thái độ làm việc của nhóm sinh viên:", bold=True, size=26, space_before=100, space_after=50))
    for _ in range(4):
        body.append(p(".....................................................................................................................................................................", color="888888", space_after=40))
    body.append(p("2. Đánh giá về tính cấp thiết, độ khó và khối lượng công việc hoàn thành:", bold=True, size=26, space_before=100, space_after=50))
    for _ in range(4):
        body.append(p(".....................................................................................................................................................................", color="888888", space_after=40))
    body.append(p("3. Đánh giá về tính sáng tạo, chất lượng kỹ thuật và kết quả thực nghiệm:", bold=True, size=26, space_before=100, space_after=50))
    for _ in range(4):
        body.append(p(".....................................................................................................................................................................", color="888888", space_after=40))
    body.append(p("4. Điểm đánh giá và kết luận:", bold=True, size=26, space_before=100, space_after=50))
    body.append(p("• Điểm bằng số: .......................................      • Điểm bằng chữ: .........................................................", space_after=50))
    body.append(p("• Cho phép bảo vệ trước Hội đồng:   [   ] Đồng ý          [   ] Không đồng ý", space_after=200))
    body.append(p("Đà Nẵng, ngày …. Tháng 10 năm 2026", align="right", italic=True, size=24))
    body.append(p("Giảng viên hướng dẫn", align="right", bold=True, size=26))
    body.append(p("(Ký và ghi rõ họ tên)", align="right", italic=True, size=22, space_after=400))
    body.append(p("TS. Hoàng Hữu Đức", align="right", bold=True, size=26))
    body.append(page_break())

    # NHẬN XÉT CỦA CÁN BỘ PHẢN BIỆN
    body.append(heading1("NHẬN XÉT CỦA CÁN BỘ PHẢN BIỆN"))
    body.append(p("(Dành cho Cán bộ chấm phản biện Hội đồng Khoa học máy tính)", align="center", italic=True, size=24, space_after=150))
    body.append(p("1. Đánh giá tính chuẩn mực và hình thức trình bày của báo cáo:", bold=True, size=26, space_before=100, space_after=50))
    for _ in range(4):
        body.append(p(".....................................................................................................................................................................", color="888888", space_after=40))
    body.append(p("2. Đánh giá tính chính xác về mặt lý thuyết hệ điều hành và công nghệ:", bold=True, size=26, space_before=100, space_after=50))
    for _ in range(4):
        body.append(p(".....................................................................................................................................................................", color="888888", space_after=40))
    body.append(p("3. Đánh giá tính ứng dụng và độ tin cậy của các số liệu thực nghiệm:", bold=True, size=26, space_before=100, space_after=50))
    for _ in range(4):
        body.append(p(".....................................................................................................................................................................", color="888888", space_after=40))
    body.append(p("4. Câu hỏi chất vấn dành cho nhóm sinh viên khi bảo vệ:", bold=True, size=26, space_before=100, space_after=50))
    body.append(p("Câu 1: ............................................................................................................................................................", space_after=40))
    body.append(p("Câu 2: ............................................................................................................................................................", space_after=150))
    body.append(p("Đà Nẵng, ngày …. Tháng 10 năm 2026", align="right", italic=True, size=24))
    body.append(p("Cán bộ phản biện", align="right", bold=True, size=26))
    body.append(p("(Ký và ghi rõ họ tên)", align="right", italic=True, size=22, space_after=400))
    body.append(page_break())

    # MỤC LỤC
    body.append(heading1("MỤC LỤC"))
    toc_items = [
        ("LỜI CẢM ƠN", "iii"),
        ("NHẬN XÉT CỦA GIẢNG VIÊN HƯỚNG DẪN", "iv"),
        ("NHẬN XÉT CỦA CÁN BỘ PHẢN BIỆN", "v"),
        ("DANH MỤC TỪ VIẾT TẮT", "viii"),
        ("DANH MỤC HÌNH ẢNH", "ix"),
        ("DANH MỤC BẢNG BIỂU", "xi"),
        ("MỞ ĐẦU", "1"),
        ("CHƯƠNG 1: TỔNG QUAN VỀ ĐỀ TÀI", "4"),
        ("  1.1. Đặt vấn đề và bối cảnh nghiên cứu", "4"),
        ("    1.1.1. Sự hội tụ giữa MLOps và hạ tầng mã nguồn mở Linux", "4"),
        ("    1.1.2. Thách thức phân phối phần mềm: Rolling Release vs. LTS", "7"),
        ("    1.1.3. Vấn đề an ninh Container mặc định và nguy cơ Container Escape", "9"),
        ("    1.1.4. Nhu cầu cấp thiết về nền tảng MLOps không đặc quyền (Rootless)", "11"),
        ("  1.2. Mục tiêu nghiên cứu của đề tài", "13"),
        ("    1.2.1. Mục tiêu tổng quát", "13"),
        ("    1.2.2. Mục tiêu kỹ thuật cụ thể", "13"),
        ("    1.2.3. Sản phẩm và kết quả mong đợi", "15"),
        ("  1.3. Đối tượng và phạm vi nghiên cứu", "16"),
        ("    1.3.1. Đối tượng nghiên cứu", "16"),
        ("    1.3.2. Phạm vi triển khai", "16"),
        ("    1.3.3. Giới hạn kỹ thuật của đề tài", "17"),
        ("  1.4. Phương pháp luận nghiên cứu", "18"),
        ("    1.4.1. Phương pháp nghiên cứu lý thuyết", "18"),
        ("    1.4.2. Phương pháp thực nghiệm đối sánh (Empirical Benchmarking)", "19"),
        ("    1.4.3. Phương pháp đánh giá an ninh đa tầng (Defense in Depth)", "20"),
        ("  1.5. Ý nghĩa khoa học và giá trị thực tiễn", "21"),
        ("    1.5.1. Ý nghĩa khoa học", "21"),
        ("    1.5.2. Giá trị thực tiễn đối với doanh nghiệp", "22"),
        ("CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ CÔNG NGHỆ CỐT LÕI", "24"),
        ("  2.1. Tổng quan hệ điều hành Linux: Arch Linux và Ubuntu Server", "24"),
        ("    2.1.1. Kiến trúc hạt nhân Linux Kernel (Kernel Space vs. User Space)", "24"),
        ("    2.1.2. Phân tích triết lý The Arch Way và mô hình Rolling Release", "27"),
        ("    2.1.3. Đặc điểm mô hình Enterprise LTS của Ubuntu Server", "30"),
        ("  2.2. Công nghệ Containerization và cơ chế cô lập hạt nhân", "32"),
        ("    2.2.1. Bản chất Container so với Máy ảo (Virtual Machine)", "32"),
        ("    2.2.2. Phân tích 6 loại Linux Namespaces trong cô lập tiến trình", "35"),
        ("    2.2.3. Cơ chế kiểm soát tài nguyên cgroups v1 và cgroups v2", "38"),
        ("  2.3. Công nghệ Rootless Container Engine", "41"),
        ("    2.3.1. Rủi ro của Docker Daemon chạy quyền Root truyền thống", "41"),
        ("    2.3.2. Kiến trúc Rootless Docker unprivileged trên Arch Linux", "44"),
        ("    2.3.3. Cơ chế ánh xạ subuid/subgid và mạng slirp4netns", "47"),
        ("  2.4. Công nghệ tường lửa Stateful: nftables vs. UFW", "50"),
        ("    2.4.1. Kiến trúc Netfilter Hooks trong Linux Kernel", "50"),
        ("    2.4.2. Bảng lọc gói tin hiệu năng cao nftables", "52"),
        ("    2.4.3. Uncomplicated Firewall (UFW) trên Ubuntu", "55"),
        ("  2.5. Hệ sinh thái công cụ MLOps mã nguồn mở", "57"),
        ("    2.5.1. Vòng đời MLOps chuẩn công nghiệp", "57"),
        ("    2.5.2. MLflow Tracking Server và PostgreSQL Metadata Store", "59"),
        ("    2.5.3. MinIO Object Storage tương thích Amazon S3", "61"),
        ("    2.5.4. Khung vi dịch vụ FastAPI và công cụ OCR Tesseract", "63"),
        ("    2.5.5. Hệ thống giám sát Prometheus và Grafana", "65"),
        ("  2.6. Tiêu chuẩn an ninh CIS Benchmark và mô hình Defense in Depth", "67"),
        ("CHƯƠNG 3: PHƯƠNG PHÁP NGHIÊN CỨU VÀ THIẾT KẾ HỆ THỐNG", "70"),
        ("  3.1. Triết lý thiết kế và quy trình nghiên cứu tổng thể", "70"),
        ("  3.2. Đặc tả yêu cầu hệ thống (System Requirements)", "73"),
        ("    3.2.1. Yêu cầu chức năng (Functional Requirements)", "73"),
        ("    3.2.2. Yêu cầu phi chức năng (Non-Functional Requirements)", "75"),
        ("  3.3. Thiết kế kiến trúc tổng thể Dual-Node MLOps Platform", "77"),
        ("    3.3.1. Sơ đồ phân tầng kiến trúc", "77"),
        ("    3.3.2. Sơ đồ luồng dữ liệu suy luận và giám sát", "80"),
        ("  3.4. Thiết kế phân đoạn mạng an ninh Zero-Trust", "82"),
        ("  3.5. Thiết kế chiến lược bảo mật 7 lớp Defense in Depth", "85"),
        ("  3.6. Thiết kế công cụ dòng lệnh tương tác và kiểm định tự động", "88"),
        ("  3.7. Kế hoạch triển khai và ma trận trách nhiệm RACI", "90"),
        ("CHƯƠNG 4: TRIỂN KHAI THỰC NGHIỆM VÀ VẬN HÀNH HỆ THỐNG", "93"),
        ("  4.1. Chuẩn bị môi trường phần cứng và phân vùng hệ thống", "93"),
        ("  4.2. Triển khai hạ tầng và gia cố bảo mật Node Arch Linux", "95"),
        ("    4.2.1. Thiết lập tài khoản mlops unprivileged", "95"),
        ("    4.2.2. Hardening OpenSSH Server trên cổng 2222", "96"),
        ("    4.2.3. Tinh chỉnh tham số hạt nhân Linux sysctl cho MLOps", "98"),
        ("    4.2.4. Xây dựng bộ quy tắc tường lửa stateful nftables", "100"),
        ("    4.2.5. Cơ chế Rollback tự động phục hồi an ninh", "103"),
        ("  4.3. Cài đặt và cấu hình Rootless Docker Engine trên Arch Linux", "105"),
        ("    4.3.1. Cấu hình User Namespaces và subuid/subgid", "105"),
        ("    4.3.2. Thiết lập ủy quyền tài nguyên cgroups v2", "107"),
        ("    4.3.3. Kích hoạt tính năng Systemd User Lingering", "109"),
        ("  4.4. Đóng gói và tối ưu hóa vi dịch vụ AI OCR bằng FastAPI", "111"),
        ("    4.4.1. Kỹ thuật Multi-Stage Dockerfile", "111"),
        ("    4.4.2. Thực thi dưới tài khoản không đặc quyền UID 10001", "113"),
        ("    4.4.3. Tích hợp endpoint thu thập metrics cho Prometheus", "115"),
        ("  4.5. Triển khai MLOps Core Stack với Docker Compose", "117"),
        ("    4.5.1. Cấu trúc tệp docker-compose.yml đa phân vùng mạng", "117"),
        ("    4.5.2. Kết nối MLflow Server với PostgreSQL và MinIO", "120"),
        ("    4.5.3. Tự động hóa vòng đời dịch vụ bằng Systemd User Service", "122"),
        ("  4.6. Xây dựng công cụ Terminal CLI tương tác thời gian thực", "124"),
        ("    4.6.1. Thiết kế Menu điều khiển ANSI Color", "124"),
        ("    4.6.2. Phân tích kết quả quét OCR và đo đạc thời gian xử lý", "127"),
        ("  4.7. Triển khai đối sánh Node Ubuntu Server 22.04 LTS", "129"),
        ("    4.7.1. Xử lý bài toán SSH socket-activation trên Ubuntu", "129"),
        ("    4.7.2. Cấu hình tường lửa UFW và sao lưu trạng thái", "131"),
        ("    4.7.3. Triển khai Docker Daemon cấp hệ thống", "133"),
        ("  4.8. Triển khai hệ thống giám sát Prometheus và Grafana", "135"),
        ("  4.9. Vận hành kịch bản kiểm định an ninh tự động 04_verify_system.sh", "138"),
        ("CHƯƠNG 5: ĐÁNH GIÁ ĐỊNH LƯỢNG BENCHMARK VÀ BẢO MẬT", "142"),
        ("  5.1. Kết quả kiểm chứng an ninh và Zero-Trust Network", "142"),
        ("  5.2. Đánh giá bảo mật: Rootless Docker vs. Rootful Docker", "146"),
        ("    5.2.1. Thử nghiệm tấn công leo thang Container Escape", "146"),
        ("    5.2.2. Kiểm tra quyền sở hữu tệp tin trên Host Filesystem", "148"),
        ("  5.3. Đánh giá đối kháng tài nguyên phần cứng (Resource Footprint)", "150"),
        ("    5.3.1. Chiếm dụng bộ nhớ RAM tĩnh khi khởi động (Idle OS)", "150"),
        ("    5.3.2. Chiếm dụng bộ nhớ RAM động khi vận hành cụm MLOps Stack", "153"),
        ("    5.3.3. Thời gian khởi động hệ thống và độ gọn nhẹ phần mềm", "155"),
        ("  5.4. Thử nghiệm tải trọng vi dịch vụ AI Inference (Load Testing)", "157"),
        ("    5.4.1. Thiết lập kịch bản kiểm thử tải với Locust / Benchmark", "157"),
        ("    5.4.2. So sánh thông lượng xử lý trung bình (Requests/Second)", "159"),
        ("    5.4.3. Phân tích độ trễ phân vị p50, p95 và p99", "162"),
        ("  5.5. Đánh giá công nghệ tường lửa: nftables vs. UFW", "165"),
        ("  5.6. Phân tích đánh đổi kỹ thuật (Trade-offs) và bài học kinh nghiệm", "168"),
        ("CHƯƠNG 6: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN", "172"),
        ("  6.1. Kết luận tổng quan đề tài", "172"),
        ("    6.1.1. Tóm tắt các kết quả đạt được", "172"),
        ("    6.1.2. Mức độ hoàn thành các mục tiêu đề ra", "174"),
        ("    6.1.3. Đóng góp khoa học và kỹ thuật của đồ án", "176"),
        ("  6.2. Hướng phát triển và mở rộng trong tương lai", "178"),
        ("CHƯƠNG 7: TÀI LIỆU THAM KHẢO", "181")
    ]
    for item, pg in toc_items:
        is_cap = item.startswith("CHƯƠNG") or item in ["LỜI CẢM ƠN", "NHẬN XÉT CỦA GIẢNG VIÊN HƯỚNG DẪN", "NHẬN XÉT CỦA CÁN BỘ PHẢN BIỆN", "DANH MỤC TỪ VIẾT TẮT", "DANH MỤC HÌNH ẢNH", "DANH MỤC BẢNG BIỂU", "MỞ ĐẦU", "CHƯƠNG 7: TÀI LIỆU THAM KHẢO"]
        dots = ". " * int((88 - len(item)) / 2)
        body.append(p(f"{item} {dots} {pg}", bold=is_cap, size=23 if is_cap else 21, color="002060" if is_cap else "000000", space_after=30))
    body.append(page_break())

    # DANH MỤC TỪ VIẾT TẮT
    body.append(heading1("DANH MỤC TỪ VIẾT TẮT"))
    abbr_headers = ["Từ viết tắt", "Tên tiếng Anh đầy đủ", "Ý nghĩa / Giải thích chuyên ngành"]
    abbr_rows = [
        ["MLOps", "Machine Learning Operations", "Quy trình vận hành, triển khai và tự động hóa vòng đời mô hình học máy."],
        ["IaC", "Infrastructure as Code", "Quản lý và cấp phát hạ tầng CNTT tự động thông qua mã kịch bản."],
        ["OS", "Operating System", "Hệ điều hành máy tính (Arch Linux, Ubuntu Server)."],
        ["LTS", "Long-Term Support", "Mô hình hỗ trợ dài hạn (thường từ 5 năm của Ubuntu)."],
        ["UID / GID", "User Identifier / Group Identifier", "Định danh người dùng và nhóm người dùng trong hệ điều hành Linux."],
        ["cgroups", "Control Groups", "Tính năng nhân Linux giới hạn và cô lập tài nguyên CPU, RAM, I/O."],
        ["CIS", "Center for Internet Security", "Tổ chức bảo mật phi lợi nhuận ban hành các tiêu chuẩn an ninh hệ thống."],
        ["CVE", "Common Vulnerabilities and Exposures", "Hệ thống danh mục các lỗ hổng và rủi ro an ninh thông tin đã biết."],
        ["DoD / DiD", "Defense in Depth", "Chiến lược an ninh phòng thủ đa tầng theo chiều sâu."],
        ["RPS", "Requests Per Second", "Số lượng yêu cầu API được xử lý thành công trong một giây."],
        ["TSDB", "Time Series Database", "Cơ sở dữ liệu chuỗi thời gian chuyên dụng cho giám sát (Prometheus)."],
        ["OCR", "Optical Character Recognition", "Công nghệ nhận dạng ký tự quang học từ tệp tin hình ảnh."],
        ["mTLS", "Mutual Transport Layer Security", "Giao thức xác thực lẫn nhau giữa hai đầu nút giao tiếp mạng."],
        ["UFW", "Uncomplicated Firewall", "Giao diện quản trị tường lửa đơn giản trên các bản phân phối Debian/Ubuntu."]
    ]
    body.append(table_grid(abbr_headers, abbr_rows))
    body.append(page_break())

    # DANH MỤC HÌNH ẢNH
    body.append(heading1("DANH MỤC HÌNH ẢNH"))
    figs = [
        ("Hình 1.1: Vòng đời phần mềm Rolling Release (Arch Linux) vs. Fixed Release LTS (Ubuntu)", "5"),
        ("Hình 1.2: Chu trình khép kín của nền tảng MLOps trong môi trường sản xuất", "8"),
        ("Hình 1.3: Mô hình tấn công phá rào Container Escape khi Docker daemon chạy quyền root", "10"),
        ("Hình 2.1: Kiến trúc phân tầng nhân Linux: Phân định ranh giới User Space và Kernel Space", "25"),
        ("Hình 2.2: So sánh kiến trúc cô lập giữa Máy ảo truyền thống (Hypervisor) và Container", "33"),
        ("Hình 2.3: Mô hình 6 không gian tên Linux Namespaces cô lập tiến trình ứng dụng", "36"),
        ("Hình 2.4: Cây phân cấp quản trị và giới hạn tài nguyên phân tán cgroups v2", "39"),
        ("Hình 2.5: Kiến trúc Rootless Docker unprivileged và cơ chế cầu nối mạng slirp4netns", "45"),
        ("Hình 2.6: Sơ đồ luồng duyệt gói tin qua các Netfilter Hooks trong nhân Linux Kernel", "51"),
        ("Hình 2.7: Kiến trúc vi dịch vụ thu thập chỉ số chuỗi thời gian Prometheus và Grafana", "66"),
        ("Hình 3.1: Kiến trúc tổng thể phân tầng Dual-Node MLOps Isolation Architecture", "78"),
        ("Hình 3.2: Sơ đồ luồng dữ liệu suy luận AI OCR và luồng giám sát chỉ số từ xa", "81"),
        ("Hình 3.3: Sơ đồ phân đoạn mạng Zero-Trust: mlops-frontend và mlops-backend", "83"),
        ("Hình 3.4: Chiến lược an ninh phòng thủ chiều sâu Defense in Depth với 7 lớp pháo đài", "86"),
        ("Hình 3.5: Tiến độ thực hiện đề tài trong 6 tuần theo biểu đồ Gantt", "91"),
        ("Hình 4.1: Cấu trúc thư mục mã nguồn tự động hóa Infrastructure as Code (IaC)", "94"),
        ("Hình 4.2: Tệp dịch vụ quản lý vòng đời MLOps Stack cấp người dùng mlops-stack.service", "123"),
        ("Hình 4.3: Giao diện Terminal tương tác AI OCR Scanner hoạt động trực tiếp (ai_cli.sh)", "125"),
        ("Hình 4.4: Màn hình kết quả nhận diện ký tự từ ảnh chụp và đo lường độ trễ trên Terminal", "128"),
        ("Hình 4.5: Kết quả kiểm tra toàn diện 5 bài kiểm tra an ninh bằng script 04_verify_system.sh", "140"),
        ("Hình 5.1: Biểu đồ chiếm dụng bộ nhớ RAM tĩnh (Idle OS) giữa Arch Linux và Ubuntu Server", "151"),
        ("Hình 5.2: Biểu đồ tiêu thụ RAM khi vận hành toàn bộ 5 vi dịch vụ MLOps Stack", "154"),
        ("Hình 5.3: Biểu đồ so sánh thông lượng xử lý suy luận trung bình (Requests Per Second)", "160"),
        ("Hình 5.4: Biểu đồ phân bổ độ trễ phân vị p50, p95 và p99 dưới tải trọng 500 requests", "163")
    ]
    for f_name, f_pg in figs:
        dots = ". " * int((88 - len(f_name)) / 2)
        body.append(p(f"{f_name} {dots} {f_pg}", size=22, space_after=30))
    body.append(page_break())

    # DANH MỤC BẢNG BIỂU
    body.append(heading1("DANH MỤC BẢNG BIỂU"))
    tbls = [
        ("Bảng 1.1: So sánh đặc tính kiến trúc giữa Arch Linux (Rolling) và Ubuntu Server (LTS)", "6"),
        ("Bảng 1.2: Các sự cố an ninh nghiêm trọng bắt nguồn từ việc chạy Docker đặc quyền root", "11"),
        ("Bảng 1.3: Ma trận phân bổ trách nhiệm thành viên nhóm theo chuẩn RACI", "23"),
        ("Bảng 2.1: Phân loại và chức năng của 6 loại Linux Namespaces", "37"),
        ("Bảng 2.2: So sánh kỹ thuật giữa cơ chế cgroups v1 và kiến trúc cây đơn cgroups v2", "40"),
        ("Bảng 2.3: Ma trận đối sánh an ninh giữa Rootless Docker và Rootful Docker truyền thống", "48"),
        ("Bảng 2.4: So sánh cú pháp, kiến trúc thực thi giữa nftables và UFW", "56"),
        ("Bảng 3.1: Quy hoạch không gian địa chỉ IP, cổng dịch vụ và chính sách mạng", "84"),
        ("Bảng 3.2: Ma trận rủi ro hệ thống và biện pháp đối phó tương ứng", "87"),
        ("Bảng 4.1: Danh mục các tham số hạt nhân Linux sysctl tối ưu hóa cho MLOps", "99"),
        ("Bảng 4.2: Phân tích các tầng chỉ thị trong Dockerfile tối ưu hóa FastAPI OCR Microservice", "114"),
        ("Bảng 5.1: Bảng tổng hợp kết quả kiểm chứng an ninh 5 chốt chặn Zero-Trust", "144"),
        ("Bảng 5.2: Bảng đo lường chiếm dụng bộ nhớ RAM tĩnh và động giữa hai hệ điều hành", "152"),
        ("Bảng 5.3: Bảng tổng hợp số liệu Benchmark hiệu năng vi dịch vụ AI Inference", "161"),
        ("Bảng 5.4: Bảng phân tích các điểm đánh đổi kỹ thuật (Trade-offs) trong triển khai", "169"),
        ("Bảng 6.1: Đánh giá mức độ hoàn thành 6 mục tiêu SMART đã cam kết trong đề tài", "175")
    ]
    for t_name, t_pg in tbls:
        dots = ". " * int((88 - len(t_name)) / 2)
        body.append(p(f"{t_name} {dots} {t_pg}", size=22, space_after=30))
    body.append(page_break())

    return body
