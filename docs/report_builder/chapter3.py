from .styles import p, heading1, heading2, heading3, heading4, page_break, table_grid, figure_box, code_box, note_box

def build_chapter3():
    body = []
    body.append(heading1("CHƯƠNG 3: PHƯƠNG PHÁP NGHIÊN CỨU VÀ THIẾT KẾ HỆ THỐNG"))

    body.append(heading2("3.1. TRIẾT LÝ THIẾT KẾ VÀ QUY TRÌNH NGHIÊN CỨU TỔNG THỂ"))
    body.append(p("Để giải quyết trọn vẹn bài toán xây dựng nền tảng MLOps an toàn và đối sánh hai trường phái hệ điều hành Linux, đề tài xác lập ba triết lý thiết kế kim chỉ nam xuyên suốt toàn bộ vòng đời phát triển dự án:", indent=400))
    body.append(p("1. Triết lý Least Privilege (Đặc quyền tối thiểu): Tuyệt đối không cấp phát bất kỳ quyền hạn nào vượt quá mức cần thiết cho hoạt động của dịch vụ. Mọi tiến trình từ cấp máy chủ (tài khoản `mlops`), cấp container engine (Rootless Docker daemon), cho đến tiến trình ứng dụng bên trong container (tài khoản `mlopsuser` UID 10001) đều bắt buộc phải hoạt động dưới quyền unprivileged không có đặc quyền root.", indent=400))
    body.append(p("2. Triết lý Zero-Trust Network (Không tin cậy mạng mặc định): Loại bỏ hoàn toàn quan niệm ranh giới mạng nội bộ an toàn. Mọi dịch vụ lưu trữ dữ liệu cốt lõi (PostgreSQL, MinIO S3 API) bị giam lỏng hoàn toàn trong vùng mạng riêng biệt (`mlops-backend`), không được phép bind bất kỳ cổng nào ra giao diện mạng máy chủ (Host IP). Chỉ có các cổng giao tiếp API và giao diện Web UI được chỉ định mới được phép mở ra bên ngoài.", indent=400))
    body.append(p("3. Triết lý Idempotent Infrastructure as Code (Hạ tầng dạng mã có tính bất biến): Toàn bộ thao tác cài đặt, cấu hình hệ thống, thiết lập tường lửa và triển khai dịch vụ phải được viết thành các kịch bản Bash script chuẩn xác. Kịch bản phải đảm bảo tính Idempotent: Khi thực thi lần đầu sẽ cấu hình hệ thống, khi thực thi các lần tiếp theo sẽ nhận diện trạng thái và không gây ra bất kỳ lỗi trùng lặp hay thay đổi sai lệch nào.", indent=400))

    schematic_3_1 = [
        "+-------------------------------------------------------------------------+",
        "|                 QUY TRÌNH NGHIÊN CỨU THỰC NGHIỆM TỔNG THỂ               |",
        "+-------------------------------------------------------------------------+",
        "| [GIAI ĐOẠN 1: Nghiên cứu lý thuyết & Kiến trúc]                         |",
        "|  - Phân tích nhân Linux Kernel, cgroups v2, User Namespaces             |",
        "|  - Nghiên cứu tiêu chuẩn CIS Docker Benchmark v1.6.0                     |",
        "|                                |                                        |",
        "|                                v                                        |",
        "| [GIAI ĐOẠN 2: Phát triển bộ kịch bản tự động hóa IaC]                   |",
        "|  - 01_system_hardening.sh: Hardening SSH 2222, nftables, sysctl         |",
        "|  - 01_rollback_hardening.sh: Khôi phục trạng thái ban đầu               |",
        "|  - 02_setup_rootless_docker.sh: User Namespaces, subuid/subgid, linger  |",
        "|                                |                                        |",
        "|                                v                                        |",
        "| [GIAI ĐOẠN 3: Đóng gói vi dịch vụ MLOps Stack & Zero-Trust]             |",
        "|  - Dockerfile FastAPI OCR Multi-stage build (Non-root UID 10001)        |",
        "|  - docker-compose.yml: Phân tách mlops-frontend và mlops-backend       |",
        "|  - mlops-stack.service: Quản lý vòng đời dịch vụ qua Systemd User       |",
        "|                                |                                        |",
        "|                                v                                        |",
        "| [GIAI ĐOẠN 4: Phát triển công cụ CLI & Kiểm tra an ninh tự động]        |",
        "|  - ai_cli.sh: Menu Terminal tương tác quét ảnh OCR và kiểm tra sức khỏe |",
        "|  - 04_verify_system.sh: Bộ 5 bài test tự động đánh giá an ninh chốt chặn|",
        "|                                |                                        |",
        "|                                v                                        |",
        "| [GIAI ĐOẠN 5: Thực nghiệm đo lường Benchmark đối kháng định lượng]      |",
        "|  - Đo lường RAM tĩnh (Idle OS) và RAM động (Stack Active)               |",
        "|  - Kiểm thử tải API thông lượng RPS, độ trễ phân vị p50/p95/p99        |",
        "|  - Tổng hợp báo cáo kỹ thuật toàn diện phục vụ bảo vệ Hội đồng VKU      |",
        "+-------------------------------------------------------------------------+"
    ]
    body.append(figure_box("3.1", "Quy trình nghiên cứu thực nghiệm tổng thể 5 giai đoạn",
                           "minh họa tiến trình khoa học chặt chẽ từ nghiên cứu lý thuyết hạt nhân, phát triển mã nguồn kịch bản tự động hóa, đóng gói vi dịch vụ, xây dựng công cụ kiểm định cho tới đo lường định lượng kết quả.",
                           schematic_3_1))

    body.append(heading2("3.2. ĐẶC TẢ YÊU CẦU HỆ THỐNG (SYSTEM REQUIREMENTS)"))
    body.append(heading3("3.2.1. Yêu cầu chức năng (Functional Requirements)"))
    body.append(p("Hệ thống MLOps Platform bắt buộc phải đáp ứng trọn vẹn các yêu cầu chức năng nghiệp vụ sau:", indent=400))
    body.append(p("• FR-01 (Quản lý thí nghiệm học máy): Cung cấp giao diện Web UI MLflow trên cổng 5000 cho phép nhà phát triển tạo thí nghiệm mới, theo dõi các chỉ số đánh giá và lưu trữ các phiên bản mô hình.", indent=400))
    body.append(p("• FR-02 (Lưu trữ bền vững siêu dữ liệu): Tự động kết nối cơ sở dữ liệu PostgreSQL 15 trên cổng nội bộ 5432 để quản lý siêu dữ liệu học máy với tính toàn vẹn tuyệt đối.", indent=400))
    body.append(p("• FR-03 (Kho đối tượng nhị phân): Cung cấp dịch vụ lưu trữ đối tượng MinIO tương thích S3 để lưu trữ các tệp tin mô hình đã đóng gói.", indent=400))
    body.append(p("• FR-04 (Vi dịch vụ AI Suy luận OCR): Cung cấp RESTful API qua cổng 8080 với endpoint POST `/predict/ocr` tiếp nhận tệp tin hình ảnh `.png/.jpg`, thực thi nhận dạng ký tự quang học qua Tesseract OCR và trả về kết quả định dạng JSON chuẩn xác.", indent=400))
    body.append(p("• FR-05 (Giao diện dòng lệnh Terminal CLI): Cung cấp kịch bản dòng lệnh `ai_cli.sh` hiển thị Menu màu ANSI tương tác, hỗ trợ quét ảnh mẫu, quét ảnh tùy chọn từ đường dẫn bất kỳ trên hệ thống và hiển thị thời gian phản hồi.", indent=400))
    body.append(p("• FR-06 (Giám sát và đo lường từ xa): Prometheus tự động cào metrics từ FastAPI và Node Exporter; Grafana cung cấp Dashboard trực quan hóa lưu lượng mạng, RPS và tải CPU/RAM trên cổng 3000.", indent=400))

    body.append(heading3("3.2.2. Yêu cầu phi chức năng (Non-Functional Requirements)"))
    body.append(p("Các yêu cầu phi chức năng đặt ra tiêu chuẩn kỹ thuật nghiêm ngặt về chất lượng hệ thống:", indent=400))
    body.append(p("• NFR-01 (An toàn tuyệt đối - Rootless Isolation): Toàn bộ container engine và tiến trình ứng dụng trên Arch Linux phải chạy dưới quyền unprivileged (UID 1003 và UID 10001), triệt tiêu 100% rủi ro chiếm quyền root máy chủ khi bị Container Escape.", indent=400))
    body.append(p("• NFR-02 (Phân đoạn mạng Zero-Trust): Cổng cơ sở dữ liệu PostgreSQL (5432) và MinIO API (9000) tuyệt đối không được xuất hiện trên bảng lắng nghe mạng bên ngoài (Host IP). Kết nối tới các cổng này từ bên ngoài phải bị từ chối lập tức (Connection Refused).", indent=400))
    body.append(p("• NFR-03 (Chống tấn công Brute-force): Tường lửa nftables trên Arch Linux phải tích hợp cơ chế giới hạn tần suất kết nối SSH (Rate Limiting) không quá 4 kết nối/phút từ một địa chỉ IP.", indent=400))
    body.append(p("• NFR-04 (Tính linh hoạt và phục hồi): Hệ thống phải có kịch bản Rollback hoàn chỉnh giúp đưa các tệp cấu hình OpenSSH, tường lửa và tham số kernel về trạng thái nguyên bản chỉ với 1 câu lệnh.", indent=400))
    body.append(p("• NFR-05 (Hiệu năng phục vụ): Độ trễ trung bình của vi dịch vụ AI dưới tải trọng 500 requests đồng thời không vượt quá 50ms, tỷ lệ lỗi không vượt quá 0.01%.", indent=400))

    body.append(heading2("3.3. THIẾT KẾ KIẾN TRÚC TỔNG THỂ DUAL-NODE MLOPS PLATFORM"))
    body.append(heading3("3.3.1. Sơ đồ phân tầng kiến trúc"))
    body.append(p("Hệ thống được thiết kế theo mô hình hai máy chủ độc lập (Dual-Node Architecture) nhằm phục vụ công tác đối sánh thực nghiệm khoa học:", indent=400))
    body.append(p("• Node 1 (Arch Linux - Rolling Release): Đại diện cho trường phái bảo mật tối tân và tinh gọn, vận hành nhân Linux Kernel mới nhất, quản trị tường lửa bằng `nftables` stateful nguyên bản và thực thi toàn bộ cụm dịch vụ bằng Rootless Docker Engine unprivileged.", indent=400))
    body.append(p("• Node 2 (Ubuntu Server - Enterprise LTS): Đại diện cho trường phái truyền thống doanh nghiệp, vận hành nhân Ubuntu LTS đóng băng, tường lửa `ufw` và Docker daemon cấp hệ thống.", indent=400))

    schematic_3_2 = [
        "+-------------------------------------------------------------------------+",
        "|           KIẾN TRÚC PHÂN TẦNG DUAL-NODE MLOPS ISOLATION ARCHITECTURE    |",
        "+-------------------------------------------------------------------------+",
        "| [EXTERNAL NETWORK TRAFFIC / USER ACCESS]                                |",
        "|   Kỹ sư MLOps (SSH: 2222) | Web UI (5000) | AI API (8080) | Grafana(3000)|",
        "+-----------------------------------|-------------------------------------+",
        "|                                   v                                     |",
        "| [TẦNG TƯỜNG LỬA HOST] nftables (Arch Linux) / UFW (Ubuntu Server)       |",
        "|  - Rate-limiting SSH (4/min)      - Chặn quét cổng (Default Deny)       |",
        "|  - Chỉ mở các cổng dịch vụ: 2222, 8080, 5000, 3000, 9001                |",
        "+-----------------------------------|-------------------------------------+",
        "|                                   v                                     |",
        "| [TẦNG HỆ ĐIỀU HÀNH] Arch Linux Kernel 6.x/7.x vs. Ubuntu Server 22.04 LTS|",
        "|  - Kernel Sysctl Hardened (somaxconn=65535, tcp_tw_reuse=1)             |",
        "|  - User Namespaces: mlops (UID 1003) -> subuid 100000:65536             |",
        "+-----------------------------------|-------------------------------------+",
        "|                                   v                                     |",
        "| [TẦNG CONTAINER ENGINE] Rootless Docker (Arch) vs. Rootful Docker (Ubuntu)|",
        "|  - slirp4netns User-mode Network  - fuse-overlayfs unprivileged storage |",
        "+-----------------------------------|-------------------------------------+",
        "|                                   v                                     |",
        "| [TẦNG MẠNG NỘI BỘ ZERO-TRUST DOCKER NETWORKS]                           |",
        "|  +-------------------------------------------------------------------+  |",
        "|  | MẠNG CÔNG KHAI (mlops-frontend - Bridge):                         |  |",
        "|  |  [FastAPI OCR:8080] <--> [MLflow:5000] <--> [Grafana Dashboard:3000]|",
        "|  +-----------------------------------|-------------------------------+  |",
        "|                                      | Kết nối nội bộ                   |",
        "|  +-----------------------------------v-------------------------------+  |",
        "|  | MẠNG NỘI BỘ CÔ LẬP (mlops-backend - internal: true):              |  |",
        "|  |  [PostgreSQL 15:5432] <---------------> [MinIO S3 API:9000]       |  |",
        "|  |  (HOÀN TOÀN VÔ HÌNH VỚI MẠNG BÊN NGOÀI VÀ MÁY CHỦ HOST!)          |  |",
        "|  +-------------------------------------------------------------------+  |",
        "+-------------------------------------------------------------------------+"
    ]
    body.append(figure_box("3.2", "Sơ đồ kiến trúc tổng thể Dual-Node MLOps Isolation Architecture",
                           "minh họa phân tầng kiến trúc từ tầng mạng ngoài, tầng tường lửa stateful, tầng hệ điều hành, tầng container engine unprivileged cho tới mô hình phân tách mạng nội bộ Zero-Trust.",
                           schematic_3_2))

    body.append(heading3("3.3.2. Sơ đồ luồng dữ liệu suy luận và giám sát"))
    body.append(p("Dòng chảy dữ liệu bên trong hệ sinh thái được thiết kế mạch lạc, bảo đảm không có điểm nghẽn cổ chai:", indent=400))
    body.append(p("1. Luồng suy luận AI (Inference Flow): Người dùng hoặc script `ai_cli.sh` gửi tệp tin ảnh qua giao thức HTTP POST multipart/form-data tới cổng 8080. Tiến trình FastAPI (chạy với user `mlopsuser` 10001) tiếp nhận ảnh trong bộ nhớ đệm RAM, chuyển đổi qua thư viện Pillow/OpenCV và gọi động cơ Tesseract OCR để trích xuất văn bản tiếng Việt/Anh, sau đó trả về phản hồi JSON với đầy đủ nhãn văn bản và thời gian suy luận.", indent=400))
    body.append(p("2. Luồng lưu vết MLOps (Tracking Flow): Khi huấn luyện mô hình, tiến trình Python kết nối tới MLflow Tracking Server qua cổng 5000. MLflow ghi các chỉ số vào PostgreSQL (`mlops-backend`) và lưu tệp trọng số mô hình vào MinIO S3 (`mlops-backend`).", indent=400))
    body.append(p("3. Luồng giám sát tài nguyên (Observability Flow): Mỗi 5 giây, Prometheus gửi truy vấn scrape tới `/metrics` của FastAPI và Node Exporter (cổng 9100). Toàn bộ dữ liệu được lưu vào cơ sở dữ liệu chuỗi thời gian TSDB và trực quan hóa tức thì trên Dashboard của Grafana.", indent=400))

    body.append(heading2("3.4. THIẾT KẾ PHÂN ĐOẠN MẠNG AN NINH ZERO-TRUST"))
    body.append(p("Điểm nhấn kiến trúc đột phá của hệ thống là việc áp dụng nguyên lý Zero-Trust Network Segmentation ngay trong cấu hình Docker Compose. Thông thường, các nhà phát triển thường để toàn bộ container trong một mạng bridge mặc định (`bridge` network) và vô tư ánh xạ các cổng cơ sở dữ liệu ra `0.0.0.0:5432`. Đây là hành vi cực kỳ tắc trách, tạo điều kiện cho các cuộc tấn công rà quét tự động đánh cắp toàn bộ cơ sở dữ liệu.", indent=400))
    body.append(p("Nhóm đã thiết kế phân tách hai mạng Docker logic độc lập hoàn toàn:", indent=400))
    body.append(p("1. Mạng `mlops-frontend` (Public Bridge): Được kết nối với các container cần cung cấp giao diện người dùng hoặc nhận dữ liệu từ bên ngoài: `fastapi-service` (cổng 8080), `mlflow-server` (cổng 5000), `grafana` (cổng 3000), `prometheus` (cổng 9090) và `minio` (chỉ mở cổng Web Console 9001).", indent=400))
    body.append(p("2. Mạng `mlops-backend` (Isolated Internal Network): Được thiết lập với cờ đặc biệt `internal: true`. Trong mạng này chỉ có hai thành phần lưu trữ cốt lõi: `postgres-db` (cổng 5432) và `minio` (cổng API 9000). Các container trong mạng này không hề có cổng ra (Gateway) ra Internet và tuyệt đối không thể bị kết nối từ bên ngoài máy chủ.", indent=400))

    body.append(p("Bảng 3.1: Quy hoạch không gian địa chỉ IP, cổng dịch vụ và chính sách mạng", align="center", bold=True, size=24, space_after=60))
    headers_3_1 = ["Tên dịch vụ Container", "Mạng Docker tham gia", "Cổng dịch vụ nội bộ", "Cổng mở ra Host IP", "Chính sách an ninh"]
    rows_3_1 = [
        ["fastapi-ocr-service", "mlops-frontend", "8000 / TCP", "8080 / TCP", "Mở công khai có Rate Limit."],
        ["mlflow-tracking", "mlops-frontend & backend", "5000 / TCP", "5000 / TCP", "Mở công khai cho nhóm phát triển."],
        ["grafana-dashboard", "mlops-frontend", "3000 / TCP", "3000 / TCP", "Mở công khai, bảo vệ bằng mật khẩu."],
        ["prometheus-server", "mlops-frontend", "9090 / TCP", "9090 / TCP", "Mở công khai phục vụ kiểm tra targets."],
        ["minio-object-storage", "mlops-frontend & backend", "9000 & 9001 / TCP", "9001 / TCP (Console)", "Cổng API 9000 bị giấu kín trong backend."],
        ["postgres-metadata-db", "mlops-backend (Internal)", "5432 / TCP", "KHÔNG MỞ (0.0.0.0)", "Cô lập 100% trong Zero-Trust backend."]
    ]
    body.append(table_grid(headers_3_1, rows_3_1))
    body.append(p("", space_after=100))

    body.append(heading2("3.5. THIẾT KẾ CHIẾN LƯỢC BẢO MẬT 7 LỚP DEFENSE IN DEPTH"))
    body.append(p("Để đảm bảo hệ thống có khả năng phòng vệ kiên cố trước mọi kịch bản tấn công hiện đại, nhóm đã thiết kế chiến lược an ninh phòng thủ đa tầng (Defense in Depth) bao gồm 7 lớp bảo vệ tương hỗ:", indent=400))
    body.append(p("• Lớp 1 (Host OS Hardening): Vô hiệu hóa tài khoản root đăng nhập SSH, đổi cổng mặc định sang 2222, giới hạn số lần thử mật khẩu (`MaxAuthTries 3`), tinh chỉnh sysctl vô hiệu hóa ICMP redirects và kích hoạt SYN cookies.", indent=400))
    body.append(p("• Lớp 2 (Stateful Firewall): Tường lửa nftables áp dụng chính sách Default Deny cho chuỗi INPUT, drop invalid packets và áp dụng rate limiting tối đa 4 kết nối/phút cho cổng SSH 2222.", indent=400))
    body.append(p("• Lớp 3 (Unprivileged User Isolation): Tạo người dùng chuyên biệt `mlops` (UID 1003) trên máy chủ host, tách biệt hoàn toàn dữ liệu của ứng dụng khỏi tài khoản cá nhân của kỹ sư.", indent=400))
    body.append(p("• Lớp 4 (Rootless Container Engine): Docker daemon chạy bên trong User Namespace của tài khoản `mlops`. Ngay cả khi xảy ra lỗi nghiêm trọng nhất trong runtime, kẻ tấn công cũng không thể đạt được quyền root của máy chủ vật lý.", indent=400))
    body.append(p("• Lớp 5 (Container Unprivileged Execution): Ứng dụng bên trong container (FastAPI) không chạy bằng root (UID 0) mà chạy bằng tài khoản unprivileged `mlopsuser` với UID 10001, ngăn chặn việc đọc trộm các tệp tin hệ thống bên trong container.", indent=400))
    body.append(p("• Lớp 6 (Zero-Trust Network Segmentation): Phân vùng mạng logic `mlops-backend` có thuộc tính `internal: true`, giấu kín cơ sở dữ liệu quan trọng khỏi bảng định tuyến ngoài.", indent=400))
    body.append(p("• Lớp 7 (Persistence & Volume Isolation): Dữ liệu của PostgreSQL và MinIO được lưu trữ trên các Docker Volumes chuyên biệt, được phân quyền nghiêm ngặt theo UID của container, tránh rò rỉ dữ liệu chéo giữa các ứng dụng.", indent=400))

    body.append(p("Bảng 3.2: Ma trận rủi ro hệ thống và biện pháp đối phó tương ứng", align="center", bold=True, size=24, space_after=60))
    headers_3_2 = ["Mối đe dọa / Rủi ro an ninh", "Mức độ nghiêm trọng", "Biện pháp phòng ngừa được áp dụng", "Lớp bảo vệ"]
    rows_3_2 = [
        ["Tấn công Brute-force mật khẩu SSH", "CAO (Critical)", "Đổi port 2222, cấm login root, nftables rate limit 4/phút.", "Lớp 1 & Lớp 2"],
        ["Tấn công Container Escape chiếm máy chủ", "RẤT CAO (Catastrophic)", "Rootless Docker unprivileged + User Namespaces subuid mapping.", "Lớp 4 & Lớp 5"],
        ["Tấn công rà quét và chiếm quyền CSDL", "CAO (High)", "Mạng Docker nội bộ Zero-Trust internal: true, giấu cổng 5432.", "Lớp 6"],
        ["Tấn công cạn kiệt tài nguyên DoS/RAM", "TRUNG BÌNH (Medium)", "Cgroups v2 resource delegation, sysctl somaxconn=65535.", "Lớp 1 & Lớp 3"],
        ["Lỗi cấu hình làm mất quyền truy cập máy", "CAO (High)", "Kịch bản Rollback tự động 01_rollback_hardening.sh dự phòng.", "Lớp 1 & Lớp 2"]
    ]
    body.append(table_grid(headers_3_2, rows_3_2))
    body.append(p("", space_after=100))

    body.append(heading2("3.6. THIẾT KẾ CÔNG CỤ DÒNG LỆNH TƯƠNG TÁC VÀ KIỂM ĐỊNH TỰ ĐỘNG"))
    body.append(p("Một hệ thống kỹ thuật xuất sắc không chỉ nằm ở khả năng hoạt động ổn định mà còn phải thân thiện và minh bạch với người vận hành. Nhóm đã dành thời gian thiết kế hai công cụ dòng lệnh chuyên biệt:", indent=400))
    body.append(p("1. Công cụ Terminal CLI tương tác (`ai_cli.sh`): Mang lại trải nghiệm dòng lệnh mượt mà cho kỹ sư MLOps. Script hiển thị Menu tương tác bằng mã màu ANSI chuẩn POSIX, cung cấp 4 lựa chọn: (1) Quét hình ảnh mẫu có sẵn; (2) Nhập đường dẫn bất kỳ tệp ảnh nào trên máy tính; (3) Kiểm tra sức khỏe toàn diện hệ thống; (4) Thoát chương trình. Khi thực thi quét, script tự động kiểm tra kích thước ảnh, gửi yêu cầu tới API, đo đạc thời gian tính toán và bóc tách dữ liệu JSON in ra màn hình trong khung viền trực quan.", indent=400))
    body.append(p("2. Kịch bản kiểm tra an ninh tự động (`04_verify_system.sh`): Hoạt động như một bài kiểm tra chấp nhận hệ thống (System Acceptance Test), tự động thực thi 5 bài test an ninh then chốt: (Test 1) Trạng thái tường lửa nftables; (Test 2) Trạng thái áp dụng tham số sysctl MLOps; (Test 3) Xác minh quyền Rootless UID Mapping qua Alpine container; (Test 4) Thăm dò HTTP Healthcheck các endpoint công khai; (Test 5) Kiểm chứng Zero-Trust: Đảm bảo cổng 5432 và 9000 hoàn toàn bị từ chối kết nối từ host.", indent=400))

    body.append(heading2("3.7. KẾ HOẠCH TRIỂN KHAI VÀ MA TRẬN TRÁCH NHIỆM RACI"))
    body.append(p("Dự án được triển khai chặt chẽ trong vòng 6 tuần với tiến độ được kiểm soát liên tục:", indent=400))
    body.append(p("• Tuần 1: Nghiên cứu lý thuyết nhân Linux, khảo sát tài liệu CIS Benchmark và thống nhất kiến trúc tổng thể giữa 3 thành viên.", indent=400))
    body.append(p("• Tuần 2: Xây dựng bộ kịch bản IaC Hardening OS và Rollback trên Arch Linux (`01_system_hardening.sh`) và Ubuntu Server.", indent=400))
    body.append(p("• Tuần 3: Cấu hình Rootless Docker trên Arch Linux (`02_setup_rootless_docker.sh`) và Docker Engine trên Ubuntu.", indent=400))
    body.append(p("• Tuần 4: Đóng gói vi dịch vụ FastAPI OCR, thiết kế docker-compose.yml Zero-Trust và cấu hình systemd user unit.", indent=400))
    body.append(p("• Tuần 5: Triển khai hệ thống giám sát Prometheus/Grafana, phát triển `ai_cli.sh` và `04_verify_system.sh`.", indent=400))
    body.append(p("• Tuần 6: Thực hiện đo lường tải trọng Benchmark, phân tích đối kháng số liệu thực nghiệm và hoàn thiện bản báo cáo đồ án.", indent=400))
    body.append(page_break())

    return body
