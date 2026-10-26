from .styles import p, heading1, heading2, heading3, page_break, table_grid, figure_box, image_figure

def build_chapter1():
    body = []
    body.append(heading1("CHƯƠNG 1: TỔNG QUAN VỀ ĐỀ TÀI"))
    
    body.append(heading2("1.1. ĐẶT VẤN ĐỀ VÀ BỐI CẢNH NGHIÊN CỨU"))
    body.append(heading3("1.1.1. Sự hội tụ giữa MLOps và hạ tầng mã nguồn mở Linux"))
    body.append(p("Sự phát triển vượt bậc của các mô hình học sâu (Deep Learning) và học máy truyền thống đã tạo ra một cuộc cách mạng trong xử lý thông tin số. Tuy nhiên, việc đưa các mô hình này vào môi trường thực tế đặt ra các thách thức hoàn toàn khác biệt so với phát triển phần mềm truyền thống. Một ứng dụng phần mềm thông thường chỉ phụ thuộc vào mã nguồn (Code) và các thư viện liên kết. Trong khi đó, một dịch vụ AI phụ thuộc vào bộ ba hữu cơ: Mã nguồn thuật toán, Tập dữ liệu huấn luyện (Training Data) và Bộ tham số tối ưu (Model Weights/Hyperparameters).", indent=400))
    body.append(p("Sự thay đổi không ngừng của dữ liệu ngoài thực tế dẫn tới hiện tượng trôi dạt mô hình (Model Drift), khiến độ chính xác suy giảm dần theo thời gian. Để duy trì chất lượng dịch vụ, quy trình MLOps đòi hỏi một chuỗi cung ứng phần mềm liên tục: Từ khâu thu thập dữ liệu mới, lưu vết phiên bản dữ liệu, tự động kích hoạt tiến trình huấn luyện lại, so sánh đánh giá độ chính xác, đăng ký mô hình vào kho tập trung (Model Registry), cho đến việc đóng gói và phục vụ suy luận thời gian thực qua giao tiếp API.", indent=400))
    
    schematic_1_2 = [
        "+-------------------------------------------------------------------------+",
        "|                 CHU TRÌNH VÒNG ĐỜI MLOPS KHÉP KÍN                       |",
        "+-------------------------------------------------------------------------+",
        "| [1. Data Pipeline]  --->  [2. Model Training]  --->  [3. Tracking Server]|",
        "| Raw Data & Labels         Hyperparameter Tuning      MLflow + Postgres   |",
        "|         |                         |                          |          |",
        "|         v                         v                          v          |",
        "| [6. Telemetry & Alert]<-- [5. Model Serving]   <---  [4. Artifact Store] |",
        "| Prometheus + Grafana      FastAPI OCR Service        MinIO S3 Buckets   |",
        "+-------------------------------------------------------------------------+"
    ]
    body.append(image_figure("rIdImg1_2", "1.2", "Chu trình khép kín của nền tảng MLOps trong môi trường sản xuất", "mô tả dòng chảy dữ liệu tự động hóa liên tục từ dữ liệu thô ban đầu, qua huấn luyện, lưu vết siêu tham số với MLflow, đóng gói lưu trữ mô hình trên MinIO S3, triển khai phục vụ suy luận với FastAPI và giám sát thời gian thực với Prometheus.", cx=5486400, cy=2286000))

    body.append(p("Trong toàn bộ chu trình phức tạp này, hệ điều hành Linux đóng vai trò là xương sống hạ tầng không thể thay thế. Hạt nhân Linux chịu trách nhiệm phân phối hàng gigabyte bộ nhớ RAM cho các tiến trình huấn luyện, xử lý các luồng socket mạng TCP với độ trễ thấp và cô lập các môi trường phụ thuộc thông qua công nghệ container.", indent=400))

    body.append(heading3("1.1.2. Thách thức phân phối phần mềm: Rolling Release vs. LTS"))
    body.append(p("Khi triển khai hạ tầng cho MLOps, một quyết định kiến trúc mang tính sống còn là lựa chọn bản phân phối Linux nền tảng. Hiện nay, cộng đồng công nghệ phân chia sâu sắc giữa hai triết lý phát hành:", indent=400))
    body.append(p("1. Triết lý Rolling Release (Arch Linux): Arch Linux tuân thủ nguyên lý phát triển linh hoạt tối đa. Thay vì phát hành các bản phân phối theo số phiên bản cố định (như bản 20.04, 22.04), Arch Linux vận hành một cây phả hệ phần mềm duy nhất liên tục chuyển động. Mỗi khi các nhà phát triển upstream của Linux Kernel, Docker hoặc Python phát hành mã nguồn mới, gói phần mềm sẽ được biên dịch và đưa ngay vào kho lưu trữ chính thức sau khi vượt qua các bài kiểm thử cơ bản.", indent=400))
    body.append(p("Lợi thế của mô hình này đối với MLOps là vô cùng to lớn: Hệ thống luôn tiếp cận được những bản vá lỗi hiệu năng mới nhất của nhân Linux, các cải tiến về quản lý bộ nhớ cgroups v2 và tốc độ xử lý mạng vượt trội của Netfilter. Tuy nhiên, rủi ro tiềm ẩn là nguy cơ xung đột gói phần mềm hoặc thay đổi cú pháp cấu hình đột ngột, đòi hỏi người kỹ sư phải xây dựng các kịch bản Infrastructure as Code (IaC) tự động hóa để kiểm soát toàn bộ trạng thái hệ điều hành.", indent=400))
    body.append(p("2. Triết lý Long-Term Support (Ubuntu Server): Canonical định hình Ubuntu Server như một pháo đài ổn định cho môi trường doanh nghiệp. Các phiên bản LTS được phát hành định kỳ 2 năm một lần (như 22.04 LTS, 24.04 LTS) và cam kết hỗ trợ bảo mật trong 5 đến 10 năm. Toàn bộ các gói phần mềm cốt lõi đều bị đóng băng phiên bản (Version Freeze), chỉ tiếp nhận các bản vá bảo mật khẩn cấp.", indent=400))
    body.append(p("Mặc dù đảm bảo tính nhất quán và dễ quản trị cho các nhóm vận hành truyền thống, nhược điểm của Ubuntu Server là sự lỗi thời của các công cụ nền tảng. Đôi khi các tính năng bảo mật mới của kernel hoặc các tối ưu hóa I/O quan trọng cho AI không được cập nhật kịp thời, đồng thời hệ thống mặc định cài đặt sẵn nhiều dịch vụ không cần thiết (như snapd, multipathd), làm lãng phí một lượng tài nguyên RAM đáng kể của máy chủ.", indent=400))

    body.append(p("Bảng 1.1: So sánh đặc tính kiến trúc giữa Arch Linux (Rolling) và Ubuntu Server (LTS)", align="center", bold=True, size=24, space_after=60))
    headers_1_1 = ["Đặc tính so sánh", "Arch Linux (Rolling Release)", "Ubuntu Server (Enterprise LTS)"]
    rows_1_1 = [
        ["Triết lý thiết kế", "The Arch Way: Tối giản, thanh lịch, người dùng tự quyết định mọi thành phần.", "Canonical Standard: Thân thiện, cài đặt sẵn cấu hình, tối ưu cho đại chúng."],
        ["Mô hình phát hành", "Rolling Release: Cập nhật liên tục, không có khái niệm nâng cấp phiên bản lớn.", "Fixed Release: Chu kỳ phát hành cố định 2 năm/lần cho bản LTS, hỗ trợ 5 năm."],
        ["Phiên bản Linux Kernel", "Hạt nhân mới nhất (Kernel 6.x / 7.x bleeding-edge) với đầy đủ tính năng mới.", "Hạt nhân ổn định đóng băng (Kernel 5.15 / 6.8 LTS) được Canonical hỗ trợ."],
        ["Cơ chế quản trị gói", "Pacman + Arch User Repository (AUR) với hàng chục ngàn gói mã nguồn mở.", "Advanced Package Tool (APT) + Snap packages được đóng gói sẵn."],
        ["Cơ chế Container mặc định", "Người dùng tự cấu hình; hỗ trợ hoàn hảo mô hình Rootless unprivileged.", "Docker Engine truyền thống chạy bằng quyền root daemon cấp hệ thống."],
        ["Tài nguyên chiếm dụng tĩnh", "Cực kỳ tinh gọn (~400MB RAM sau khi boot), không có dịch vụ ngầm dư thừa.", "Trung bình (~750MB - 1GB RAM sau khi boot) do chứa nhiều tiến trình nền."],
        ["Công nghệ tường lửa", "nftables stateful nguyên bản trong kernel với cú pháp hiện đại.", "UFW (Uncomplicated Firewall) hoạt động như một lớp vỏ bọc iptables."]
    ]
    body.append(table_grid(headers_1_1, rows_1_1))
    body.append(p("", space_after=100))

    body.append(heading3("1.1.3. Vấn đề an ninh Container mặc định và nguy cơ Container Escape"))
    body.append(p("Trong hầu hết các tài liệu hướng dẫn cài đặt Docker thông dụng trên Internet, các lập trình viên thường được hướng dẫn thêm tài khoản người dùng vào nhóm `docker` (`usermod -aG docker $USER`). Thao tác này trên thực tế mang lại sự tiện lợi giả tạo, nhưng tạo ra một lỗ hổng an ninh thảm khốc.", indent=400))
    body.append(p("Khi Docker daemon chạy dưới quyền root (UID 0), bất kỳ người dùng nào có quyền giao tiếp với socket `/var/run/docker.sock` đều có quyền năng tương đương quyền root trên máy chủ vật lý. Kẻ tấn công chỉ cần khởi chạy một container đơn giản với cờ `-v /:/host` là đã có thể đọc, ghi và sửa đổi toàn bộ các tệp tin hệ thống của máy chủ lưu trữ (Host OS), bao gồm cả việc sửa đổi tệp `/etc/shadow` để chiếm toàn quyền điều khiển máy tính.", indent=400))

    schematic_1_3 = [
        "+-------------------------------------------------------------------------+",
        "|           MÔ HÌNH TẤN CÔNG CONTAINER ESCAPE KHI CHẠY ROOT               |",
        "+-------------------------------------------------------------------------+",
        "| [Kẻ tấn công] ---> [Khai thác RCE trong FastAPI Microservice]           |",
        "|                           |                                             |",
        "|                           v                                             |",
        "|       [Chiếm quyền root UID 0 bên trong Container]                      |",
        "|                           |                                             |",
        "|                           v                                             |",
        "|       [Khai thác runc CVE-2019-5736 hoặc mount Docker Socket]           |",
        "|                           |                                             |",
        "|                           v                                             |",
        "|    [THOÁT RÀO THÀNH CÔNG: CHIẾM QUYỀN ROOT MÁY CHỦ HOST (UID 0)]        |",
        "+-------------------------------------------------------------------------+"
    ]
    body.append(figure_box("1.3", "Mô hình tấn công phá rào Container Escape khi Docker daemon chạy quyền root",
                           "minh họa đường dẫn tấn công điển hình khi kẻ xấu chiếm quyền điều khiển tiến trình ứng dụng bên trong container và lợi dụng quyền root của Docker daemon để thoát rào, chiếm toàn bộ máy chủ vật lý.",
                           schematic_1_3))

    body.append(p("Bảng 1.2: Các sự cố an ninh nghiêm trọng bắt nguồn từ việc chạy Docker đặc quyền root", align="center", bold=True, size=24, space_after=60))
    headers_1_2 = ["Mã định danh lỗ hổng", "Thành phần bị ảnh hưởng", "Cơ chế tấn công và mức độ thiệt hại"]
    rows_1_2 = [
        ["CVE-2019-5736", "runc container runtime", "Ghi đè binary runc trên máy chủ từ bên trong container, cho phép kẻ tấn công thực thi mã độc với quyền root trên toàn bộ máy chủ."],
        ["CVE-2020-15257", "containerd shim API", "Rò rỉ abstract socket của containerd cho phép các tiến trình trong container gửi chỉ thị điều khiển trực tiếp tới containerd daemon."],
        ["Exposed Docker Socket", "/var/run/docker.sock", "Lập trình viên mount socket vào container để quản lý; kẻ xâm nhập dùng API để spawn container mới mount toàn bộ thư mục root / của host."],
        ["Cryptojacking Botnet", "Docker API Port 2375", "Hàng ngàn máy chủ mở cổng Docker API không xác thực bị quét và tự động cài cắm container đào tiền ảo Monero làm sập tài nguyên."]
    ]
    body.append(table_grid(headers_1_2, rows_1_2))
    body.append(p("", space_after=100))

    body.append(heading3("1.1.4. Nhu cầu cấp thiết về nền tảng MLOps không đặc quyền (Rootless)"))
    body.append(p("Trước những rủi ro an ninh nghiêm trọng nêu trên, việc chuyển đổi mô hình sang Rootless Containerization là giải pháp triệt để và mang tính cách mạng nhất. Trong kiến trúc Rootless Docker, bản thân Docker daemon không chạy dưới quyền tài khoản root hệ thống mà hoạt động hoàn toàn bên trong không gian người dùng của một tài khoản unprivileged độc lập (trong đề tài này là tài khoản `mlops`).", indent=400))
    body.append(p("Nhờ sự kết hợp tinh vi giữa tính năng User Namespaces của Linux Kernel và các công cụ cầu nối như `rootlesskit` cùng `slirp4netns`, tiến trình bên trong container dù có tin rằng mình đang chạy với quyền root (UID 0 ảo), thì dưới con mắt của nhân Linux máy chủ, tiến trình đó thực chất chỉ là một người dùng bình thường với UID lớn (ví dụ UID 100000). Ngay cả khi xảy ra sự cố Container Escape nghiêm trọng nhất, kẻ tấn công khi thoát ra ngoài máy chủ cũng chỉ có quyền hạn của một người dùng thông thường, không thể phá hủy cấu hình hệ điều hành hay đánh cắp dữ liệu của các tiến trình khác.", indent=400))

    body.append(heading2("1.2. MỤC TIÊU NGHIÊN CỨU CỦA ĐỀ TÀI"))
    body.append(heading3("1.2.1. Mục tiêu tổng quát"))
    body.append(p("Mục tiêu tổng quát của đề tài là xây dựng, cấu hình và triển khai thành công một hệ sinh thái MLOps mã nguồn mở hoàn chỉnh trên hai hệ điều hành Arch Linux và Ubuntu Server; hiện thực hóa mô hình Rootless Containerization và tường lửa stateful hiện đại; từ đó thực hiện đánh giá thực nghiệm định lượng đối sánh toàn diện về an ninh và hiệu năng giữa hai trường phái Linux.", indent=400))

    body.append(heading3("1.2.2. Mục tiêu kỹ thuật cụ thể"))
    body.append(p("Đề tài cam kết hoàn thành 6 mục tiêu kỹ thuật cụ thể theo tiêu chuẩn SMART:", indent=400))
    body.append(p("1. Mục tiêu 1 (Tự động hóa hạ tầng IaC): Xây dựng bộ kịch bản tự động hóa 100% bằng Bash script cài đặt và gia cố an ninh hệ thống, đảm bảo tính Idempotent (chạy lặp lại nhiều lần không sinh lỗi) và bắt buộc phải có kịch bản Rollback tương ứng để hoàn trả hệ thống về trạng thái ban đầu.", indent=400))
    body.append(p("2. Mục tiêu 2 (Bảo mật tầng hệ điều hành): Hardening dịch vụ OpenSSH sang cổng 2222, cấm đăng nhập root; tinh chỉnh các tham số kernel qua sysctl để tối ưu hóa hàng đợi socket cho MLOps; thiết lập tường lửa stateful (nftables trên Arch Linux và UFW trên Ubuntu) với chính sách chặn mặc định (Default Deny).", indent=400))
    body.append(p("3. Mục tiêu 3 (Kiến trúc Rootless Docker unprivileged): Triển khai thành công Docker Engine unprivileged trên Arch Linux thông qua User Namespaces (ánh xạ subuid/subgid 100000:65536) và cgroups v2 resource delegation, tích hợp dịch vụ systemd user unit tự động khởi động cùng hệ điều hành.", indent=400))
    body.append(p("4. Mục tiêu 4 (Đóng gói cụm MLOps Stack chuẩn Zero-Trust): Thiết kế kiến trúc phân tách hai mạng Docker nội bộ (`mlops-backend` cô lập hoàn toàn cơ sở dữ liệu PostgreSQL, MinIO API; `mlops-frontend` mở cổng MLflow, FastAPI, Grafana). Đóng gói dịch vụ FastAPI OCR bằng Dockerfile Multi-Stage chạy dưới tài khoản non-root UID 10001.", indent=400))
    body.append(p("5. Mục tiêu 5 (Phát triển công cụ kiểm định và tương tác): Xây dựng công cụ kiểm tra tự động 04_verify_system.sh đánh giá tính toàn vẹn 5 chốt chặn an ninh; phát triển công cụ dòng lệnh ai_cli.sh cho phép kỹ sư tương tác quét ảnh OCR và kiểm tra sức khỏe hệ thống trực tiếp trên Terminal bằng mã màu ANSI.", indent=400))
    body.append(p("6. Mục tiêu 6 (Đo lường Benchmark đối kháng định lượng): Thiết kế kịch bản load test đo lường thông lượng xử lý (RPS), độ trễ phân vị p50/p95/p99 của API và mức tiêu thụ tài nguyên RAM/CPU tĩnh và động giữa Arch Linux và Ubuntu Server.", indent=400))

    body.append(heading3("1.2.3. Sản phẩm và kết quả mong đợi"))
    body.append(p("Kết quả bàn giao của đề tài bao gồm:", indent=400))
    body.append(p("• Kho mã nguồn Git hoàn chỉnh tuân thủ Conventional Commits và mô hình phân nhánh chuyên nghiệp.", indent=400))
    body.append(p("• Hai hệ thống máy ảo hoạt động ổn định: Node Arch Linux (Rolling Release, Rootless Docker, nftables) và Node Ubuntu Server (LTS, Rootful Docker, UFW).", indent=400))
    body.append(p("• Bộ kịch bản IaC Bash script đầy đủ các tính năng Hardening, Setup, Deploy, Verify và Rollback.", indent=400))
    body.append(p("• Bản báo cáo kỹ thuật toàn diện dày trên 80 trang trình bày đầy đủ cơ sở khoa học, kiến trúc, mã nguồn và số liệu thực nghiệm.", indent=400))

    body.append(heading2("1.3. ĐỐI TƯỢNG VÀ PHẠM VI NGHIÊN CỨU"))
    body.append(heading3("1.3.1. Đối tượng nghiên cứu"))
    body.append(p("Đối tượng nghiên cứu chính của đề tài bao gồm:", indent=400))
    body.append(p("• Hạt nhân hệ điều hành Linux (Linux Kernel Space): Cơ chế quản lý tiến trình, cơ chế ảo hóa không gian tên Namespaces, hệ thống kiểm soát tài nguyên cgroups v2 và khung xử lý gói tin Netfilter.", indent=400))
    body.append(p("• Các bản phân phối Linux: Arch Linux đại diện cho mô hình Rolling Release và Ubuntu Server 22.04 LTS đại diện cho mô hình Long-Term Support.", indent=400))
    body.append(p("• Công nghệ container hóa: Docker Engine, RootlessKit, fuse-overlayfs, slirp4netns.", indent=400))
    body.append(p("• Các dịch vụ MLOps mã nguồn mở: MLflow Tracking Server, PostgreSQL Database, MinIO Object Storage, FastAPI framework, Tesseract OCR Engine, Prometheus Time-Series Database và Grafana Visualization.", indent=400))

    body.append(heading3("1.3.2. Phạm vi triển khai"))
    body.append(p("Phạm vi triển khai của đề tài tập trung vào việc thiết lập và so sánh hạ tầng máy chủ cục bộ (On-premises / Local Lab Environment) được ảo hóa bằng Oracle VM VirtualBox hoặc chạy trực tiếp trên phần cứng máy trạm của sinh viên. Toàn bộ các dịch vụ được triển khai thực nghiệm độc lập trên hai môi trường Arch Linux và Ubuntu Server với cấu hình phần cứng tương đương (2 CPU vCore, 4GB - 8GB RAM, 40GB SSD) để đảm bảo tính khách quan và khoa học của các số liệu đối sánh.", indent=400))

    body.append(heading3("1.3.3. Giới hạn kỹ thuật của đề tài"))
    body.append(p("Để tập trung tối đa vào mục tiêu chuyên môn của học phần \"Linux và Phần mềm nguồn mở\", đề tài xác định rõ các giới hạn sau:", indent=400))
    body.append(p("• Giới hạn về Trí tuệ nhân tạo: Đề tài tập trung vào khía cạnh Quản trị hệ thống, Hạ tầng và Triển khai (Infrastructure & Operations), không nghiên cứu sâu về thuật toán huấn luyện mạng nơ-ron phức tạp hay tối ưu hóa độ chính xác mô hình. Khối lượng công việc AI được đại diện bằng một mô hình nhận dạng ký tự quang học (OCR) nhẹ nhàng và thực tế, sử dụng Tesseract OCR và OpenCV tích hợp qua FastAPI.", indent=400))
    body.append(p("• Giới hạn về hạ tầng phân tán: Đề tài nghiên cứu sâu mô hình máy chủ đơn (Single-Host Node Isolation) trên cả hai hệ điều hành, không triển khai cụm phân tán đa máy chủ Kubernetes để tránh làm loãng trọng tâm nghiên cứu về đặc tính hạt nhân của từng OS.", indent=400))

    body.append(heading2("1.4. PHƯƠNG PHÁP LUẬN NGHIÊN CỨU"))
    body.append(heading3("1.4.1. Phương pháp nghiên cứu lý thuyết"))
    body.append(p("Nhóm tác giả tiến hành thu thập, dịch thuật và tổng hợp các tài liệu học thuật chính thống từ các tổ chức tiêu chuẩn hóa và các dự án mã nguồn mở uy tín: Tài liệu kiến trúc nhân Linux của kernel.org, chuẩn bảo mật CIS Docker Benchmark v1.6.0 của Center for Internet Security, tài liệu hướng dẫn Rootless Mode của Docker Inc., cẩm nang kỹ thuật của ArchWiki và Ubuntu Server Guide. Trên cơ sở đó, nhóm xây dựng khung lý thuyết vững chắc về cách thức các công nghệ tương tác ở cấp độ hạt nhân hệ điều hành.", indent=400))

    body.append(heading3("1.4.2. Phương pháp thực nghiệm đối sánh (Empirical Benchmarking)"))
    body.append(p("Phương pháp thực nghiệm đối sánh được thiết kế với tính chặt chẽ cao:", indent=400))
    body.append(p("• Thiết lập môi trường thử nghiệm đối xứng: Cả hai node Arch Linux và Ubuntu Server đều được cấp phát cấu hình tài nguyên phần cứng đồng nhất.", indent=400))
    body.append(p("• Áp dụng cùng một kịch bản tải trọng: Sử dụng công cụ kiểm thử tải tự động để bắn liên tục 500 requests với mức độ tương tranh 10 kết nối đồng thời vào endpoint `/predict/ocr` của vi dịch vụ AI.", indent=400))
    body.append(p("• Thu thập dữ liệu đa chiều: Ghi nhận số liệu tài nguyên qua `free -m`, `vmstat`, `systemd-analyze` và các chỉ số chuỗi thời gian do Prometheus thu thập từ Node Exporter.", indent=400))

    body.append(heading3("1.4.3. Phương pháp đánh giá an ninh đa tầng (Defense in Depth)"))
    body.append(p("Đánh giá an ninh không chỉ dựa trên việc hệ thống có hoạt động hay không, mà phải được kiểm chứng qua các kịch bản tấn công giả định (Simulated Attack Scenarios):", indent=400))
    body.append(p("• Thử nghiệm quét cổng (Port Scanning) từ bên ngoài bằng Nmap để kiểm tra hiệu lực chặn của nftables và UFW.", indent=400))
    body.append(p("• Thử nghiệm truy cập trái phép cổng nội bộ của cơ sở dữ liệu PostgreSQL (5432) để kiểm chứng ranh giới Zero-Trust.", indent=400))
    body.append(p("• Kiểm tra sự tương quan giữa danh tính UID tiến trình bên trong container và UID trên máy chủ host để chứng minh hiệu lực của User Namespaces.", indent=400))

    body.append(heading2("1.5. Ý NGHĨA KHOA HỌC VÀ GIÁ TRỊ THỰC TIỄN"))
    body.append(heading3("1.5.1. Ý nghĩa khoa học"))
    body.append(p("Đề tài cung cấp một công trình nghiên cứu đối sánh thực nghiệm độc lập và có hệ thống giữa hai trường phái phát hành hệ điều hành Linux tiêu biểu nhất hiện nay. Các số liệu thu thập được về mức tiêu thụ RAM tĩnh, thời gian khởi động hệ điều hành và độ trễ xử lý mạng cung cấp bằng chứng định lượng rõ ràng cho thấy: Việc loại bỏ các dịch vụ nền dư thừa theo triết lý \"The Arch Way\" giúp giải phóng tài nguyên phần cứng quý giá như thế nào để phục vụ cho các thuật toán tính toán nặng nề của Trí tuệ nhân tạo.", indent=400))

    body.append(heading3("1.5.2. Giá trị thực tiễn đối với doanh nghiệp"))
    body.append(p("Đối với các doanh nghiệp và tổ chức công nghệ, kết quả của đề tài mang lại những giá trị ứng dụng trực tiếp:", indent=400))
    body.append(p("• Cung cấp bộ kịch bản tự động hóa IaC hoàn chỉnh, có thể tái sử dụng ngay để triển khai một pháo đài MLOps an toàn trong môi trường thực tế mà không cần cấu hình thủ công phức tạp.", indent=400))
    body.append(p("• Chứng minh tính khả thi và hướng dẫn chi tiết cách triển khai Rootless Docker unprivileged – giải pháp giúp loại bỏ hoàn toàn một trong những rủi ro an ninh nghiêm trọng nhất của container hóa.", indent=400))
    body.append(p("• Định hình chuẩn mực phân tách mạng Zero-Trust giúp bảo vệ an toàn cho cơ sở dữ liệu và kho dữ liệu học máy trước nguy cơ rò rỉ thông tin nội bộ.", indent=400))

    body.append(p("Bảng 1.3: Ma trận phân bổ trách nhiệm thành viên nhóm theo chuẩn RACI", align="center", bold=True, size=24, space_after=60))
    headers_1_3 = ["Hạng mục công việc", "Nguyễn Công Đức (Lead)", "Nguyễn Tùng Dương (TV2)", "Nguyễn Văn C (TV3)"]
    rows_1_3 = [
        ["Nghiên cứu kiến trúc & Lập kế hoạch", "A / R (Chịu trách nhiệm chính)", "C (Tham vấn)", "C (Tham vấn)"],
        ["Hardening & IaC Node Arch Linux", "A / R (Thực hiện toàn bộ)", "I (Thông báo)", "I (Thông báo)"],
        ["Cấu hình Rootless Docker & nftables", "A / R (Thực hiện toàn bộ)", "I (Thông báo)", "I (Thông báo)"],
        ["Hardening & IaC Node Ubuntu Server", "C (Hỗ trợ kỹ thuật)", "A / R (Thực hiện toàn bộ)", "I (Thông báo)"],
        ["Cấu hình UFW & Docker daemon Ubuntu", "C (Hỗ trợ kỹ thuật)", "A / R (Thực hiện toàn bộ)", "I (Thông báo)"],
        ["Đóng gói Docker Compose & FastAPI OCR", "A / R (Thiết kế & Đóng gói)", "C (Kiểm thử Ubuntu)", "C (Tích hợp metrics)"],
        ["Thiết lập Prometheus, Grafana & Metrics", "C (Hỗ trợ endpoint)", "I (Thông báo)", "A / R (Thực hiện toàn bộ)"],
        ["Kịch bản kiểm tra an ninh & CLI Terminal", "A / R (Viết script & CLI)", "C (Kiểm thử tương thích)", "I (Thông báo)"],
        ["Thực thi Benchmark & Phân tích số liệu", "A (Chủ trì đo lường Arch)", "R (Đo lường Ubuntu)", "R (Thu thập TSDB)"],
        ["Biên soạn báo cáo đồ án chính thức", "A / R (Tổng hợp & Viết chính)", "R (Đóng góp phần Ubuntu)", "R (Đóng góp Monitor/BM)"]
    ]
    body.append(table_grid(headers_1_3, rows_1_3))
    body.append(p("Ghi chú: R (Responsible) – Người thực hiện; A (Accountable) – Người chịu trách nhiệm phê duyệt; C (Consulted) – Người được tham vấn ý kiến; I (Informed) – Người được thông báo tiến độ.", italic=True, size=21, space_before=40, space_after=120))
    body.append(page_break())

    return body
