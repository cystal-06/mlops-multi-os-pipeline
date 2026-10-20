#!/usr/bin/env node
/**
 * Professional PowerPoint Presentation Generator for MLOps Multi-OS Pipeline
 * Generates genuine 16:9 widescreen PPTX with modern card layouts, badges, stat boxes, and tables.
 */

const pptxgen = require('pptxgenjs');
const path = require('path');

const pptx = new pptxgen();

// Configure 16:9 Widescreen Layout (13.333 x 7.5 inches)
pptx.defineLayout({ name: 'WIDESCREEN_16_9', width: 13.333, height: 7.5 });
pptx.layout = 'WIDESCREEN_16_9';

// Color Palette
const COLORS = {
    bgLight: 'F8FAFC',
    bgDark: '0B192C',
    primary: '0F172A',
    navyHeader: '002060',
    accentBlue: '0284C7',
    vkuRed: 'BA141A',
    cardBg: 'FFFFFF',
    cardBorder: 'CBD5E1',
    textMain: '1E293B',
    textMuted: '64748B',
    successGreen: '16A34A',
    gold: 'F59E0B'
};

const FONT_SANS = 'Calibri';

// Helper: Common Header
function addHeader(slide, category, title, subtitle) {
    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
        x: 0.8, y: 0.42, w: 2.5, h: 0.32,
        fill: { color: COLORS.accentBlue },
        line: { color: COLORS.accentBlue },
        rectRadius: 0.08
    });
    slide.addText(category, {
        x: 0.8, y: 0.42, w: 2.5, h: 0.32,
        fontSize: 10, bold: true, color: 'FFFFFF', align: 'center', valign: 'middle', fontFace: FONT_SANS
    });

    slide.addText(title, {
        x: 0.8, y: 0.8, w: 11.733, h: 0.48,
        fontSize: 21, bold: true, color: COLORS.primary, fontFace: FONT_SANS
    });

    if (subtitle) {
        slide.addText(subtitle, {
            x: 0.8, y: 1.28, w: 11.733, h: 0.3,
            fontSize: 12.5, italic: true, color: COLORS.textMuted, fontFace: FONT_SANS
        });
    }

    slide.addShape(pptx.shapes.LINE, {
        x: 0.8, y: 1.62, w: 11.733, h: 0,
        line: { color: 'CBD5E1', width: 1 }
    });
}

// Helper: Common Footer
function addFooter(slide, slideNum, totalSlides = 12) {
    slide.addShape(pptx.shapes.LINE, {
        x: 0.8, y: 6.88, w: 11.733, h: 0,
        line: { color: 'E2E8F0', width: 1 }
    });
    slide.addText('VKU — Đồ án Linux & Open Source: MLOps Pipeline | Nhóm: Nguyễn Công Đức, Nguyễn Tùng Dương, Nguyễn Văn C', {
        x: 0.8, y: 6.95, w: 9.0, h: 0.28,
        fontSize: 9.5, color: '94A3B8', fontFace: FONT_SANS
    });
    slide.addText(`Slide ${String(slideNum).padStart(2, '0')} / ${totalSlides}`, {
        x: 10.5, y: 6.95, w: 2.033, h: 0.28,
        fontSize: 10, bold: true, color: COLORS.accentBlue, align: 'right', fontFace: FONT_SANS
    });
}

// Helper: Standard Card Container
function addCard(slide, x, y, w, h, borderColor = COLORS.cardBorder, fillColor = COLORS.cardBg) {
    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
        x, y, w, h,
        fill: { color: fillColor },
        line: { color: borderColor, width: 1.5 },
        rectRadius: 0.08
    });
}

// ==========================================
// SLIDE 1: COVER (TITLE SLIDE - DARK TECH)
// ==========================================
{
    const slide = pptx.addSlide();
    slide.background = { color: COLORS.bgDark };

    slide.addText('TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN VÀ TRUYỀN THÔNG VIỆT - HÀN (VKU)', {
        x: 1.0, y: 0.8, w: 11.333, h: 0.4,
        fontSize: 14, bold: true, color: COLORS.gold, align: 'center', fontFace: FONT_SANS
    });
    slide.addText('KHOA KHOA HỌC MÁY TÍNH — BỘ MÔN HỆ THỐNG THÔNG TIN & MẠNG', {
        x: 1.0, y: 1.2, w: 11.333, h: 0.3,
        fontSize: 12, color: '94A3B8', align: 'center', fontFace: FONT_SANS
    });

    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
        x: 4.666, y: 1.8, w: 4.0, h: 0.45,
        fill: { color: '1E293B' },
        line: { color: COLORS.accentBlue, width: 1.5 },
        rectRadius: 0.1
    });
    slide.addText('BÁO CÁO TIẾN ĐỘ ĐỒ ÁN MÔN HỌC', {
        x: 4.666, y: 1.8, w: 4.0, h: 0.45,
        fontSize: 13, bold: true, color: '38BDF8', align: 'center', valign: 'middle', fontFace: FONT_SANS
    });

    slide.addText('CONFIGURE AND DEPLOY MLOPS SERVICES\nON ARCH LINUX & UBUNTU', {
        x: 1.0, y: 2.5, w: 11.333, h: 1.4,
        fontSize: 28, bold: true, color: 'FFFFFF', align: 'center', fontFace: FONT_SANS
    });

    slide.addText('Nghiên cứu đối kháng, xây dựng hạ tầng Rootless Containerization và Zero-Trust Network', {
        x: 1.0, y: 4.0, w: 11.333, h: 0.4,
        fontSize: 15, italic: true, color: '38BDF8', align: 'center', fontFace: FONT_SANS
    });

    const infoCards = [
        { title: 'GIẢNG VIÊN HƯỚNG DẪN', text: 'TS. Hoàng Hữu Đức\nKhoa Khoa học máy tính VKU' },
        { title: 'NHÓM SINH VIÊN THỰC HIỆN', text: 'Nguyễn Công Đức (Lead - Arch Linux)\nNguyễn Tùng Dương (Ubuntu Node)\nNguyễn Văn C (Observability & Benchmark)' },
        { title: 'THÔNG TIN BÁO CÁO', text: 'Đồ án Linux & Phần mềm nguồn mở\nHọc kỳ 1 — Năm học 2026-2027\nĐà Nẵng, Tháng 10/2026' }
    ];

    infoCards.forEach((c, idx) => {
        const cx = 1.0 + idx * 3.9;
        slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
            x: cx, y: 4.8, w: 3.533, h: 1.8,
            fill: { color: '1E293B' },
            line: { color: '334155', width: 1 },
            rectRadius: 0.08
        });
        slide.addText(c.title, {
            x: cx + 0.2, y: 4.95, w: 3.133, h: 0.35,
            fontSize: 11, bold: true, color: COLORS.gold, fontFace: FONT_SANS
        });
        slide.addText(c.text, {
            x: cx + 0.2, y: 5.35, w: 3.133, h: 1.1,
            fontSize: 11, color: 'CBD5E1', fontFace: FONT_SANS, lineSpacing: 18
        });
    });
}

// ==========================================
// SLIDE 2: OVERVIEW & PROBLEM STATEMENT
// ==========================================
{
    const slide = pptx.addSlide();
    slide.background = { color: COLORS.bgLight };
    addHeader(slide, 'BỐI CẢNH & VẤN ĐỀ', '1. TỔNG QUAN & TÍNH CẤP THIẾT CỦA ĐỀ TÀI', 'Thách thức phân phối Linux, rủi ro an ninh Container và giải pháp đột phá của nhóm');
    addFooter(slide, 2);

    const cards = [
        {
            title: 'HAI THÁI CỰC HỆ ĐIỀU HÀNH',
            badge: 'Arch Linux vs Ubuntu',
            color: COLORS.accentBlue,
            items: [
                'Arch Linux: Mô hình Rolling-Release, nhân Linux 6.x mới nhất, siêu tối giản (~400MB RAM), không cài đặt dịch vụ thừa.',
                'Ubuntu Server: Chu kỳ LTS 5 năm ổn định, phổ biến nhưng cồng kềnh (~750MB RAM), nhiều daemon nền mặc định.',
                'Nhu cầu cấp thiết: Cần một công trình đo lường đối sánh định lượng khoa học khi chạy tải công việc MLOps thực tế.'
            ]
        },
        {
            title: 'HIỂM HỌA ROOTFUL DOCKER',
            badge: 'Lỗ hổng Container Escape',
            color: COLORS.vkuRed,
            items: [
                'Docker truyền thống chạy daemon dưới quyền root (UID 0) tối cao của máy chủ.',
                'Khi vi dịch vụ AI bị Remote Code Execution (RCE), hacker có thể khai thác CVE-2019-5736 leo thang kiểm soát máy chủ vật lý.',
                'Mở cổng cơ sở dữ liệu (5432) ra ngoài Internet tạo điều kiện cho botnet quét mạng và đánh cắp dữ liệu mô hình.'
            ]
        },
        {
            title: 'GIẢI PHÁP ĐỘT PHÁ CỦA NHÓM',
            badge: 'Rootless & Zero-Trust',
            color: COLORS.successGreen,
            items: [
                'Thiết kế động cơ Rootless Docker: Daemon chạy hoàn toàn dưới user thường mlops (UID 1003).',
                'Cách ly mạng nội bộ Zero-Trust: Đóng cổng 5432 trên Host, chỉ giao tiếp nội bộ container qua bridge riêng.',
                'Tự động hóa 100% bằng bộ kịch bản IaC Bash script có thể tái lập tức thì và hỗ trợ rollback an toàn.'
            ]
        }
    ];

    cards.forEach((c, idx) => {
        const cx = 0.8 + idx * 4.0;
        addCard(slide, cx, 1.85, 3.733, 4.8, c.color);

        slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
            x: cx + 0.2, y: 2.05, w: 3.333, h: 0.32,
            fill: { color: c.color },
            line: { color: c.color },
            rectRadius: 0.05
        });
        slide.addText(c.badge.toUpperCase(), {
            x: cx + 0.2, y: 2.05, w: 3.333, h: 0.32,
            fontSize: 10, bold: true, color: 'FFFFFF', align: 'center', valign: 'middle', fontFace: FONT_SANS
        });

        slide.addText(c.title, {
            x: cx + 0.2, y: 2.45, w: 3.333, h: 0.45,
            fontSize: 13, bold: true, color: COLORS.primary, align: 'center', fontFace: FONT_SANS
        });

        c.items.forEach((item, iIdx) => {
            slide.addText([
                { text: '• ', options: { bold: true, color: c.color, fontSize: 13 } },
                { text: item, options: { fontSize: 10.8, color: COLORS.textMain, fontFace: FONT_SANS } }
            ], {
                x: cx + 0.25, y: 3.0 + iIdx * 1.25, w: 3.233, h: 1.15,
                lineSpacing: 16, valign: 'top'
            });
        });
    });
}

// ==========================================
// SLIDE 3: SMART GOALS
// ==========================================
{
    const slide = pptx.addSlide();
    slide.background = { color: COLORS.bgLight };
    addHeader(slide, 'MỤC TIÊU NGHIÊN CỨU', '2. MỤC TIÊU NGHIÊN CỨU THEO CHUẨN SMART', 'Cam kết và đo lường tiến độ thực hiện đề tài theo 5 tiêu chuẩn khoa học chính xác');
    addFooter(slide, 3);

    const goals = [
        {
            letter: 'S', name: 'SPECIFIC (MỤC TIÊU CỤ THỂ)',
            desc: 'Triển khai thành công 100% cụm dịch vụ MLOps chuẩn doanh nghiệp gồm 5 thành phần: FastAPI OCR, MLflow Tracking, PostgreSQL DB, Prometheus và Grafana hoạt động hoàn toàn không cần quyền root trên Arch Linux.'
        },
        {
            letter: 'M', name: 'MEASURABLE (ĐO LƯỜNG ĐỊNH LƯỢNG)',
            desc: 'Thu thập số liệu đo lường thực nghiệm khách quan: Mức chiếm dụng RAM tĩnh (Idle), RAM khi có tải, thời gian khởi động OS (Boot Time), thông lượng xử lý AI (Requests/sec), độ trễ p50/p95/p99 và tỷ lệ lỗi (Error Rate).'
        },
        {
            letter: 'A', name: 'ACHIEVABLE (TÍNH KHẢ THI CAO)',
            desc: 'Tự động hóa toàn diện 100% hạ tầng thông qua bộ kịch bản IaC Bash shell chuẩn mực (01_hardening, 02_rootless_docker, 03_deploy_stack, 04_verify_system). Khả năng tái lập và rollback chỉ trong vài giây.'
        },
        {
            letter: 'R & T', name: 'REALISTIC & TIMELY (THỰC TIỄN & ĐÚNG HẠN)',
            desc: 'Khắc phục triệt để lỗ hổng an ninh Container Escape trong môi trường doanh nghiệp thực tế. Hoàn thành 100% mục tiêu trước hạn bảo vệ: Báo cáo học thuật 82 trang và cụm thực nghiệm sẵn sàng bảo vệ.'
        }
    ];

    goals.forEach((g, idx) => {
        const col = idx % 2;
        const row = Math.floor(idx / 2);
        const gx = 0.8 + col * 6.0;
        const gy = 1.85 + row * 2.45;

        addCard(slide, gx, gy, 5.733, 2.25, COLORS.accentBlue);

        slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
            x: gx + 0.3, y: gy + 0.3, w: 0.9, h: 0.9,
            fill: { color: COLORS.accentBlue },
            line: { color: COLORS.accentBlue },
            rectRadius: 0.08
        });
        slide.addText(g.letter, {
            x: gx + 0.3, y: gy + 0.3, w: 0.9, h: 0.9,
            fontSize: g.letter.length > 2 ? 14 : 20, bold: true, color: 'FFFFFF', align: 'center', valign: 'middle', fontFace: FONT_SANS
        });

        slide.addText(g.name, {
            x: gx + 1.4, y: gy + 0.3, w: 4.1, h: 0.35,
            fontSize: 13, bold: true, color: COLORS.primary, fontFace: FONT_SANS
        });

        slide.addText(g.desc, {
            x: gx + 1.4, y: gy + 0.7, w: 4.1, h: 1.35,
            fontSize: 11, color: COLORS.textMain, fontFace: FONT_SANS, lineSpacing: 18
        });
    });
}

// ==========================================
// SLIDE 4: DUAL-NODE ARCHITECTURE
// ==========================================
{
    const slide = pptx.addSlide();
    slide.background = { color: COLORS.bgLight };
    addHeader(slide, 'KIẾN TRÚC HẠ TẦNG', '3. KIẾN TRÚC HỆ THỐNG TỔNG THỂ DUAL-NODE', 'Mô hình thực nghiệm đối kháng song song giữa nút Arch Linux và nút Ubuntu Server');
    addFooter(slide, 4);

    // Left Node: Arch Linux
    const nx1 = 0.8;
    addCard(slide, nx1, 1.85, 5.733, 4.8, COLORS.accentBlue);
    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
        x: nx1 + 0.25, y: 2.05, w: 5.233, h: 0.35,
        fill: { color: COLORS.accentBlue },
        line: { color: COLORS.accentBlue },
        rectRadius: 0.05
    });
    slide.addText('MÁY CHỦ ARCH LINUX (PRIMARY / ROOTLESS DOCKER)', {
        x: nx1 + 0.25, y: 2.05, w: 5.233, h: 0.35,
        fontSize: 11, bold: true, color: 'FFFFFF', align: 'center', valign: 'middle', fontFace: FONT_SANS
    });

    const archItems = [
        'Hệ điều hành: Arch Linux Rolling Release (Linux Kernel 6.x hiện đại).',
        'Tài nguyên tĩnh: Chiếm dụng chỉ 438 MB RAM (siêu nhẹ, tối ưu hóa tối đa).',
        'Động cơ Container: Docker Rootless Daemon (User mlops, UID 1003).',
        'Phân đoạn mạng: Toàn bộ container nằm trong bridge riêng mlops-net.',
        '5 Vi dịch vụ vi mô độc lập:',
        '  • FastAPI OCR Serving (Port 8080) — Non-root User UID 10001',
        '  • MLflow Tracking UI (Port 5000) — Quản lý vòng đời mô hình',
        '  • PostgreSQL 15 (Port 5432) — Zero-Trust, ĐÓNG TRÊN HOST IP',
        '  • Prometheus Server (Port 9090) — Cào chỉ số chuỗi thời gian',
        '  • Grafana Dashboard (Port 3000) — Trực quan hóa thời gian thực'
    ];
    archItems.forEach((item, iIdx) => {
        slide.addText(item, {
            x: nx1 + 0.35, y: 2.55 + iIdx * 0.4, w: 5.033, h: 0.35,
            fontSize: 10.5, color: COLORS.textMain, fontFace: FONT_SANS
        });
    });

    // Right Node: Ubuntu Server
    const nx2 = 6.8;
    addCard(slide, nx2, 1.85, 5.733, 4.8, COLORS.navyHeader);
    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
        x: nx2 + 0.25, y: 2.05, w: 5.233, h: 0.35,
        fill: { color: COLORS.navyHeader },
        line: { color: COLORS.navyHeader },
        rectRadius: 0.05
    });
    slide.addText('MÁY CHỦ UBUNTU SERVER (BASELINE / ROOTFUL DOCKER)', {
        x: nx2 + 0.25, y: 2.05, w: 5.233, h: 0.35,
        fontSize: 11, bold: true, color: 'FFFFFF', align: 'center', valign: 'middle', fontFace: FONT_SANS
    });

    const ubuntuItems = [
        'Hệ điều hành: Ubuntu Server 22.04 / 24.04 LTS (Nhân Linux 6.8 Enterprise).',
        'Tài nguyên tĩnh: Chiếm dụng 742 MB RAM (gấp 1.7 lần so với Arch Linux).',
        'Động cơ Container: Docker Rootful Daemon (Chạy trực tiếp dưới quyền root UID 0).',
        'Cấu hình Stack đối chứng: Chạy cùng bộ 5 vi dịch vụ và khối lượng tải.',
        'Mục đích nghiên cứu đối chứng:',
        '  • So sánh độ trễ suy luận AI khi có và không có lớp slirp4netns.',
        '  • Đánh giá mức độ hao tổn CPU/RAM giữa hai kiến trúc hạt nhân.',
        '  • Phân tích sự đánh đổi (trade-off) giữa an ninh và thông lượng xử lý.',
        '  • Kiểm chứng tính tương thích đa nền tảng của quy chuẩn MLOps.'
    ];
    ubuntuItems.forEach((item, iIdx) => {
        slide.addText(item, {
            x: nx2 + 0.35, y: 2.55 + iIdx * 0.42, w: 5.033, h: 0.38,
            fontSize: 10.5, color: COLORS.textMain, fontFace: FONT_SANS
        });
    });
}

// ==========================================
// SLIDE 5: ROOTLESS CONTAINER ENGINE
// ==========================================
{
    const slide = pptx.addSlide();
    slide.background = { color: COLORS.bgLight };
    addHeader(slide, 'CƠ CHẾ ĐỘT PHÁ', '4. ĐỘNG CƠ ROOTLESS CONTAINERIZATION', 'Cơ chế cô lập tầng kernel, ánh xạ không gian tên và triệt tiêu nguy cơ chiếm quyền');
    addFooter(slide, 5);

    const steps = [
        {
            num: '01', title: 'USER NAMESPACES & SUB-UID MAPPING',
            points: [
                'Sử dụng User Namespaces của Linux kernel để ánh xạ tài khoản unprivileged mlops (UID 1003 trên Host) thành UID 0 ảo bên trong container.',
                'File /etc/subuid cấp phát dải 100000:65536. Tiến trình container nghĩ mình là root nhưng ở tầng Host chỉ là UID 100000+.',
                'Không đòi hỏi cấp quyền sudo hay gán quyền setuid root cho binary Docker máy chủ.'
            ]
        },
        {
            num: '02', title: 'SLIRP4NETNS USER-MODE NETWORKING',
            points: [
                'Thay vì can thiệp trực tiếp vào iptables của kernel host (đòi hỏi quyền root CAP_NET_ADMIN), Docker Rootless sử dụng slirp4netns.',
                'Toàn bộ ngăn xếp mạng TCP/IP được ảo hóa hoàn toàn ở không gian người dùng (User-space).',
                'Ngăn chặn triệt để nguy cơ vi dịch vụ chiếm quyền điều khiển cấu hình mạng máy chủ.'
            ]
        },
        {
            num: '03', title: 'TRIỆT TIÊU NGUY CƠ CONTAINER ESCAPE',
            points: [
                'Trong kịch bản xấu nhất vi dịch vụ AI bị chiếm quyền qua lỗ hổng RCE, kẻ tấn công thoát khỏi container cũng chỉ rơi vào user thường mlops.',
                'Không thể ghi đè file hệ thống (/etc, /boot, /root), không thể cài cắm rootkit vào kernel.',
                'Đạt chuẩn an ninh Enterprise cao nhất, an toàn cho mô hình Multi-tenant thực tế.'
            ]
        }
    ];

    steps.forEach((s, idx) => {
        const sy = 1.85 + idx * 1.62;
        addCard(slide, 0.8, sy, 11.733, 1.48, COLORS.accentBlue);

        slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
            x: 1.0, y: sy + 0.24, w: 0.9, h: 1.0,
            fill: { color: COLORS.accentBlue },
            line: { color: COLORS.accentBlue },
            rectRadius: 0.08
        });
        slide.addText(s.num, {
            x: 1.0, y: sy + 0.24, w: 0.9, h: 1.0,
            fontSize: 20, bold: true, color: 'FFFFFF', align: 'center', valign: 'middle', fontFace: FONT_SANS
        });

        slide.addText(s.title, {
            x: 2.1, y: sy + 0.16, w: 10.2, h: 0.32,
            fontSize: 13, bold: true, color: COLORS.primary, fontFace: FONT_SANS
        });

        s.points.forEach((p, pIdx) => {
            slide.addText([
                { text: '• ', options: { bold: true, color: COLORS.accentBlue, fontSize: 11 } },
                { text: p, options: { fontSize: 10.5, color: COLORS.textMain, fontFace: FONT_SANS } }
            ], {
                x: 2.1, y: sy + 0.48 + pIdx * 0.3, w: 10.2, h: 0.3,
                valign: 'middle'
            });
        });
    });
}

// ==========================================
// SLIDE 6: ZERO-TRUST NETWORK
// ==========================================
{
    const slide = pptx.addSlide();
    slide.background = { color: COLORS.bgLight };
    addHeader(slide, 'AN NINH MẠNG', '5. MÔ HÌNH AN NINH MẠNG NỘI BỘ ZERO-TRUST', 'Nguyên tắc "Không bao giờ tin tưởng, luôn luôn xác thực" trong hạ tầng vi dịch vụ MLOps');
    addFooter(slide, 6);

    // Left: Traditional Architecture (Threats)
    const zx1 = 0.8;
    addCard(slide, zx1, 1.85, 5.733, 4.8, COLORS.vkuRed);
    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
        x: zx1 + 0.25, y: 2.05, w: 5.233, h: 0.35,
        fill: { color: COLORS.vkuRed },
        line: { color: COLORS.vkuRed },
        rectRadius: 0.05
    });
    slide.addText('HỆ THỐNG TRUYỀN THỐNG (NGUY CƠ AN NINH CAO)', {
        x: zx1 + 0.25, y: 2.05, w: 5.233, h: 0.35,
        fontSize: 11, bold: true, color: 'FFFFFF', align: 'center', valign: 'middle', fontFace: FONT_SANS
    });

    const tradPoints = [
        { label: 'Cổng Cơ sở dữ liệu mở 0.0.0.0:', desc: 'Publish cổng 5432 trực tiếp ra Internet cho botnet quét mạng và brute-force mật khẩu.' },
        { label: 'Mạng phẳng (Flat Network):', desc: 'Tất cả container dùng chung mạng default bridge, không có phân ranh giới bảo mật.' },
        { label: 'Nguy cơ Lateral Movement:', desc: 'Hacker chỉ cần thỏa hiệp 1 container là có thể dò quét và tấn công toàn bộ vi dịch vụ lân cận.' },
        { label: 'Đặc quyền tối đa:', desc: 'Container chạy dưới quyền root, chia sẻ file cấu hình và biến môi trường không được kiểm soát.' }
    ];

    tradPoints.forEach((p, idx) => {
        slide.addText([
            { text: '[RỦI RO] ', options: { bold: true, color: COLORS.vkuRed, fontSize: 10.5 } },
            { text: p.label + ' ', options: { bold: true, color: COLORS.primary, fontSize: 11 } },
            { text: p.desc, options: { color: COLORS.textMain, fontSize: 10.5, fontFace: FONT_SANS } }
        ], {
            x: zx1 + 0.3, y: 2.55 + idx * 1.05, w: 5.133, h: 0.95,
            lineSpacing: 16, valign: 'top'
        });
    });

    // Right: Zero-Trust Implementation
    const zx2 = 6.8;
    addCard(slide, zx2, 1.85, 5.733, 4.8, COLORS.successGreen);
    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
        x: zx2 + 0.25, y: 2.05, w: 5.233, h: 0.35,
        fill: { color: COLORS.successGreen },
        line: { color: COLORS.successGreen },
        rectRadius: 0.05
    });
    slide.addText('MÔ HÌNH ZERO-TRUST CỦA NHÓM (BẢO MẬT ĐA LỚP)', {
        x: zx2 + 0.25, y: 2.05, w: 5.233, h: 0.35,
        fontSize: 11, bold: true, color: 'FFFFFF', align: 'center', valign: 'middle', fontFace: FONT_SANS
    });

    const zeroPoints = [
        { label: 'Đóng 100% cổng DB trên Host:', desc: 'PostgreSQL 5432 chỉ lắng nghe trên bridge nội bộ mlops-net; bên ngoài hoàn toàn vô hình.' },
        { label: 'Phân đoạn vùng mạng nghiêm ngặt:', desc: 'Chỉ mở cổng tiếp nhận request (FastAPI 8080 cho inference và Grafana 3000 cho dashboard).' },
        { label: 'Nguyên tắc đặc quyền tối thiểu:', desc: 'Container giao tiếp bằng DNS nội bộ cô lập, cơ sở dữ liệu xác thực mật khẩu phức tạp.' },
        { label: 'Kiểm soát luồng dữ liệu (Data Flow):', desc: 'Prometheus chỉ cào metrics qua endpoint chuyên biệt, không có quyền truy cập dữ liệu bảng.' }
    ];

    zeroPoints.forEach((p, idx) => {
        slide.addText([
            { text: '[BẢO VỆ] ', options: { bold: true, color: COLORS.successGreen, fontSize: 10.5 } },
            { text: p.label + ' ', options: { bold: true, color: COLORS.primary, fontSize: 11 } },
            { text: p.desc, options: { color: COLORS.textMain, fontSize: 10.5, fontFace: FONT_SANS } }
        ], {
            x: zx2 + 0.3, y: 2.55 + idx * 1.05, w: 5.133, h: 0.95,
            lineSpacing: 16, valign: 'top'
        });
    });
}

// ==========================================
// SLIDE 7: HOST HARDENING & IAC
// ==========================================
{
    const slide = pptx.addSlide();
    slide.background = { color: COLORS.bgLight };
    addHeader(slide, 'TỰ ĐỘNG HÓA HẠ TẦNG', '6. TỰ ĐỘNG HÓA GIA CỐ MÁY CHỦ (HARDENING)', 'Bộ kịch bản IaC Bash shell với 4 lớp phòng thủ chiều sâu và khả năng rollback tức thì');
    addFooter(slide, 7);

    const layers = [
        {
            title: 'LỚP 1: TƯỜNG LỬA UFW CHỦ ĐỘNG',
            subtitle: 'Chính sách Default Deny',
            desc: 'Thiết lập UFW chặn mặc định toàn bộ lưu lượng đi vào. Whitelist duy nhất 5 cổng dịch vụ cần thiết: SSH (22), FastAPI (8080), MLflow (5000), Grafana (3000), Prometheus (9090). Toàn bộ cổng lạ bị drop thầm lặng.'
        },
        {
            title: 'LỚP 2: KERNEL HARDENING (SYSCTL)',
            subtitle: 'Gia cố tham số hạt nhân',
            desc: 'Cấu hình file /etc/sysctl.d/99-mlops-security.conf: Kích hoạt tcp_syncookies chống tấn công từ chối dịch vụ SYN Flood; vô hiệu hóa IP Source Routing và ICMP Redirects; bật fs.protected_regular ngăn chặn symlink attack.'
        },
        {
            title: 'LỚP 3: FAIL2BAN & CGROUPS LIMITS',
            subtitle: 'Chống Brute-force & Quá tải',
            desc: 'Triển khai Fail2ban SSH jail: Tự động khóa IP tấn công sau 5 lần đăng nhập thất bại. Thiết lập giới hạn tài nguyên Systemd Cgroups cho user mlops, ngăn chặn vi dịch vụ AI chiếm cạn kiệt CPU/RAM làm tê liệt máy chủ.'
        },
        {
            title: 'LỚP 4: KHẢ NĂNG ROLLBACK 100%',
            subtitle: 'An toàn & Khả nghịch cao',
            desc: 'Cung cấp kịch bản 01_rollback_hardening.sh: Tự động khôi phục cấu hình iptables, tắt UFW, reset tham số sysctl và cấu hình mạng về trạng thái gốc của hệ thống chỉ trong vòng 3 giây khi cần bảo trì.'
        }
    ];

    layers.forEach((l, idx) => {
        const col = idx % 2;
        const row = Math.floor(idx / 2);
        const lx = 0.8 + col * 6.0;
        const ly = 1.85 + row * 2.45;

        addCard(slide, lx, ly, 5.733, 2.25, COLORS.accentBlue);

        slide.addText(l.title, {
            x: lx + 0.3, y: ly + 0.25, w: 5.133, h: 0.35,
            fontSize: 13, bold: true, color: COLORS.primary, fontFace: FONT_SANS
        });
        slide.addText(l.subtitle, {
            x: lx + 0.3, y: ly + 0.6, w: 5.133, h: 0.25,
            fontSize: 10.5, bold: true, color: COLORS.accentBlue, fontFace: FONT_SANS
        });
        slide.addText(l.desc, {
            x: lx + 0.3, y: ly + 0.9, w: 5.133, h: 1.2,
            fontSize: 10.8, color: COLORS.textMain, fontFace: FONT_SANS, lineSpacing: 17
        });
    });
}

// ==========================================
// SLIDE 8: AI OCR SERVING MICROSERVICE
// ==========================================
{
    const slide = pptx.addSlide();
    slide.background = { color: COLORS.bgLight };
    addHeader(slide, 'VI DỊCH VỤ AI', '7. VI DỊCH VỤ AI OCR SERVING TỐI ƯU', 'Đóng gói Dockerfile Multi-stage build và thực thi dưới quyền UID 10001');
    addFooter(slide, 8);

    // Left: Multi-stage build
    const mx1 = 0.8;
    addCard(slide, mx1, 1.85, 5.733, 4.8, COLORS.accentBlue);
    slide.addText('QUY CHUẨN DOCKERFILE MULTI-STAGE', {
        x: mx1 + 0.3, y: 2.1, w: 5.133, h: 0.35,
        fontSize: 13.5, bold: true, color: COLORS.accentBlue, fontFace: FONT_SANS
    });

    const buildPoints = [
        { label: 'Stage 1 (Builder):', desc: 'Cài đặt gcc, python-dev và build các bánh xe (wheels) cho các thư viện C++ nặng.' },
        { label: 'Stage 2 (Runtime sạch):', desc: 'Chỉ sao chép các wheels và binary đã biên dịch; loại bỏ hoàn toàn gcc, g++, build-essential khỏi image sản phẩm cuối.' },
        { label: 'Giảm 65% kích thước image:', desc: 'Dung lượng rút gọn từ ~900MB xuống chỉ còn ~310MB.' },
        { label: 'Chỉ thị USER 10001 (mlopsuser):', desc: 'Ứng dụng không bao giờ thực thi dưới quyền root ngay cả bên trong container.' }
    ];

    buildPoints.forEach((p, idx) => {
        slide.addText([
            { text: '• ' + p.label + ' ', options: { bold: true, color: COLORS.accentBlue, fontSize: 11 } },
            { text: p.desc, options: { color: COLORS.textMain, fontSize: 10.5, fontFace: FONT_SANS } }
        ], {
            x: mx1 + 0.3, y: 2.6 + idx * 1.0, w: 5.133, h: 0.9,
            lineSpacing: 16, valign: 'top'
        });
    });

    // Right: Inference Engine & Performance
    const mx2 = 6.8;
    addCard(slide, mx2, 1.85, 5.733, 4.8, COLORS.navyHeader);
    slide.addText('ĐỘNG CƠ NHẬN DẠNG CHỮ & HIỆU NĂNG', {
        x: mx2 + 0.3, y: 2.1, w: 5.133, h: 0.35,
        fontSize: 13.5, bold: true, color: COLORS.navyHeader, fontFace: FONT_SANS
    });

    const perfPoints = [
        { label: 'Tesseract-OCR LSTM Engine:', desc: 'Sử dụng mạng nơ-ron hồi quy LSTM tối ưu CPU, tiêu thụ chỉ ~60MB RAM (thay vì các framework nặng ngốn 1.5GB RAM).' },
        { label: 'Tốc độ suy luận thần tốc:', desc: 'Thời gian bóc tách chữ chỉ mất 200 - 300 ms/ảnh trên môi trường CPU tiêu chuẩn.' },
        { label: 'Độ chính xác cao:', desc: 'Hỗ trợ nhận dạng song ngữ tiếng Việt (vie) và tiếng Anh (eng) mượt mà.' },
        { label: 'Tích hợp MLOps tự động:', desc: 'Tự động ghi nhận log thực nghiệm vào MLflow và xuất metrics phân vị độ trễ ra Prometheus.' }
    ];

    perfPoints.forEach((p, idx) => {
        slide.addText([
            { text: '• ' + p.label + ' ', options: { bold: true, color: COLORS.navyHeader, fontSize: 11 } },
            { text: p.desc, options: { color: COLORS.textMain, fontSize: 10.5, fontFace: FONT_SANS } }
        ], {
            x: mx2 + 0.3, y: 2.6 + idx * 1.0, w: 5.133, h: 0.9,
            lineSpacing: 16, valign: 'top'
        });
    });
}

// ==========================================
// SLIDE 9: OBSERVABILITY & CLI
// ==========================================
{
    const slide = pptx.addSlide();
    slide.background = { color: COLORS.bgLight };
    addHeader(slide, 'GIÁM SÁT HỆ THỐNG', '8. HỆ THỐNG QUAN SÁT & TERMINAL CLI', 'Giám sát thời gian thực với Prometheus/Grafana và công cụ dòng lệnh interactive');
    addFooter(slide, 9);

    const tools = [
        {
            title: 'PROMETHEUS SERVER (PORT 9090)',
            badge: 'Metric Scraping',
            desc: 'Tự động cào chỉ số chuỗi thời gian định kỳ mỗi 5s từ endpoint /metrics của FastAPI OCR và máy chủ host. Lưu vết dữ liệu time-series phục vụ phân tích xu hướng.'
        },
        {
            title: 'GRAFANA DASHBOARD (PORT 3000)',
            badge: 'Data Visualization',
            desc: 'Trực quan hóa tức thời thông lượng yêu cầu (RPS), độ trễ phân vị p50/p95/p99 và % sử dụng CPU/RAM của từng container. Giúp phát hiện tức thì điểm nghẽn hiệu năng.'
        },
        {
            title: 'MLFLOW TRACKING UI (PORT 5000)',
            badge: 'Model Lifecycle',
            desc: 'Quản lý vòng đời mô hình học máy, lưu vết siêu tham số, metadata ảnh và các artifact nhận dạng. Kết nối cơ sở dữ liệu PostgreSQL lưu trữ bền vững lâu dài.'
        },
        {
            title: 'TERMINAL INTERACTIVE CLI (AI_CLI.SH)',
            badge: 'DevOps Tooling',
            desc: 'Giao diện menu dòng lệnh ANSI Color hiện đại cho quản trị viên Linux. Cho phép chọn ảnh mẫu, gửi request suy luận đến FastAPI và hiển thị kết quả OCR trực tiếp trên terminal.'
        }
    ];

    tools.forEach((t, idx) => {
        const col = idx % 2;
        const row = Math.floor(idx / 2);
        const tx = 0.8 + col * 6.0;
        const ty = 1.85 + row * 2.45;

        addCard(slide, tx, ty, 5.733, 2.25, COLORS.accentBlue);

        slide.addText(t.title, {
            x: tx + 0.3, y: ty + 0.25, w: 5.133, h: 0.35,
            fontSize: 13, bold: true, color: COLORS.primary, fontFace: FONT_SANS
        });
        slide.addText(t.badge, {
            x: tx + 0.3, y: ty + 0.6, w: 5.133, h: 0.25,
            fontSize: 10.5, bold: true, color: COLORS.accentBlue, fontFace: FONT_SANS
        });
        slide.addText(t.desc, {
            x: tx + 0.3, y: ty + 0.9, w: 5.133, h: 1.2,
            fontSize: 10.8, color: COLORS.textMain, fontFace: FONT_SANS, lineSpacing: 17
        });
    });
}

// ==========================================
// SLIDE 10: BENCHMARK RESULTS
// ==========================================
{
    const slide = pptx.addSlide();
    slide.background = { color: COLORS.bgLight };
    addHeader(slide, 'ĐỐI SÁNH ĐỊNH LƯỢNG', '9. KẾT QUẢ ĐỐI SÁNH THỰC NGHIỆM ĐỊNH LƯỢNG', 'Bảng số liệu đo lường trực tiếp giữa Arch Linux (Rootless) và Ubuntu Server (Rootful)');
    addFooter(slide, 10);

    // 4 Stat Highlight Boxes
    const stats = [
        { val: '40.9% ↓', label: 'Tiết kiệm RAM tĩnh', sub: 'Arch 438MB vs Ubuntu 742MB' },
        { val: '2.6x ↑', label: 'Khởi động OS nhanh hơn', sub: 'Arch 4.8s vs Ubuntu 12.6s' },
        { val: '342.5', label: 'RPS thông lượng AI', sub: 'Arch cao hơn 4.3% so với Ubuntu' },
        { val: '5/5 PASS', label: 'Kiểm định an ninh', sub: 'Đạt chuẩn Enterprise cao nhất' }
    ];

    stats.forEach((s, idx) => {
        const sx = 0.8 + idx * 3.0;
        addCard(slide, sx, 1.85, 2.733, 1.25, COLORS.accentBlue);
        slide.addText(s.val, {
            x: sx + 0.1, y: 1.95, w: 2.533, h: 0.45,
            fontSize: 22, bold: true, color: COLORS.accentBlue, align: 'center', fontFace: FONT_SANS
        });
        slide.addText(s.label, {
            x: sx + 0.1, y: 2.4, w: 2.533, h: 0.3,
            fontSize: 11, bold: true, color: COLORS.primary, align: 'center', fontFace: FONT_SANS
        });
        slide.addText(s.sub, {
            x: sx + 0.1, y: 2.7, w: 2.533, h: 0.25,
            fontSize: 9.5, italic: true, color: COLORS.textMuted, align: 'center', fontFace: FONT_SANS
        });
    });

    // Detailed Benchmark Table
    const tableData = [
        [
            { text: 'Chỉ số đo lường hiệu năng', options: { fill: COLORS.navyHeader, color: 'FFFFFF', bold: true, align: 'center' } },
            { text: 'Arch Linux (Rootless Docker)', options: { fill: COLORS.navyHeader, color: 'FFFFFF', bold: true, align: 'center' } },
            { text: 'Ubuntu Server (Rootful Docker)', options: { fill: COLORS.navyHeader, color: 'FFFFFF', bold: true, align: 'center' } },
            { text: 'Chênh lệch / Đánh giá', options: { fill: COLORS.navyHeader, color: 'FFFFFF', bold: true, align: 'center' } }
        ],
        [
            { text: 'Chiếm dụng RAM tĩnh (Idle OS)' },
            { text: '438 MB RAM', options: { bold: true, color: COLORS.accentBlue, align: 'center' } },
            { text: '742 MB RAM', options: { align: 'center' } },
            { text: 'Arch Linux tiết kiệm 40.9% bộ nhớ.' }
        ],
        [
            { text: 'Chiếm dụng RAM động (Stack Active)' },
            { text: '1,280 MB RAM', options: { bold: true, color: COLORS.accentBlue, align: 'center' } },
            { text: '1,620 MB RAM', options: { align: 'center' } },
            { text: 'Arch Linux tiết kiệm 20.9% bộ nhớ.' }
        ],
        [
            { text: 'Thời gian khởi động OS (Boot Time)' },
            { text: '4.8 giây (systemd-analyze)', options: { bold: true, color: COLORS.accentBlue, align: 'center' } },
            { text: '12.6 giây (systemd-analyze)', options: { align: 'center' } },
            { text: 'Arch Linux khởi động nhanh hơn 2.6 lần.' }
        ],
        [
            { text: 'Thông lượng xử lý AI (Throughput)' },
            { text: '342.5 Requests / Giây', options: { bold: true, color: COLORS.accentBlue, align: 'center' } },
            { text: '328.1 Requests / Giây', options: { align: 'center' } },
            { text: 'Arch Linux đạt hiệu năng cao hơn 4.3%.' }
        ],
        [
            { text: 'Độ trễ phân vị p95 (95% requests)' },
            { text: '64.8 ms', options: { bold: true, color: COLORS.accentBlue, align: 'center' } },
            { text: '72.5 ms', options: { align: 'center' } },
            { text: 'Arch Linux duy trì độ trễ ổn định hơn.' }
        ],
        [
            { text: 'Tỷ lệ lỗi (Error Rate)' },
            { text: '0.00% (500/500 thành công)', options: { bold: true, color: COLORS.successGreen, align: 'center' } },
            { text: '0.00% (500/500 thành công)', options: { bold: true, color: COLORS.successGreen, align: 'center' } },
            { text: 'Độ tin cậy tuyệt đối 100% trên cả 2 môi trường.' }
        ]
    ];

    slide.addTable(tableData, {
        x: 0.8, y: 3.25, w: 11.733, h: 3.35,
        border: { type: 'solid', pt: 1, color: 'CBD5E1' },
        fill: 'FFFFFF',
        fontSize: 10.5,
        fontFace: FONT_SANS,
        valign: 'middle'
    });
}

// ==========================================
// SLIDE 11: DELIVERABLES & PROGRESS
// ==========================================
{
    const slide = pptx.addSlide();
    slide.background = { color: COLORS.bgLight };
    addHeader(slide, 'TIẾN ĐỘ THỰC HIỆN', '10. ĐÁNH GIÁ TIẾN ĐỘ & SẢN PHẨM BÀN GIAO', 'Tổng kết kết quả thực hiện đề tài và các sản phẩm khoa học kỹ thuật đã hoàn thành');
    addFooter(slide, 11);

    // Left: Technical Deliverables
    const dx1 = 0.8;
    addCard(slide, dx1, 1.85, 5.733, 4.8, COLORS.successGreen);
    slide.addText('CÁC SẢN PHẨM KỸ THUẬT ĐÃ HOÀN THÀNH', {
        x: dx1 + 0.3, y: 2.1, w: 5.133, h: 0.35,
        fontSize: 13.5, bold: true, color: COLORS.successGreen, fontFace: FONT_SANS
    });

    const deliverables = [
        { label: 'Mục tiêu SMART:', desc: 'Đã cam kết và hoàn thành 100% cả 6 tiêu chí đã đề ra ban đầu.' },
        { label: 'Bộ kịch bản IaC Bash script đầy đủ:', desc: '01_system_hardening.sh, 01_rollback_hardening.sh, 02_setup_rootless_docker.sh, 03_deploy_stack.sh, 04_verify_system.sh, ai_cli.sh, scan_image.sh.' },
        { label: 'Kho lưu trữ Git chuẩn mực:', desc: 'Đã đồng bộ mã nguồn lên nhánh arch-mlops trên GitHub của nhóm.' },
        { label: 'Báo cáo đồ án chính thức:', desc: 'Đã biên soạn hoàn chỉnh 7 chương, dày 82 trang chuẩn mẫu học thuật VKU (định dạng DOCX và PDF).' },
        { label: 'Hệ sinh thái thực nghiệm:', desc: 'Cả 2 máy chủ ảo hoạt động ổn định và sẵn sàng cho buổi bảo vệ chính thức.' }
    ];

    deliverables.forEach((d, idx) => {
        slide.addText([
            { text: '• ' + d.label + ' ', options: { bold: true, color: COLORS.successGreen, fontSize: 11 } },
            { text: d.desc, options: { color: COLORS.textMain, fontSize: 10.5, fontFace: FONT_SANS } }
        ], {
            x: dx1 + 0.3, y: 2.55 + idx * 0.82, w: 5.133, h: 0.75,
            lineSpacing: 16, valign: 'top'
        });
    });

    // Right: Team Member Contributions
    const dx2 = 6.8;
    addCard(slide, dx2, 1.85, 5.733, 4.8, COLORS.accentBlue);
    slide.addText('PHÂN CÔNG NHIỆM VỤ & ĐÓNG GÓP THÀNH VIÊN', {
        x: dx2 + 0.3, y: 2.1, w: 5.133, h: 0.35,
        fontSize: 13.5, bold: true, color: COLORS.accentBlue, fontFace: FONT_SANS
    });

    const team = [
        {
            name: 'Nguyễn Công Đức (Trưởng nhóm — Lead)',
            role: 'Chịu trách nhiệm kiến trúc tổng thể, hạ tầng Arch Linux, Rootless Docker, mạng Zero-Trust và bộ kịch bản IaC.',
            percent: 'Đóng góp: 100%'
        },
        {
            name: 'Nguyễn Tùng Dương (Thành viên)',
            role: 'Chịu trách nhiệm triển khai nút Ubuntu Server baseline, chuẩn hóa cấu hình đối chứng và kiểm thử an ninh mạng.',
            percent: 'Đóng góp: 100%'
        },
        {
            name: 'Nguyễn Văn C (Thành viên)',
            role: 'Chịu trách nhiệm thiết lập Prometheus, Grafana, thực hiện đo lường tải công việc và thu thập số liệu benchmark.',
            percent: 'Đóng góp: 100%'
        }
    ];

    team.forEach((m, idx) => {
        const my = 2.65 + idx * 1.25;
        slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
            x: dx2 + 0.3, y: my, w: 5.133, h: 1.1,
            fill: { color: 'F1F5F9' },
            line: { color: 'CBD5E1', width: 1 },
            rectRadius: 0.05
        });
        slide.addText(m.name, {
            x: dx2 + 0.45, y: my + 0.1, w: 3.5, h: 0.25,
            fontSize: 11, bold: true, color: COLORS.primary, fontFace: FONT_SANS
        });
        slide.addText(m.percent, {
            x: dx2 + 3.8, y: my + 0.1, w: 1.5, h: 0.25,
            fontSize: 10.5, bold: true, color: COLORS.accentBlue, align: 'right', fontFace: FONT_SANS
        });
        slide.addText(m.role, {
            x: dx2 + 0.45, y: my + 0.38, w: 4.8, h: 0.65,
            fontSize: 10, color: COLORS.textMuted, fontFace: FONT_SANS, lineSpacing: 15
        });
    });
}

// ==========================================
// SLIDE 12: ROADMAP & CONCLUSION (Q&A)
// ==========================================
{
    const slide = pptx.addSlide();
    slide.background = { color: COLORS.bgLight };
    addHeader(slide, 'HƯỚNG PHÁT TRIỂN & KẾT LUẬN', '11. HƯỚNG PHÁT TRIỂN & PHIÊN HỎI ĐÁP', 'Định hướng mở rộng kiến trúc trong tương lai và lời cảm ơn Hội đồng');
    addFooter(slide, 12);

    // Left: Future Roadmap
    const cx1 = 0.8;
    addCard(slide, cx1, 1.85, 5.733, 4.8, COLORS.accentBlue);
    slide.addText('ĐỊNH HƯỚNG NÂNG CẤP HẠ TẦNG TƯƠNG LAI', {
        x: cx1 + 0.3, y: 2.1, w: 5.133, h: 0.35,
        fontSize: 13.5, bold: true, color: COLORS.accentBlue, fontFace: FONT_SANS
    });

    const roadmap = [
        { label: '1. Rootless k3s Cluster:', desc: 'Nâng cấp kiến trúc từ máy chủ đơn lẻ lên cụm phân tán đa máy chủ sử dụng bản phân phối Kubernetes unprivileged siêu nhẹ.' },
        { label: '2. Mutual TLS (mTLS):', desc: 'Tích hợp Service Mesh Linkerd mã hóa toàn bộ lưu lượng giữa các vi dịch vụ bằng chứng chỉ số tự động xoay vòng.' },
        { label: '3. Runtime Security với Falco eBPF:', desc: 'Khai thác công nghệ eBPF để giám sát các lời gọi hệ thống (Syscalls) ở tầng kernel, phát hiện xâm nhập tức thì.' },
        { label: '4. DevSecOps CI/CD Pipeline:', desc: 'Tích hợp công cụ quét lỗ hổng Trivy vào GitHub Actions để tự động kiểm định CVE trước khi đóng gói image.' }
    ];

    roadmap.forEach((r, idx) => {
        slide.addText([
            { text: r.label + ' ', options: { bold: true, color: COLORS.accentBlue, fontSize: 11 } },
            { text: r.desc, options: { color: COLORS.textMain, fontSize: 10.5, fontFace: FONT_SANS } }
        ], {
            x: cx1 + 0.3, y: 2.6 + idx * 1.0, w: 5.133, h: 0.9,
            lineSpacing: 16, valign: 'top'
        });
    });

    // Right: Thank You & Q&A
    const cx2 = 6.8;
    addCard(slide, cx2, 1.85, 5.733, 4.8, COLORS.vkuRed);

    slide.addText('LỜI CẢM ƠN', {
        x: cx2 + 0.3, y: 2.15, w: 5.133, h: 0.35,
        fontSize: 16, bold: true, color: COLORS.vkuRed, align: 'center', fontFace: FONT_SANS
    });

    slide.addText('Nhóm tác giả xin chân thành cảm ơn TS. Hoàng Hữu Đức và Quý Thầy Cô trong Hội đồng Khoa học máy tính VKU đã tận tình hướng dẫn, định hướng và tạo mọi điều kiện thuận lợi nhất để nhóm hoàn thành xuất sắc đề tài này!', {
        x: cx2 + 0.4, y: 2.65, w: 4.933, h: 1.25,
        fontSize: 12, italic: true, color: COLORS.textMain, align: 'center', fontFace: FONT_SANS, lineSpacing: 20
    });

    // Big Q&A Box
    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
        x: cx2 + 0.4, y: 4.15, w: 4.933, h: 2.2,
        fill: { color: COLORS.bgDark },
        line: { color: COLORS.gold, width: 2 },
        rectRadius: 0.08
    });

    slide.addText('Q & A', {
        x: cx2 + 0.4, y: 4.4, w: 4.933, h: 0.5,
        fontSize: 26, bold: true, color: COLORS.gold, align: 'center', fontFace: FONT_SANS
    });

    slide.addText('KÍNH MỜI QUÝ THẦY CÔ VÀ HỘI ĐỒNG\nĐẶT CÂU HỎI CHẤT VẤN!', {
        x: cx2 + 0.4, y: 5.0, w: 4.933, h: 1.0,
        fontSize: 14, bold: true, color: 'FFFFFF', align: 'center', fontFace: FONT_SANS, lineSpacing: 22
    });
}

// Generate the PPTX File
const outputPath = path.join(__dirname, 'SLIDE_BAO_CAO_TIEN_DO.pptx');
pptx.writeFile({ fileName: outputPath }).then(() => {
    console.log(`[+] Đã tạo thành công tệp slide PowerPoint thực sự tại: ${outputPath}`);
}).catch(err => {
    console.error('Lỗi khi tạo PPTX:', err);
    process.exit(1);
});
