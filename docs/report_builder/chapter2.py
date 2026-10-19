from .styles import p, heading1, heading2, heading3, heading4, page_break, table_grid, figure_box, code_box, note_box

def build_chapter2():
    body = []
    body.append(heading1("CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ CÔNG NGHỆ CỐT LÕI"))

    body.append(heading2("2.1. TỔNG QUAN HỆ ĐIỀU HÀNH LINUX: ARCH LINUX VÀ UBUNTU SERVER"))
    body.append(heading3("2.1.1. Kiến trúc hạt nhân Linux Kernel (Kernel Space vs. User Space)"))
    body.append(p("Hệ điều hành Linux được xây dựng theo kiến trúc hạt nhân nguyên khối (Monolithic Kernel) nhưng sở hữu tính mô-đun hóa cao (Loadable Kernel Modules). Để đảm bảo tính ổn định và an ninh của toàn bộ hệ thống máy tính, bộ vi xử lý (CPU) áp dụng các cấp độ bảo vệ phần cứng (thường được gọi là CPU Privilege Rings trên kiến trúc x86_64, từ Ring 0 đến Ring 3). Nhân Linux phân chia ranh giới bộ nhớ và quyền thực thi thành hai không gian tách biệt hoàn toàn:", indent=400))
    body.append(p("1. Không gian hạt nhân (Kernel Space - Ring 0): Đây là vùng thực thi có đặc quyền tối cao nhất của hệ điều hành. Mã nguồn nhân Linux và các trình điều khiển thiết bị (Device Drivers) hoạt động tại đây. Kernel Space có toàn quyền truy cập trực tiếp vào bộ nhớ vật lý, các thanh ghi phần cứng của CPU, các cổng I/O và điều khiển trực tiếp các luồng ngắt (Interrupt Requests). Bất kỳ lỗi truy cập bộ nhớ nghiêm trọng nào (Kernel Panic) xảy ra trong không gian này đều có thể làm treo toàn bộ máy chủ.", indent=400))
    body.append(p("2. Không gian người dùng (User Space - Ring 3): Đây là môi trường cách ly an toàn dành riêng cho các tiến trình ứng dụng thông thường, các trình nền hệ thống (Daemons như systemd, dockerd) và các thư viện liên kết (GNU C Library - glibc). Các tiến trình trong User Space bị giới hạn nghiêm ngặt về quyền truy cập bộ nhớ và hoàn toàn không thể tương tác trực tiếp với phần cứng máy tính.", indent=400))

    schematic_2_1 = [
        "+-------------------------------------------------------------------------+",
        "|                 KIẾN TRÚC PHÂN TẦNG NHÂN LINUX                          |",
        "+-------------------------------------------------------------------------+",
        "| [USER SPACE - Ring 3]                                                   |",
        "|   FastAPI Service | MLflow Server | Prometheus | Bash Shell | dockerd   |",
        "|                     |                      |                            |",
        "|                     v                      v                            |",
        "|            [GNU C Library - glibc (Standard POSIX API)]                 |",
        "+---------------------|----------------------|----------------------------+",
        "|                     | System Calls (trap)  | (sysenter / syscall)       |",
        "+---------------------v----------------------v----------------------------+",
        "| [KERNEL SPACE - Ring 0]                                                 |",
        "|   +-------------------+  +-------------------+  +-------------------+   |",
        "|   | Process Scheduler |  | Memory Management |  | Virtual Filesystem|   |",
        "|   +-------------------+  +-------------------+  +-------------------+   |",
        "|   | cgroups v2 Engine |  | Linux Namespaces  |  | Netfilter Hooks   |   |",
        "|   +-------------------+  +-------------------+  +-------------------+   |",
        "|                                                                         |",
        "|             [Device Drivers: Network, Storage, CPU, Bus]                |",
        "+-------------------------------------------------------------------------+",
        "| [HARDWARE PLATFORM] CPU x86_64 | Physical RAM | NVMe SSD | NIC Adapter  |",
        "+-------------------------------------------------------------------------+"
    ]
    body.append(figure_box("2.1", "Kiến trúc phân tầng nhân Linux: Phân định ranh giới User Space và Kernel Space",
                           "minh họa cơ chế tương tác giữa các ứng dụng MLOps trong không gian người dùng và các hệ thống con bên trong hạt nhân Linux thông qua giao diện lời gọi hệ thống System Calls.",
                           schematic_2_1))

    body.append(p("Để thực hiện các thao tác vào/ra (I/O) như mở socket mạng gửi dự báo OCR, đọc ảnh từ đĩa cứng hoặc cấp phát bộ nhớ ảo mới, tiến trình ứng dụng trong User Space bắt buộc phải phát ra một lời gọi hệ thống (System Call). Lời gọi này chuyển đổi chế độ thực thi của CPU từ Ring 3 xuống Ring 0, kích hoạt bộ xử lý ngắt phần mềm của hạt nhân để thực hiện tác vụ thay cho ứng dụng, sau đó trả kết quả về User Space.", indent=400))

    body.append(heading3("2.1.2. Phân tích triết lý The Arch Way và mô hình Rolling Release"))
    body.append(p("Arch Linux là một bản phân phối Linux độc lập dành cho kiến trúc x86_64, được sáng lập bởi Judd Vinet vào năm 2002. Khác biệt với hầu hết các bản phân phối hướng tới người dùng phổ thông, Arch Linux tuân thủ triệt để tài liệu triết lý mang tên \"The Arch Way\" với 5 nguyên lý kỹ thuật cốt lõi:", indent=400))
    body.append(p("• Simplicity (Tính tối giản): Tối giản ở đây được định nghĩa theo góc nhìn của kiến trúc hệ thống, nghĩa là loại bỏ hoàn toàn các lớp vỏ bọc đồ họa trừu tượng không cần thiết, không cài đặt sẵn các script tự động cấu hình can thiệp vào tệp tin của người dùng. Hệ thống chỉ chứa đúng những gì người quản trị chủ động cài đặt.", indent=400))
    body.append(p("• Modernity (Tính hiện đại): Arch Linux luôn là bản phân phối tiên phong áp dụng các công nghệ mới nhất từ cộng đồng phát triển upstream. Hạt nhân Linux Kernel luôn là phiên bản stable mới nhất, hệ thống khởi động hoàn toàn bằng systemd nguyên bản, cơ chế phân bổ cgroups v2 và hệ thống tường lửa nftables được kích hoạt mặc định.", indent=400))
    body.append(p("• Pragmatism (Tính thực dụng): Arch Linux không cực đoan về mặt bản quyền phần mềm; hệ thống sẵn sàng cung cấp cả các gói phần mềm nguồn mở lẫn phần mềm độc quyền nếu chúng đem lại hiệu quả thực tế cao cho người dùng.", indent=400))
    body.append(p("• User Centrality (Lấy người dùng làm trung tâm): Hệ thống trao toàn quyền quyết định cho người quản trị. Không có quyết định cấu hình ngầm nào được đưa ra mà không có sự đồng ý của kỹ sư.", indent=400))
    body.append(p("• Versatility (Tính linh hoạt): Có thể tùy biến Arch Linux thành một máy chủ tối giản không màn hình (Headless Server) tiêu thụ dưới 400MB RAM hoặc một máy trạm điện toán khoa học mạnh mẽ.", indent=400))

    body.append(heading3("2.1.3. Đặc điểm mô hình Enterprise LTS của Ubuntu Server"))
    body.append(p("Ubuntu Server là bản phân phối Linux máy chủ phổ biến nhất thế giới do tập đoàn Canonical phát triển dựa trên nền tảng Debian GNU/Linux. Trọng tâm cốt lõi của Ubuntu Server xoay quanh khái niệm Hỗ trợ dài hạn (Long-Term Support - LTS):", indent=400))
    body.append(p("• Độ ổn định doanh nghiệp: Mỗi bản LTS được phát hành 2 năm một lần vào tháng 4 (như phiên bản 20.04 LTS, 22.04 LTS, 24.04 LTS) và được bảo đảm cập nhật bản vá an ninh liên tục trong 5 năm (và mở rộng lên 10 năm với gói Ubuntu Pro). Tính chất đóng băng phiên bản giúp các doanh nghiệp tài chính hoặc viễn thông yên tâm rằng các giao diện lập trình API và hành vi của hệ điều hành sẽ không bao giờ thay đổi đột ngột.", indent=400))
    body.append(p("• Hệ sinh thái đám mây toàn diện: Ubuntu Server là hình ảnh máy chủ mặc định trên hầu hết các nền tảng điện toán đám mây lớn (AWS EC2, Google Cloud Platform, Microsoft Azure).", indent=400))
    body.append(p("• Tuy nhiên, tính chất đóng băng phiên bản cũng mang lại những trở ngại kỹ thuật nhất định đối với các hệ thống MLOps hiện đại: Các gói phần mềm như Docker Engine, Python runtime hoặc thư viện tối ưu hóa mạng của kernel thường chậm hơn từ 1 đến 2 năm so với các bản phát hành upstream mới nhất. Đồng thời, cấu hình mặc định của Ubuntu kích hoạt nhiều dịch vụ nền như `snapd`, `unattended-upgrades`, `multipathd` khiến mức tiêu thụ bộ nhớ RAM ban đầu tăng cao đáng kể.", indent=400))

    body.append(heading2("2.2. CÔNG NGHỆ CONTAINERIZATION VÀ CƠ CHẾ CÔ LẬP HẠT NHÂN"))
    body.append(heading3("2.2.1. Bản chất Container so với Máy ảo (Virtual Machine)"))
    body.append(p("Trong lịch sử ảo hóa hạ tầng, sự ra đời của công nghệ Container đã định nghĩa lại cách thức đóng gói và vận hành phần mềm. Để hiểu rõ bản chất kỹ thuật, cần phân biệt rõ ranh giới kiến trúc giữa Máy ảo (Virtual Machine) và Container:", indent=400))
    body.append(p("• Máy ảo (Virtual Machine): Sử dụng một lớp phần mềm trung gian gọi là Hypervisor (loại 1 như VMware ESXi, KVM hoặc loại 2 như Oracle VirtualBox) để ảo hóa toàn bộ phần cứng vật lý (CPU, RAM, BIOS, Card mạng ảo). Mỗi máy ảo bắt buộc phải cài đặt một hệ điều hành khách (Guest OS) hoàn chỉnh bao gồm cả kernel riêng, hệ thống tệp tin và các dịch vụ nền. Điều này dẫn tới mức độ chiếm dụng tài nguyên khổng lồ (hàng gigabyte dung lượng đĩa và RAM) cùng thời gian khởi động tính bằng phút.", indent=400))
    body.append(p("• Container: Hoàn toàn không ảo hóa phần cứng và không chạy một hệ điều hành khách riêng biệt nào. Một container thực chất chỉ là một tiến trình bình thường của Linux (Normal Linux Process) trong User Space, nhưng được nhân Linux \"khoác lên\" hai chiếc áo bảo vệ kỹ thuật số: Không gian tên (Namespaces) để tạo ra ảo ảnh về sự cô lập hoàn toàn, và Nhóm điều khiển (Control Groups - cgroups) để đặt ra trần giới hạn về lượng tài nguyên mà tiến trình được phép tiêu thụ.", indent=400))

    schematic_2_2 = [
        "+-----------------------------------+  +-----------------------------------+",
        "|       MÁY ẢO TRUYỀN THỐNG         |  |        CONTAINER HIỆN ĐẠI         |",
        "+-----------------------------------+  +-----------------------------------+",
        "| [App A]     [App B]     [App C]   |  | [App A]     [App B]     [App C]   |",
        "| [Libs A]    [Libs B]    [Libs C]  |  | [Libs A]    [Libs B]    [Libs C]  |",
        "| [Guest OS]  [Guest OS]  [Guest OS]|  +-----------------------------------+",
        "| (Kernel)    (Kernel)    (Kernel)  |  |   CONTAINER RUNTIME (Docker/runc) |",
        "+-----------------------------------+  +-----------------------------------+",
        "|       HYPERVISOR (KVM/ESXi)       |  |     CHUNG HẠT NHÂN LINUX KERNEL   |",
        "+-----------------------------------+  |   (Namespaces, cgroups v2, nft)   |",
        "|       HOST OPERATING SYSTEM       |  +-----------------------------------+",
        "+-----------------------------------+  |       HOST OPERATING SYSTEM       |",
        "|         PHYSICAL HARDWARE         |  |         PHYSICAL HARDWARE         |",
        "+-----------------------------------+  +-----------------------------------+"
    ]
    body.append(figure_box("2.2", "So sánh kiến trúc cô lập giữa Máy ảo truyền thống (Hypervisor) và Container",
                           "minh họa sự khác biệt nền tảng: Máy ảo nhân bản toàn bộ hệ điều hành khách khiến hệ thống nặng nề, trong khi Container chia sẻ trực tiếp nhân Linux Kernel giúp khởi động tức thì và tiết kiệm tối đa bộ nhớ.",
                           schematic_2_2))

    body.append(heading3("2.2.2. Phân tích 6 loại Linux Namespaces trong cô lập tiến trình"))
    body.append(p("Không gian tên (Namespaces) là một tính năng nền tảng của hạt nhân Linux, cho phép bao bọc các tài nguyên toàn cục của hệ thống thành những thể hiện độc lập, trừu tượng. Đối với các tiến trình chạy bên trong một namespace nhất định, chúng chỉ nhìn thấy không gian tài nguyên thuộc về riêng mình mà không hề hay biết về sự tồn tại của các tiến trình khác trên hệ thống.", indent=400))
    body.append(p("Hạt nhân Linux cung cấp 6 không gian tên cơ bản để kiến tạo nên một container:", indent=400))
    body.append(p("1. PID Namespace (Process ID): Cô lập cây định danh tiến trình. Bên trong container, tiến trình chính (Init process) luôn nhìn thấy mình mang PID 1, nhưng trên cây tiến trình của máy chủ host, nó thực chất mang một PID ngẫu nhiên (ví dụ PID 45120). Điều này cho phép container tự quản lý các tiến trình con mà không gây xung đột với host.", indent=400))
    body.append(p("2. Mount Namespace (mnt): Cô lập danh sách các điểm gắn kết hệ thống tệp tin (Mount Points). Mỗi container sở hữu một cây thư mục gốc (`/`) hoàn toàn độc lập thông qua cơ chế `pivot_root`, ngăn chặn container đọc hoặc ghi vào hệ thống tệp của máy chủ.", indent=400))
    body.append(p("3. Network Namespace (net): Cô lập toàn bộ ngăn xếp giao thức mạng, bao gồm danh sách giao diện mạng ảo (veth pairs), bảng định tuyến IP (Routing Table), các quy tắc tường lửa và danh sách các cổng socket đang lắng nghe.", indent=400))
    body.append(p("4. IPC Namespace (Inter-Process Communication): Cô lập các cơ chế truyền thông liên tiến trình như hàng đợi thông điệp POSIX/System V, bộ nhớ chia sẻ (Shared Memory) và cờ hiệu Semaphores.", indent=400))
    body.append(p("5. UTS Namespace (UNIX Timesharing System): Cho phép container thiết lập tên máy chủ (Hostname) và tên miền (Domainname) riêng biệt mà không ảnh hưởng tới máy chủ.", indent=400))
    body.append(p("6. User Namespace (user): Đây là tính năng bảo mật tối quan trọng nhất. Nó cho phép ánh xạ dải định danh người dùng (UID) và nhóm (GID) bên trong container sang một dải UID/GID hoàn toàn khác trên máy chủ lưu trữ. Nhờ đó, một tiến trình chạy với quyền root (UID 0) bên trong container thực chất chỉ tương ứng với một người dùng bình thường (UID 100000) trên host vật lý.", indent=400))

    body.append(p("Bảng 2.1: Phân loại và chức năng của 6 loại Linux Namespaces", align="center", bold=True, size=24, space_after=60))
    headers_2_1 = ["Loại Namespace", "Cờ System Call", "Tài nguyên hệ thống được cô lập"]
    rows_2_1 = [
        ["PID Namespace", "CLONE_NEWPID", "Cây tiến trình, số định danh PID và tín hiệu điều khiển."],
        ["Mount Namespace", "CLONE_NEWNS", "Hệ thống tệp tin, phân vùng đĩa và các điểm gắn kết mount."],
        ["Network Namespace", "CLONE_NEWNET", "Giao diện mạng ảo, địa chỉ IP, bảng định tuyến và cổng socket."],
        ["IPC Namespace", "CLONE_NEWIPC", "Bộ nhớ chia sẻ (shm), hàng đợi thông điệp và cờ hiệu IPC."],
        ["UTS Namespace", "CLONE_NEWUTS", "Tên máy chủ (Hostname) và tên miền nhận diện hệ thống."],
        ["User Namespace", "CLONE_NEWUSER", "Bảng ánh xạ định danh người dùng (UID) và nhóm người dùng (GID)."]
    ]
    body.append(table_grid(headers_2_1, rows_2_1))
    body.append(p("", space_after=100))

    body.append(heading3("2.2.3. Cơ chế kiểm soát tài nguyên cgroups v1 và cgroups v2"))
    body.append(p("Trong khi Namespaces tạo ra ranh giới ảo thị giác cho tiến trình, Control Groups (cgroups) là công cụ thực thi quyền lực của hạt nhân nhằm kiểm soát và giới hạn lượng tài nguyên phần cứng vật lý mà một nhóm tiến trình được phép tiêu thụ. Nếu không có cgroups, một container bị lỗi rò rỉ bộ nhớ hoặc bị tấn công từ chối dịch vụ (DoS / Fork Bomb) có thể vắt kiệt toàn bộ RAM và CPU của máy chủ, làm sập toàn bộ các dịch vụ lân cận.", indent=400))
    body.append(p("Lịch sử phát triển cgroups trải qua hai giai đoạn biến đổi lớn:", indent=400))
    body.append(p("• Kiến trúc cgroups v1 (Legacy): Mỗi loại tài nguyên (CPU, Memory, blkio, pids) được quản lý bởi một cây phân cấp (Hierarchy) hoàn toàn độc lập. Sự phân mảnh này dẫn tới việc rất khó đồng bộ hóa chính sách: Một tiến trình có thể nằm ở node cha trong cây CPU nhưng lại nằm ở node con trong cây Memory, gây ra xung đột khóa hạt nhân và tình trạng thắt cổ chai hiệu năng I/O.", indent=400))
    body.append(p("• Kiến trúc cgroups v2 (Unified Hierarchy): Được giới thiệu trong các phiên bản Linux Kernel hiện đại, cgroups v2 hợp nhất toàn bộ các bộ điều khiển tài nguyên vào một cây phân cấp duy nhất. Mỗi tiến trình chỉ thuộc về duy nhất một nhóm điều khiển. Đặc biệt, cgroups v2 hỗ trợ cơ chế ủy quyền an toàn (Safe Delegation) cho phép người dùng không có quyền root (unprivileged user) được tự do tạo nhóm con và phân bổ hạn mức CPU/RAM cho các container của chính mình. Đây chính là viên gạch nền tảng kỹ thuật bắt buộc để vận hành Rootless Docker.", indent=400))

    body.append(heading2("2.3. CÔNG NGHỆ ROOTLESS CONTAINER ENGINE"))
    body.append(heading3("2.3.1. Rủi ro của Docker Daemon chạy quyền Root truyền thống"))
    body.append(p("Kiến trúc truyền thống của Docker bao gồm một tiến trình daemon nền (`dockerd`) chạy liên tục với đặc quyền root tối cao trên máy chủ. Người dùng thông thường muốn tương tác với daemon phải gửi lệnh qua socket Unix tại `/var/run/docker.sock`. Như đã phân tích, cơ chế này tiềm ẩn ba mối nguy hại bảo mật sống còn:", indent=400))
    body.append(p("1. Rủi ro đặc quyền tối cao: Daemon nắm giữ toàn bộ các Linux Capabilities mạnh nhất (`CAP_SYS_ADMIN`, `CAP_NET_ADMIN`, `CAP_SYS_PTRACE`). Bất kỳ lỗi tràn bộ đệm hay lỗ hổng thực thi mã từ xa nào bên trong `dockerd` hoặc `containerd` đều biến máy chủ thành con mồi trực tiếp của kẻ tấn công.", indent=400))
    body.append(p("2. Thảm họa Container Escape: Khi ứng dụng bị tấn công (như lỗi SQL Injection hoặc RCE trong microservice), kẻ tấn công chiếm được quyền shell bên trong container. Nếu container chạy với cấu hình mặc định (không bật userns-remap), kẻ tấn công chính là root (UID 0) trên host. Bằng cách khai thác các lỗ hổng nhân Linux hoặc các lỗ hổng trong runtime runc, chúng có thể phá rào và chiếm quyền máy chủ.", indent=400))
    body.append(p("3. Gắn kết phân vùng nguy hiểm: Người dùng có quyền chạy Docker có thể vô tình hoặc cố ý mount các tệp tin hệ thống nhạy cảm như `/etc`, `/root`, hoặc `/var/log` vào bên trong container để sửa đổi tùy ý mà không cần gõ mật khẩu `sudo`.", indent=400))

    body.append(heading3("2.3.2. Kiến trúc Rootless Docker unprivileged trên Arch Linux"))
    body.append(p("Rootless Docker là chế độ hoạt động tiên tiến cho phép cài đặt và thực thi toàn bộ hệ sinh thái Docker (dockerd, containerd, runc và các container) hoàn toàn bên trong không gian người dùng của một tài khoản thông thường (không cần đặc quyền `sudo` hay quyền `root`).", indent=400))
    body.append(p("Trên hệ điều hành Arch Linux, kiến trúc này được hiện thực hóa thông qua sự phối hợp nhịp nhàng giữa bốn thành phần kỹ thuật:", indent=400))
    body.append(p("• `rootlesskit`: Công cụ khởi tạo môi trường không gian tên người dùng (User Namespace) độc lập, thiết lập ánh xạ UID/GID ảo và quản lý vòng đời của daemon con.", indent=400))
    body.append(p("• `slirp4netns`: Ngăn xếp mạng ảo User-mode TCP/IP. Do người dùng unprivileged không có quyền tạo card mạng ảo `veth` và cầu nối `bridge` trực tiếp trên host kernel, `slirp4netns` tạo ra một ngăn xếp mạng ảo hoàn toàn trong User Space để định tuyến lưu lượng giữa container và thế giới Internet bên ngoài.", indent=400))
    body.append(p("• `fuse-overlayfs`: Trình điều khiển hệ thống tệp tin phân tầng chạy trong không gian người dùng thông qua giao diện FUSE, thay thế cho trình điều khiển native overlay2 vốn yêu cầu quyền root của kernel.", indent=400))
    body.append(p("• Systemd User Services: Trình quản lý dịch vụ cấp người dùng quản lý vòng đời của dockerd thông qua socket độc lập đặt tại `/run/user/<UID>/docker.sock`.", indent=400))

    schematic_2_5 = [
        "+-------------------------------------------------------------------------+",
        "|              KIẾN TRÚC ROOTLESS DOCKER TRÊN ARCH LINUX                  |",
        "+-------------------------------------------------------------------------+",
        "| [UNPRIVILEGED USER SPACE - Tài khoản mlops UID 1003]                    |",
        "|                                                                         |",
        "|   +-----------------------------------------------------------------+   |",
        "|   | USER NAMESPACE CỦA ROOTLESSKIT (Mapped: 0 -> 1003, 1-65535)     |   |",
        "|   |                                                                 |   |",
        "|   |  [Rootless Docker Daemon] <--> Socket: /run/user/1003/docker.sock|   |",
        "|   |             |                                                   |   |",
        "|   |             v                                                   |   |",
        "|   |  [Rootless Containerd]                                          |   |",
        "|   |             |                                                   |   |",
        "|   |             +--> [Storage: fuse-overlayfs (~/.local/share/docker)|   |",
        "|   |             +--> [Network: slirp4netns TAP device tap0]         |   |",
        "|   |                                                                 |   |",
        "|   |  [RUNNING CONTAINER: FastAPI OCR Microservice]                  |   |",
        "|   |  (Inside UID: 10001 unprivileged -> Outside Host UID: 110000)   |   |",
        "|   +-----------------------------------------------------------------+   |",
        "+-------------------------------------------------------------------------+",
        "| [HOST LINUX KERNEL - Arch Linux 6.x / 7.x]                              |",
        "|  Hạt nhân chỉ nhìn thấy các tiến trình thông thường của UID 1003.       |",
        "|  KHÔNG CÓ TIẾN TRÌNH ROOT NÀO HOẠT ĐỘNG THAY MẶT CHO CONTAINER!         |",
        "+-------------------------------------------------------------------------+"
    ]
    body.append(figure_box("2.5", "Kiến trúc Rootless Docker unprivileged và cơ chế cầu nối mạng slirp4netns",
                           "mô tả ranh giới cô lập tuyệt đối của Rootless Docker trên Arch Linux: Toàn bộ daemon và container bị giam lỏng bên trong User Namespace của tài khoản mlops, triệt tiêu hoàn toàn khả năng can thiệp vào máy chủ host.",
                           schematic_2_5))

    body.append(heading3("2.3.3. Cơ chế ánh xạ subuid/subgid và mạng slirp4netns"))
    body.append(p("Để Rootless Docker có thể hoạt động, hệ điều hành Linux sử dụng hai tệp tin cấu hình bảo mật tại `/etc/subuid` và `/etc/subgid`. Cấu trúc của các tệp tin này định nghĩa dải định danh phụ trợ được phép ủy quyền cho một tài khoản cụ thể. Trong đồ án này, cấu hình được thiết lập chính xác như sau:", indent=400))
    
    code_subuid = [
        "# Tệp tin /etc/subuid và /etc/subgid",
        "mlops:100000:65536"
    ]
    body.append(code_box(code_subuid, "Cấu hình ánh xạ Subordinate User Namespaces"))
    
    body.append(p("Ý nghĩa kỹ thuật của chỉ thị này được giải thích như sau: Tài khoản người dùng `mlops` được phép sở hữu một dải không gian gồm 65,536 định danh người dùng ảo, bắt đầu từ số định danh 100,000 trên máy chủ vật lý. Khi một container khởi chạy dưới chế độ Rootless, UID 0 bên trong container sẽ tương ứng với chính UID 1003 của user `mlops` trên host, và các UID từ 1 đến 65,535 bên trong container sẽ lần lượt được dịch chuyển thành các UID từ 100,000 đến 165,535 trên máy chủ.", indent=400))
    body.append(p("Hệ quả an ninh trực tiếp: Ngay cả khi kẻ tấn công bằng cách nào đó phá rào thành công và thoát ra khỏi container với quyền root ảo (UID 0), dưới góc nhìn của kernel máy chủ, kẻ tấn công cũng chỉ là tài khoản `mlops` bình thường, không thể chạm tới các tệp tin hệ thống hay can thiệp vào tiến trình của người dùng khác.", indent=400))

    body.append(heading2("2.4. CÔNG NGHỆ TƯỜNG LỬA STATEFUL: NFTABLES VS. UFW"))
    body.append(heading3("2.4.1. Kiến trúc Netfilter Hooks trong Linux Kernel"))
    body.append(p("Netfilter là hệ thống con xử lý gói tin mạng cốt lõi nằm sâu bên trong nhân Linux. Mọi gói tin IP đi vào, đi qua hoặc phát sinh từ máy tính đều phải di chuyển qua một chuỗi các móc câu xử lý (Hooks) được đặt tại các vị trí chiến lược của ngăn xếp mạng:", indent=400))
    body.append(p("• `NF_INET_PRE_ROUTING`: Móc câu đón nhận gói tin ngay khi vừa rời khỏi card mạng vật lý, trước khi bảng định tuyến đưa ra quyết định chuyển tiếp.", indent=400))
    body.append(p("• `NF_INET_LOCAL_IN`: Dành cho các gói tin có địa chỉ IP đích chính là máy chủ cục bộ (ví dụ kết nối SSH tới port 2222 hoặc gọi API port 8080).", indent=400))
    body.append(p("• `NF_INET_FORWARD`: Dành cho các gói tin chỉ đi ngang qua máy chủ để chuyển tiếp sang một mạng khác (ví dụ lưu lượng giữa các mạng container).", indent=400))
    body.append(p("• `NF_INET_LOCAL_OUT`: Dành cho các gói tin được phát sinh cục bộ từ các tiến trình của máy chủ gửi ra bên ngoài.", indent=400))
    body.append(p("• `NF_INET_POST_ROUTING`: Móc câu xử lý gói tin ngay trước khi đưa xuống card mạng vật lý để truyền đi; thường dùng để thực hiện biên dịch địa chỉ mạng (Source NAT / Masquerade).", indent=400))

    body.append(heading3("2.4.2. Bảng lọc gói tin hiệu năng cao nftables"))
    body.append(p("`nftables` là dự án mã nguồn mở hiện đại được thiết kế nhằm thay thế hoàn toàn hệ sinh thái công cụ cũ kỹ đã tồn tại hơn 20 năm gồm `iptables`, `ip6tables`, `arptables` và `ebtables`. Điểm đột phá của `nftables` nằm ở kiến trúc máy ảo dòng lệnh (Pseudo-State Machine / Virtual Machine) hoạt động trực tiếp trong không gian hạt nhân.", indent=400))
    body.append(p("Thay vì phải duy trì nhiều công cụ riêng biệt cho IPv4 và IPv6, `nftables` cung cấp một họ bảng thống nhất (`inet`) cho phép một quy tắc duy nhất có thể lọc đồng thời cả hai giao thức. `nftables` hỗ trợ cấu trúc dữ liệu nâng cao như Sets (tập hợp) và Maps (bảng ánh xạ), cho phép kiểm tra hàng ngàn địa chỉ IP hoặc cổng dịch vụ với độ phức tạp thuật toán O(1) hoặc O(log N), thay vì phải quét tuần tự từng dòng quy tắc như `iptables` truyền thống.", indent=400))

    body.append(heading3("2.4.3. Uncomplicated Firewall (UFW) trên Ubuntu"))
    body.append(p("Ngược lại với cách tiếp cận trực diện và cấu hình sâu của `nftables` trên Arch Linux, Ubuntu Server sử dụng `ufw` (Uncomplicated Firewall) như một giải pháp quản trị tường lửa mặc định hướng tới người dùng doanh nghiệp. Về bản chất kỹ thuật, `ufw` không phải là một hệ thống lọc gói tin độc lập trong kernel, mà chỉ đóng vai trò là một giao diện dòng lệnh (Frontend Interface) trừu tượng hóa các câu lệnh `iptables/nftables` phức tạp phía sau.", indent=400))
    body.append(p("Ưu điểm của `ufw` là cú pháp cực kỳ ngắn gọn, dễ đọc, dễ học (ví dụ: `ufw allow 2222/tcp`). Tuy nhiên, nhược điểm là thiếu sự linh hoạt để xây dựng các kịch bản stateful phức tạp (như rate-limiting theo dõi thời gian thực hoặc lọc gói tin TCP flags chuyên sâu) và đôi khi xảy ra xung đột không mong muốn với các quy tắc tự động do Docker daemon chèn vào iptables.", indent=400))

    body.append(p("Bảng 2.4: So sánh cú pháp, kiến trúc thực thi giữa nftables và UFW", align="center", bold=True, size=24, space_after=60))
    headers_2_4 = ["Tiêu chí so sánh", "nftables (Arch Linux)", "UFW (Ubuntu Server)"]
    rows_2_4 = [
        ["Bản chất công nghệ", "Hệ thống lọc gói tin native hiện đại của nhân Linux.", "Lớp vỏ bọc (wrapper) bằng Python thao tác lên iptables."],
        ["Họ giao thức", "Bảng thống nhất inet xử lý đồng thời cả IPv4 và IPv6.", "Quản lý riêng biệt qua các tệp cấu hình /etc/default/ufw."],
        ["Hiệu năng lọc gói", "Cực cao; thực thi bằng bytecode VM với tra cứu Sets O(1).", "Trung bình; phụ thuộc vào cấu trúc chuỗi tuần tự của iptables."],
        ["Khả năng Rate Limiting", "Hỗ trợ native stateful meter (ví dụ: limit rate 4/minute).", "Hỗ trợ cơ bản qua từ khóa limit (chỉ áp dụng đơn giản cho SSH)."],
        ["Độ linh hoạt cấu hình", "Toàn quyền kiểm soát mọi Hook, Chain, Priority và Action.", "Bị giới hạn trong các kịch bản đóng mở cổng thông dụng."]
    ]
    body.append(table_grid(headers_2_4, rows_2_4))
    body.append(p("", space_after=100))

    body.append(heading2("2.5. HỆ SINH THÁI CÔNG CỤ MLOPS MÃ NGUỒN MỞ"))
    body.append(heading3("2.5.1. Vòng đời MLOps chuẩn công nghiệp"))
    body.append(p("Hệ sinh thái MLOps mã nguồn mở được nhóm nghiên cứu lựa chọn kỹ lưỡng nhằm tái hiện trọn vẹn một môi trường sản xuất thực tế tại doanh nghiệp, bao gồm 5 thành phần vi dịch vụ tương tác chặt chẽ với nhau:", indent=400))

    body.append(heading3("2.5.2. MLflow Tracking Server và PostgreSQL Metadata Store"))
    body.append(p("MLflow là nền tảng quản lý vòng đời học máy mã nguồn mở hàng đầu thế giới do Databricks khởi xướng. Trong kiến trúc của đề tài, MLflow đảm nhận hai vai trò sống còn:", indent=400))
    body.append(p("• Tracking Server: Cung cấp giao diện Web UI (cổng 5000) và REST API để các kỹ sư ghi nhận siêu tham số (Hyperparameters như learning_rate, batch_size), các chỉ số đánh giá (Metrics như loss, accuracy, F1-score) của từng lần chạy thí nghiệm.", indent=400))
    body.append(p("• Backend Store (PostgreSQL 15): Toàn bộ thông tin định danh thí nghiệm, thẻ siêu dữ liệu và trạng thái mô hình được lưu trữ bền vững trong cơ sở dữ liệu quan hệ PostgreSQL tại cơ sở dữ liệu `mlflow_db`, đảm bảo tính toàn vẹn dữ liệu theo chuẩn ACID.", indent=400))

    body.append(heading3("2.5.3. MinIO Object Storage tương thích Amazon S3"))
    body.append(p("Trong khi siêu dữ liệu dạng bảng được lưu trong PostgreSQL, các tệp tin nhị phân có dung lượng lớn (Model Weights, Checkpoints, Dataset zip) bắt buộc phải được lưu trữ trong một kho lưu trữ đối tượng (Object Storage). Nhóm sử dụng MinIO – một hệ thống lưu trữ đối tượng phân tán mã nguồn mở hiệu năng cao, cung cấp API tương thích 100% với chuẩn công nghiệp Amazon S3. MLflow giao tiếp với MinIO qua cổng API 9000 bằng giao thức S3 client để tự động tải lên và phiên bản hóa các tệp mô hình đã huấn luyện.", indent=400))

    body.append(heading3("2.5.4. Khung vi dịch vụ FastAPI và công cụ OCR Tesseract"))
    body.append(p("FastAPI là một web framework hiện đại, hiệu năng cao được xây dựng trên nền tảng Starlette và Pydantic, hỗ trợ lập trình bất đồng bộ (Asynchronous I/O) nguyên bản với Python 3.10+. FastAPI được nhóm sử dụng để đóng gói vi dịch vụ AI Serving, cung cấp endpoint `/predict/ocr` đón nhận các tệp tin hình ảnh tải lên.", indent=400))
    body.append(p("Công cụ AI cốt lõi được tích hợp là Tesseract OCR – công cụ nhận dạng ký tự quang học mã nguồn mở mạnh mẽ nhất hiện nay do Google bảo trợ phát triển. Lựa chọn Tesseract OCR kết hợp Pillow/OpenCV giúp vi dịch vụ hoạt động cực kỳ nhẹ nhàng, tiêu thụ ít bộ nhớ RAM và không đòi hỏi các thư viện GPU CUDA cồng kềnh, hoàn toàn phù hợp để đánh giá năng lực xử lý thuần túy của hệ điều hành Linux.", indent=400))

    body.append(heading3("2.5.5. Hệ thống giám sát Prometheus và Grafana"))
    body.append(p("Khả năng quan sát (Observability) là trụ cột không thể thiếu trong vận hành MLOps. Hệ thống giám sát bao gồm:", indent=400))
    body.append(p("• Prometheus: Hệ thống giám sát và cơ sở dữ liệu chuỗi thời gian (TSDB). Prometheus hoạt động theo mô hình kéo (Pull-model), định kỳ mỗi 5 giây gửi yêu cầu HTTP GET tới endpoint `/metrics` của vi dịch vụ FastAPI và Node Exporter trên cổng 9100 để thu thập các chỉ số về CPU, bộ nhớ, số lượng yêu cầu API và độ trễ xử lý.", indent=400))
    body.append(p("• Grafana: Nền tảng phân tích và trực quan hóa dữ liệu hàng đầu. Grafana kết nối trực tiếp với Prometheus Data Source để vẽ các bảng điều khiển thời gian thực (Dashboards), giúp kỹ sư hệ thống nắm bắt tức thì tình trạng sức khỏe của toàn bộ hạ tầng.", indent=400))

    body.append(heading3("2.5.6. Kiến trúc mạng thần kinh LSTM trong công cụ Tesseract OCR"))
    body.append(p("Tesseract OCR là một trong những dự án nhận dạng ký tự quang học mã nguồn mở có bề dày lịch sử lâu đời và độ chính xác cao nhất hiện nay. Từ phiên bản 4.0 trở đi, Tesseract đã chuyển đổi toàn bộ cơ chế nhận dạng truyền thống dựa trên trích xuất đặc trưng hình học (Pattern Matching) sang mạng thần kinh hồi quy tích hợp bộ nhớ dài-ngắn (Long Short-Term Memory - LSTM).", indent=400))
    body.append(p("Quy trình nhận diện ký tự từ ảnh của Tesseract gồm 4 giai đoạn nối tiếp:", indent=400))
    body.append(p("1. Tiền xử lý hình ảnh (Image Pre-processing): Hình ảnh đầu vào được chuyển đổi sang ảnh xám (Grayscale), cân bằng độ tương phản, khử nhiễu Gauss và nhị phân hóa (Binarization) qua thuật toán Otsu.", indent=400))
    body.append(p("2. Phân tích bố cục tài liệu (Line Finding & Layout Analysis): Thuật toán tìm kiếm các dòng văn bản theo chiều ngang, phát hiện khoảng cách giữa các từ (Word Spaces) và phân đoạn các khối văn bản (Bounding Boxes).", indent=400))
    body.append(p("3. Suy luận chuỗi qua LSTM (Sequence Classification): Dòng văn bản được đưa qua mô hình mạng nơ-ron LSTM đa lớp (Multi-layer LSTM). Mạng đọc chuỗi tín hiệu điểm ảnh và dự đoán xác suất xuất hiện của từng ký tự dựa trên ngữ cảnh xung quanh.", indent=400))
    body.append(p("4. Hậu xử lý và mô hình ngôn ngữ (Language Model & CTC Decoding): Kết quả dự đoán được tinh chỉnh bằng từ điển ngôn ngữ tiếng Việt (vie.traineddata) và tiếng Anh (eng.traineddata) qua cơ chế Connectionist Temporal Classification (CTC), cho phép bóc tách chính xác ngay cả các dấu thanh tiếng Việt phức tạp.", indent=400))

    body.append(heading3("2.5.7. Cơ chế lưu vết siêu tham số và phiên bản hóa mô hình của MLflow"))
    body.append(p("MLflow đóng vai trò là kho lưu trữ tập trung (Central Registry) cho toàn bộ tài nguyên học máy. Khi kỹ sư thực thi một tác vụ huấn luyện hoặc đánh giá mô hình, thư viện MLflow Python SDK tương tác với Tracking Server qua giao thức REST API:", indent=400))
    body.append(p("• `mlflow.start_run()`: Khởi tạo một phiên thí nghiệm mới với mã định danh Run ID duy nhất dạng UUIDv4.", indent=400))
    body.append(p("• `mlflow.log_param()`: Ghi nhận các siêu tham số đầu vào vào bảng `params` trong PostgreSQL.", indent=400))
    body.append(p("• `mlflow.log_metric()`: Ghi nhận các chỉ số chuỗi thời gian (Metrics Time-series) vào bảng `metrics` trong PostgreSQL.", indent=400))
    body.append(p("• `mlflow.log_artifact()`: Tải các tệp tin mô hình nhị phân (Model Artifacts) lên kho lưu trữ đối tượng MinIO S3 bucket, bảo đảm tính phiên bản hóa độc lập tuyệt đối.", indent=400))

    body.append(heading2("2.6. TIÊU CHUẨN AN NINH CIS BENCHMARK VÀ MÔ HÌNH DEFENSE IN DEPTH"))
    body.append(p("Center for Internet Security (CIS) là tổ chức phi lợi nhuận uy tín toàn cầu chuyên ban hành các tài liệu hướng dẫn gia cố an ninh kỹ thuật (Security Benchmarks) được thừa nhận rộng rãi trong các tiêu chuẩn thanh toán PCI-DSS, chuẩn ISO 27001 và đạo luật y tế HIPAA. Tài liệu CIS Docker Benchmark v1.6.0 đưa ra hơn 100 khuyến nghị bảo mật khắt khe được phân loại thành 5 nhóm trọng yếu:", indent=400))
    body.append(p("• Nhóm 1 (Host Configuration): Yêu cầu phân vùng đĩa riêng biệt cho `/var/lib/docker`, kích hoạt auditd ghi log các lời gọi hệ thống liên quan đến Docker, và cập nhật kernel lên phiên bản mới nhất.", indent=400))
    body.append(p("• Nhóm 2 (Docker Daemon Configuration): Khuyến nghị cấu hình `userns-remap` hoặc chuyển sang Rootless mode, vô hiệu hóa giao tiếp liên container không cần thiết (`icc: false`), và kích hoạt ghi log tập trung.", indent=400))
    body.append(p("• Nhóm 3 (Docker daemon configuration files): Thiết lập quyền sở hữu `root:root` và quyền truy cập `chmod 644` hoặc `600` cho tất cả các tệp cấu hình daemon.", indent=400))
    body.append(p("• Nhóm 4 (Container Images and Build Files): Bắt buộc tạo và chỉ định người dùng unprivileged trong Dockerfile (`USER non-root`), sử dụng multi-stage build để tối giản hóa image.", indent=400))
    body.append(p("• Nhóm 5 (Container Runtime): Cấm chạy container với cờ `--privileged`, giới hạn tài nguyên CPU/RAM qua cgroups, và phân tách mạng nội bộ Zero-Trust.", indent=400))
    body.append(p("Đề tài áp dụng triệt để mô hình Phòng thủ chiều sâu (Defense in Depth) lấy cảm hứng từ các khuyến nghị của CIS Benchmark. Thay vì chỉ trông cậy vào một chốt chặn duy nhất, hệ thống thiết lập một chuỗi 7 tầng pháo đài độc lập: Từ cấp độ hạt nhân Linux, qua tường lửa, cấu hình SSH, mô hình Rootless unprivileged, phân tách mạng nội bộ Zero-Trust, cho tới việc giới hạn quyền người dùng bên trong container.", indent=400))
    body.append(page_break())

    return body

