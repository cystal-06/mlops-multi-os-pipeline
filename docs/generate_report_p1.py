import zipfile
import xml.sax.saxutils as saxutils

def generate_part1_docx(output_path):
    # XML Document Generation following VKU format for first 20 pages
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

    # ---------------- PAGE 1: BÌA CHÍNH ----------------
    body_xml.append(p("TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN VÀ", align="center", bold=True, size=28, space_before=200, space_after=50))
    body_xml.append(p("TRUYỀN THÔNG VIỆT – HÀN", align="center", bold=True, size=28, space_after=50))
    body_xml.append(p("KHOA KHOA HỌC MÁY TÍNH", align="center", bold=True, size=28, space_after=150))
    body_xml.append(p("----🙠🙢----", align="center", size=24, space_after=300))
    body_xml.append(p("VKU", align="center", bold=True, size=72, color="BA141A", space_after=600))
    body_xml.append(p("ĐỒ ÁN MÔN HỌC:", align="center", bold=True, size=36, space_after=100))
    body_xml.append(p("LINUX VÀ PHẦN MỀM NGUỒN MỞ", align="center", bold=True, size=36, space_after=400))
    body_xml.append(p("ĐỀ TÀI: Configure and Deploy MLOps (Machine Learning Ops) Services on Arch Linux & Ubuntu", align="center", bold=True, size=32, color="BA141A", space_after=800))
    
    body_xml.append(p("Sinh viên thực hiện : Nguyễn Công Đức (Trưởng nhóm - Arch Linux)", bold=True, size=26, space_before=400, space_after=50))
    body_xml.append(p("                      Nguyễn Tùng Dương (Thành viên - Ubuntu Infra)", bold=True, size=26, space_after=50))
    body_xml.append(p("                      Thành viên 3 (Thành viên - Observability & Benchmark)", bold=True, size=26, space_after=150))
    body_xml.append(p("Giảng viên hướng dẫn : TS. Hoàng Hữu Đức", bold=True, size=26, space_after=600))
    body_xml.append(p("Đà Nẵng, tháng 10 năm 2026", align="center", size=26, space_before=400))
    body_xml.append(page_break())

    # ---------------- PAGE 2: LỜI CẢM ƠN ----------------
    body_xml.append(p("LỜI CẢM ƠN", align="center", bold=True, size=36, space_before=300, space_after=300))
    body_xml.append(p("Em xin gửi lời cảm ơn chân thành đến TS. Hoàng Hữu Đức – người thầy đã tận tình hướng dẫn, đồng hành và hỗ trợ chúng em trong suốt quá trình thực hiện đề tài \"Configure and Deploy MLOps (Machine Learning Ops) Services on Arch Linux & Ubuntu\".", size=26, space_after=150))
    body_xml.append(p("Ngay từ những ngày đầu hình thành ý tưởng, thầy đã định hướng rõ ràng cho nhóm về bản chất môn học: tập trung sâu vào kỹ thuật quản trị hệ thống Linux, kiến trúc hạt nhân (Kernel), kỹ thuật gia cố bảo mật chuyên sâu (Security Hardening), và so sánh đối kháng thực nghiệm giữa hai trường phái Linux đối lập: Arch Linux (Rolling Release, DIY) và Ubuntu Server (LTS, Enterprise).", size=26, space_after=150))
    body_xml.append(p("Trong suốt quá trình triển khai – từ việc xây dựng script tự động hóa Bash idempotent, cấu hình tường lửa nftables và UFW, thiết lập cơ chế cô lập Rootless Docker qua User Namespaces và cgroups v2, đến đóng gói microservice AI OCR và giám sát Prometheus/Grafana – nhóm em luôn nhận được những lời khuyên sâu sắc, sự hỗ trợ kỹ thuật và nguồn động viên quý báu từ thầy.", size=26, space_after=150))
    body_xml.append(p("Chúng em cũng xin gửi lời cảm ơn chân thành đến quý Thầy Cô trong Khoa Khoa Học Máy Tính và Hội đồng phản biện Trường Đại học Công nghệ Thông tin và Truyền thông Việt – Hàn đã tạo điều kiện thuận lợi nhất để nhóm hoàn thành và báo cáo đồ án.", size=26, space_after=150))
    body_xml.append(p("Một lần nữa, chúng em kính chúc thầy luôn dồi dào sức khỏe, hạnh phúc và gặt hái thêm nhiều thành công rực rỡ trong sự nghiệp nghiên cứu và giảng dạy.", size=26, space_after=300))
    body_xml.append(p("Chúng em xin chân thành cảm ơn!", align="right", bold=True, size=26))
    body_xml.append(page_break())

    # ---------------- PAGE 3: NHẬN XÉT CỦA GIẢNG VIÊN ----------------
    body_xml.append(p("NHẬN XÉT", align="center", bold=True, size=36, space_before=300, space_after=100))
    body_xml.append(p("(Của giảng viên hướng dẫn)", align="center", size=26, space_after=300))
    for _ in range(16):
        body_xml.append(p("....................................................................................................................................................................", size=24, space_after=80))
    body_xml.append(p("Đà Nẵng, ngày .... tháng 10 năm 2026", align="right", size=26, space_before=200))
    body_xml.append(p("Chữ ký giảng viên hướng dẫn", align="right", bold=True, size=26, space_after=400))
    body_xml.append(p("TS. Hoàng Hữu Đức", align="right", bold=True, size=28))
    body_xml.append(page_break())

    # ---------------- PAGE 4: MỤC LỤC TỔNG QUÁT ----------------
    body_xml.append(p("MỤC LỤC", align="center", bold=True, size=36, space_before=200, space_after=200))
    body_xml.append(p("LỜI CẢM ƠN ...................................................................................................................................... 2", size=24, space_after=60))
    body_xml.append(p("NHẬN XÉT CỦA GIẢNG VIÊN ..................................................................................................... 3", size=24, space_after=60))
    body_xml.append(p("MỤC LỤC ........................................................................................................................................... 4", size=24, space_after=60))
    body_xml.append(p("DANH MỤC HÌNH ẢNH ................................................................................................................ 6", size=24, space_after=60))
    body_xml.append(p("DANH MỤC BẢNG BIỂU ............................................................................................................... 7", size=24, space_after=60))
    body_xml.append(p("MỞ ĐẦU ........................................................................................................................................... 8", size=24, bold=True, space_after=60))
    body_xml.append(p("CHƯƠNG 1: TỔNG QUAN VỀ ĐỀ TÀI ....................................................................................... 10", size=24, bold=True, space_after=60))
    body_xml.append(p("  1.1. Đặt vấn đề ................................................................................................................................. 10", size=24, space_after=40))
    body_xml.append(p("    1.1.1. Bối cảnh MLOps và nhu cầu chuẩn hóa hạ tầng Linux ..................................................... 10", size=24, space_after=40))
    body_xml.append(p("    1.1.2. Thách thức phân phối phần mềm: Rolling Release vs. LTS .................................................. 12", size=24, space_after=40))
    body_xml.append(p("    1.1.3. Lỗ hổng bảo mật đặc quyền Root trên Container Docker truyền thống .................................. 13", size=24, space_after=40))
    body_xml.append(p("  1.2. Mục tiêu đề tài ........................................................................................................................... 14", size=24, space_after=40))
    body_xml.append(p("    1.2.1. Mục tiêu tổng quát ................................................................................................................ 14", size=24, space_after=40))
    body_xml.append(p("    1.2.2. Các mục tiêu cụ thể ............................................................................................................... 15", size=24, space_after=40))
    body_xml.append(p("    1.2.3. Kết quả mong đợi .................................................................................................................. 16", size=24, space_after=40))
    body_xml.append(p("  1.3. Đối tượng và phạm vi nghiên cứu .......................................................................................... 17", size=24, space_after=40))
    body_xml.append(p("  1.4. Phương pháp nghiên cứu và thực nghiệm .............................................................................. 18", size=24, space_after=40))
    body_xml.append(p("  1.5. Ý nghĩa khoa học và thực tiễn của đề tài ................................................................................. 19", size=24, space_after=40))
    body_xml.append(p("CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ KIẾN TRÚC HỆ THỐNG .................................................... 21", size=24, bold=True, space_before=100, space_after=60))
    body_xml.append(p("CHƯƠNG 3: THIẾT KẾ VÀ QUY CHUẨN TRIỂN KHAI IAC ........................................................ 35", size=24, bold=True, space_after=60))
    body_xml.append(p("CHƯƠNG 4: TRIỂN KHAI VÀ THỰC NGHIỆM ĐỐI KHÁNG ..................................................... 48", size=24, bold=True, space_after=60))
    body_xml.append(p("CHƯƠNG 5: ĐÁNH GIÁ ĐỊNH LƯỢNG BENCHMARK & BẢO MẬT .......................................... 62", size=24, bold=True, space_after=60))
    body_xml.append(p("CHƯƠNG 6: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN ................................................................... 72", size=24, bold=True, space_after=60))
    body_xml.append(p("TÀI LIỆU THAM KHẢO ................................................................................................................. 76", size=24, bold=True, space_after=60))
    body_xml.append(page_break())

    # ---------------- PAGE 5: DANH MỤC HÌNH ẢNH & BẢNG ----------------
    body_xml.append(p("DANH MỤC HÌNH ẢNH & BẢNG BIỂU", align="center", bold=True, size=32, space_before=200, space_after=200))
    body_xml.append(p("Hình 1.1: So sánh vòng đời phát hành giữa Rolling Release (Arch) và LTS (Ubuntu) .................... 12", size=24, space_after=50))
    body_xml.append(p("Hình 1.2: Mô hình tấn công Container Escape khi chia sẻ chung User Namespace root .................. 14", size=24, space_after=50))
    body_xml.append(p("Hình 2.1: Sơ đồ kiến trúc phân tầng Dual-Node MLOps Platform ................................................... 22", size=24, space_after=50))
    body_xml.append(p("Hình 2.2: Cơ chế ánh xạ User Namespaces (subuid/subgid) trong Rootless Docker ........................ 27", size=24, space_after=50))
    body_xml.append(p("Hình 2.3: Kiến trúc lọc gói tin Stateful Firewall bằng nftables trên Arch Linux ......................... 31", size=24, space_after=50))
    body_xml.append(p("Hình 3.1: Sơ đồ luồng phân tách mạng Zero-Trust giữa frontend và backend database ................. 38", size=24, space_after=50))
    body_xml.append(p("Hình 4.1: Log Terminal quá trình cài đặt tự động 01_system_hardening.sh ................................... 50", size=24, space_after=50))
    body_xml.append(p("Hình 4.2: Kết quả kiểm tra trạng thái Docker daemon cấp unprivileged user ................................. 54", size=24, space_after=50))
    body_xml.append(p("Hình 4.3: Giao diện Terminal tương tác AI OCR Scanner (ai_cli.sh) ............................................... 58", size=24, space_after=50))
    body_xml.append(p("Hình 5.1: Biểu đồ giám sát thời gian thực CPU và RAM trên Grafana Dashboard ........................... 65", size=24, space_after=150))
    
    body_xml.append(p("Bảng 1.1: Ma trận so sánh tính năng cốt lõi giữa Arch Linux và Ubuntu Server ............................. 13", size=24, space_after=50))
    body_xml.append(p("Bảng 2.1: Danh mục dịch vụ MLOps và quy hoạch cổng mạng ....................................................... 24", size=24, space_after=50))
    body_xml.append(p("Bảng 4.1: Danh mục các bài kiểm tra tự động trong 04_verify_system.sh ..................................... 56", size=24, space_after=50))
    body_xml.append(p("Bảng 5.1: Kết quả Benchmark so sánh thông lượng RPS và độ trễ p95 giữa 2 hệ điều hành ............ 68", size=24, space_after=50))
    body_xml.append(p("Bảng 5.2: So sánh lượng chiếm dụng RAM tĩnh và động (Footprint Analysis) ............................... 70", size=24, space_after=50))
    body_xml.append(page_break())

    # ---------------- PAGE 6 - 8: MỞ ĐẦU ----------------
    body_xml.append(p("MỞ ĐẦU", align="center", bold=True, size=36, space_before=200, space_after=200))
    body_xml.append(p("Trong làn sóng bùng nổ của Trí tuệ nhân tạo (AI) và Học máy (Machine Learning), việc chuyển giao các mô hình từ môi trường thử nghiệm sang vận hành thực tế đã đặt ra một tiêu chuẩn mới mang tên MLOps (Machine Learning Operations). Tương tự như DevOps trong phát triển phần mềm truyền thống, MLOps đòi hỏi sự kết hợp chặt chẽ giữa mã nguồn, dữ liệu, cấu hình hạ tầng và quy trình tự động hóa. Tuy nhiên, một hệ thống MLOps hiện đại không thể vận hành tách rời khỏi nền tảng cốt lõi của nó: Hệ điều hành Linux.", size=26, space_after=150))
    body_xml.append(p("Linux hiện diện ở hơn 90% các máy chủ tính toán hiệu năng cao, siêu máy tính và trung tâm dữ liệu trên thế giới. Dẫu vậy, thế giới mã nguồn mở Linux không phải là một khối đồng nhất, mà phân hóa sâu sắc thành hai trường phái triết lý phát triển hoàn toàn trái ngược nhau:", size=26, space_after=150))
    body_xml.append(p("• Trường phái Rolling Release (tiêu biểu là Arch Linux): Đại diện cho sự tự do, triết lý tối giản (\"The Arch Way\"), liên tục cập nhật hạt nhân Linux Kernel và các gói phần mềm lên phiên bản mới nhất ngay khi phát hành. Đây là môi trường lý tưởng cho các kỹ sư muốn tiếp cận công nghệ hạt nhân mới nhất, khả năng tùy biến sâu và kiểm soát tối đa từng byte tài nguyên hệ thống.", size=26, space_after=100))
    body_xml.append(p("• Trường phái Long-Term Support - LTS (tiêu biểu là Ubuntu Server): Đại diện cho tính ổn định, chuẩn mực doanh nghiệp, với chu kỳ phát hành có kế hoạch và cam kết hỗ trợ bảo mật nhiều năm. Ubuntu cung cấp cấu hình mặc định sẵn sàng sử dụng (Out-of-the-box), giảm thiểu chi phí quản trị nhưng chấp nhận sử dụng các phiên bản kernel và gói phần mềm cũ hơn.", size=26, space_after=150))
    body_xml.append(p("Vấn đề đặt ra là: Trong cùng một khối lượng công việc MLOps cụ thể (bao gồm theo dõi thí nghiệm với MLflow, lưu trữ metadata PostgreSQL, lưu trữ artifact S3 MinIO, phục vụ mô hình FastAPI và giám sát Prometheus/Grafana), sự khác biệt về triết lý hệ điều hành, cơ chế bảo mật (tường lửa nftables so với UFW), và đặc biệt là phương thức containerization (Rootless Docker unprivileged so với Docker daemon truyền thống) sẽ tạo ra sự khác biệt như thế nào về độ an toàn và hiệu năng?", size=26, space_after=150))
    body_xml.append(p("Phần lớn các tài liệu kỹ thuật hiện nay chỉ tập trung triển khai container trên một hệ điều hành duy nhất mà bỏ qua việc so sánh đối kháng thực nghiệm giữa hai nền tảng đối lập này. Bên cạnh đó, việc lạm dụng quyền root trong quản trị container Docker đã và đang gây ra các thảm họa bảo mật nghiêm trọng (như lỗ hổng container escape, lộ Docker socket).", size=26, space_after=150))
    body_xml.append(p("Xuất phát từ thực tiễn trên, nhóm nghiên cứu đã lựa chọn thực hiện đề tài: \"Configure and Deploy MLOps (Machine Learning Ops) Services on Arch Linux & Ubuntu\". Đề tài tập trung xây dựng hai môi trường độc lập hoàn toàn, tự động hóa 100% bằng Infrastructure as Code (Bash Script), áp dụng các tiêu chuẩn an ninh khắt khe nhất của hệ điều hành Linux và đo lường định lượng hiệu năng thực tế.", size=26, space_after=150))
    body_xml.append(page_break())

    # ---------------- PAGE 9 - 14: CHƯƠNG 1: TỔNG QUAN VỀ ĐỀ TÀI ----------------
    body_xml.append(p("CHƯƠNG 1: TỔNG QUAN VỀ ĐỀ TÀI", align="center", bold=True, size=36, space_before=200, space_after=200))
    body_xml.append(p("1.1. ĐẶT VẤN ĐỀ", bold=True, size=28, space_before=150, space_after=100))
    body_xml.append(p("1.1.1. Bối cảnh MLOps và nhu cầu chuẩn hóa hạ tầng Linux", bold=True, size=26, space_before=100, space_after=80))
    body_xml.append(p("MLOps là sự giao thoa giữa Khoa học dữ liệu (Data Science), Kỹ thuật phần mềm (Software Engineering) và Vận hành hệ thống (Operations). Khác với các ứng dụng web thông thường, hệ thống MLOps đòi hỏi sự phối hợp nhịp nhàng giữa nhiều dịch vụ có trạng thái (stateful) và không trạng thái (stateless):", size=26, space_after=100))
    body_xml.append(p("- MLflow Tracking Server: Đóng vai trò máy chủ trung tâm ghi nhận metadata thí nghiệm, thông số siêu dữ liệu và quản lý phiên bản mô hình (Model Registry).", size=26, space_after=60))
    body_xml.append(p("- PostgreSQL Relational Database: Cơ sở dữ liệu quan hệ mạnh mẽ đảm bảo tính toàn vẹn dữ liệu cho MLflow thay thế cho SQLite đơn luồng.", size=26, space_after=60))
    body_xml.append(p("- MinIO Object Storage: Hệ thống lưu trữ đối tượng tương thích chuẩn Amazon S3, tối ưu hóa cho các tệp nhị phân model nặng.", size=26, space_after=60))
    body_xml.append(p("- FastAPI Inference Microservice: Dịch vụ web bất đồng bộ hiệu năng cao phục vụ nhận diện chữ từ hình ảnh (AI OCR Scanner), xuất metrics thời gian thực.", size=26, space_after=60))
    body_xml.append(p("- Prometheus & Grafana: Cụm giám sát chuỗi thời gian (TSDB) và hiển thị trực quan tài nguyên phần cứng máy chủ cùng lưu lượng mạng.", size=26, space_after=120))
    body_xml.append(p("Toàn bộ các thành phần này đòi hỏi một hạ tầng hệ điều hành Linux ổn định, khả năng quản trị tài nguyên CPU/RAM chặt chẽ và cơ chế bảo mật mạng nghiêm ngặt.", size=26, space_after=150))

    body_xml.append(p("1.1.2. Thách thức phân phối phần mềm: Rolling Release vs. LTS", bold=True, size=26, space_before=100, space_after=80))
    body_xml.append(p("Trong quản trị hệ thống Linux, việc lựa chọn bản phân phối (Linux Distribution) luôn là quyết định mang tính chiến lược của doanh nghiệp:", size=26, space_after=100))
    body_xml.append(p("• Arch Linux (Rolling Release): Không có khái niệm phiên bản cố định. Hệ điều hành liên tục nhận các bản vá hạt nhân Kernel mới nhất từ nhánh phát triển upstream của Linus Torvalds. Người quản trị phải tự tay cấu hình từng thành phần (DIY). Điều này mang lại hiệu năng tối đa và tính năng mới nhất của cgroups v2, nhưng đòi hỏi trình độ chuyên môn cao để đảm bảo hệ thống không bị đổ vỡ.", size=26, space_after=100))
    body_xml.append(p("• Ubuntu Server (LTS): Phát hành định kỳ 2 năm một lần với 5 năm hỗ trợ an ninh. Các gói phần mềm được đóng băng phiên bản để ưu tiên độ ổn định tuyệt đối. Mặc dù dễ vận hành, nhưng hệ thống thường phải dùng các phiên bản kernel cũ và cấu hình mặc định đôi khi chưa được tối ưu hóa cho tải MLOps hiệu năng cao.", size=26, space_after=150))

    body_xml.append(p("1.1.3. Lỗ hổng bảo mật đặc quyền Root trên Container Docker truyền thống", bold=True, size=26, space_before=100, space_after=80))
    body_xml.append(p("Theo mặc định, Docker daemon chạy dưới quyền root (UID 0) của hệ thống host. Các container bên trong cũng chạy với UID 0. Đây là một lỗ hổng an ninh mang tính hệ thống:", size=26, space_after=100))
    body_xml.append(p("- Container Escape: Nếu một lỗ hổng thực thi mã từ xa (RCE) xảy ra trong ứng dụng AI (ví dụ: tràn bộ đệm xử lý ảnh), kẻ tấn công chiếm được quyền root trong container và có thể vượt rào thoát ra chiếm toàn quyền kiểm soát máy tính thật (Host OS). Lỗ hổng runc CVE-2019-5736 là bằng chứng tiêu biểu.", size=26, space_after=80))
    body_xml.append(p("- Lộ Docker Socket (/var/run/docker.sock): Bất kỳ người dùng nào có quyền ghi vào socket này đều tương đương nắm giữ quyền root tối cao của máy chủ.", size=26, space_after=120))
    body_xml.append(p("Để giải quyết triệt để vấn đề này, đề tài triển khai công nghệ Rootless Docker trên Arch Linux — nơi Docker daemon và toàn bộ container chạy hoàn toàn dưới một tài khoản người dùng không đặc quyền (non-root), sử dụng User Namespaces (subuid/subgid) để đảm bảo dù container bị chiếm quyền, kẻ tấn công vẫn vô hại trên hệ thống host.", size=26, space_after=150))

    body_xml.append(p("1.2. MỤC TIÊU ĐỀ TÀI", bold=True, size=28, space_before=150, space_after=100))
    body_xml.append(p("1.2.1. Mục tiêu tổng quát", bold=True, size=26, space_before=100, space_after=80))
    body_xml.append(p("Thiết kế, tự động hóa và triển khai hoàn chỉnh hai hệ thống MLOps độc lập trên hai bản phân phối Linux đối lập (Arch Linux và Ubuntu Server); thực hiện so sánh đối kháng định lượng về mức độ bảo mật, thông lượng phục vụ API và mức tiêu thụ tài nguyên phần cứng.", size=26, space_after=120))

    body_xml.append(p("1.2.2. Các mục tiêu cụ thể", bold=True, size=26, space_before=100, space_after=80))
    body_xml.append(p("1. Tự động hóa 100% bằng Infrastructure as Code: Xây dựng bộ script Bash idempotent tuân thủ strict mode (set -euo pipefail), có bẫy lỗi và có script rollback tương ứng cho cả hai hệ điều hành.", size=26, space_after=60))
    body_xml.append(p("2. Gia cố an ninh hệ điều hành (OS Hardening): Đổi cổng SSH sang port 2222, cấm đăng nhập root; triển khai tường lửa gốc nftables có rate-limiting chống brute-force trên Arch Linux và UFW trên Ubuntu Server.", size=26, space_after=60))
    body_xml.append(p("3. Triển khai Rootless Container Isolation: Cấu hình User Namespaces, cgroups v2 resource delegation và systemd lingering để chạy Docker hoàn toàn không cần quyền root trên Arch Linux.", size=26, space_after=60))
    body_xml.append(p("4. Phân tách mạng Zero-Trust: Thiết lập hai mạng Docker bridge riêng biệt; giấu kín hoàn toàn cổng 5432 (Postgres) và cổng S3 nội bộ khỏi giao diện mạng của host.", size=26, space_after=60))
    body_xml.append(p("5. Xây dựng AI Vision Microservice: Đóng gói ứng dụng FastAPI phục vụ nhận diện chữ từ ảnh (OCR Engine) siêu nhẹ, hỗ trợ giao diện Terminal tương tác (CLI) và trích xuất metrics.", size=26, space_after=60))
    body_xml.append(p("6. Đo lường và Đánh giá Thực nghiệm (Benchmarking): Bắn tải đo đạc thông lượng (RPS), độ trễ (Latency) và footprint bộ nhớ RAM giữa Arch Linux và Ubuntu Server.", size=26, space_after=150))

    body_xml.append(p("1.3. ĐỐI TƯỢNG VÀ PHẠM VI NGHIÊN CỨU", bold=True, size=28, space_before=150, space_after=100))
    body_xml.append(p("• Đối tượng nghiên cứu: Hệ điều hành Arch Linux x86_64 (Kernel 7.x bleeding-edge), Ubuntu Server 22.04/24.04 LTS (Kernel 5.x/6.x); Docker Engine, RootlessKit; Tường lửa nftables và UFW; Hệ sinh thái MLOps mã nguồn mở (MLflow, PostgreSQL, MinIO, FastAPI, Prometheus, Grafana).", size=26, space_after=100))
    body_xml.append(p("• Phạm vi nghiên cứu: Hai nút tính toán hoạt động độc lập (Dual-node Isolation), không thiết lập cụm giao tiếp mạng giữa hai bên để đảm bảo tính khách quan của phép thử nghiệm đối kháng.", size=26, space_after=100))
    body_xml.append(p("• Giới hạn đề tài: Đề tài tập trung chuyên sâu vào tầng Hạ tầng Hệ thống Linux và Bảo mật Container (System Infrastructure & Container Security), không đi sâu vào việc tối ưu hóa độ chính xác của thuật toán học sâu.", size=26, space_after=150))

    body_xml.append(p("1.4. PHƯƠNG PHÁP NGHIÊN CỨU", bold=True, size=28, space_before=150, space_after=100))
    body_xml.append(p("Đề tài áp dụng phương pháp nghiên cứu thực nghiệm kết hợp đối sánh định lượng:", size=26, space_after=80))
    body_xml.append(p("1. Phương pháp lý thuyết: Phân tích kiến trúc hạt nhân Linux, cơ chế điều khiển tiến trình cgroups v2, không gian tên User Namespaces và tiêu chuẩn bảo mật CIS Benchmark.", size=26, space_after=60))
    body_xml.append(p("2. Phương pháp thực nghiệm: Lập trình kịch bản Bash tự động triển khai hệ thống trên máy thật Arch Linux và máy ảo Ubuntu Server.", size=26, space_after=60))
    body_xml.append(p("3. Phương pháp đo lường: Sử dụng công cụ curl/hey bắn tải đo thông số hiệu năng và sử dụng lệnh Linux thu thập mức độ sử dụng RAM, CPU.", size=26, space_after=150))

    body_xml.append(p("1.5. Ý NGHĨA KHOA HỌC VÀ THỰC TIỄN", bold=True, size=28, space_before=150, space_after=100))
    body_xml.append(p("• Ý nghĩa khoa học: Đóng góp một góc nhìn so sánh thực nghiệm toàn diện và chuẩn mực giữa hai mô hình phát hành hệ điều hành Linux (Rolling Release vs. LTS) trong bối cảnh chịu tải MLOps hiện đại.", size=26, space_after=100))
    body_xml.append(p("• Ý nghĩa thực tiễn: Cung cấp một bộ mẫu triển khai (Production-ready Template) hoàn toàn tự động, có thể ứng dụng trực tiếp cho các doanh nghiệp vừa và nhỏ muốn xây dựng nền tảng MLOps an toàn, tiết kiệm chi phí và đạt chuẩn an ninh thông tin cao.", size=26, space_after=150))

    # Finish XML structure
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
    out_docx = "/home/nguyencongduc/mlops-multi-os-pipeline/docs/BAO_CAO_MLOPS_PHAN_1.docx"
    generate_part1_docx(out_docx)
    print("Done generating part 1 docx.")
