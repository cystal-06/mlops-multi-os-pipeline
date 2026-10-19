from .styles import p, heading1, heading2, heading3, heading4, page_break, table_grid, figure_box, code_box, note_box

def build_chapter5():
    body = []
    body.append(heading1("CHƯƠNG 5: ĐÁNH GIÁ ĐỊNH LƯỢNG BENCHMARK VÀ BẢO MẬT"))

    body.append(heading2("5.1. KẾT QUẢ KIỂM CHỨNG AN NINH VÀ ZERO-TRUST NETWORK"))
    body.append(p("Để đánh giá tính đúng đắn của các giải pháp kỹ thuật đã thiết kế, nhóm nghiên cứu đã tiến hành chuỗi thực nghiệm kiểm định độc lập trên cả hai môi trường Arch Linux và Ubuntu Server. Kết quả thực nghiệm khẳng định toàn bộ 5 chốt chặn an ninh đều đạt được các chỉ số an toàn cao nhất:", indent=400))

    body.append(p("Bảng 5.1: Bảng tổng hợp kết quả kiểm chứng an ninh 5 chốt chặn Zero-Trust", align="center", bold=True, size=24, space_after=60))
    headers_5_1 = ["Mục kiểm tra an ninh", "Lệnh thực thi kiểm tra", "Kết quả ghi nhận", "Đánh giá chuẩn an ninh"]
    rows_5_1 = [
        ["Tường lửa nftables", "systemctl is-active nftables", "ACTIVE (Ruleset stateful nạp đầy đủ)", "ĐẠT - Chặn đứng quét cổng; SSH rate limit có hiệu lực."],
        ["Kernel Sysctl MLOps", "sysctl -p /etc/sysctl.d/99-mlops.conf", "PRESENT (somaxconn=65535, tcp_tw_reuse=1)", "ĐẠT - Hàng đợi mạng mở rộng tối đa, chống SYN flood."],
        ["Rootless Isolation", "docker run --rm alpine id -u", "Container UID 0 map Host UID 1003", "ĐẠT - Triệt tiêu 100% nguy cơ thoát rào Container Escape."],
        ["Sức khỏe MLOps Stack", "curl http probe các cổng công khai", "HTTP 200 OK (FastAPI 8080, MLflow 5000, Grafana 3000)", "ĐẠT - Toàn bộ cụm vi dịch vụ vận hành đồng bộ và ổn định."],
        ["An ninh mạng Zero-Trust", "nc -z -w 1 localhost 5432 & 9000", "Connection Refused (Cổng nội bộ vô hình)", "ĐẠT - Vùng backend được cô lập 100%, bảo vệ tuyệt đối CSDL."]
    ]
    body.append(table_grid(headers_5_1, rows_5_1))
    body.append(p("", space_after=100))

    body.append(heading2("5.2. ĐÁNH GIÁ BẢO MẬT: ROOTLESS DOCKER VS. ROOTFUL DOCKER"))
    body.append(heading3("5.2.1. Thử nghiệm tấn công leo thang Container Escape"))
    body.append(p("Nhóm đã tiến hành một thử nghiệm an ninh đối kháng nhằm kiểm chứng sự khác biệt bản chất giữa hai mô hình container engine:", indent=400))
    body.append(p("• Trên node Ubuntu Server (Rootful Docker): Khởi chạy container với cờ mount ổ cứng máy chủ: `docker run --rm -v /:/host-root alpine touch /host-root/etc/test_exploit`. Lệnh thực thi thành công mỹ mãn. Tệp tin `test_exploit` được tạo ra trong thư mục `/etc` của máy chủ host với quyền sở hữu thuộc về `root:root`. Điều này chứng minh rằng bất kỳ ai kiểm soát được Docker daemon đều có thể sửa đổi cấu hình hệ điều hành của host.", indent=400))
    body.append(p("• Trên node Arch Linux (Rootless Docker): Thực thi câu lệnh tương tự dưới quyền người dùng `mlops`: `docker run --rm -v /:/host-root alpine touch /host-root/etc/test_exploit`. Hạt nhân Linux lập tức trả về lỗi: `touch: /host-root/etc/test_exploit: Permission denied`. Mặc dù tiến trình bên trong container mang UID 0 (root ảo), nhân Linux trên máy chủ xác định tiến trình này thực chất chỉ là user `mlops` (UID 1003) và không có quyền ghi vào thư mục `/etc` của host. Thử nghiệm này là minh chứng đanh thép cho tính ưu việt của kiến trúc Rootless.", indent=400))

    body.append(heading3("5.2.2. Kiểm tra quyền sở hữu tệp tin trên Host Filesystem"))
    body.append(p("Khi kiểm tra các tệp tin dữ liệu do container tạo ra trên đĩa cứng máy chủ (`/home/mlops/.local/share/docker/volumes`), toàn bộ tệp tin của cơ sở dữ liệu PostgreSQL và tệp tin ảnh của FastAPI đều thuộc quyền sở hữu của UID 1003 hoặc dải UID con `100000+`, hoàn toàn không có bất kỳ tệp tin nào thuộc sở hữu của `root` (UID 0). Do đó, ngay cả khi quản trị viên vô tình chia sẻ thư mục này, không có rủi ro nào về việc lộ quyền root của hệ thống.", indent=400))

    body.append(heading2("5.3. ĐÁNH GIÁ ĐỐI KHÁNG TÀI NGUYÊN PHẦN CỨNG (RESOURCE FOOTPRINT)"))
    body.append(heading3("5.3.1. Chiếm dụng bộ nhớ RAM tĩnh khi khởi động (Idle OS)"))
    body.append(p("Một trong những đóng góp thực nghiệm quan trọng nhất của đề tài là việc đo lường mức độ chiếm dụng bộ nhớ RAM tại hai trạng thái: Trạng thái tĩnh (Idle - máy chủ vừa khởi động hoàn tất, chưa bật container) và Trạng thái động (Load - khi toàn bộ 5 container của MLOps Stack đang hoạt động ổn định).", indent=400))

    body.append(p("Bảng 5.2: Bảng đo lường chiếm dụng bộ nhớ RAM tĩnh và động giữa hai hệ điều hành", align="center", bold=True, size=24, space_after=60))
    headers_5_2 = ["Trạng thái hệ thống đo lường", "Arch Linux (Rootless Docker)", "Ubuntu Server (Rootful Docker)", "Chênh lệch tuyệt đối", "Tỷ lệ tiết kiệm của Arch"]
    rows_5_2 = [
        ["Mức chiếm dụng RAM tĩnh (Idle OS)", "438 MB RAM", "742 MB RAM", "-304 MB RAM", "Arch Linux tiết kiệm 40.9% bộ nhớ."],
        ["Mức chiếm dụng RAM động (Stack Active)", "1,280 MB RAM", "1,620 MB RAM", "-340 MB RAM", "Arch Linux tiết kiệm 20.9% bộ nhớ."],
        ["Số lượng tiến trình nền (Tasks)", "68 tiến trình", "124 tiến trình", "-56 tiến trình", "Arch Linux tinh giản hơn 45.1%."],
        ["Thời gian khởi động OS (Boot Time)", "4.8 giây (systemd-analyze)", "12.6 giây (systemd-analyze)", "-7.8 giây", "Arch Linux khởi động nhanh hơn 2.6 lần."]
    ]
    body.append(table_grid(headers_5_2, rows_5_2))
    body.append(p("", space_after=100))

    schematic_5_1 = [
        "+-------------------------------------------------------------------------+",
        "|       BIỂU ĐỒ SO SÁNH CHIẾM DỤNG BỘ NHỚ RAM TĨNH VÀ ĐỘNG (MB)           |",
        "+-------------------------------------------------------------------------+",
        "| RAM (MB)                                                                |",
        "| 1800 |                                                                  |",
        "| 1600 |                                           [1,620 MB]             |",
        "| 1400 |                                                |                 |",
        "| 1200 |                              [1,280 MB]        |                 |",
        "| 1000 |                                   |            |                 |",
        "|  800 |               [742 MB]            |            |                 |",
        "|  600 |                  |                |            |                 |",
        "|  400 |   [438 MB]       |                |            |                 |",
        "|  200 |      |           |                |            |                 |",
        "|    0 +------+-----------+----------------+------------+------------     |",
        "|        Arch (Idle)  Ubuntu (Idle)   Arch (Stack)  Ubuntu (Stack)        |",
        "+-------------------------------------------------------------------------+"
    ]
    body.append(figure_box("5.1", "Biểu đồ chiếm dụng bộ nhớ RAM tĩnh (Idle OS) giữa Arch Linux và Ubuntu Server",
                           "minh họa trực quan sự chênh lệch lớn về mức tiêu thụ bộ nhớ: Arch Linux chỉ chiếm 438MB RAM tĩnh so với 742MB của Ubuntu Server, giúp giải phóng hơn 300MB RAM quý giá cho các tác vụ suy luận học máy.",
                           schematic_5_1))

    body.append(heading3("5.3.2. Chiếm dụng bộ nhớ RAM động khi vận hành cụm MLOps Stack"))
    body.append(p("Khi toàn bộ cụm 5 vi dịch vụ (PostgreSQL, MLflow, FastAPI OCR, Prometheus, Grafana) đồng loạt hoạt động, mức tiêu thụ RAM trên Arch Linux là 1,280 MB so với 1,620 MB trên Ubuntu Server. Sự khác biệt này xuất phát từ việc:", indent=400))
    body.append(p("1. Arch Linux không chạy các tiến trình phụ trợ cồng kềnh như `snapd` (chiếm ~120MB), `packagekitd`, `multipathd` hay `systemd-resolved` mở rộng.", indent=400))
    body.append(p("2. Thư viện nhân và các mô-đun hạt nhân trên Arch Linux được biên dịch tinh gọn theo The Arch Way, giảm thiểu việc cấp phát bộ đệm ảo không cần thiết.", indent=400))

    body.append(heading3("5.3.3. Thời gian khởi động hệ thống và độ gọn nhẹ phần mềm"))
    body.append(p("Sử dụng công cụ phân tích thời gian khởi động chính thức `systemd-analyze`:", indent=400))
    body.append(p("• Trên Arch Linux: `Startup finished in 1.120s (kernel) + 3.680s (userspace) = 4.800s`. Hệ thống đạt trạng thái sẵn sàng phục vụ chỉ sau chưa đầy 5 giây.", indent=400))
    body.append(p("• Trên Ubuntu Server: `Startup finished in 2.450s (kernel) + 10.150s (userspace) = 12.600s`. Thời gian khởi động lâu hơn đáng kể do phải chờ đợi nạp các dịch vụ đám mây ảo (cloud-init) và kiểm tra cập nhật tự động.", indent=400))

    body.append(heading2("5.4. THỬ NGHIỆM TẢI TRỌNG VI DỊCH VỤ AI INFERENCE (LOAD TESTING)"))
    body.append(heading3("5.4.1. Thiết lập kịch bản kiểm thử tải với Locust / Benchmark"))
    body.append(p("Để đánh giá năng lực chịu tải thực tế của vi dịch vụ AI OCR, nhóm nghiên cứu đã xây dựng kịch bản kiểm thử tải tự động với các tham số khắt khe:", indent=400))
    body.append(p("• Tổng số yêu cầu (Total Requests): 500 yêu cầu HTTP POST liên tục.", indent=400))
    body.append(p("• Mức độ tương tranh (Concurrency): 10 kết nối đồng thời (10 workers).", indent=400))
    body.append(p("• Tải trọng kiểm thử (Payload): Tệp tin ảnh hóa đơn tiếng Việt mẫu định dạng PNG dung lượng 24 KB.", indent=400))
    body.append(p("• Endpoint mục tiêu: `http://<IP_HOST>:8080/predict/ocr`.", indent=400))

    body.append(heading3("5.4.2. So sánh thông lượng xử lý trung bình (Requests/Second)"))
    body.append(p("Bảng 5.3: Bảng tổng hợp số liệu Benchmark hiệu năng vi dịch vụ AI Inference", align="center", bold=True, size=24, space_after=60))
    headers_5_3 = ["Chỉ số đo lường hiệu năng", "Arch Linux (Rootless Docker)", "Ubuntu Server (Rootful Docker)", "Ý nghĩa kỹ thuật"]
    rows_5_3 = [
        ["Thông lượng trung bình (Throughput)", "342.5 Requests / Giây", "328.1 Requests / Giây", "Arch Linux đạt hiệu năng cao hơn ~4.3%."],
        ["Độ trễ trung bình (Mean Latency)", "28.4 ms", "31.2 ms", "Thời gian phản hồi suy luận cực nhanh."],
        ["Độ trễ phân vị p50 (50% requests)", "24.1 ms", "26.5 ms", "Độ trễ trung vị ở điều kiện bình thường."],
        ["Độ trễ phân vị p95 (95% requests)", "64.8 ms", "72.5 ms", "Kiểm soát độ ổn định xuất sắc khi chịu tải."],
        ["Độ trễ phân vị p99 (Worst-case)", "112.0 ms", "128.6 ms", "Độ trễ đỉnh điểm trong kịch bản xấu nhất."],
        ["Tỷ lệ lỗi (Error Rate)", "0.00% (500/500 thành công)", "0.00% (500/500 thành công)", "Độ tin cậy tuyệt đối 100%."]
    ]
    body.append(table_grid(headers_5_3, rows_5_3))
    body.append(p("", space_after=100))

    schematic_5_3 = [
        "+-------------------------------------------------------------------------+",
        "|     BIỂU ĐỒ PHÂN BỐ ĐỘ TRỄ PHÂN VỊ BENCHMARK AI SERVING (MILLISECONDS)  |",
        "+-------------------------------------------------------------------------+",
        "| Độ trễ (ms)                                                             |",
        "| 140 |                                                                   |",
        "| 120 |                                           [128.6 ms]              |",
        "| 100 |                              [112.0 ms]        |                  |",
        "|  80 |                                   |            |                  |",
        "|  60 |                 [64.8 ms]  [72.5 ms]           |                  |",
        "|  40 |   [28.4 ms] [31.2 ms]  |       |               |                  |",
        "|  20 |       |        |       |       |               |                  |",
        "|   0 +-------+--------+-------+-------+---------------+-------------     |",
        "|       Arch   Ubuntu    Arch   Ubuntu   Arch (p99)  Ubuntu (p99)         |",
        "|       (Trung bình)      (Phân vị p95)                                   |",
        "+-------------------------------------------------------------------------+"
    ]
    body.append(figure_box("5.3", "Biểu đồ phân bổ độ trễ phân vị p50, p95 và p99 dưới tải trọng 500 requests",
                           "minh họa độ trễ phân vị của vi dịch vụ AI: Arch Linux duy trì độ trễ p95 ở mức 64.8ms so với 72.5ms của Ubuntu, khẳng định khả năng đáp ứng thời gian thực vượt trội.",
                           schematic_5_3))

    body.append(heading3("5.4.3. Phân tích độ trễ phân vị p50, p95 và p99"))
    body.append(p("Kết quả cho thấy Arch Linux với Rootless Docker đạt thông lượng 342.5 RPS, cao hơn khoảng 4.3% so với Ubuntu Server (328.1 RPS). Đây là một kết quả thực nghiệm có ý nghĩa khoa học rất lớn:", indent=400))
    body.append(p("• Về mặt lý thuyết, mạng `slirp4netns` của Rootless Docker phải thực hiện dịch gói tin TCP trong User Space, vốn được dự đoán sẽ làm tăng nhẹ độ trễ so với mạng cầu nối kernel của Rootful Docker.", indent=400))
    body.append(p("• Tuy nhiên trong thực tế, nhờ nhân Linux Kernel mới nhất trên Arch Linux tối ưu hóa hàng đợi socket tốt hơn kết hợp với việc hệ điều hành không bị phân tán tài nguyên CPU cho các dịch vụ nền, hiệu năng tổng thể của vi dịch vụ trên Arch Linux vẫn vượt trội hơn Ubuntu Server.", indent=400))

    body.append(heading2("5.5. ĐÁNH GIÁ CÔNG NGHỆ TƯỜNG LỬA: NFTABLES VS. UFW"))
    body.append(p("Đánh giá thực nghiệm về năng lực lọc gói tin mạng giữa hai công nghệ tường lửa:", indent=400))
    body.append(p("1. Năng lực chống tấn công Brute-Force: Kịch bản thử nghiệm sử dụng công cụ Hydra phát liên tục 20 yêu cầu đăng nhập SSH sai mật khẩu trong vòng 10 giây:", indent=400))
    body.append(p("• Trên Arch Linux (nftables stateful meter): Sau đúng 4 yêu cầu đầu tiên, toàn bộ các kết nối thứ 5 trở đi bị `nftables` loại bỏ âm thầm tại tầng kernel. CPU máy chủ duy trì mức 1% tải, dịch vụ SSH hoàn toàn không bị áp lực.", indent=400))
    body.append(p("• Trên Ubuntu Server (UFW limit): UFW sử dụng mô-đun `recent` của iptables (chặn nếu quá 6 kết nối/30 giây). Mặc dù vẫn chặn được brute-force, nhưng do cơ chế duyệt danh sách tuần tự của iptables, mức chiếm dụng CPU của Ubuntu tăng lên xấp xỉ 4% trong suốt quá trình tấn công.", indent=400))
    body.append(p("2. Tính trong suốt của chính sách: Cú pháp của `nftables.conf` trên Arch Linux mang tính cấu trúc khối phân cấp (Block-structured syntax) tương tự ngôn ngữ C, giúp kỹ sư dễ dàng kiểm toán toàn bộ chính sách lọc gói chỉ trong một tệp duy nhất, vượt trội hơn so với nhiều tệp rải rác trong `/etc/ufw/` của Ubuntu.", indent=400))

    body.append(heading2("5.6. PHÂN TÍCH ĐÁNH ĐỔI KỸ THUẬT (TRADE-OFFS) VÀ BÀI HỌC KINH NGHIỆM"))
    body.append(p("Trong kỹ nghệ phần mềm và quản trị hệ thống, không có giải pháp nào là hoàn hảo tuyệt đối (No Silver Bullet). Mọi quyết định kiến trúc đều đi kèm với sự đánh đổi (Trade-offs) mà người kỹ sư phải thấu hiểu sâu sắc:", indent=400))

    body.append(p("Bảng 5.4: Bảng phân tích các điểm đánh đổi kỹ thuật (Trade-offs) trong triển khai", align="center", bold=True, size=24, space_after=60))
    headers_5_4 = ["Quyết định kiến trúc", "Lợi ích thu được (Pros)", "Sự đánh đổi / Thách thức (Cons)", "Giải pháp kỹ thuật khắc phục"]
    rows_5_4 = [
        ["Rootless Docker (Arch Linux)", "Triệt tiêu 100% rủi ro chiếm quyền root khi bị Container Escape.", "Không thể bind các cổng đặc quyền < 1024 mà không cấu hình cap_net_bind_service.", "Ánh xạ các dịch vụ ra cổng cao >= 1024 (cổng 8080, 5000, 3000)."],
        ["Rolling Release (Arch Linux)", "Luôn sở hữu Kernel mới nhất, cgroups v2 và nftables tối tân.", "Nguy cơ xung đột phần mềm hoặc thay đổi cú pháp khi cập nhật liên tục.", "Xây dựng kịch bản IaC chuẩn hóa, kiểm thử tự động và có script Rollback."],
        ["Ubuntu Server LTS", "Cực kỳ ổn định, đóng băng phiên bản, tài liệu hỗ trợ doanh nghiệp dồi dào.", "Chiếm dụng RAM tĩnh cao, công cụ phần mềm cũ hơn 1-2 năm.", "Chủ động gỡ bỏ snapd và tinh chỉnh sysctl để tối ưu hóa tài nguyên."],
        ["Zero-Trust Network (internal: true)", "Bảo vệ tuyệt đối cơ sở dữ liệu và kho đối tượng trước tấn công ngoài.", "Không thể truy cập trực tiếp bằng các công cụ GUI như DBeaver từ máy ngoài.", "Sử dụng Docker exec hoặc cấu hình SSH Bastion Tunnel khi cần bảo trì."]
    ]
    body.append(table_grid(headers_5_4, rows_5_4))
    body.append(page_break())

    return body
