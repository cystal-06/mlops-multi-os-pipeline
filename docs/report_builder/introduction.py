from .styles import p, heading1, heading2, page_break

def build_introduction():
    body = []
    body.append(heading1("MỞ ĐẦU"))
    
    body.append(heading2("1. Tính cấp thiết của đề tài"))
    body.append(p("Trong làn sóng chuyển đổi số và bùng nổ của Trí tuệ nhân tạo (AI) trên toàn thế giới, các thuật toán học máy (Machine Learning) đã rời khỏi phạm vi phòng thí nghiệm hàn lâm để trở thành động cơ cốt lõi phục vụ các hoạt động kinh doanh trực tuyến, từ nhận dạng hình ảnh, xử lý ngôn ngữ tự nhiên cho đến dự báo tài chính tự động. Tuy nhiên, sự dịch chuyển này đã làm phát sinh một nút thắt cổ chai kỹ thuật khổng lồ: Khoảng cách giữa việc xây dựng một mô hình toán học hoạt động trên máy tính cá nhân của nhà khoa học dữ liệu (Data Scientist) và việc vận hành mô hình đó một cách liên tục, ổn định, an toàn tại môi trường sản xuất (Production) phục vụ hàng triệu người dùng.", indent=400))
    body.append(p("Thuật ngữ MLOps (Machine Learning Operations) ra đời như một triết lý kỹ thuật mới, kế thừa các nguyên lý tự động hóa của DevOps (CI/CD, Infrastructure as Code, Monitoring) nhưng tích hợp thêm các yêu cầu đặc thù của trí tuệ nhân tạo như quản lý vòng đời mô hình (Model Registry), lưu vết siêu tham số (Experiment Tracking) và kiểm soát sự trôi dạt của dữ liệu (Data Drift).", indent=400))
    body.append(p("Hệ điều hành Linux là nền tảng điện toán chiếm ưu thế tuyệt đối khi vận hành hơn 90% khối lượng công việc MLOps toàn cầu. Dẫu vậy, trong hệ sinh thái phong phú của mã nguồn mở, việc lựa chọn bản phân phối Linux (Linux Distribution) tối ưu luôn gây ra nhiều tranh luận gay gắt giữa hai trường phái đối lập:", indent=400))
    body.append(p("• Trường phái Rolling Release (đại diện tiêu biểu là Arch Linux): Đề cao triết lý tối giản (\"The Arch Way\"), liên tục cập nhật hạt nhân Linux Kernel và các gói phần mềm upstream mới nhất từng ngày mà không cần cài đặt lại phiên bản. Lợi thế là khả năng khai thác các tính năng mới nhất của nhân Linux (cgroups v2, eBPF, nftables nâng cao), nhưng đòi hỏi kỹ sư quản trị phải có năng lực làm chủ hệ thống chuyên sâu.", indent=400))
    body.append(p("• Trường phái Fixed Release / Long-Term Support (đại diện tiêu biểu là Ubuntu Server LTS): Đóng băng các phiên bản phần mềm trong chu kỳ 5 năm, hướng tới sự ổn định tuyệt đối và dễ dàng triển khai hàng loạt trong doanh nghiệp, nhưng đi kèm với sự cồng kềnh của các dịch vụ chạy ngầm mặc định và sự chậm trễ trong việc tiếp cận công nghệ kernel mới.", indent=400))
    body.append(p("Mặt khác, trong khi container hóa bằng Docker đã trở thành tiêu chuẩn de-facto để đóng gói vi dịch vụ MLOps, thì đại đa số các hệ thống hiện nay vẫn mắc phải sai lầm an ninh nghiêm trọng: Triển khai Docker daemon dưới quyền quản trị tối cao (root - UID 0). Cấu hình này mở toang cánh cửa cho các cuộc tấn công thoát rào container (Container Escape), biến việc chiếm đoạt một container vi dịch vụ AI trở thành bàn đạp để chiếm quyền điều khiển toàn bộ máy chủ vật lý.", indent=400))
    body.append(p("Xuất phát từ thực tiễn trên, đề tài \"Configure and Deploy MLOps (Machine Learning Ops) Services on Arch Linux & Ubuntu\" được thực hiện nhằm giải quyết trọn vẹn bài toán xây dựng nền tảng MLOps an toàn, tiên phong triển khai công nghệ Rootless Containerization trên Arch Linux và thực hiện đối sánh định lượng toàn diện với Ubuntu Server.", indent=400))

    body.append(heading2("2. Mục đích và nhiệm vụ nghiên cứu"))
    body.append(p("Mục đích nghiên cứu của đề tài là xây dựng thành công một hệ sinh thái MLOps mã nguồn mở cấp doanh nghiệp độc lập hoàn toàn trên hai hệ điều hành Arch Linux và Ubuntu Server, áp dụng các kỹ thuật an ninh tiên tiến (Rootless Docker, nftables, Zero-Trust network) và thực hiện đo lường tải trọng định lượng nhằm đưa ra các khuyến nghị kiến trúc cho cộng đồng kỹ thuật.", indent=400))
    body.append(p("Để hoàn thành mục đích nói trên, các nhiệm vụ cụ thể được xác định bao gồm:", indent=400))
    body.append(p("1. Nghiên cứu lý thuyết chuyên sâu về kiến trúc hạt nhân Linux Kernel, phân tầng không gian người dùng và hạt nhân, cơ chế cgroups v2, User Namespaces và mạng Netfilter.", indent=400))
    body.append(p("2. Thiết kế và hiện thực hóa bộ kịch bản tự động hóa hạ tầng (IaC) bằng Bash script tuân thủ tính Idempotent và có khả năng phục hồi (Rollback) an toàn.", indent=400))
    body.append(p("3. Triển khai kiến trúc Rootless Docker Engine unprivileged trên Arch Linux, vô hiệu hóa hoàn toàn đặc quyền root của container runtime.", indent=400))
    body.append(p("4. Đóng gói vi dịch vụ AI OCR bằng FastAPI và triển khai cụm MLOps Stack gồm: MLflow Server, PostgreSQL, MinIO S3, Prometheus và Grafana.", indent=400))
    body.append(p("5. Xây dựng công cụ kiểm tra an ninh tự động 04_verify_system.sh và giao diện dòng lệnh tương tác ai_cli.sh cho người quản trị.", indent=400))
    body.append(p("6. Thực hiện kịch bản thử nghiệm chịu tải (Benchmarking) đối sánh hiệu năng thông lượng (RPS), độ trễ (Latency) và mức chiếm dụng RAM giữa Arch Linux và Ubuntu Server.", indent=400))

    body.append(heading2("3. Phương pháp nghiên cứu"))
    body.append(p("Đề tài áp dụng kết hợp ba phương pháp nghiên cứu chính: Phương pháp nghiên cứu lý thuyết (tổng hợp tài liệu chuẩn RFC, tài liệu chính thức của ArchWiki, Docker Docs, Canonical Ubuntu Server); Phương pháp thực nghiệm đối kháng (xây dựng hai hệ thống máy ảo độc lập, triển khai cùng một khối lượng công việc MLOps Stack và đo lường thông số); Phương pháp phân tích định lượng (thu thập số liệu thống kê qua Apache Bench, Prometheus TSDB và phân tích phương sai).", indent=400))

    body.append(heading2("4. Bố cục của đồ án"))
    body.append(p("Báo cáo đồ án được cấu trúc thành 7 chương chính như sau:", indent=400))
    body.append(p("• Chương 1: Tổng quan về đề tài – Giới thiệu bối cảnh, mục tiêu, đối tượng, phạm vi và ý nghĩa khoa học của đề tài.", indent=400))
    body.append(p("• Chương 2: Cơ sở lý thuyết và công nghệ cốt lõi – Phân tích bản chất nhân Linux, công nghệ Containerization, Rootless Docker, tường lửa nftables và hệ sinh thái MLOps.", indent=400))
    body.append(p("• Chương 3: Phương pháp nghiên cứu và thiết kế hệ thống – Thiết kế kiến trúc tổng thể, phân đoạn mạng Zero-Trust, bảo mật 7 lớp Defense in Depth và ma trận rủi ro.", indent=400))
    body.append(p("• Chương 4: Triển khai thực nghiệm và vận hành hệ thống – Trình bày chi tiết mã nguồn kịch bản IaC, cấu hình hệ thống trên Arch Linux và Ubuntu Server, giao diện CLI và công cụ xác minh.", indent=400))
    body.append(p("• Chương 5: Đánh giá định lượng benchmark và bảo mật – Phân tích các số liệu thực nghiệm về an ninh, chiếm dụng RAM và hiệu năng chịu tải API.", indent=400))
    body.append(p("• Chương 6: Kết luận và hướng phát triển – Tóm tắt các kết quả đạt được, đánh giá mục tiêu và đề xuất hướng mở rộng hệ thống.", indent=400))
    body.append(p("• Chương 7: Tài liệu tham khảo – Danh mục các tài liệu học thuật và tiêu chuẩn kỹ thuật quốc tế được trích dẫn.", indent=400))
    body.append(page_break())

    return body
